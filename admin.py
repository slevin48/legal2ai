import streamlit as st
import pandas as pd
import openai

def get_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# Load the data
def load_data():
    return pd.read_csv('data/legal-prompts-embeddings-with-category.csv')

# Streamlit app layout for browsing prompts
st.title("Prompt categorization")
data = load_data()

# Display barchart of the categories using plotly
category_counts = data['Category_predicted'].value_counts().sort_values(ascending=False)
st.write(category_counts)
st.bar_chart(category_counts, color='count', use_container_width=True, horizontal=True)

# Add a search bar to filter prompts
search_query = st.text_input("Search prompts:")
filtered_data = data[data['Prompt'].str.contains(search_query, case=False, na=False)]
st.dataframe(filtered_data.drop(columns=['Domain','Embedding']), hide_index=True, use_container_width=True)
st.write(f"Found {filtered_data.shape[0]} prompts")