import pdfplumber
from pathlib import Path


def load_pdf(file_path: str) -> dict:
    path = Path(file_path)
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({"page": i + 1, "text": text, "width": page.width, "height": page.height})
    return {"source": str(path), "page_count": len(pages), "pages": pages}
