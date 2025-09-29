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

## Connect to database
conn = sqlite3.connect("../data/AmazonData.db")

## Load data from AmazonData table
def load_AmazonData():
    return pd.read_sql_query("SELECT * FROM AmazonData;", conn)

df = load_AmazonData()

## Add logo
LOGO = Image.open('../Images/Picture1.png')
left, mid, right = st.columns([1,3,1])
st.image(LOGO, width=180)

## Page title
st.set_page_config(page_title="Amazon Analytics", page_icon="📊", layout="wide")
st.markdown('<h1 style="font-size:50px; font-weight:800; color:#DB2323; margin-bottom:10px;">Amazon Analytics Dashboard</h1>', unsafe_allow_html=True)
st.markdown("An interactive dashboard where you can analyze Dashboard and ChatBot")

## Tabs
tab_overview, tab_chatbot = st.tabs(["Overview", "Chatbot"])

## Theme settings
PURPLE = "#4B2E83"
BOT_BG = "#222831"   # background for bot answers
BOT_TEXT = "#FFFFFF" # bot text color

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
/* Assistant message box */
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

## Tab styles
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

# ---------------- Overview Tab ----------------
with tab_overview:
    df_view = load_AmazonData()
    st.subheader(f"AmazonData Details ({len(df_view)})")
    st.dataframe(df_view, use_container_width=True)

# ---------------- Chatbot Tab ----------------
with tab_chatbot:
    st.subheader("💬 Chatbot For Analysis")

    ## Get user input
    user_message = st.chat_input("Ask about Amazon products or DB structure...")

    if user_message:
        ## Show user message
        st.chat_message("user").write(user_message)

        ## Connect to DB
        conn = sqlite3.connect("../data/AmazonData.db")
        cursor = conn.cursor()

        # --- CASE 1: Ask about tables ---
        if "tables" in user_message.lower():
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [t[0] for t in cursor.fetchall()]
            conn.close()
            st.markdown(f"<div class='assistant-box'>📂 Tables in DB: {tables}</div>", unsafe_allow_html=True)

        # --- CASE 2: Ask about columns ---
        elif "columns" in user_message.lower():
            cursor.execute("PRAGMA table_info(AmazonData);")
            columns = [c[1] for c in cursor.fetchall()]
            conn.close()
            st.markdown(f"<div class='assistant-box'>📑 Columns in AmazonData: {columns}</div>", unsafe_allow_html=True)

        # --- CASE 3: Highest discounted_price ---
        elif "highest discounted_price" in user_message.lower() or "top" in user_message.lower():
            query = """
            SELECT product_name, discounted_price
            FROM AmazonData
            ORDER BY discounted_price DESC
            LIMIT 5;
            """
            df = pd.read_sql(query, conn)
            conn.close()
            if df.empty:
                st.markdown("<div class='assistant-box'>⚠️ No data found.</div>", unsafe_allow_html=True)
            else:
                st.subheader("📊 Top 5 Products (Highest Discounted Price)")
                st.dataframe(df, use_container_width=True)

        # --- CASE 4: Lowest discounted_price ---
        elif "lowest discounted_price" in user_message.lower() or "cheapest" in user_message.lower():
            query = """
            SELECT product_name, discounted_price
            FROM AmazonData
            ORDER BY discounted_price ASC
            LIMIT 5;
            """
            df = pd.read_sql(query, conn)
            conn.close()
            if df.empty:
                st.markdown("<div class='assistant-box'>⚠️ No data found.</div>", unsafe_allow_html=True)
            else:
                st.subheader("📉 Lowest 5 Products (Discounted Price)")
                st.dataframe(df, use_container_width=True)

        # --- CASE 5: Average rating per category ---
        elif "average rating" in user_message.lower():
            query = """
            SELECT category, ROUND(AVG(rating),2) AS avg_rating
            FROM AmazonData
            GROUP BY category
            ORDER BY avg_rating DESC;
            """
            df = pd.read_sql(query, conn)
            conn.close()
            if df.empty:
                st.markdown("<div class='assistant-box'>⚠️ No data found.</div>", unsafe_allow_html=True)
            else:
                st.subheader("⭐ Average Rating per Category")
                st.dataframe(df, use_container_width=True)

        # --- CASE 6: General Questions (RAG style with Groq) ---
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

            if df.empty:
                db_context = "No matching data found in the database."
            else:
                db_context = df.to_string(index=False)

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

            assistant_response = completion.choices[0].message.content
            st.markdown(f"<div class='assistant-box'>{assistant_response}</div>", unsafe_allow_html=True)