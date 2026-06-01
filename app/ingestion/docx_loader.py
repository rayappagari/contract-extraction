from pathlib import Path
from docx import Document


def load_docx(file_path: str) -> dict:
    path = Path(file_path)
    doc = Document(str(path))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    full_text = "\n".join(paragraphs)
    return {"source": str(path), "paragraph_count": len(paragraphs), "text": full_text}
