from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
from PIL import Image
import pytesseract

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def read_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def read_xlsx(path):
    df = pd.read_excel(path)
    return df.to_string()

def read_image(path):
    img = Image.open(path)
    return pytesseract.image_to_string(img)

def extract_content(path):
    if path.endswith(".txt"):
        return read_txt(path)
    if path.endswith(".pdf"):
        return read_pdf(path)
    if path.endswith(".docx"):
        return read_docx(path)
    if path.endswith(".xlsx"):
        return read_xlsx(path)
    if path.endswith((".png", ".jpg", ".jpeg")):
        return read_image(path)
    return "Unsupported file format."
