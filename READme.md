📊 Amazon Product Reviews Analysis

This project focuses on analyzing Amazon product reviews using Excel, Python (Pandas), SQLite, and AI-powered sentiment analysis with Hugging Face.
It represents a practical workflow for data cleaning, feature engineering, and storage in a database, forming the foundation for deeper analysis and chatbot integration.

📂 Project Structure
WEEK3_PROJECT/             
│── src/                 
│   ├── Sentiment_Analysis.py        # Test script for single-sentence sentiment analysis                   
│   ├── sentiment_batch.py           # Batch pipeline: adds sentiment columns to dataset and DB                    
│   └── amazon_product_reviews.xlsx  # Cleaned dataset (Excel source file)            
│                        
│── AmazonData.db                    # SQLite database with full dataset + engineered features                                 
│── Conn.ipynb                       # Notebook for database connection and SQL queries                     

🧹 Data Cleaning & Filtering (Excel)

Before moving to Python, the dataset was carefully cleaned in Excel to ensure consistent and reliable analysis:

Price Columns (discounted_price, actual_price)

Removed currency symbols ($, SAR, ₹).

Removed thousand separators (, and Indian-style separators like 1,79,691).


Removed % symbols.


Cleaned rating_count by removing commas and storing as integers.


This Excel step gave a clean, analysis-ready dataset that could be safely imported into Python and SQLite.

⚙️ Features & Workflow
1. Data Import & Database Integration

Used Pandas to load the cleaned Excel file.

Stored the dataset into SQLite (AmazonData.db)

Enabled running SQL queries directly from Python or Jupyter Notebook.

2. Feature Engineering

Sentiment Analysis applied on review_content using the Hugging Face multilingual sentiment model.

Added two new columns to the dataset and DB :

sentiment_label → Positive / Neutral / Negative

sentiment_score → Confidence score (0–1)

3. Scripts

Sentiment_Analysis.py: Quick test of the Hugging Face model on single sentences.

sentiment_batch.py: Full batch pipeline that processes every review in Excel, appends sentiment columns, and updates the SQLite DB.

🚀 Tech Stack

Python: Pandas, SQLite, Transformers (Hugging Face)

Excel: Initial cleaning & filtering

SQLite: Database storage (AmazonData.db)

Jupyter Notebook: For queries and interactive exploration

📈 Next Steps

Perform statistical analysis (e.g., how discount percentage affects sentiment).

Build visualizations (top-rated products, discount vs. rating trends).

Extend into a chatbot that can answer queries like:

“Show me all negative reviews for Electronics products.”


## Author & Acknowledgments
Author: Ahmad Alali


### License   
This project is licensed under the MIT License.