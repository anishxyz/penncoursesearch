import ast
import asyncio
import re
import pandas as pd
import pinecone
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

# open ai auth
api_key = os.environ["OPENAI_KEY"]
openai.api_key = api_key

# pinecone auth
api_key = os.environ["PINE_CONE_API_KEY"]
pinecone.init(api_key=api_key, environment="northamerica-northeast1-gcp")
index = pinecone.Index("penn-courses")

context_len = 1500
context_dist = 0.21

global global_df


def initialize_cache_sync():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cache_embeddings())


async def cache_embeddings():
    data = pd.read_parquet('data/courses_embed.parquet')
    # data['professor_stats'] = data['professor_stats'].apply(ast.literal_eval)
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

        if row['distances'] > context_dist and cur_len >= context_len:
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

    # print("Context created.")
    print(cur_len)
    # Return the context
    return {"context": context, "courses": relevant_courses}


async def create_context_pinecone(question):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for the question
    q_embedding = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    course_pattern = r'(?i)([A-Za-z]{2,6})\s?([0-9]{3,4})'
    courses_in_question = []

    for match in re.finditer(course_pattern, question):
        course_name = match.group(1)
        course_number = match.group(2)

        course = course_name + '-' + course_number

        if len(course_number) == 3:
            course1 = course + '0'
            courses_in_question.append(course1.upper())
            course2 = course + '8'
            courses_in_question.append(course2.upper())
        else:
            courses_in_question.append(course.upper())

    # print(courses_in_question)

    fetch_response = {}
    if courses_in_question:
        fetch_response = index.fetch(ids=courses_in_question)

    matches = index.query(
        vector=q_embedding,
        top_k=20,
        include_values=False,
        include_metadata=True
    )

    # Construct relevant_courses from fetch_response
    relevant_courses = {}

    # List to store related_matches
    related_matches_list = []

    for course_id, details in fetch_response.get('vectors', {}).items():
        course = {
            "id": details.get('id', ''),
            "score": '',  # Score not available in fetch_response
            "combined": details.get('metadata', {}).get('combined', ''),
            "description": details.get('metadata', {}).get('description', ''),
            "link": details.get('metadata', {}).get('link', ''),
            "professor_stats": details.get('metadata', {}).get('professor_stats', ''),
            "title": details.get('metadata', {}).get('title', ''),
            "tokens": details.get('metadata', {}).get('tokens', '')
        }

        related_matches = index.query(
            vector=details.get('values', {}),
            top_k=5,
            include_values=False,
            include_metadata=True
        )

        relevant_courses[course_id] = course
        related_matches_list.extend(related_matches.get('matches', []))

    # Prepend related_matches to matches
    matches['matches'] = related_matches_list + matches['matches']

    # Add courses from matches
    for match in matches.get('matches', []):
        if match.get('id', '') not in relevant_courses:
            course = {
                "id": match.get('id', ''),
                "score": match.get('score', ''),
                "combined": match.get('metadata', {}).get('combined', ''),
                "description": match.get('metadata', {}).get('description', ''),
                "link": match.get('metadata', {}).get('link', ''),
                "professor_stats": match.get('metadata', {}).get('professor_stats', ''),
                "title": match.get('metadata', {}).get('title', ''),
                "tokens": match.get('metadata', {}).get('tokens', '')
            }
            relevant_courses[match.get('id', '')] = course

    return {"context": [], "courses": list(relevant_courses.values())}


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
        print(p)
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

        res = await create_context_pinecone(user_input)
        print(res['courses'])
        # context = await create_context_parquet(user_input)
        # resp = await answer_chat(question=user_input, debug=False, context=context["context"])
        # print(resp)


if __name__ == '__main__':
    asyncio.run(start())

