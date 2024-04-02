
<<<<<<< HEAD
from langchain_community.chat_models import ChatOpenAI
=======
from langchain_community.chat_models import ChatCohere
>>>>>>> facccae66ed0241c2782eed4e3f3c8842aaefdd1
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import streamlit as st
import os
from dotenv import load_dotenv

# Load the .env file from the current directory
load_dotenv()

# Access variables using os.getenv()
<<<<<<< HEAD
OpenAI_API_KEY = os.getenv("OpenAI_API_KEY")
print(OpenAI_API_KEY)
=======
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

>>>>>>> facccae66ed0241c2782eed4e3f3c8842aaefdd1
prompt=PromptTemplate(
    input_variables=["chat_history","question"],
    template="""You are a kind AI agent, you are currently talking to human answer him/her in a friendly tone 
    
    chat_history:{chat_history}
    human:{question}
    AI: """
)

<<<<<<< HEAD
llm=ChatOpenAI(model="gpt-4",api_key=OpenAI_API_KEY)
=======
llm=ChatCohere(api_key=COHERE_API_KEY)
>>>>>>> facccae66ed0241c2782eed4e3f3c8842aaefdd1
memory=ConversationBufferMemory(memory_key="chat_history")
llm_chain=LLMChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True
) 
st.set_page_config(
    page_title="Chat with me",
    layout="wide"
)

st.title="Chat with me"
user_prompt=st.chat_input()

if "messages" not in st.session_state:
    st.session_state.messages=[
        {"role":"assistant","content":"Hello there, ask anything"}
    ]
else:
    for message in st.session_state.messages:
        if message["role"] != "assistant":  # Skip the initial assistant message
            memory.save_context(
        {'input': message['content']},  # Use 'content' key for message content
        {'output': message['content'] if message['role'] == 'assistant' else ''  }  # Store assistant's response as output
    )
    
for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])



if user_prompt is not None:
    st.session_state.messages.append({"role":"user","content":user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

if st.session_state.messages[-1]["role"]!="assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loding..."):
            ai_response=llm_chain.predict(question=user_prompt)
            st.write(ai_response)
    new_ai_response={"role":"assistant","content":ai_response}
    st.session_state.messages.append(new_ai_response)

<<<<<<< HEAD
=======

# with st.sidebar:
#     st.header("Conversation History")
#     for message in st.session_state.messages:
#         with st.expander(message["role"]):
#             st.write(message["content"])

>>>>>>> facccae66ed0241c2782eed4e3f3c8842aaefdd1
   
with st.sidebar:
    st.header("Chat History")
    with st.expander('conversation'): st.info(memory.buffer)
    
    if st.sidebar.button("Clear History"):
<<<<<<< HEAD
        st.session_state.messages = []
=======
        st.session_state.messages = []
>>>>>>> facccae66ed0241c2782eed4e3f3c8842aaefdd1
