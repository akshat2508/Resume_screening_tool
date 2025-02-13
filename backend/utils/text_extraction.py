import pdfplumber
import pytesseract
import cv2
import os
from PIL import Image
from docx import Document

# Set Tesseract path (only needed for Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text(file_path):
    _, ext = os.path.splitext(file_path)
    if ext.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext.lower() == ".docx":
        return extract_text_from_docx(file_path)
    elif ext.lower() in [".jpg", ".png", ".jpeg"]:
        return extract_text_from_image(file_path)
    else:
        return "Unsupported file type"

if __name__ == "__main__":
    file_path = input("Enter file path: ")
    print("Extracted Text:\n", extract_text(file_path))
