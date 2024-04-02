from pymilvus import MilvusClient

# # Replace uri and token with your own
# client = MilvusClient(
#     uri="https://in03-86febedb9550389.api.gcp-us-west1.zillizcloud.com", # Cluster endpoint obtained from the console
#     token="b4b4ed0dc810e8718d8b7c27241b2ad0e2941d239be8cd3a7a1aa9e04dc33c9ae35ef4e4d9dad56fd0ffb9f8d8902e5312064886" # API key or a colon-separated cluster username and password
# )

# # Create a collection
# # client.create_collection(
# #     collection_name="langchain",
# #     dimension=768
# # )
# res = client.describe_collection(
#     collection_name="langchain"
# )

# print(res)

from pymilvus import MilvusClient

# Replace with your GCP Milvus instance details
HOST = "https://in03-86febedb9550389.api.gcp-us-west1.zillizcloud.com"  # Example endpoint
# PORT = 19530  # Default port, but check your instance
COLLECTION_NAME = "langchain"  # Your collection name

# Replace with your authentication credentials
# USERNAME = "<your_username>"
PASSWORD = "b4b4ed0dc810e8718d8b7c27241b2ad0e2941d239be8cd3a7a1aa9e04dc33c9ae35ef4e4d9dad56fd0ffb9f8d8902e5312064886"  # Or API key depending on authentication method

# Create Milvus client
client = MilvusClient(
    host=HOST,
    
    collection_name=COLLECTION_NAME,
    # username=USERNAME,
    password=PASSWORD,
)

# Test connection
try:
    print("Successfully connected to Milvus instance!")
except Exception as e:
    print(f"Error connecting to Milvus: {e}")

# ... (Use the client object for Milvus operations)
