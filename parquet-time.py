import pandas as pd
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")

# Load the Parquet file into a DataFrame
# df = pd.read_parquet('data/courses_embed.parquet')
df = pd.read_csv('data/courses_embed_plus.csv')


# def create_department_link(course_id):
#     department_code = course_id.split(' ')[0].lower()
#     return f"https://catalog.upenn.edu/courses/{department_code}/"
#
#
# # Add a new column 'links' to the DataFrame
# df['link'] = df['id'].apply(create_department_link)
#
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(df.head())


df.to_parquet('data/courses_embed.parquet')
