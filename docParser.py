import PyPDF2
import requests
from io import BytesIO

def extract_content_from_pdf(pdf_url):
    try:
        # Fetch the PDF content
        response = requests.get(pdf_url)
        response.raise_for_status()
        pdf_content = BytesIO(response.content)

        # Read the PDF using PyPDF2
        pdf_reader = PyPDF2.PdfReader(pdf_content)

        # Extract text from each page
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() or ""
        return pdf_text.strip()
    except Exception as e:
        print(f"Error processing {pdf_url}: {e}")
        return None


if __name__ == "__main__":
    
    url = 'https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2025/02/2025020474.pdf'
    
    pdf_text = extract_content_from_pdf(url)
    
    with open('raw_text.txt', 'w', encoding='utf-8') as f:
        f.write(pdf_text)
    
    print("Raw text extracted")