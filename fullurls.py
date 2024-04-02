from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
import re
import time

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
    unwanted_paths = ['https://sunnah.com/about', 'https://sunnah.com/contact', 'https://sunnah.com/privacy','https://sunnah.com/searchtips','https://sunnah.com/news','changelog','narrator/',
                      'https://quranicaudio.com','https://salah.com'
                      'https://quran.com','https://sunnah.com/developers','https://sunnah.com/support',
                        "/support", "/developers", "/contact",
                        "https://www.facebook.com/Sunnahcom-104172848076350", "https://www.instagram.com/_sunnahcom/", 
                      "https://twitter.com/SunnahCom", "https://statcounter.com/"]
    return any(unwanted_path in link for unwanted_path in unwanted_paths)

def is_valid_url(url, base_domain):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc) and parsed_url.netloc == base_domain

def crawl_website(start_url, session, max_depth=5):
    visited = set()
    stack = [(start_url, 0)]  # Stack of URLs to visit, each with their corresponding depth

    while stack:
        url, depth = stack.pop()
        if url in visited or depth > max_depth:  # Corrected condition to skip visited URLs or URLs beyond max depth
            continue

        visited.add(url)
        content = fetch_page_content(url, session)
        if content:
            print(url)  # Moved URL printing here to ensure uniqueness
            soup = BeautifulSoup(content, 'html.parser')
            base_domain = urlparse(url).netloc
            links = [a.get('href') for a in soup.find_all('a', href=True)]

            for link in links:
                full_link = urljoin(url, link)
                if not is_unwanted_link(full_link) and is_valid_url(full_link, base_domain) and full_link not in visited:
                    stack.append((full_link, depth + 1))

if __name__ == "__main__":
    starting_url = 'https://sunnah.com/bukhari'
    with requests.Session() as session:
        crawl_website(starting_url, session)
