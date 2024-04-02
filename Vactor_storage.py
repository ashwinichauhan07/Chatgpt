import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, PodSpec
import os
from dotenv import load_dotenv
import re




# Load the .env file from the current directory
load_dotenv()

# Access variables using os.getenv()
Pincone_API_KEY = os.getenv("pincone_API_KEY")
# Initialize Pinecone
#
pc = Pinecone(api_key=Pincone_API_KEY)
index_name = "websitetext"
vector_dimension = 384

# Check if the index exists and create it if not
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=vector_dimension,
        metric="cosine",  # or "euclidean", depending on your use case
        spec=PodSpec(
            pod_type="starter",
            environment="gcp-starter"  # Choose the region that is closest to you or your users
        )
    )

# Connect to the Pinecone index
index = pc.Index(name=index_name)

model = SentenceTransformer('all-MiniLM-L6-v2')
def text_to_vector(text):
    return model.encode(text)

# Initialize a requests session
session = requests.Session()



def fetch_page_content(url, session):
    """Fetch the content of the page."""
    try:
        response = session.get(url)
        response.raise_for_status()  # Raises an HTTPError for 4XX or 5XX status codes
        return response.content
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def scrape_text_from_link(url, session):
    """Scrape and print the text from the given URL."""
    content = fetch_page_content(url, session)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        content = ' '.join(paragraphs)
        # Convert text to vector
        vector = text_to_vector(content)
        # Insert into Pinecone (using URL as ID for simplicity)
        index.upsert(vectors=[(url, vector)])
        print(f"Inserted text vector from {url} into Pinecone.")  # Print first 500 characters for brevity


def is_unwanted_link(link):
    """Check if the link contains one of the undesired paths."""
    unwanted_paths = ['/about', '/contact', '/privacy','/searchtips','/news','changelog','narrator/',
                      'https://quranicaudio.com','https://salah.com'
                      'https://quran.com','https://sunnah.com/developers','https://sunnah.com/support']
    return any(unwanted_path in link for unwanted_path in unwanted_paths)


def is_desired_format(url):
    # This regex checks if the URL follows a specific pattern without a colon in the specific part
    pattern = r'https://sunnah\.com/([^/:]+)(/\d+)?(/|$)'
    match = re.search(pattern, url)
    if match:
        # print(f"Matched URL: {url}")  # Debugging output
        return True


def is_valid_url(url, base_domain):
    """Checks if a URL is valid and belongs to the same domain."""
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc) and parsed_url.netloc == base_domain

def crawl_website(url, session, visited=set()):
    """Crawl a website, visiting all unique links within the same domain."""
    if url in visited:
        return
    visited.add(url)

    scrape_text_from_link(url, session)  # Scrape text from the current page

    content = fetch_page_content(url, session)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        base_domain = urlparse(url).netloc
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        for link in links:
            full_link = urljoin(url, link)
            if not is_unwanted_link(full_link) and is_valid_url(full_link, base_domain) and full_link not in visited and is_desired_format(full_link):
                crawl_website(full_link, session, visited)

# Starting URL for crawling
url = 'https://sunnah.com/'  # Replace with your target URL

# Start the crawling process
crawl_website(url, session)