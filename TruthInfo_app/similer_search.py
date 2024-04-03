import streamlit as st
from sentence_transformers import SentenceTransformer
import requests
from final_vectore import *
# from storeQA_pinecone import qadataset_store
import os
from comparing_answer import compute_similarities
from dotenv import load_dotenv
from pinecone import Pinecone
from database import *  # this contains the necessary database operations


# Load the .env file
load_dotenv()

# Initialize Pinecone
Pincone_API_KEY = os.getenv("pincone_API_KEY")  # Corrected variable name
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

    # try to fetch similer question from mysql database
    ans=similarity_search(question)
    # Convert your query to a vector
    query_vector = model.encode(question)
    query_vector_list = query_vector.tolist()

    # search_qurey_finalvector(query_vector_list)

    # Query Pinecone Index
    results = index.query(vector=query_vector_list,top_k=5,include_metadata=True)
    # print(results)

    if not results["matches"]:
        # Directly respond if no relevant documents are found
        st.write("I don't know.")
        # Optionally, insert a default response into the database for tracking
        # insert_qa(question, ["I don't know."], "")

    else:
        # question_id = insert_question_once(question)
        document_ids = [hit["id"] for hit in results["matches"]]
        document_ids_str = str(document_ids)
        text_content = index.fetch(ids=[document_ids_str])
        
        metadata_list = [match.get("metadata", {}) for match in results["matches"]]
        api_key = os.getenv('OPENAI_API_KEY')
        
        # Initialize header for OpenAI API
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        answers=[]
        for idx, doc_id in enumerate(document_ids):
            metadata = metadata_list[idx]
            url = metadata.get("url", "URL not available")
            title = metadata.get("title", "Title not available")
            # print(f"Document ID: {doc_id}, URL: {url}, Title: {title}")
            # prompt = f"Based on the following documents: {doc_id}. What is the answer to: '{question}'?"
            # prompt=f"Answer the users {question} using the DOCUMENT {doc_id}. If the DOCUMENT doesn’t contain the facts to answer the QUESTION return 'Dont know'."
            prompt = f"Based on the following documents: {doc_id}."
    
            data = {
            'model': "gpt-3.5-turbo",
            'messages': [
                {"role": "system", "content": "You are expert in islam. Give answers for question from provided document. Please ensure the information is accurate and reliable. If you cannot find answer related to the query, please respond with 'Dont know'. if Topic is not related to provided content, then say 'Query is not related to topic. ' "},
                # {"role": "system", "content": "Answer the users QUESTION using the DOCUMENTS. Keep your answer ground in the facts of the DOCUMENT. If the DOCUMENT doesn’t contain the facts to answer the QUESTION return 'Dont know'. if Topic is not related to provided content, then say 'Query is not related to topic. ' "},
                # {"role": "user", "content": prompt}
                {"role": "user", "content": prompt + "\n\n" + question}
            ],
            'max_tokens': 500,
            
            }
        
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        
        # print(response)
           
            if response.status_code == 200:
                response_data = response.json()
                text_data = response_data.get('choices', [])[0].get('message', {}).get('content', 'No response.')
                answers.append(text_data)
                # print(text_data)
                # Insert the relevant question and single answer into the database
                # insert_answer(question_id, text_data)
                # qadataset_store(question, text_data, document_ids)

                

            # Display the single response
                st.write(idx+1)
                st.write(f"**URL:** {url}\n**Title:** {title}")
                st.write(f"**Response:** {text_data}")
            else:
            # Handle potential errors or fallback
                st.write("Query is not releted to topic.")

    similarity_score=compute_similarities(ans, answers)
    print("Score: ",similarity_score)
    similarity_score = similarity_score or 0.0
                
    if similarity_score < 0.60:
        insert_qa(question, answers,document_ids)
    
