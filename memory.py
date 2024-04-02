import os
from contants import COHERE_API_KEY
from langchain.llms import Cohere
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
import streamlit as st
input=st.text_input('Input:')
os.environ["COHERE_API_KEY"]=COHERE_API_KEY

llm=Cohere(model="command",max_tokens=100, temperature=0.75)
memory= ConversationBufferMemory()
conversation= ConversationChain(
    llm=llm, verbose=True, memory=memory
)
if input:
    response=conversation.predict(input=input)
    st.write(response)

    
print(conversation.memory.buffer)