from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain.document_transformers import BeautifulSoupTransformer
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.milvus import Milvus
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import StructuredOutputParser
from langchain.chains import LLMChain

import asyncio
import streamlit as st

import os
from dotenv import load_dotenv

# Load the .env file from the current directory
load_dotenv()

# Access variables using os.getenv()
OpenAI_API_KEY = os.getenv("OpenAI_API_KEY")



#web scraping 
urls = ['https://sunnah.com/']
llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125",  api_key=OpenAI_API_KEY)


loader = WebBaseLoader('https://sunnah.com/')
docs = loader.load()
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(docs, tags_to_extract=["span"])
    # print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000,
                                                                    chunk_overlap=0)
splits = splitter.split_documents(docs_transformed)


COLLECTION_NAME = 'doc_qa_db'
DIMENSION = 786
URI = 'https://in03-86febedb9550389.api.gcp-us-west1.zillizcloud.com'
TOKEN = 'b4b4ed0dc810e8718d8b7c27241b2ad0e2941d239be8cd3a7a1aa9e04dc33c9ae35ef4e4d9dad56fd0ffb9f8d8902e5312064886'
connection_args = { 'uri': URI, 'token': TOKEN }



vectorstore = Milvus.from_documents(documents=splits, embedding=OpenAIEmbeddings(),
                                    collection_name=COLLECTION_NAME,
                                    connection_args=connection_args,
                                    )

# retrive from vector
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# print('retriver',retriever)
prompt = PromptTemplate(
    input_variables=["question"],
    template="""You are a exper in islam, give similer answer from given question
    
    human:{question}
    AI: """
)


# memory = ConversationBufferMemory(memory_key="chat_history")

# llm_chain = create_extraction_chain(structured_schema, llm,prompt)


llm_chain=LLMChain( llm=llm,prompt=prompt)

# st.set_page_config(page_title="Chat with me", layout="wide")
st.title="Chat with me"
user_prompt=st.chat_input()

if "messages" not in st.session_state:
    st.session_state.messages=[
        {"role":"assistant","content":"Hello there, ask anything"}
    ]
# else:
#     for message in st.session_state.messages:
#         if message["role"] != "assistant":  # Skip the initial assistant message
#             memory.save_context(
#         {'input': message['content']},  # Use 'content' key for message content
#         {'output': message['content'] if message['role'] == 'assistant' else ''  }  # Store assistant's response as output
#     )
    
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

   
# with st.sidebar:
#     st.header("Chat History")
#     with st.expander('conversation'): st.info(memory.buffer)
    
#     if st.sidebar.button("Clear History"):
#         st.session_state.messages = []