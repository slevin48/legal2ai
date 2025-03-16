import streamlit as st
import pandas as pd

# Load the data
def load_categories():
    return pd.read_csv('data/categories-list.csv', header=None, names=['category'])

cat = load_categories()

# Streamlit app layout
st.write("## Categories")

# Display categories as a dataframe
st.write(cat)