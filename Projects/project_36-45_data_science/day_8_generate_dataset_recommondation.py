import pandas as pd 
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import streamlit as st

data = [
    {
        "title":"the silent forect",
        "author":"Jane hill",
        "genre":"mystery",
        "description":"THis desciptfdfdfdsfkd dsfndksfds fewgwfrer  grrggt"
    },
    {
        "title":"the silent forect1",
        "author":"Jane hill1",
        "genre":"mystery1",
        "description":"THis desciptfdfdfdsfkd dsfndksfds fewgwfrer  grrggt1"
    },
    {
        "title":"the silent forect2",
        "author":"Jane hill2",
        "genre":"mystery3",
        "description":"THis desciptfdfdfdsfkd dsfndksfds fewgwfrer  grrggt3"
    }
]
df = pd.DataFrame(data)
df.to_csv("books.csv",index=False)
print("Book dataset created")