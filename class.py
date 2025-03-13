import streamlit as st
import openai
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
import ast

def load_categories_embeddings():
    df = pd.read_csv('data/categories-list-embeddings.csv')
    # Convert the embedding string into an actual list of floats
    df['embedding'] = df['embedding'].apply(ast.literal_eval)
    return df

def get_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

cat = load_categories_embeddings()

st.title("Classification")

email = st.text_input("Enter email to classify","bob@avocat.fr")
if st.button("Classify"):
    # compare email embedding with each category embedding
    email_emb = get_embedding(email)
    cos_sim = [cosine_similarity(np.array(email_emb).reshape(1, -1), np.array(x).reshape(1, -1))[0][0] for x in cat['embedding']]
    cat['similarity'] = cos_sim
    cat.sort_values('similarity', ascending=False).head()
    # Get top 15 most similar categories
    top_n = cat.nlargest(15, 'similarity')

    st.write(f'Top 15 Similar Categories for {email}')
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_n['category'], y=top_n['similarity'], data=top_n)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Category')
    plt.ylabel('Cosine Similarity')
    plt.tight_layout()
    st.pyplot(plt)