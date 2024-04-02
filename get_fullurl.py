import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re


def is_desired_format(url):
    # This regex checks if the URL follows a specific pattern without a colon in the specific part
    pattern = r'https://sunnah\.com/([^/:]+)(/\d+)?(/|$)'
    match = re.search(pattern, url)
    if match:
        print(f"Matched URL: {url}")  # Debugging output
        return True

def fetch_page_content(url, session):
    try:
        response = session.get(url)
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

def crawl_website(url, session, visited=set(), depth=0, max_depth=5):
    """Crawls a website from a starting URL, visiting all unique links within the same domain."""
    if url in visited :
        return
    visited.add(url)

    content = fetch_page_content(url, session)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        base_domain = urlparse(url).netloc
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        for link in links:
            full_link = urljoin(url, link)
            # Ensure the link is not unwanted, is valid, and has not been visited
            if not is_unwanted_link(full_link) and is_valid_url(full_link, base_domain) and full_link not in visited and is_desired_format(full_link):
                print(full_link)
                crawl_website(full_link, session, visited, depth+1, max_depth)

# Start the crawl
if __name__ == "__main__":
    starting_url = 'https://sunnah.com/'
    with requests.Session() as session:
        crawl_website(starting_url, session)