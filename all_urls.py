import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import time

# def is_desired_format(url):
#     # This regex checks if the URL follows a specific pattern without a colon in the specific part
#     pattern = r'https://sunnah\.com/([^/:]+)(/\d+)?(/|$)'
#     match = re.search(pattern, url)
#     if match:
#         print(f"Matched URL: {url}")  # Debugging output
#         return True




def fetch_page_content(url, session):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        time.sleep(1)  # Sleep for 1 second before making a request
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX
        return response.content
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def is_unwanted_link(link):
    """Check if the link contains one of the undesired paths."""
    unwanted_paths = ['/about', '/contact', '/privacy','/searchtips','/news','changelog','narrator/',
                      'https://quranicaudio.com','https://salah.com'
                      'https://quran.com','https://sunnah.com/developers','https://sunnah.com/support']  # Add more paths as needed
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

            for link in links:
                full_link = urljoin(url, link)
                # Ensure the link is not unwanted, is valid, and has not been visited
                if not is_unwanted_link(full_link) and is_valid_url(full_link, base_domain) and full_link not in visited :
                      # or process it as needed
                    stack.append((full_link, depth + 1))

# Start the crawl
if __name__ == "__main__":
    starting_url = 'https://sunnah.com/'
    with requests.Session() as session:
        crawl_website(starting_url, session)