import streamlit as st
import pandas as pd
import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import ast

def get_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# Load the data
def load_data():
    return pd.read_csv('data/legal-prompts-embeddings-with-category.csv')

def load_categories():
    return pd.read_csv('data/categories-embeddings.csv')

# Streamlit app layout
st.sidebar.title("Centre d'administration")
view = st.sidebar.radio("Choisir une vue:", ["Categorisation des prompts","Exploration des catégories","Categoriser un nouveau prompt"], label_visibility='collapsed')
data = load_data()

if view == "Categorisation des prompts":
    # Browsing prompts
    st.subheader("Categorisation des prompts")

    # Display barchart of the categories using plotly
    category_counts = data['Category_predicted'].value_counts().sort_values(ascending=False)
    st.write(category_counts)
    st.bar_chart(category_counts, color='count', use_container_width=True, horizontal=True)

    # Add a search bar to filter prompts
    search_query = st.text_input("Search prompts:")
    filtered_data = data[data['Prompt'].str.contains(search_query, case=False, na=False)]
    st.dataframe(filtered_data.drop(columns=['Domain','Embedding']), hide_index=True, use_container_width=True)
    st.write(f"Found {filtered_data.shape[0]} prompts")

elif view == "Exploration des catégories":
    # Browsing categories
    st.subheader("Exploration des catégories")
    selected_category = st.selectbox("Sélectionner une catégorie:", data['Category_predicted'].unique())
    
    # Filter data for the selected category
    category_data = data[data['Category_predicted'] == selected_category]
    
    # Display prompts in the selected category
    st.write(f"Prompts dans la catégorie *{selected_category}* :")
    st.dataframe(category_data[['Prompt']], hide_index=True, use_container_width=True)

elif view == "Categoriser un nouveau prompt":
    st.subheader("Categorisation de nouveaux prompts")
    new_prompt = st.text_input("Entrer un nouveau prompt:")

    cat = load_categories()
    category_embeddings = cat['Embedding']
    category_embeddings = [ast.literal_eval(emb) for emb in category_embeddings]

    if new_prompt:
        # Get embedding for the new prompt
        new_embedding = get_embedding(new_prompt)
        
        # Reshape the new embedding to a 2D array
        new_embedding = np.array(new_embedding).reshape(1, -1)
        
        # Ensure category_embeddings is a 2D array
        category_embeddings_2d = np.array(category_embeddings) 
        if category_embeddings_2d.ndim == 1:
            category_embeddings_2d = category_embeddings_2d.reshape(-1, 1)
        
        # Compute cosine similarity
        similarities = cosine_similarity(new_embedding, category_embeddings_2d)[0]
        
        # Find the most similar prompt
        most_similar_idx = np.argmax(similarities)
        most_similar_category = cat['Category'][most_similar_idx]
        st.write("Appartient à la catégorie : ",most_similar_category)
        st.write("Score de similarité : ",similarities[most_similar_idx])

