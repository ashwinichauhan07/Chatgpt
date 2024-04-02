import os
<<<<<<< HEAD
# from contants import COHERE_API_KEY
=======
from contants import COHERE_API_KEY
>>>>>>> facccae66ed0241c2782eed4e3f3c8842aaefdd1
#from langchain.llms import cohere
import streamlit as st
from langchain.schema import HumanMessage, SystemMessage,AIMessage
from langchain.chat_models import cohere
<<<<<<< HEAD

=======
import shelve
>>>>>>> facccae66ed0241c2782eed4e3f3c8842aaefdd1
import cohere


#os.environ["COHERE_API_KEY"]=COHERE_API_KEY
#client = ChatCohere(temperature=0.7, api_key=COHERE_API_KEY)
co = cohere.Client('k9UV95uPtYxrklUp13NowufdqwmxWb9zvGvs4c23')
st.title("Chatbot")

#cohere_model=co.generate(model="command-nightly")
# Set a default model
#if "cohere_model" not in st.session_state:
   # st.session_state["cohere_model"] =co.generate(model="command-nightly")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt:=st.chat_input("What is up?"):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistent"):
        message_palceholder=st.empty()
        full_response=""

for response in co.chat.completion.create(
    model="command-nightly",
    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
    stream=True,
):
    full_response+=(response.choices[0].delta.content or "")
    message_palceholder.markdown(full_response)
st.session_state.messages.append({"role":"assistant","content":full_response})