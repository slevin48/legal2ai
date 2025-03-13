import streamlit as st
import pandas as pd

# Load the data
def load_categories():
    return pd.read_csv('data/categories-list.csv', header=None, names=['category'])

cat = load_categories()

# Streamlit app layout
st.title("Admin")

# Display categories in a text area
categories = st.text_area("Categories", value="\n".join(cat['category'].tolist()), height=300)