import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote, quote
import unicodedata

def clean_unicode_characters(text):
    return unicodedata.normalize('NFC', text)

def get_document_links(url):
    document_extensions = ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"]

    # Properly encode parentheses in the URL
    url = url.replace("(", "%28").replace(")", "%29")

    # Add headers to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers",
        "Referer": "https://www.google.com/"  # Optional: sometimes helps to specify a referrer
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        # response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # if any(href.lower().endswith(ext) for ext in document_extensions):
        
        full_link = urljoin(url, href)
        decoded_link = unquote(full_link)
        cleaned_link = clean_unicode_characters(decoded_link)
        
        try:
            response = requests.get(cleaned_link)
            print(cleaned_link)
            print("😭😭😭")
            print(response.headers)
            print("🛐🛐🛐🛐🛐🛐🛐🛐🛐")
        except Exception:
            print("frgbrg")
        
        links.append(cleaned_link)

    return links

def save_links_to_file(links, filename="document_links.txt"):
    try:
        with open(filename, 'w') as file:
            for link in links:
                file.write(link + "\n")
        print(f"Successfully saved {len(links)} links to {filename}")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    website_url = "https://sbi.co.in/web/careers/current-openings"
    document_links = get_document_links(website_url)

    if document_links:
        save_links_to_file(document_links)
    else:
        print("No document links found.")