from langchain_community.vectorstores.milvus import Milvus
from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections
from pymilvus import MilvusClient
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from sentence_transformers import SentenceTransformer
import os
import time
from dotenv import load_dotenv

# Load the .env file from the current directory
load_dotenv()

COLLECTION_NAME = 'chatgpt'
DIMENSION = 384
URI = 'https://in03-693adc71aaf8473.api.gcp-us-west1.zillizcloud.com'
TOKEN = 'b4b4ed0dc810e8718d8b7c27241b2ad0e2941d239be8cd3a7a1aa9e04dc33c9ae35ef4e4d9dad56fd0ffb9f8d8902e5312064886'
# connection_args = { 'uri': URI, 'token': TOKEN }
client = MilvusClient(
    uri=URI, # Cluster endpoint obtained from the console
    token=TOKEN # API key or a colon-separated cluster username and password
)
# client.create_collection(
#     collection_name=COLLECTION_NAME,
#     dimension=DIMENSION
# )
existing_collections = client.list_collections()
# connections.connect(alias="default", host=URI, token=TOKEN)
if COLLECTION_NAME not in existing_collections:
    # Define fields for the collection
    # fields = [
    #     FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),  # Primary key field
    #     FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=255),  # Assuming title is a short text
    #     FieldSchema(name="text_vector", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION),
    #     FieldSchema(name="link", dtype=DataType.VARCHAR, max_length=2048)  # URLs can be long
    #     # Add other fields if necessary
    # ]
    # schema = client.create_schema(fields, description="Document QA Database")

    # Create collection
    client.create_collection(collection_name=COLLECTION_NAME,dimension=DIMENSION,
                             primary_field_name='id',id_type="int",auto_id=True,
                             vector_field_name="text_vector",)
else:
    collection = client.describe_collection(
    collection_name=COLLECTION_NAME
)
    


model = SentenceTransformer('all-MiniLM-L6-v2')
def text_to_vector(text):
    return model.encode(text)

# Initialize a requests session
session = requests.Session()

# Initialize the model for converting text to vectors (ensure consistency with your indexing process)
def scrape_text_from_link(url, session):
    content = fetch_page_content(url, session)
    all_content=[]
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        # print(soup)
        # paragraphs = [p.get_text() for p in soup.find_all('p')]
        # div_content = soup.find('div', class_='text_details')
        # paragraphs = div_content.find('p') if div_content else None
        paragraphs = [p.get_text() for p in soup.find('div', class_='text_details').find_all('p')] if soup.find('div', class_='text_details') else []

        all_content.extend(paragraphs)

# Extract text from elements with class 'transliteration'
        transliterations = [elem.get_text() for elem in soup.find_all(class_='transliteration')]
        all_content.extend(transliterations)

# Extract text from elements with class 'translation'
        translations = [elem.get_text() for elem in soup.find_all(class_='translation')]
        all_content.extend(translations)
        references = [elem.get_text() for elem in soup.find_all(class_='hadith_reference')]
        all_content.extend(references)
        title=[elem.get_text() for elem in soup.find_all(class_='englishchapter')]
        all_content.extend(title)
        # print(all_content)

# Combine all collected content into a single string
        combined_content = ' '.join(all_content)

# Generate a vector from the combined content
        vector = text_to_vector(combined_content)
        vector_list = vector.tolist() 
        # print(vector)
        
        data=[

            {
                
                "title": title,
                "text_vector": vector_list,
                "link": url,

             }
            ]

        
        # print(data)
   
        mr = client.insert(collection_name=COLLECTION_NAME,data=data )
        print(f"Inserted text vector from {url} and title:{title}  ")
        


        
def fetch_page_content(url, session):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        # time.sleep(1)  # Sleep for 1 second before making a request
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX
        return response.content
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def is_unwanted_link(link):
    """Check if the link contains one of the undesired paths."""
    unwanted_paths = ['https://sunnah.com/about', 'https://sunnah.com/contact', 'https://sunnah.com/privacy','https://sunnah.com/searchtips','https://sunnah.com/news','changelog','narrator/',
                      'https://quranicaudio.com','https://salah.com'
                      'https://quran.com','https://sunnah.com/developers','https://sunnah.com/support',
                        "/support", "/developers", "/contact",'/support','/developers','/about', '/news',
                        "https://www.facebook.com/Sunnahcom-104172848076350", "https://www.instagram.com/_sunnahcom/", 
                      "https://twitter.com/SunnahCom", "https://statcounter.com/"]  # Add more paths as needed
    return any(unwanted_path in link for unwanted_path in unwanted_paths)
def is_valid_url(url, base_domain):
    """Checks if a URL is valid and belongs to the same domain as the base domain."""
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc) and parsed_url.netloc == base_domain

def crawl_website(start_url, session, max_depth=5):   
    """Crawls a website from a starting URL, visiting all unique links within the same domain."""
    
    visited = set()
    
    stack = [(start_url, 0)]  # Stack of URLs to visit, each with their corresponding depth

    while stack:
        url, depth = stack.pop()
        if url in visited and depth > max_depth:
            continue

        visited.add(url)
        content = fetch_page_content(url, session)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            base_domain = urlparse(url).netloc
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            scrape_text_from_link(url, session)
            for link in links:
                full_link = urljoin(url, link)
                # Ensure the link is not unwanted, is valid, and has not been visited
                if not is_unwanted_link(full_link) and is_valid_url(full_link, base_domain) and full_link not in visited :
                    # print(full_link)  # or process it as needed
                    stack.append((full_link, depth + 1))

# Start the crawl
if __name__ == "__main__":
    starting_url = 'https://sunnah.com/muslim:1422a'
    with requests.Session() as session:
        crawl_website(starting_url, session)
