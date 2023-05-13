import json

import numpy as np
import pinecone
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import ast

load_dotenv()
api_key = os.environ["PINE_CONE_API_KEY"]

pinecone.init(api_key=api_key, environment="northamerica-northeast1-gcp")
index = pinecone.Index("penn-courses")

df = pd.read_parquet('data/courses_embed_plus.parquet')

print(df)

# Define a function to get the professor information
def get_professors_info(course_id):
    url = f"https://penncoursereview.com/api/base/current/courses/{course_id.replace(' ', '-')}/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed for {course_id}")
        return None

    course_data = response.json()

    professors_info = []
    added_professors = set()

    for section in course_data['sections']:
        for instructor in section['instructors']:
            instructor_id = instructor['id']
            if instructor_id not in added_professors:
                added_professors.add(instructor_id)
                professors_info.append({
                    'name': instructor['name'],
                    'course_quality': section['course_quality'],
                    'instructor_quality': section['instructor_quality'],
                    'difficulty': section['difficulty'],
                    'work_required': section['work_required']
                })

    print(f"Success for {course_id}")
    return professors_info


def transform_row(row):
    id = row['id'].replace(' ', '-')
    vector = row['embedding'].tolist()

    # prof = get_professors_info(id)
    # row["professor_stats"] = prof

    # Check if professor_stats is None, if not convert to list
    professor_stats = row["professor_stats"]
    # print(professor_stats)
    if professor_stats is not None:
        professor_stats = professor_stats.replace("}\n {", "}, {")
        professor_stats = ast.literal_eval(professor_stats)

        if not professor_stats:
            professor_stats = ['TBD']
    else:
        professor_stats = []

    professor_stats = json.dumps(professor_stats)

    metadata = {
        "title": row["title"],
        "description": row["description"],
        "combined": row["combined"],
        "tokens": row["tokens"],
        "professor_stats": professor_stats,  # Use the processed professor_stats
        "link": row["link"]
    }

    return id, vector, metadata


data_to_insert = df.apply(transform_row, axis=1).tolist()

for item in data_to_insert:
    try:
        index.upsert([item])
        print(f"Upserted {item[0]} successfully")
    except Exception as e:
        print(f"Error upserting {item[0]}: {e}")



