import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

df = pd.read_csv("books.csv") 
df['title'] = df['title'].strip()
df['description'] = df['description'].fillna("")

vetorizer = TfidfVectorizer(stop_words='english')
tfidf_metrix = vetorizer.fit_transform(df['description'])

cosine_sim = cosine_similarity(tfidf_metrix,tfidf_metrix)

indices = pd.Series(df.index,index=df['title'].str.lower()).drop_duplicates() 

def get_recommendation(title,df,cosine_sim,indices):
    title = title.strip().lower()
    
    if title not in indices.index:
        return f"{title} Not found in dataset"
    idx = indices.loc[title]
    if isinstance(idx,pd.Series):
        idx = idx.iloc[0]
    idx = indices[title]
    sim_score = list(enumerate(cosine_sim[idx]))
    sim_score = sorted(sim_score,key=lambda x: x[1],reverse=True)[1:6]
    
    books_indices = [i[0] for i in sim_score]
    df[['title','author']].iloc[books_indices] 
    
    
st.title("Book Reommendation engine") 
st.write("Enter book name and  get similar recommendation ")   

select_book = st.text_input("Book: Title ")

if select_book:
    results = get_recommendation(select_book,df,cosine_sim,indices)
    #st.table(results)
    if isinstance(results,pd.DataFrame):
        st.table(results)
    else:
        st.warning(results)    