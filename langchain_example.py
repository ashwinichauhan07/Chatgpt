import os
from contants import COHERE_API_KEY
from langchain.llms import Cohere
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.memory import ConversationBufferMemory

os.environ["COHERE_API_KEY"]=COHERE_API_KEY

#streamlit framework
import streamlit as st

#st.title('Langchain Demo')
st.title(' :green[_Hypothetical POC_] ')
#st.markdown("*Search _the_ topic")
input_text=st.text_input("Search the topic")

#prompt Template
first_text = PromptTemplate(
    input_variables=['topic'],
    template="Tell me about {topic}"
)

person_memory= ConversationBufferMemory(input_key='topic',memory_key='chat_history')
dob_memory= ConversationBufferMemory(input_key='title',memory_key='chat_history')
description_memory= ConversationBufferMemory(input_key='dob',memory_key='discription_history')

llm=Cohere(model="command", temperature=0.75)
chain=LLMChain(llm=llm, prompt=first_text, verbose=True,output_key='title',memory=person_memory)

#prompt Template
second_text = PromptTemplate(
    input_variables=['title'],
    template="when was {title} born"
)
chain2=LLMChain(llm=llm, prompt=second_text, verbose=True,output_key='dob',memory=dob_memory)

#prompt Template
third_text = PromptTemplate(
    input_variables=['dob'],
    template="Mension 5 major events happened around {dob} in the world"
)
chain3=LLMChain(llm=llm, prompt=third_text, verbose=True,output_key='description',memory=description_memory)

parent_chain=SequentialChain(chains=[chain,chain2,chain3],input_variables=['topic'], output_variables=['title','dob','description'],verbose=True)



if input_text:
    st.write(parent_chain({'topic':input_text}))

<<<<<<< HEAD
=======
    #with st.expander('person name'): st.info(person_memory.buffer)
    #with st.expander('Mejor Events'): st.info(description_memory.buffer)

>>>>>>> facccae66ed0241c2782eed4e3f3c8842aaefdd1
   
with st.sidebar:
    st.header("Chat History")
    with st.expander('person name'): st.info(person_memory.buffer)
    with st.expander('Mejor Events'): st.info(description_memory.buffer)
    #st.write("Person Name:", person_memory.buffer)
    #st.write("Major Events:", description_memory.buffer)