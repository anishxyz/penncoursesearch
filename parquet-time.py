import pandas as pd
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")

# Load the Parquet file into a DataFrame
df = pd.read_parquet('data/courses_embed.parquet')

# Print the DataFrame
print(df['tokens'])


