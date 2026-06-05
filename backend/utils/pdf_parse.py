import pdfplumber
from pathlib import Path

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
    except Exception as e:
        raise ValueError(f"PDF解析失败: {str(e)}")
    return text.strip()

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    text_length = len(text)
    start = 0
    
    while start < text_length:
        end = start + chunk_size
        if end < text_length:
            last_space = text.rfind(' ', start, end)
            if last_space != -1 and last_space > start:
                end = last_space
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
    
    return chunks

def process_pdf(file_path):
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    return {
        "text": text,
        "chunks": chunks,
        "chunk_count": len(chunks)
    }