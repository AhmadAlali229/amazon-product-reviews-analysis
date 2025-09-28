import sqlite3
import pandas as pd
from transformers import pipeline

# Load Excel
df = pd.read_excel("../data/amazon_product_reviews.xlsx")

# Sentiment model
sentiment = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

# Add sentiment columns
df["sentiment_label"] = df["review_content"].fillna("").astype(str).apply(lambda x: sentiment(x[:512])[0]["label"])
df["sentiment_score"] = df["review_content"].fillna("").astype(str).apply(lambda x: sentiment(x[:512])[0]["score"])

# Save to SQLite
conn = sqlite3.connect("../data/AmazonData.db")
df.to_sql("AmazonData", conn, if_exists="replace", index=False)
conn.close()

print(" Done! Database updated with sentiment columns.")
