from PyPDF2 import PdfReader

def summarize_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text_content = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text_content += extracted

    return text_content[:1000] + "\n\nSummary truncated."
