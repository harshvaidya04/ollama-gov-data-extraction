import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import csv

def extract_raw_html(url):
    # Fetch the content of the page
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return None
    
    return response.text

def scrape_data(url, class_name=None, id_name=None):
    
    raw_text = extract_raw_html(url)

    # Parse the HTML content
    soup = BeautifulSoup(raw_text, 'html.parser')
    
    content_array = [div for div in soup.find_all("div", class_=class_name)]

    exam_page_links = extract_exam_page_links(content_array)

    return exam_page_links

def extract_exam_page_links(content_array):

    exam_page_links = []

    for content in content_array:
        if content:  # Skip None or empty content
            soup = BeautifulSoup(str(content), "html.parser")
            link = soup.find("a")["href"]

            if not link.startswith("http"):
                link = "https://upsc.gov.in/" + (link)
            exam_page_links.append(link)

    return exam_page_links


if __name__ == '__main__':
    active_url = 'https://upsc.gov.in/examinations/active-exams'  # Replace with the URL you want to scrape
    class_name = 'field-content'  # Replace with the class or id you need
    id_name = ''

    active_exam_page_links = scrape_data(active_url, class_name=class_name, id_name=id_name)
    
    
    csv_filename = "../Server/data/LinksData/Multiple/UPSC.csv"

    # Write data to CSV file
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["COMPANY", "LINK"])  # Writing header
        for link in active_exam_page_links:
            writer.writerow(["UPSC", link])
    
    print("UPSC Links extracted and saved to UPSC.csv")

def extract_UPSC_links():
    active_url = 'https://upsc.gov.in/examinations/active-exams'  # Replace with the URL you want to scrape
    class_name = 'field-content'  # Replace with the class or id you need
    id_name = ''

    active_exam_page_links = scrape_data(active_url, class_name=class_name, id_name=id_name)
    
    csv_filename = "../Server/data/LinksData/Multiple/UPSC.csv"

    # Write data to CSV file
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["COMPANY", "LINK"])  # Writing header
        for link in active_exam_page_links:
            writer.writerow(["UPSC", link])
    
    print("UPSC Links extracted and saved to UPSC.csv")
