from transformers import pipeline

model_name = "tabularisai/multilingual-sentiment-analysis"


sentiment_pipe = pipeline("text-classification", model=model_name)

print(sentiment_pipe("I love this product!"))
