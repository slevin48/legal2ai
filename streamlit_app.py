import streamlit as st

# Set page title and icon
st.set_page_config(page_title="Legal2AI", page_icon="⚖️")
# st.sidebar.write(dict(os.environ))
# Password protection
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

st.logo('img/legal2ai.png')
if check_password():
        
    # Define your pages 📄
    
    class_page = st.Page("class.py", title="Classification", icon="📄")
    admin_page = st.Page("admin.py", title="Administration", icon="⚙️")

    # Create the navigation
    pg = st.navigation(
        {
            "Main": [class_page],
            "Admin": [admin_page],
        },
        position="sidebar",
        expanded=True
    )
    pg.run()