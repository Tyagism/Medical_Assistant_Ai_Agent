# pdf_utils.py
import requests
from pathlib import Path
import fitz  # pymupdf
from tqdm import tqdm

def download_pdf(url, out_dir="pdfs"):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = url.split("/")[-1].split("?")[0]
    if not fname.endswith(".pdf"):
        fname = fname + ".pdf"
    out_path = out_dir / fname
    if out_path.exists():
        return str(out_path)
    try:
        r = requests.get(url, stream=True, timeout=30)
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(1024 * 32):
                f.write(chunk)
        return str(out_path)
    except Exception as e:
        print("Download failed:", e, url)
        return None

def extract_text_from_pdf(path, max_pages=None):
    """Extract text from a PDF file using PyMuPDF (fitz). Returns full text."""
    doc = fitz.open(path)
    text_lines = []
    n = doc.page_count
    pages = range(n) if max_pages is None else range(min(n, max_pages))
    for i in pages:
        page = doc.load_page(i)
        text = page.get_text("text")
        text_lines.append(text)
    doc.close()
    return "\n\n".join(text_lines)
