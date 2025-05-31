# main.py

"""
1. User question
2. Read column names from table
3. Read 5 sample rows from table
4. Pass column names + sample rows to LLM (LLM1) to generate schema
5. Pass User question + schema context to LLM (LLM2) to generate SQL
6. Execute SQL and show result
"""

import json
import sqlite3
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

# --- Config ---
DB_PATH = "csvchatbot.db"
TABLE_NAME = "claims"
OPENAI_MODEL = "gpt-3.5-turbo"  
TEMPERATURE = 0.2

# --- Step 1: User question ---
user_question = "How many policy states were available?"

# --- Step 2: Connect to DB and read schema ---
conn = sqlite3.connect(DB_PATH)
sample_df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME} LIMIT 5", conn)
column_names = sample_df.columns.tolist()

llm = ChatOpenAI(temperature= TEMPERATURE, model = OPENAI_MODEL)

# --- Step 3: Generate Table Summary Context (LLM1) ---
prompt_schema = PromptTemplate(
    input_variables= ["column","sample_rows"],
    template =(
    """
    You are a data expert. Given the following column names and sample rows from a table, describe the table's structure.
    
    Column Names: {column}
    
    Sample Rows:
    {sample_rows}
    
    can you list out all the column names and their data type.

    For each column, write a short description based on your knowledge with in the given context.
    Strictly use below format:

    Table Name: Claims
    1. Column name : type. clear description
    Only return the numbers list. Do not give any explanation, extra spaces or othe stuff
    Then print a line
    """
    )
)

chain = prompt_schema | llm


response_schema = chain.invoke(
    {
        "column": json.dumps(column_names),
        "sample_rows" : sample_df
     }
)
schema_text = response_schema.content
print(schema_text)


# LLM2 : SQL Query generation
prompt_sql = PromptTemplate(
    input_variables= ["table","schema","question"],
    template =(
    """
    You are a data expert who can convert natural queries to SQL Queries.
    You will be given 
    1: Table name
    2: Schema: All the column in  the SQl table with type and short description.
    3: User Question in Natural laguage

    Your Job is to write SQL query to answer user question
    Table name: {table}
    Schema : {schema}
    User Question: {question}

    Respond with only one single SQl query , No other text.
    """
    )
)

formatted_sql_prompt = prompt_sql.format(
    table = TABLE_NAME,
    schema = schema_text,
    question =user_question

)

response_sql=llm.invoke(formatted_sql_prompt)
sql_query=response_sql.content
print(sql_query)

# Run SQL Query

result=pd.read_sql_query(sql_query,conn)
print(f"Below is the Answer to Your Question: {result}")

#Conversational Response


prompt_answer=PromptTemplate(
    input_variables=["question","answer"],
    template=(
        """You are a Professional Business Analyst who can answer user question and the best tone and context
        Below is the user question and answer. Kindly frame a Very professional answer

        User Question:{question}
        Answer: {answer}

        Answer in 50 words. Dont just tell the number. Tell interesting story along the line as well

     """
    )
)


chain2=prompt_answer | llm 

answer_schema=chain2.invoke(
    {
        "question":user_question,
        "answer":result
    }
)


print(answer_schema.content)

