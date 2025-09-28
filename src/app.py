## import Libaries
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from PIL import Image
conn = sqlite3.connect("..\data\AmazonData.db") #connecting with database

##Loading Database
def load_AmazonData():
    return pd.read_sql_query("SELECT * FROM AmazonData;", conn)

df = load_AmazonData()

#Add logo
##LOGO = Image.open('..\Images\Picture1.png')
##left, mid, right = st.columns([1,3,1])
##st.image(LOGO, width=180)

st.set_page_config(page_title="Amazon Analytics", page_icon="📊", layout="wide")# Title
st.markdown('<h1 style="font-size:50px; font-weight:800; margin-bottom:10px;">Amazon Analytics Dashboard</h1>', unsafe_allow_html=True)#Styling Title
st.markdown("An interactive dashboard where you can analyze Dashboard and ChatBot")#Descreption

tab_overview, tab_chatbot = st.tabs(["Overview", "Chatbot"])#Creating Taps to be usesd later

# --- ultra simple theme ---
PURPLE = "#5B2BE0"
PINK   = "#FF3B6A"

st.markdown(f"""
<style>
/* Shading color */
.stApp {{
  background: linear-gradient(135deg, {PURPLE} 0%, {PINK} 100%);
  color: #FFFFFF;
}}
/*    button color */
button[kind="primary"], button[data-baseweb="button"] {{
  background: {PINK};
  color: #FFFFFF;
}}
</style>
""", unsafe_allow_html=True)


#Style for tabs when used
st.markdown("""
    <style>
    /* make the tabs text a bit bigger */
    button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] p {
        font-size: 18px;
        font-weight: 600;
    }
    /* add some padding so tabs look larger */
    button[data-baseweb="tab"] {
        padding: 12px 20px;
    }
    </style>
""", unsafe_allow_html=True)

#Using Overview Tab
with tab_overview:

  # Creating table to show AmazonData details
    df_view = load_AmazonData()   # call the function to get the DataFrame

    st.subheader(f"AmazonData Details ({len(df_view)})")
    st.dataframe(df_view, use_container_width=True)


#Using add chatbot Tab
with tab_chatbot:
    # 
    xChat= st.chat_input(placeholder="Your message")
    ##st.chat_message(xChat)

