# SmartSQL-Natural-Language-to-SQL-Chatbot-using-LangChain-OpenAI
## 🧠 SmartSQL: Natural Language to SQL Chatbot using LangChain + OpenAI

---

## 🚀 Features

- 🧾 Converts natural language questions into SQL queries
- 📊 Retrieves real-time answers from a structured database
- 🧠 Uses two-step LLM reasoning:
  - LLM1: Generates schema understanding from sample data
  - LLM2: Converts schema + question into valid SQL
- 💬 Adds a human-like response on top of SQL results
- ⚙️ Easily configurable to support any SQLite database

---




## ⚙️ Setup Instructions

Clone the repo  
git clone https://github.com/Bhargavik01/sql-chatbot.git  
cd sql-chatbot

## Create virtual environment
python3 -m venv sqlchatbot
source sqlchatbot/bin/activate

## Install dependencies
pip install -r requirements.txt  
Create .env file  
OPENAI_API_KEY=your-openai-key  
Run the chatbot   
python main.py


## 📋 Example


## User Question: How many policy states were available?
SELECT COUNT(DISTINCT policy_state) FROM claims;
## Response:
There are 12 unique policy states recorded in the claims dataset, highlighting the geographic spread of the insurance policies. This suggests a diverse customer base and potential regional trends in claims.

🔮 Future Enhancements
 Add a web-based UI using Streamlit or React
 Dockerize for portable deployment
 Support for multiple database types (Postgres, MySQL)
 Embed OpenLineage for data lineage tracking
 Add query history and session memory
 
## 🤖 Powered By
LangChain  
OpenAI  
Pandas  
SQLite


