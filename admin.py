import streamlit as st
import shutil, os

def zip_chat():
  # Zip the chat folder
  shutil.make_archive('chat', 'zip', 'chat')
  st.toast('Chat zipped!',icon = "🥞")

@st.experimental_dialog("Cast your vote")
def delete_chat():
    st.write("❌ Are you sure you want to delete the chat history?")
    if st.button("Delete chat history"):
        shutil.rmtree('chat')
        os.mkdir('chat')
        st.rerun() 

assistant_emojis = ['🤖', '⚖️', '👩‍⚖️', '🧑‍⚖️', '🧑‍💼']
user_emojis = ['🐱', '🙂', '🤓', '🤐', '👨‍💼']
models_name = ['gpt-4o-mini', 'gpt-4o']

if 'avatar' not in st.session_state:
  st.session_state.avatar = {"assistant": "🤖", "user": "🐱"}

if 'model' not in st.session_state:
    st.session_state.model = 'gpt-4o-mini'

if 'debug' not in st.session_state:
  st.session_state.debug = False

st.session_state.model = st.selectbox('Select Model', models_name,index=models_name.index(st.session_state.model))

col1,col2 = st.columns(2)
current_assistant = st.session_state.get('avatar', {}).get('assistant', '🤖')
current_user = st.session_state.get('avatar', {}).get('user', '🐱')

with col1:
  assistant = st.radio('Select Assistant', assistant_emojis, index=assistant_emojis.index(current_assistant))
with col2:
  user = st.radio('Select User', user_emojis, index=user_emojis.index(current_user))
st.session_state.avatar = {"assistant": assistant, "user": user}

if st.toggle('Export history'):
  zip_chat()
  st.download_button('Download chat history',open('chat.zip', 'rb'),'chat.zip',mime='application/zip')

if st.button('Delete history'):
  delete_chat()

st.session_state.debug = st.toggle('Debug mode',value=st.session_state.debug)
if st.session_state.debug:
  st.sidebar.write(st.session_state)
