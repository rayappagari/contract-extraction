from pathlib import Path
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.docx_loader import load_docx


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def route_file(file_path: str) -> dict:
    path = Path(file_path)
    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}. Supported: {SUPPORTED_EXTENSIONS}")
    if ext == ".pdf":
        return load_pdf(file_path)
    if ext == ".docx":
        return load_docx(file_path)
