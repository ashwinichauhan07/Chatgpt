import streamlit as st
from sentence_transformers import SentenceTransformer
import requests
from pymilvus import MilvusClient
import os
from dotenv import load_dotenv

# from database import *

# Assuming all your imports and initializations are done here

# Load the .env file
load_dotenv()

# Initialize Pinecone
COLLECTION_NAME = 'chatgpt'
DIMENSION = 384
URI = 'https://in03-693adc71aaf8473.api.gcp-us-west1.zillizcloud.com'
TOKEN = 'b4b4ed0dc810e8718d8b7c27241b2ad0e2941d239be8cd3a7a1aa9e04dc33c9ae35ef4e4d9dad56fd0ffb9f8d8902e5312064886'
# connection_args = { 'uri': URI, 'token': TOKEN }
client = MilvusClient(
    uri=URI, # Cluster endpoint obtained from the console
    token=TOKEN # API key or a colon-separated cluster username and password
)

collections = client.list_collections()
# print("collection",collections)
res = client.describe_collection(
    collection_name=COLLECTION_NAME
)

# Initialize the model for converting text to vectors
model = SentenceTransformer('all-MiniLM-L6-v2')

# Streamlit UI
st.title("Chat with Me")

question = st.text_input("Enter your question:", " ")

if st.button("Submit"):
    # Convert your query to a vector
    query_vector = model.encode(question)
    query_vector_list = query_vector.tolist()
    # print(query_vector)
    # Query Pinecone Index
    search_params = {
    "metric_type": "IP",
    "params": {"nprobe": 10}
    }
    top_k = 3 # Number of results you want

# Adjust the below search method call according to your Milvus version and setup
    results = client.search(collection_name=COLLECTION_NAME, 
                        data=[query_vector_list],  
                        # search_params=search_params, 
                        limit=top_k, 
                        output_fields=["title", "link", "text_vector","id"])
                        #  output_fields=["text_vector","id"])
    # print(results)
    documents = []
    for result in results:
        for hit in result:
            id=hit['id']
            # title = hit['entity'].get('title', 'No Title')  # Handle potential missing title
            url = hit['entity'].get('link', 'No URL')
        # Handle potential missing URL
            print("url",url)
            print("id",id)
            documents.append(f"{id} ")  # Combine title and URL with separator

    # for result in results:
    #     for hit in result:
    #         print(f"ID: {hit['id']}") # Combine title and URL with separator
    #         id=hit['id']
             
    
    # prompt = f"Based on the following documents: {documents} What is the answer to: '{question}'?"
    prompt = f"Based on the following documents: {id} "
    api_key = os.getenv('OPENAI_API_KEY', 'OpenAI_API_KEY')
    
    data = {
            'model': "gpt-3.5-turbo",
            'messages': [
                {"role": "system", "content": "Exctract answer  for the question based on the provided id.Please do not provide false articles Please ensure the answer is accurate and reliable. If you cannot find answer related to the query, please respond with 'Dont know'. if Topic is not related to provided content, then say 'Query is not related to topic. ' "},
                # {"role": "system", "content": "Please give answers from the provided documents related to question. Please ensure the answer is accurate and reliable. If you cannot find answer related to the query, please respond with 'Dont know'. if Topic is not related to provided content, then say 'Query is not related to topic. ' "},
                {"role": "user", "content": prompt + "\n\n" + question}
            ],
            'max_tokens': 250,
            'n': 5,  # Adjust based on how many responses you want
        }
        
    headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
    
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    
    if response.status_code == 200:
        response_data = response.json()
        text_data = [choice['message']['content'] for choice in response_data.get('choices', [])]
        # st.write(text_data)
    # Insert question and answers into the database
        # insert_qa(question, text_data,document_id_str)

    # Display the response(s) in numeric format
        # for idx, answer in enumerate(text_data, start=1):
        #     st.write(f"{idx}. {answer}")
        for idx, answer in enumerate(text_data, start=1):
            st.write(f"{idx}. {answer}")
# Run this app with `streamlit run your_script_name.py`
