import certifi
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity
import openai
import tiktoken
from dotenv import load_dotenv
import os

# set up from environment
from pymongo import MongoClient

load_dotenv()
tokenizer = tiktoken.get_encoding("cl100k_base")

# Access the API key environment variable
api_key = os.environ["OPENAI_KEY"]
openai.api_key = api_key

# mongo setup
mongodb_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())
db = client['course-embeddings']
collection = db['catalog']

context_len = 1200


async def create_context_mongodb(question, max_len=context_len):
    """
    Create a context for a question by finding the most similar context from the documents in the collection
    """

    # Get the embeddings for the question
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the documents from the MongoDB collection
    docs = list(collection.find({}))

    # Get the distances from the embeddings
    distances = distances_from_embeddings(q_embeddings, [doc['embedding'] for doc in docs], distance_metric='cosine')

    # Add distances to each document
    for i, doc in enumerate(docs):
        doc['distances'] = distances[i]

    # Sort the documents by distance
    sorted_docs = sorted(docs, key=lambda x: x['distances'], reverse=False)

    returns = []
    cur_len = 0

    # Add the text to the context until the context is too long
    for doc in sorted_docs:
        n_tokens = len(tokenizer.encode(doc['combined']))
        cur_len += n_tokens

        # If the context is too long, break
        if cur_len > max_len:
            break

        # Else add it to the text that is being returned
        returns.append(f"{doc['combined']}")

    # Return the context
    return "\n\n###\n\n".join(returns)


async def answer_chat(
    model="gpt-3.5-turbo",
    question="?",
    debug=False,
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context_mongodb(question)
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        p = f'You are a bot to help students find courses from the University of Pennsylvania Course Catalog. Master degree courses have a course code of 5000 or more. Prioritize recommending lower level classes when it makes sense or give both high and low level classes. I will include context for each query to help you. \n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:'
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


async def query_response(q):
    try:
        ans = await answer_chat(question=q, debug=False)
        print(ans)
        return ans

    except Exception as e:
        print(e)
        return "An error occurred"


if __name__ == '__main__':
    while True:
        user_input = input("Enter a message: ")

        # Check for exit command
        if user_input.lower() == "exit":
            break

        # print(create_context(user_input, df))
        print(answer_chat(question=user_input, debug=True))
