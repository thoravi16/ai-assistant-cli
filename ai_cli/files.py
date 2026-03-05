from pathlib import Path
import PyPDF2
from ai_cli.ai_engine import ask_ai

def summarize_file(file_path: str):
    path = Path(file_path)

    if not path.exists():
        return "[Error] File not found"

    if path.suffix.lower() == ".txt":
        content = path.read_text(encoding="utf-8")

    elif path.suffix.lower() == ".pdf":
        content = ""
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    content += text
    else:
        return "[Error] Unsupported file type"

    content = content[:6000]

    messages = [
        {"role": "user", "content": f"Summarize this document clearly:\n\n{content}"}
    ]

    return ask_ai(messages)