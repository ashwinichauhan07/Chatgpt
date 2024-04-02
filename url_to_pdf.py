import requests
import pdfkit
import os
from urls import *
import re  # Import the regular expressions library

# Function to preprocess and load URLs from a .py file
def preprocess_and_load_urls(file_path):
    try:
        with open(file_path, 'r') as file:
            original_content = file.read()
        
        corrected_content = re.sub(r'(http[s]?://[^\s,]+)', r"'\1' ", original_content)
        corrected_code = compile(corrected_content, file_path, 'exec')
        namespace = {}
        exec(corrected_code, namespace)
        return namespace['urls']
    except Exception as e:
        print(f"Error processing URL file: {e}")
        return []

# Replace this with the path to your .py file
file_path = 'urls.py'
urls = preprocess_and_load_urls(file_path)

def save_as_pdf(url, output_filename):
    try:
        # Fetch the HTML content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Convert HTML to PDF and save it
        pdfkit.from_string(response.text, output_filename)
        print(f"Saved {url} as {output_filename}")
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
    except Exception as e:
        print(f"Failed to convert {url} to PDF: {e}")

# Ensure the output directory exists
output_dir = "website_pdfs"
os.makedirs(output_dir, exist_ok=True)

# Convert each URL to a PDF
for url in urls:
    filename = os.path.join(output_dir, url.split("//")[-1].replace("/", "_") + ".pdf")
    save_as_pdf(url, filename)
