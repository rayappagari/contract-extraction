from typing import Iterator


def chunk_text(text: str, chunk_size: int = 4000, overlap: int = 200) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def chunk_by_pages(pages: list[dict], max_chars: int = 8000) -> list[dict]:
    chunks = []
    current_chunk = {"pages": [], "text": ""}
    for page in pages:
        if len(current_chunk["text"]) + len(page["text"]) > max_chars and current_chunk["text"]:
            chunks.append(current_chunk)
            current_chunk = {"pages": [], "text": ""}
        current_chunk["pages"].append(page["page"])
        current_chunk["text"] += "\n" + page["text"]
    if current_chunk["text"]:
        chunks.append(current_chunk)
    return chunks
