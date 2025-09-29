## import Libraries
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from groq import Groq
from PIL import Image
import os
from dotenv import load_dotenv

## Load API Key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("❌ GROQ_API_KEY is not set. Please add it to your .env")

client = Groq(api_key=GROQ_API_KEY)

## Connecting with database
conn = sqlite3.connect("..\data\AmazonData.db")

## Loading Database
def load_AmazonData():
    return pd.read_sql_query("SELECT * FROM AmazonData;", conn)

df = load_AmazonData()

#Add logo 
LOGO = Image.open('..\Images\Picture1.png')
left, mid, right = st.columns([1,3,1])
st.image(LOGO, width=180)

## Page title
st.set_page_config(page_title="Amazon Analytics", page_icon="📊", layout="wide")
st.markdown('<h1 style="font-size:50px; font-weight:800; color:#DB2323; margin-bottom:10px;">Amazon Analytics Dashboard</h1>', unsafe_allow_html=True)
st.markdown("An interactive dashboard where you can analyze Dashboard and ChatBot")

## Tabs
tab_overview, tab_chatbot = st.tabs(["Overview", "Chatbot"])

# --- Theme ---
PURPLE = "#4B2E83"
BOT_BG = "#222831"   # dark gray background for bot answers
BOT_TEXT = "#FFFFFF" # white text

st.markdown(f"""
<style>
/* App background */
.stApp {{
  background-color: {PURPLE};
  color: #FFFFFF;
}}
/* Button color */
button[kind="primary"], button[data-baseweb="button"] {{
  background: {PURPLE};
  color: #FFFFFF;
}}
/* Assistant message styling */
.assistant-box {{
  background-color: {BOT_BG};
  color: {BOT_TEXT};
  padding: 12px;
  border-radius: 12px;
  margin-top: 10px;
  margin-bottom: 10px;
  font-size: 16px;
  line-height: 1.5;
}}
</style>
""", unsafe_allow_html=True)

# Style for tabs
st.markdown("""
    <style>
    button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] p {
        font-size: 18px;
        font-weight: 600;
    }
    button[data-baseweb="tab"] {
        padding: 12px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------- Overview Tab -------------------
with tab_overview:
    ## Show table from DB
    df_view = load_AmazonData()
    st.subheader(f"AmazonData Details ({len(df_view)})")
    st.dataframe(df_view, use_container_width=True)

# ------------------- Chatbot Tab -------------------
with tab_chatbot:
    st.subheader("💬 Chatbot with Database + AI")

    ## Get user input
    user_message = st.chat_input("Ask about Amazon products or DB structure...")

    if user_message:
        ## Show user message
        st.chat_message("user").write(user_message)

        ## Connect to DB
        conn = sqlite3.connect("../data/AmazonData.db")
        cursor = conn.cursor()

        ## CASE 1: If user asks about tables
        if "tables" in user_message.lower():
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [t[0] for t in cursor.fetchall()]
            conn.close()
            st.markdown(f"<div class='assistant-box'>📂 Tables in DB: {tables}</div>", unsafe_allow_html=True)

        ## CASE 2: If user asks about columns
        elif "columns" in user_message.lower():
            cursor.execute("PRAGMA table_info(AmazonData);")
            columns = [c[1] for c in cursor.fetchall()]
            conn.close()
            st.markdown(f"<div class='assistant-box'>📑 Columns in AmazonData: {columns}</div>", unsafe_allow_html=True)

        ## CASE 3: General questions (RAG style)
        else:
            query = f"""
            SELECT product_name, category, discounted_price, rating, review_content
            FROM AmazonData
            WHERE product_name LIKE '%{user_message}%'
               OR review_content LIKE '%{user_message}%'
            LIMIT 5;
            """
            df = pd.read_sql(query, conn)
            conn.close()

            ## If no results
            if df.empty:
                db_context = "No matching data found in the database."
            else:
                db_context = df.to_string(index=False)

            ## Send context + question to Groq
            completion = client.chat.completions.create(
                model="groq/compound",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers using the AmazonData database."},
                    {"role": "system", "content": f"Database context:\n{db_context}"},
                    {"role": "user", "content": user_message},
                ],
                max_completion_tokens=400,
                temperature=0.7,
                stream=False,
            )

            ## Show assistant response with styled background
            assistant_response = completion.choices[0].message.content
            st.markdown(f"<div class='assistant-box'>{assistant_response}</div>", unsafe_allow_html=True)
