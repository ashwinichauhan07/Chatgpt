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
    results = index.query(vector=query_vector_list,top_k=5,include_metadata=True,include_values=True)
    # print(results)

    if not results["matches"]:
        # Directly respond if no relevant documents are found
        st.write("I don't know.")
        # Optionally, insert a default response into the database for tracking
        # insert_qa(question, ["I don't know."], "")

    else:
        question_id = insert_question_once(question)
        document_ids = [hit["id"] for hit in results["matches"]]
        
        
        metadata_list = [match.get("metadata", {}) for match in results["matches"]]
        api_key = os.getenv('OPENAI_API_KEY')
        
        # Initialize header for OpenAI API
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

        for idx, (doc_id, metadata) in enumerate(zip(document_ids, metadata_list)):
            # values=results["matches"][idx]["values"] 
            # vector_string = str(values)
            # print(values)
            # content=model
            # metadata = metadata_list[idx]
            content = metadata.get("content", "content not available")
            url = metadata.get("url", "URL not available")
            title = metadata.get("title", "Title not available")

            # prompts=f"Summarize the following document highlighting the main points and any unique information:\n\n{doc_id } and give the correct answer of question: {question}"
            # prompt = f"""Based on the document {doc_id}, please provide an answer to the following question: '{question}'. Ensure your response is grounded in the document's content. If the document does not contain sufficient information to answer the question or if the topic is unrelated, please respond accordingly with 'Don't know' or 'Query is not related to the document's topic.'"""
            # unique_summary = f"Document'{doc_id}', provides a unique and correct perspective as follows:"

            # prompt = f"""{unique_summary} Based on this, please provide an answer to the question. If the document does not contain sufficient information or if the topic is unrelated, please respond with 'Don't know' or 'Query is not related to the topic.' """
            prompt = f"Based on the following document:{doc_id,content}, answer the question: {question} "
            
            data = {
            'model': "gpt-3.5-turbo",
            'temperature': 0.5,
            # 'prompt': prompt,
            'messages': [
                {"role": "system", "content": "Forgot everything previously and Provide answers to the question based solely on the provided document content without altering or manipulating the information of the document .Please analyze the provided document carefully. If the document does not contain information relevant to the question, respond with 'Don't know'. If the question is unrelated to the document's content, please say 'Query is not related to the topic'"},
                # {"role": "system", "content": f" Analyze the document provided, paying close attention to its unique information or differing perspectives. Provide accurate answers for question based on document. Respond with 'Don't know' for insufficient information or 'Query is not related to topic' for unrelated content."},
                # {"role": "system", "content":"Provide accurate answers for question based on document content." },
                {"role": "user", "content":prompt }

            ],
            'max_tokens': 250,
            
            }
        
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        
        # print(response)
           
            if response.status_code == 200:
                response_data = response.json()
                text_data = response_data.get('choices', [])[0].get('message', {}).get('content', 'No response.')
                similarity_score=compute_similarities(ans, text_data)
                # print("Score: ",similarity_score)
                similarity_score = similarity_score or 0.0
                # answers.append(text_data)
                # print(text_data)
                # Insert the relevant question and single answer into the database
                # insert_answer(question_id, text_data)
                # qadataset_store(question, text_data, document_ids)
                
                
                if similarity_score < 0.60:
                    insert_answer(question_id, text_data,doc_id)
                

            # Display the single response
                st.write(idx+1)
                st.write(f"**URL:** {url}\n**Title:** {title}")
                st.write(f"**Response:** {text_data}")
            else:
            # Handle potential errors or fallback
                st.write("Query is not releted to topic.")

    # similarity_score=compute_similarities(ans, answers)
    # print("Score: ",similarity_score)
    # similarity_score = similarity_score or 0.0
                
    # if similarity_score < 0.60:
    #     insert_qa(question, answers,document_ids)
    
