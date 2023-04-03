import shutil
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity
import numpy as np
import openai
import csv
import tiktoken
from dotenv import load_dotenv
import os
import pandas as pd
import sklearn


# set up from environment
load_dotenv()
tokenizer = tiktoken.get_encoding("cl100k_base")

# Access the API key environment variable
api_key = os.environ["OPENAI_KEY"]
openai.api_key = api_key

context_len = 1200


def load_df():
    # df = pd.read_csv('courses_embed.csv', index_col=0)
    # df['Embedding'] = df['Embedding'].apply(eval).apply(np.array)
    #
    # # Save DataFrame as a Parquet file
    # df.to_parquet('courses_embed.parquet')

    # Read DataFrame from Parquet file
    df = pd.read_parquet('courses_embed.parquet')
    return df


def create_context(question, df, max_len=context_len):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for the question
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the distances from the embeddings
    df['distances'] = distances_from_embeddings(q_embeddings, df['Embedding'].values, distance_metric='cosine')

    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        n_tokens = len(tokenizer.encode(row['ALL']))
        cur_len += n_tokens

        # If the context is too long, break
        if cur_len > max_len:
            break

        # Else add it to the text that is being returned
        returns.append(f"{row['ALL']}")

    # Return the context
    return "\n\n###\n\n".join(returns)


def answer_chat(
    df,
    model="gpt-3.5-turbo",
    question="?",
    debug=False,
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        df,
    )
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


async def query_response(q, df):
    try:
        ans = answer_chat(df, question=q, debug=False)
        print(ans)
        return ans

    except Exception as e:
        print(e)
        return "An error occurred"


if __name__ == '__main__':

    df = load_df()
    while True:
        user_input = input("Enter a message: ")

        # Check for exit command
        if user_input.lower() == "exit":
            break

        # print(create_context(user_input, df))
        print(answer_chat(df, question=user_input, debug=False))