import asyncio
import re
import heapq
import openai
import tiktoken
from dotenv import load_dotenv
import os
import time
import numpy as np
import logging
# set up from environment
from pymongo import MongoClient

#logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

load_dotenv()
tokenizer = tiktoken.get_encoding("cl100k_base")

# open-ai auth
api_key = os.environ["OPENAI_KEY"]
openai.api_key = api_key

# pinecone auth
api_key = os.environ["MONGODB_URI"]
client = MongoClient(api_key)
index = client["course-embeddings"]["catalog"]

token_limit = 2000  # Set your desired token limit
score_lower_bound = 0.75  # Set your desired score lower bound

courses = {}
courses_embeddings = {}

async def reset_embeddings():
    start = time.time() #DEBUG
    matches = list(index.find())
    courses.clear()
    courses_embeddings.clear()
    #creates generator to stream embeddings
    for match in matches:
            course = {
                "id": str(match.get('_id', '')),
                "department_code": match.get('department_code',''),
                "course_code": match.get('course_code',''),
                "title": match.get('title',''),
                "description": match.get('description',''),
                "professor_stats": match.get('professor_stats', ''),
            }
            course_embeddings = {
                "id": str(match.get('_id', '')),
                "embedding": np.array(match.get('embedding',''))
            }
            courses[str(match.get('_id', ''))] = course
            courses_embeddings[str(match.get('_id', ''))] = course_embeddings
    logging.debug("Time elapsed in reset_embeddings %s", time.time() - start)
    return


async def create_context(question = "", k = 10):
    """
    Create a context for a question by finding courses that are explicilty mentioned
    Otherwise just get all embeddings
    """
    start = time.time() #debug
    course_pattern = r'([A-Za-z]+)(\d+)'
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
            course3 = course_name + '-0' + course_number
            courses_in_question.append(course3.upper())
        else:
            courses_in_question.append(course.upper())

    # Get the embeddings for the question
    q_embedding = await openai.Embedding.acreate(input=question, engine='text-embedding-3-small')
    q_embedding = np.array(q_embedding['data'][0]['embedding'])

    if courses_in_question:
        logging.debug("Course found in query %s",courses_in_question)
        top_courses = []
        for course_in_question in set(courses_in_question):
            course_name,course_number = course_in_question.split('-')
            for k,v in courses.items():
                if v["department_code"] == course_name and v["course_code"] == int(course_number):
                    top_courses.append((1,courses[k]))
        return top_courses
    else: 
        logging.debug("No specific course in query")
    
    #get top k embeddings
    top_courses = []
    for (key,val) in courses_embeddings.items():
        dot_val = np.dot(q_embedding,val["embedding"])
        my_tuple = (dot_val, key)
        if len(top_courses) < k:
            heapq.heappush(top_courses, my_tuple)
        else:
            heapq.heappushpop(top_courses, my_tuple)  
    top_courses = [(embed,courses[key]) for (embed,key) in top_courses]
    logging.debug("Time elapsed in create_context %s",time.time() - start)
    return top_courses


async def answer_chat(
    model="gpt-3.5-turbo",
    question="?",
    context="",
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    # If debug, print the raw model response
    logging.debug("Context:\n %s",context)
    start = time.time() # debug purposes

    try:
        p = f'You are a bot to help students find courses from the University of Pennsylvania Course Catalog. Master degree courses have a course code of 5000 or more. Prioritize recommending lower level classes when it makes sense or give both high and low level classes. I will include context for each query to help you. Use lists when it makes sense \n\nContext: {context}\n\n---\n\nQuestion: {question} \nAnswer:'
        # Create a completions using the question and context
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": p}]
        )

        # print(response)
        tokens = response["usage"]["total_tokens"]
        logging.debug("Tokens Used: %d, Cost: %s",tokens,{tokens/1000*.002})
        logging.debug("Time elapsed in answer_chat %s",time.time()-start)
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.error(e)
        return ""


async def query_response(q, context=""):
    try:
        ans = await answer_chat(question=q, context=context)
        return ans

    except Exception as e:
        logging.error(e)
        return "An error occurred"


async def start():
    while True:
        if (len(courses) == 0):
            await reset_embeddings()
        user_input = input("Enter a message: ")
        # Check for exit command
        if user_input.lower() == "exit":
            break
        context = await create_context(user_input,10)
        context = [v for (k,v) in sorted(context,key = lambda x: x[0])]
        resp = await answer_chat(question=user_input, context=context)
        print(resp)


if __name__ == '__main__':
    asyncio.run(start())

