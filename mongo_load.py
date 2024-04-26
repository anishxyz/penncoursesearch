import os
import certifi
from pymongo import MongoClient
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from urllib import parse

# Load data from CSV into a DataFrame
# df = pd.read_parquet('data/courses_embed.parquet')
df = pd.read_csv("data/courses_embed.csv")
load_dotenv()
mongodb_uri = os.getenv('MONGODB_URI')
# Connect to MongoDB and create a collection
client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())
db = client['course-embeddings']
collection = db['catalog']

# Insert each row from the DataFrame as a document in the collection
for index, row in df.iterrows():
    embedding_str = row['embeddings']
    embedding_str = embedding_str.replace('[', '').replace(']', '')  # Remove square brackets
    embedding = [float(x.strip()) for x in embedding_str.split(',')]  # Split on commas and convert to float
    document = {
        'department_code': row['Department Code'],
        'course_code': row['Course Code'],
        'title': row['Course Title'],
        'description': row['Description'],
        'combined': row['ALL'],
        'embedding': embedding
    }
    print(f"{row['Department Code']} {row['Course Code']}")
    collection.insert_one(document)

