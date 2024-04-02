import streamlit as st
from sentence_transformers import SentenceTransformer
import requests
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from database import *
# from final_vectore import search_qurey

# Assuming all your imports and initializations are done here

# Load the .env file
load_dotenv()

# Initialize Pinecone
Pincone_API_KEY = os.getenv("pincone_API_KEY")
# Pincone_API_KEY="530ba1af-e67f-47c0-8bbc-81bb5fbc185d"
pc = Pinecone(api_key=Pincone_API_KEY)
index_name = "websitetext"
vector_dimension = 384
index = pc.Index(name=index_name)

# Initialize the model for converting text to vectors
model = SentenceTransformer('all-MiniLM-L6-v2')

# Streamlit UI
st.title("Chat with Me")

question = st.text_input("Enter your question:", "")

if st.button("Submit"):
    try:
        # Convert your query to a vector
        query_vector = model.encode(question)
        query_vector_list = query_vector.tolist()
    
        # Query Pinecone Index
        results = index.query(vector=query_vector_list, top_k=5, include_metadata=True)
        
        document_ids = [match["id"] for match in results["matches"]]
        metadata_list = [match.get("metadata", {}) for match in results["matches"]]
        print(document_ids)
        api_key = os.getenv('OPENAI_API_KEY')
        
        # Initialize header for OpenAI API
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

        st.subheader("Answer(s):")
        for idx, doc_id in enumerate(document_ids):
            metadata = metadata_list[idx]
            url = metadata.get("url", "URL not available")
            title = metadata.get("title", "Title not available")
            print(doc_id)
            # Construct prompt for each document
            prompt = f"When responding to a question, please base your answer on the information available in the document provided . If the answer is not clear or the information is not sufficient to make a conclusion, reply with 'I don't know.' If the question is not related to the topic of the document, please state, 'The query is off-topic.'"
            
            data = {
                'model': "gpt-3.5-turbo",
                'messages': [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": doc_id + "\n\n" + question}
                ],
                'max_tokens': 500,
            }
            
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            
            if response.status_code == 200:
                response_data = response.json()
                text_data = response_data.get('choices', [])[0].get('message', {}).get('content', 'No response.')
                
                # Display each document's elaboration and answer
                st.write(f"**URL:** {url}\n**Title:** {title}")
                st.write(f"**Response:** {text_data}")
                # st.write(text_data)
            else:
                st.error("Failed to receive a valid response from the language model for a document.")
    
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")






# if st.button("Submit"):
#     try:
#     # Convert your query to a vector
#         query_vector = model.encode(question)
#         query_vector_list = query_vector.tolist()
    
#     # Query Pinecone Index
#         results = index.query(vector=query_vector_list, top_k=5,include_metadata=True)
#         # print(results)

#     # Assuming `results` is the response from a Pinecone query
#         document_ids = [match["id"] for match in results["matches"]]
#         # print("documents",document_ids) 
#         metadata_list = [match.get("metadata", {}) for match in results["matches"]]

#         documents_info = ""
#         for idx, doc_id in enumerate(document_ids):
#             metadata = metadata_list[idx]
#             url = metadata.get("url", "URL not available")
#             title = metadata.get("title", "Title not available")
#             print(f"Document ID: {doc_id}, URL: {url}, Title: {title}")
#             documents_info += f"Document ID: {doc_id}, URL: {url}, Title: {title}\n"
    
#         # prompt = f"Based on the following documents: {document_ids} What is the answer to: '{question}'?"
#         prompt = f"Given the Islamic context and based on the following document information:\n{documents_info}\nWhat is the accurate answer to: '{question}'? Ensure the response includes URLs when possible and is reliable. If uncertain, respond with 'I don't know' or indicate if the query is off-topic."
#         api_key = os.getenv('OPENAI_API_KEY', 'OpenAI_API_KEY')
    
#         data = {
#             'model': "gpt-3.5-turbo",
#             'messages': [
#                 # {"role": "system", "content": "Exctract exact answer and related articles like Hadith for the question based on the content provided.Please do not provide false articles "},
#                 {"role": "system", "content": "Provide accurate and reliable answers with URLs when relevant. If the answer is not available, respond with 'I don't know'. If the question is unrelated to the topic, indicate as such."},
#                 {"role": "user", "content": prompt }
#             ],
#             'max_tokens': 250,
#             'n': 5,  # Adjust based on how many responses you want
#          }
        
#         headers = {
#             'Authorization': f'Bearer {api_key}',
#             'Content-Type': 'application/json',
#          }
    
#         response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    
#         if response.status_code == 200:
#             response_data = response.json()
#             text_data = [choice['message']['content'] for choice in response_data.get('choices', [])]
#         # st.write(text_data)
#     # Insert question and answers into the database
#         # insert_qa(question, text_data,document_id_str)

#     # Display the response(s) in numeric format
#         st.subheader("Answer(s):")
#         # for answer in text_data:
#         #     st.write(answer)
#         for idx, answer in enumerate(text_data, start=1):
#             st.write(f"{idx}. {answer}")
# # Run this app with `streamlit run your_script_name.py`
#     except requests.exceptions.RequestException as e:
#         st.error(f"An error occurred: {e}")
