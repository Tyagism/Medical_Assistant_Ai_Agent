# run_pipeline.py
import os
import json
import time
from fetchers import fetch_semantic_scholar, fetch_pubmed
from pdf_utils import download_pdf, extract_text_from_pdf
from nlp_extract import extract_features_from_doc
from index_and_store import build_structured_dataset, index_into_chroma
from tqdm import tqdm

# 1. Fetch metadata lists (example queries)
query = "skin allergy India OR contact dermatitis India OR urticaria India OR atopic dermatitis India"
ss_results = fetch_semantic_scholar(query, limit=100)
pm_results = fetch_pubmed("skin allergy India", retmax=100)

# merge sources into unified list
records = []
# convert Semantic Scholar results to unified doc format
for r in ss_results:
    records.append({
        "title": r.get("title"),
        "abstract": r.get("abstract"),
        "year": r.get("year"),
        "authors": r.get("authors"),
        "source": "semantic_scholar",
        "url": r.get("url"),
        "paperId": r.get("paperId"),
        "externalIds": r.get("externalIds", {})
    })

# convert PubMed results
for r in pm_results:
    records.append({
        "title": r.get("title"),
        "abstract": r.get("abstract"),
        "year": r.get("year"),
        "authors": r.get("authors"),
        "source": "pubmed",
        "pmid": r.get("pmid")
    })

# 2. Try to download PDFs where a direct URL exists (Semantic Scholar often has)
enriched = []
for rec in tqdm(records, desc="Downloading PDFs (if available)"):
    fulltext = None
    url = rec.get("url") or ""
    # Try direct PDF link heuristic
    try:
        if url and (url.lower().endswith(".pdf") or "pdf" in url.lower()):
            path = download_pdf(url)
            if path:
                fulltext = extract_text_from_pdf(path, max_pages=40)
        else:
            # try checking externalIds or other heuristics (if available)
            ext = rec.get("externalIds") or {}
            # some records may include a PDF link under 'PDF' or have an arXiv id
            pdf_link = ext.get("PDF") or None
            if pdf_link:
                path = download_pdf(pdf_link)
                if path:
                    fulltext = extract_text_from_pdf(path, max_pages=40)
    except Exception as e:
        # don't fail whole run for a single download issue
        print("PDF download/extract failed for:", rec.get("title"), e)
    enriched.append({**rec, "text": fulltext})
    time.sleep(0.1)  # small polite pause

# 3. Extract structured features
structured = []
for idx, doc in enumerate(tqdm(enriched, desc="Extracting features")):
    features = extract_features_from_doc(doc)
    # attach original metadata and ensure required fields exist
    features["title"] = doc.get("title") or features.get("title")
    features["authors"] = doc.get("authors") or features.get("authors", [])
    features["source"] = doc.get("source") or features.get("source", "")
    # create a stable unique id: prefer paperId -> pmid -> fallback to sequential idx
    features["id"] = doc.get("paperId") or doc.get("pmid") or f"local_{idx}"
    # ensure a text field is present for embeddings/indexing
    features["text"] = (doc.get("text") or doc.get("abstract") or features.get("summary") or "") 
    structured.append(features)

# 4. Save CSV/JSON and index into Chroma
build_structured_dataset(structured, out_csv="structured_allergy_data.csv", out_json="structured_allergy_data.json")
index_into_chroma(structured, collection_name="indian_skin_allergy", persist_dir="./chroma_db")

print("Pipeline finished. Files saved: structured_allergy_data.csv, structured_allergy_data.json")
