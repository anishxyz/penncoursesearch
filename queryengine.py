import asyncio
import re
import pinecone
import openai
import tiktoken
from dotenv import load_dotenv
import os
import json

# set up from environment
from pymongo import MongoClient

load_dotenv()
tokenizer = tiktoken.get_encoding("cl100k_base")

# open-ai auth
# api_key = os.environ["OPENAI_KEY"]
api_key = "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"
openai.api_key = api_key

# pinecone auth
# api_key = os.environ["PINE_CONE_API_KEY"]
api_key = "AZok5GinvJHHcZcgwlJZOQ8XVvX1vJXDgfAsbMQ35w2AnchDYxo0IFFNTd39yBRT"
username = "PCS"
password = "1234"
client = MongoClient(f"mongodb+srv://{username}:{password}@pennsoursesearch.epdhqbb.mongodb.net/")
index = client["course-embeddings"]["catalog"]

token_limit = 2000  # Set your desired token limit
score_lower_bound = 0.75  # Set your desired score lower bound


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
        fetch_response = index.find({
            "$text": {
                "$search": " ".join(courses_in_question)  # Assuming courses_in_question is a list of course names
            }
        })

    # For nearest-neighbor search (assumes you're using MongoDB 4.4+ and have a 2dsphere index on 'embedding' field)
    matches = index.aggregate([
            {
                "$search": {
                    "index": "_id_",
                    "knnBeta": {
                        "vector": q_embedding,  # Example: Replace with your actual query vector
                        "path": "embedding",  # Example: Replace with the name of your indexed field
                        "k": 20
                    }
                }
            },
            {
                "$limit": 20  # Limit the number of documents returned in the result set
            }
    ])

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

        related_matches = index.aggregate([
            {
                "$search": {
                    "index": "_id_",
                    "knnBeta": {
                        "vector": q_embedding,  # Example: Replace with your actual query vector
                        "path": "embedding",  # Example: Replace with the name of your indexed field
                        "k": 5
                    }
                }
            },
            {
                "$limit": 5  # Limit the number of documents returned in the result set
            }
        ])
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

    context = ""
    token_count = 0

    # Construct context from matches
    for match in matches.get('matches', []):
        if match.get('score', 0) >= score_lower_bound and token_count <= token_limit:
            context += match.get('metadata', {}).get('combined', '') + "\n\n"
            token_count += match.get('metadata', {}).get('tokens', 0)
            professor_stats = match.get('metadata', {}).get('professor_stats', None)
            if professor_stats:
                context += "Professor stats:\n" + json.dumps(professor_stats) + "\n\n"

    return {"context": context, "courses": list(relevant_courses.values())}


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
        print(e)
        return "An error occurred"


async def start():

    while True:
        user_input = input("Enter a message: ")

        # Check for exit command
        if user_input.lower() == "exit":
            break

        context = await create_context_pinecone(user_input)
        resp = await answer_chat(question=user_input, debug=False, context=context["context"])
        print(resp)


if __name__ == '__main__':
    asyncio.run(start())

