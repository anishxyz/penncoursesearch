import shutil
import openai
import csv
import tiktoken
from dotenv import load_dotenv
import os
import pandas as pd

# set up from environment
load_dotenv()
tokenizer = tiktoken.get_encoding("cl100k_base")

# Access the API key environment variable
api_key = os.environ["OPENAI_KEY"]
openai.api_key = api_key

# print(openai.Model.list())

# Define the batch size
BATCH_SIZE = 1000

# Set the original filename
filename = "FILLIN.csv"

# tokens used
tot_tokens = 0

# Check if the file already exists
if os.path.exists(filename):
    # If it does, make a copy of the file
    shutil.copyfile(filename, "courses_embed.csv")
    # Set the filename to the copy
    filename = "courses_embed.csv"

# Load the CSV file
with open(filename, "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    # Create a list to hold the embeddings
    responses = []

    # Iterate over the rows in the CSV, batching them as we go
    batch = []
    for row in reader:

        n_tokens = len(tokenizer.encode(row['ALL']))
        tot_tokens += n_tokens
        print(f"{row['Department Code']} {row['Course Code']}, {n_tokens} Tokens Used")

        # Add the description to the current batch
        batch.append(row["ALL"])

        # If the batch is full, generate embeddings for it and add them to the list
        if len(batch) == BATCH_SIZE:
            response = openai.Embedding.create(
                input=batch, engine='text-embedding-ada-002'
            )

            # Add the embeddings to the list
            responses.extend(response["data"])

            # Clear the batch
            batch = []

    # If there are any remaining rows in the CSV, generate embeddings for them and add them to the list
    if len(batch) > 0:
        response = openai.Embedding.create(
            input=batch, engine='text-embedding-ada-002'
        )

        # Add the embeddings to the list
        responses.extend(response["data"])

    final_embed = []
    for i, response in enumerate(responses):
        temp = response['embedding']
        final_embed.append(temp)

    df = pd.read_csv(filename)
    df['Embedding'] = ''
    df['Embedding'] = final_embed
    df.to_csv(filename, index=False)

    cost = tot_tokens / 1000 * 0.0004
    print("=" * 80)
    print(f"${cost} for {tot_tokens} tokens")
    print("=" * 80)
