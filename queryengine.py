import asyncio
import re
import pandas as pd
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity
import openai
import tiktoken
from dotenv import load_dotenv
import os
import json

# set up from environment
from pymongo import MongoClient

load_dotenv()
tokenizer = tiktoken.get_encoding("cl100k_base")

# Access the API key environment variable
api_key = os.environ["OPENAI_KEY"]
openai.api_key = api_key

context_len = 2000
context_dist = 0.21

global global_df


def initialize_cache_sync():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cache_embeddings())


async def cache_embeddings():
    data = pd.read_parquet('data/courses_embed.parquet')
    global global_df
    global_df = data


async def find_courses(input_question):
    course_pattern = r'(?i)([A-Za-z]{2,6})\s?([0-9]{3,4})'
    courses_in_question = set()
    for match in re.finditer(course_pattern, input_question):
        course = match.group(1) + ' ' + match.group(2)
        courses_in_question.add(course.upper())

    matching_context = []
    matching_courses = []

    # Loop through each course in courses_in_question
    for course in courses_in_question:
        # Use str.contains() to check if course is a substring of 'id'
        matching = global_df[global_df['id'].str.contains(course)]
        # Add the matching ids to the array
        # Add the matching ids to the array
        matching_context += matching['combined'].tolist()

        for _, row in matching.iterrows():
            matching_courses.append({'title': row['id'], 'description': row['description']})

    return matching_context, matching_courses


async def create_context_parquet(question):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for the question
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the distances from the embeddings
    global_df['distances'] = distances_from_embeddings(q_embeddings, global_df['embedding'].values, distance_metric='cosine')

    returns, relevant_courses = await find_courses(question)

    # print("Course Matches")
    # print(returns)

    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in global_df.sort_values('distances', ascending=True).iterrows():

        if row['distances'] > context_dist and cur_len >= 1200:
            break

        # Add the length of the text to the current length
        # print(row['distances'])
        cur_len += row['tokens'] + 4

        # If the context is too long, break
        if cur_len > context_len:
            break

        # Else add it to the text that is being returned
        returns.append(f"{row['combined']}")
        relevant_courses.append({'title': row['id'], 'description': row['description']})

    context = "\n\n###\n\n".join(returns)

    print("Context created.")

    # Return the context
    return {"context": context, "courses": relevant_courses}


async def answer_chat(
    model="gpt-3.5-turbo",
    question="?",
    debug=False,
    context=""
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        p = f'You are a bot to help students find courses from the University of Pennsylvania Course Catalog. Master degree courses have a course code of 5000 or more. Prioritize recommending lower level classes when it makes sense or give both high and low level classes. I will include context for each query to help you. Use lists when it makes sense \n\nContext: {context}\n\n---\n\nQuestion: {question} \nAnswer:'
        # Create a completions using the question and context
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": p}]
        )

        # print(response)
        tokens = response["usage"]["total_tokens"]
        print(f"Tokens Used: {tokens}, Cost: {tokens/1000 * 0.002}")
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(e)
        return ""


async def query_response(q, context=""):
    try:
        ans = await answer_chat(question=q, debug=False, context=context)
        # print(ans)
        return ans

    except Exception as e:
        print(global_df)
        print(e)
        return "An error occurred"


async def start():
    await cache_embeddings()

    while True:
        user_input = input("Enter a message: ")

        # Check for exit command
        if user_input.lower() == "exit":
            break

        resp = await answer_chat(question=user_input, debug=False)
        print(resp)


if __name__ == '__main__':
    asyncio.run(start())

