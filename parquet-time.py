import ast
import json

import numpy as np
import pandas as pd
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")

df = pd.read_csv('data/courses_embed_plus.csv')

# # Convert JSON strings to list of dictionaries for professor_stats
# df['professor_stats'] = df['professor_stats'].apply(ast.literal_eval)

# Convert DataFrame to parquet
print(df)

df['embedding'] = df['embedding'].apply(lambda x: np.array(eval(x)))

df.to_parquet('data/courses_embed_plus.parquet')
