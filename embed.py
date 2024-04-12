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
BATCH_SIZE = 10

# Set the original filename
filenameIn = "data/courses.csv"
filenameOut =  "data/courses_embed.csv"
# tokens used
tot_tokens = 0


# Load the CSV file
with open(filenameOut, "w", newline="", encoding="utf-8") as writefile:
    with open(filenameIn, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        writer = csv.DictWriter(writefile,fieldnames := ["Department Code","Course Code","Course Title","Description","ALL","embeddings"])
        writer.writeheader()
        # Create a list to hold the embeddings

        # Iterate over the rows in the CSV, batching them as we go
        copybatch = []
        batch = []
        for row in reader:

            n_tokens = len(tokenizer.encode(row['ALL']))
            tot_tokens += n_tokens
            print(f"{row['Department Code']}, {row['Course Code']}, {n_tokens} Tokens Used")

            # Add the description to the current batch
            copybatch.append(row)
            batch.append(row["ALL"])

            # If the batch is full, generate embeddings for it and add them to the list
            if len(batch) == BATCH_SIZE:
                response = openai.Embedding.create(
                    input=batch, engine='text-embedding-ada-002'
                )

                # Add the embeddings to the list
                copybatch = [x | {"embeddings":response["data"][0]["embedding"]} for x in copybatch]
                writer.writerows(copybatch)

                # Clear the batch
                copybatch = []
                batch = []
    
        # If there are any remaining rows in the CSV, generate embeddings for them and add them to the list
        if len(batch) > 0:
            response = openai.Embedding.create(
                input=batch, engine='text-embedding-ada-002'
            )

            # Add the embeddings to the list
            writer.writerows(copybatch)


        cost = tot_tokens / 1000 * 0.0004
        print("=" * 80)
        print(f"${cost} for {tot_tokens} tokens")
        print("=" * 80)
