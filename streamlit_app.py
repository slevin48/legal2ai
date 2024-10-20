import streamlit as st

# Set page title and icon
st.set_page_config(page_title="Legal2AI", page_icon="⚖️")

# Password protection for admin
def check_password(password):
    """Returns `True` if the password is correct."""
    return password == st.secrets["PASSWORD"]

# Initialize admin status in session state
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Login function
def login():

    with st.form("login_form"):
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login as Admin")
        
        if submit_button:
            if check_password(password):
                st.session_state.is_admin = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")

# Logout function
def logout():
    st.session_state.is_admin = False
    st.success("You have been logged out.")
    st.rerun()

st.logo('img/legal2ai.png')

# Define your pages
chatbot_page = st.Page("chatbot.py", title="Assistant", icon="🤖")
config_page = st.Page("config.py", title="Configuration", icon="⚙️")
admin_page = st.Page("admin.py", title="Admin", icon="📄")

# Login/Logout pages
login_page = st.Page(login, title="Log in", icon="🔑")
logout_page = st.Page(logout, title="Log out", icon="🚪")

# Create the navigation based on admin status
if not st.session_state.is_admin:
    # Non-admin user
    pg = st.navigation(
        {
            "Main": [chatbot_page],
            "Admin": [login_page],
        },
        position="sidebar",
        expanded=True
    )
else:
    # Admin user
    pg = st.navigation(
        {
            "Main": [chatbot_page],
            "Admin": [admin_page, config_page],
            "Account": [logout_page],
        },
        position="sidebar",
        expanded=True
    )

pg.run()
