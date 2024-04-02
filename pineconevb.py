from pinecone import Pinecone
from dotenv import load_dotenv
import os

# Load the .env file from the current directory
load_dotenv()

# Access variables using os.getenv()
Pincone_API_KEY = os.getenv("pincone_API_KEY")
# Initialize Pinecone
# print(Pincone_API_KEY)
#
pc = Pinecone(api_key=Pincone_API_KEY)
index_name = "websitetext"
index = pc.Index(index_name)

value=index.describe_index_stats()
print(value)