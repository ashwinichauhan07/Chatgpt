import streamlit as st
from langchain.llms import Cohere

st.title('🦜🔗 Quickstart App')

cohere_api_key = st.sidebar.text_input('COHERE_API_KEY')

def generate_response(input_text):
  #llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  llm=Cohere(model="command", max_tokens=100, temperature=0.75, cohere_api_key=cohere_api_key)
  st.info(llm(input_text))

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
  submitted = st.form_submit_button('Submit')
  if not cohere_api_key.startswith('k9'):
    st.warning('Please enter your API key!', icon='⚠')
  if submitted and cohere_api_key.startswith('k9'):
    generate_response(text)
    