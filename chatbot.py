import openai
import json, os
import streamlit as st

if 'avatar' not in st.session_state:
  avatar = {"assistant": "🤖", "user": "🐱"}
else:
  avatar = st.session_state.avatar

if 'model' not in st.session_state:
  st.session_state.model = 'gpt-4o-mini'
else:
  model = st.session_state.model

# Functions
def new_chat():
   st.session_state.convo = []
   st.session_state.id += 1

def save_chat(n):
  file_path = f'chat/convo{n}.json'
  with open(file_path,'w') as f:
    json.dump(st.session_state.convo, f, indent=4)
    
def select_chat(file):
  st.session_state.convo = []
  with open(f'chat/{file}') as f:
    st.session_state.convo = json.load(f)
  st.session_state.id = int(file.replace('.json','').replace('convo',''))

def chat_stream(messages,model='gpt-4o-mini'):
  # Generate a response from the ChatGPT model
  completion = openai.chat.completions.create(
        model=model,
        messages= messages,
        stream = True
  )
  report = []
  res_box = st.empty()
  # Looping over the response
  for resp in completion:
      if resp.choices[0].finish_reason is None:
          # join method to concatenate the elements of the list 
          # into a single string, then strip out any empty strings
          report.append(resp.choices[0].delta.content)
          result = ''.join(report).strip()
          result = result.replace('\n', '')        
          res_box.write(result) 
  return result


# Initialization
if 'convo' not in st.session_state:
    st.session_state.convo = []

n = len(os.listdir('chat'))
if 'id' not in st.session_state:
    st.session_state.id = n

if 'debug' not in st.session_state:
    st.session_state.debug = False

id = st.session_state.id

st.sidebar.write(' ## Conversations')

# models_name = ['gpt-4o-mini', 'gpt-4o']
# selected_model = st.sidebar.selectbox('Select OpenAI model', models_name)

if st.sidebar.button('New Chat 🐱'):
   new_chat()
for file in sorted(os.listdir('chat')):
  filename = file.replace('.json','')
  if st.sidebar.button(f'💬 {filename}'):
     select_chat(file)

if not st.session_state['convo']:
    with st.chat_message("assistant", avatar=avatar["assistant"]):
        st.write(open('data/welcome_message.txt',encoding='utf-8').read())
    st.session_state['convo'] = [{'role': 'system', 'content': open('data/system_prompt.txt',encoding='utf-8').read()}]
   
# Display the response in the Streamlit app
for line in st.session_state.convo:
    # st.chat_message(line.role,avatar=avatar[line.role]).write(line.content)
    if line['role'] == 'user':
      st.chat_message('user',avatar=avatar['user']).write(line['content'])
    elif line['role'] == 'assistant':
      st.chat_message('assistant',avatar=avatar['assistant']).write(line['content'])

# Create a text input widget in the Streamlit app
prompt = st.chat_input(f'convo{st.session_state.id}')

if prompt:
  # Append the text input to the conversation
  with st.chat_message('user',avatar=avatar['user']):
    st.write(prompt)
  st.session_state.convo.append({'role': 'user', 'content': prompt })
  # Query the chatbot with the complete conversation
  with st.chat_message('assistant',avatar=avatar['assistant']):
     result = chat_stream(st.session_state.convo,model)
  # Add response to the conversation
  st.session_state.convo.append({'role':'assistant', 'content':result})
  save_chat(id)

# Debug
if st.session_state.debug:
  st.sidebar.write(st.session_state)