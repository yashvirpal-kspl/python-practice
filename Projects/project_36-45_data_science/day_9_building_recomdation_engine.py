import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("books.csv") 

vetorizer = TfidfVectorizer(stop_words='english')
tfidf_metrix = vetorizer.fit_transform(df['description'])

cosine_similarities = cosine_similarity(tfidf_metrix,tfidf_metrix)

indices = pd.Series(df.index,index=df['title']) 

def get_recommendation(title,cosine_sim=cosine_similarities):
    idx = indices[title]
    sim_score = list(enumerate(cosine_sim[idx]))
    sim_score = sorted(sim_score,key=lambda x: x[1],reverse=True)[1:6]
    
    books_indices = [i[0] for i in sim_score]
    df[['title','author']].iloc[books_indices] 