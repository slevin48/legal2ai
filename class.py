import streamlit as st
import pandas as pd


# Load the data
def load_categories():
    return pd.read_csv('data/categories-list.csv', header=None, names=['category'])

cat = load_categories()

file = st.file_uploader("Upload an Excel file", type=["xlsx", "csv"])
if file:
    try:
        df = pd.read_excel(file, engine='openpyxl')
        # Check that the column 'Mail Contact' exists
        if 'Mail Contact' in df.columns:
            st.write("Original 'Mail Contact' column:")
            if st.checkbox("Show original data"):
                st.write(df['Mail Contact'])
            
            if st.button("Check Categories"):
                # Convert categories to a list
                categories = cat['category'].str.lower().tolist()
                
                # Create a mask for rows where Mail Contact contains any category
                mask = df['Mail Contact'].str.lower().apply(
                    lambda x: any(category in str(x).lower() for category in categories)
                )
                
                # Filter the dataframe to keep only matching rows
                matching_df = df[mask]
                
                if not matching_df.empty:
                    st.write("Rows with matching categories:")
                    st.write(matching_df['Mail Contact'])
                else:
                    st.warning("No matches found with any category.")
        else:
            st.error("The column 'Mail Contact' does not exist in the uploaded file.")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")