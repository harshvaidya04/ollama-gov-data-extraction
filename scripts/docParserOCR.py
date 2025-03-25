import requests
import pytesseract
import fitz
from pdf2image import convert_from_bytes
from io import BytesIO
from DeviceConstants import tesseract,poppler

# Set the path of Tesseract-OCR if not set in the environment
pytesseract.pytesseract.tesseract_cmd = tesseract

def get_pdf_page_count(pdf_bytes):
    with fitz.open("pdf", pdf_bytes) as doc:
        return len(doc)  # Fastest way to count pages

def download_pdf(url):
    """Downloads a PDF from a given URL and returns its content as bytes."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("failed to download pdf")
        raise Exception(f"Failed to download PDF, status code: {response.status_code}")

def extract_text_from_pdf(pdf_url):
    """Extracts text from a scanned PDF using OCR."""
    try:
        pdf_bytes = download_pdf(pdf_url)
        page_count = get_pdf_page_count(pdf_bytes)
        if page_count > 50:
            print("page size exceeded in ",pdf_url)
            raise Exception(f"Failed to extract text")
        
        poppler_path = poppler  # Replace with your actual path

        images = convert_from_bytes(pdf_bytes, poppler_path=poppler_path)
        
        # Convert PDF to images
        # images = convert_from_bytes(pdf_bytes)

        extracted_text = ""
        for img in images:
            text = pytesseract.image_to_string(img)
            extracted_text += text + "\n"

        return extracted_text
    except Exception:
        # print("failed to extract text")
        raise Exception(f"Failed to extract text")

if __name__ == '__main__':
    # Example usage
    pdf_url = "https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2025/02/2025020474.pdf"  # Replace with actual PDF URL
    extracted_text = extract_text_from_pdf(pdf_url)
    with open('raw_text_ocr','w',encoding='utf-8') as f: 
        f.write(extracted_text)
