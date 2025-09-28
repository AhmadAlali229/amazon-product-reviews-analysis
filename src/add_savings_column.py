import sqlite3
import pandas as pd

# 1) Connect to DB
conn = sqlite3.connect("AmazonData.db")

# 2) Load table AmazonData
df = pd.read_sql("SELECT * FROM AmazonData", conn)

# 3) Convert price columns to numeric (in case they're stored as text)
df["actual_price"] = pd.to_numeric(df["actual_price"], errors="coerce")
df["discounted_price"] = pd.to_numeric(df["discounted_price"], errors="coerce")

# 4) Add savings column
df["savings"] = df["actual_price"] - df["discounted_price"]

# 5) Save back into the same table AmazonData
df.to_sql("AmazonData", conn, if_exists="replace", index=False)

conn.close()
print("✅ Done! Added 'savings' column to AmazonData table.")
