import requests
from bs4 import BeautifulSoup
import os
import json
from dotenv import load_dotenv

# Load the .env file from the current directory
load_dotenv()

def scrape_website_content(urls):
    """Scrape content from multiple websites."""
    all_content = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        content = ' '.join(paragraphs)[:2048]  # Adjust the slice as needed
        all_content.append(content)
    combined_content = ' '.join(all_content)  # Combine all content into a single string
    return combined_content

def get_openai_response_based_on_website_content(website_urls, query):
    """Generate a response based on the content of predefined websites."""
    # Scrape the websites
    combined_content = scrape_website_content(website_urls)

    # Load your OpenAI API key from an environment variable for security
    api_key = os.getenv('OpenAI_API_KEY')
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': "gpt-3.5-turbo",
        'messages': [
            {"role": "system", "content": "give an answer and url for the given question based on the content of the websites and urls. do not modify answers give exact answer. if question is not releted to topic say i dont know or question is not related to topic"},
            {"role": "user", "content": combined_content + "\n\n" + query}  # Concatenate combined content and query
        ],
        'max_tokens': 250,
        'n': 5,  # Adjust based on how many responses you want
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        text_data = [choice['message']['content'] for choice in response_data.get('choices', [])]
        return text_data
    else:
        print(f"Error: {response.status_code}")
        return []

# Example usage
website_urls = ["https://sunnah.com", "https://sunnah.com/bukhari:3896", 
                "https://sunnah.com/tirmidhi:1109", "https://sunnah.com/bukhari:6971", 
                "https://sunnah.com/urn/511520","https://sunnah.com/bukhari:3894",
                "https://sunnah.com/ibnmajah:2026","https://sunnah.com/nasai:3519",
                "https://sunnah.com/urn/510950","https://sunnah.com/urn/511960",
                "https://sunnah.com/muslim:1422a","https://sunnah.com/adab:821",
                "https://sunnah.com/mishkat:3128","https://sunnah.com/abudawud:2101",
                "https://sunnah.com/nasai:3255","https://sunnah.com/muslim:2527d",
                "https://sunnah.com/nasai:3273","https://sunnah.com/nasai:3258","https://sunnah.com/urn/512010"]  # Replace with your predefined website URLs
query = "two words which dear to allah?"
responses = get_openai_response_based_on_website_content(website_urls, query)
for response in responses:
    print(response)
