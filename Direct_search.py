import streamlit as st
from sentence_transformers import SentenceTransformer
from pineconevb import Pinecone
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Initialize Pinecone
Pincone_API_KEY = os.getenv("pincone_API_KEY")
pc = Pinecone(api_key=Pincone_API_KEY)
index_name = "websitetext"
vector_dimension = 384
index = pc.Index(name=index_name)


# Initialize the model for converting text to vectors
model = SentenceTransformer('all-MiniLM-L6-v2')

# Streamlit UI
st.title("Search and Retrieve Documents")

question = st.text_input("Enter your question:", "")

if st.button("Submit"):
    # Convert your query to a vector
    query_vector = model.encode(question)
    query_vector_list = query_vector.tolist()
    
    # Query Pinecone Index
    results = index.query(vector=query_vector_list, top_k=3)
    
    # Assuming your Pinecone index includes metadata with the document content
    documents = [(hit["id"], hit.get("values", {})) for hit in results["matches"]]
    # print(documents)
    # Display the document contents in numeric format
    for idx, (doc_id, content) in enumerate(documents, start=1):
        st.write(f"{idx}. {content}")

# Ensure that the 'metadata' field in your Pinecone index is populated with the document content or a summary.
