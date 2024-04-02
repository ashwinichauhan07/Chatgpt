import requests
from bs4 import BeautifulSoup
import os
import json
from urllib.parse import urljoin, urlparse
 
# url = 'https://sunnah.com'
session=requests.Session()


import re


def is_desired_format(url):
    # This regex checks if the URL follows a specific pattern without a colon in the specific part
    pattern = r'https://sunnah\.com/([^/:]+)(/\d+)?(/|$)'
    match = re.search(pattern, url)
    if match:
        # print(f"Matched URL: {url}")  # Debugging output
        return True



def fetch_page_content(url, session):
    try:
        response = session.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX or 5XX
        return response.content
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def scrape_text_from_link(url, session):
    content = fetch_page_content(url, session)
    all_content = []  # List to hold all extracted content
    references = []  # List to hold all hrefs from 'a' tags
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        # print(soup)
       
        # paragraphs = [p.get_text() for p in soup.find_all('p')]
        # content = ' '.join(paragraphs)
        # all_content.append(content)
        # combined_content = ' '.join(all_content)

        # references = [a['href'] for a in soup.find_all('a', href=True)]
            # combined_references = ', '.join(references)
        


        elements = soup.find_all(['p', 'a'])

        for element in elements:
            if element.name == 'p':
        # If the element is a paragraph, extract its text
                all_content.append(element.get_text())
            elif element.name == 'a' and element.has_attr('href'):
        # If the element is an anchor tag with an href attribute, extract the href
                references.append(element['href'])
        combined_content = ' '.join(all_content)
        print(f"Text from {url}:\n{combined_content}")  # Print first 500 characters for brevity
        print(f"References from {url}:\n{references}") # Print first 500 characters for brevity
    else:
        print(f"Failed to fetch content from {url}")



def is_unwanted_link(link):
    """Check if the link contains one of the undesired paths."""
    unwanted_paths = ['https://sunnah.com/about', 'https://sunnah.com/contact', 'https://sunnah.com/privacy','https://sunnah.com/searchtips','https://sunnah.com/news','changelog','narrator/',
                      'https://quranicaudio.com','https://salah.com'
                      'https://quran.com','https://sunnah.com/developers','https://sunnah.com/support',
                        "/support", "/developers", "/contact",
                        "https://www.facebook.com/Sunnahcom-104172848076350", "https://www.instagram.com/_sunnahcom/", 
                      "https://twitter.com/SunnahCom", "https://statcounter.com/"]  # Add more paths as needed
    return any(unwanted_path in link for unwanted_path in unwanted_paths)

def is_valid_url(url, base_domain):
    """Checks if a URL is valid and belongs to the same domain as the base domain."""
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc) and parsed_url.netloc == base_domain

def crawl_website(url, session, visited=set()):
    """Crawls a website from a starting URL, visiting all unique links within the same domain."""
    if url in visited:
        return
    visited.add(url)

    content = fetch_page_content(url, session)
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        base_domain = urlparse(url).netloc
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        # print(links)
        scrape_text_from_link(url, session)  # Scrape text from the current page

        for link in links:
            full_link = urljoin(url, link)
            # print(full_link)
            if not is_unwanted_link(full_link) and is_valid_url(full_link, base_domain) and full_link not in visited and is_desired_format(full_link):
                # print(full_link)
                crawl_website(full_link, session, visited)


if __name__ == "__main__":
    starting_url = 'https://sunnah.com/'
    with requests.Session() as session:
        crawl_website(starting_url, session)


# #openai configuration 

# def get_openai_response_based_on_website_content(url, query):
#     """Generate a response based on the content of a predefined website."""
#     # Scrape the website
#     content = crawl_website(url, session)

#     # Load your OpenAI API key from an environment variable for security
#     api_key = os.getenv('OPENAI_API_KEY', 'OpenAI_API_KEY')
    
#     url = 'https://api.openai.com/v1/chat/completions'
#     headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json',
#     }
#     data = {
#         'model': "gpt-3.5-turbo",
#         'messages': [
#             {"role": "system", "content": "You are a knowledgeable assistant. Answer the question based on the content provided."},
#             {"role": "user", "content": content + "\n\n" + query}
#         ],
#         'max_tokens': 250,
#         'n': 5,  # Adjust based on how many responses you want
#     }
    
#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == 200:
#         response_data = response.json()
#         text_data = [choice['message']['content'] for choice in response_data.get('choices', [])]
#         return text_data
#     else:
#         print(f"Error: {response.status_code}")
#         return []