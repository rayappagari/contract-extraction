from PIL import Image
import pytesseract
from pathlib import Path


def run_ocr(image_path: str, lang: str = "eng") -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=lang)
    return text.strip()


def ocr_pdf_pages(pages: list[dict]) -> list[dict]:
    for page in pages:
        if not page.get("text"):
            page["text"] = ""
            page["ocr_applied"] = True
    return pages
