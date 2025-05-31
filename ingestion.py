import pandas as pd
import sqlite3
import os

# convert CSV to Pandas DF
df = pd.read_csv("/Users/gopalrao000/Desktop/Sysintelli/class/Gen AI/SQL Chatbot/insurance_claims.csv")
print(df.head())

# set up connection to SQLlite
conn = sqlite3.connect('csvchatbot.db')

# Load DF into DB
df.to_sql('claims',conn,if_exists='replace',index = True)

conn.close()