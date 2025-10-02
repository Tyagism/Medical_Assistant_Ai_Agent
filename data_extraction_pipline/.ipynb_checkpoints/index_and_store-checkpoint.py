# index_and_store.py
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
from tqdm import tqdm

EMBED_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE = 32  # reduce if low memory


def _sanitize_metadata(meta: dict):
    """
    Ensure metadata values are primitives acceptable by Chroma:
    str, int, float, bool or None. Convert lists/dicts to JSON strings.
    """
    clean = {}
    for k, v in (meta or {}).items():
        if v is None:
            clean[k] = None
        elif isinstance(v, (str, int, float, bool)):
            clean[k] = v
        elif isinstance(v, list) and all(isinstance(x, str) for x in v):
            # join lists of strings for readability
            clean[k] = "; ".join(v)
        else:
            try:
                clean[k] = json.dumps(v, ensure_ascii=False)
            except Exception:
                clean[k] = str(v)
    return clean


def build_structured_dataset(records, output_csv="structured_allergy_data.csv", output_json="structured_allergy_data.json"):
    """
    Save structured dataset into CSV and JSON formats.
    `records` should be a list of dicts produced by the extractor.
    Returns the records back for convenience.
    """
    import pandas as pd

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(records)} records to {output_csv} and {output_json}")
    return records


def index_into_chroma(records, collection_name="indian_skin_allergy", persist_dir="./chroma_db"):
    """
    Index structured dataset into ChromaDB (PersistentClient).
    `records`: list of dicts where each dict contains 'title', 'summary' or 'abstract' or 'text'.
    """
    # ensure the directory exists
    Path(persist_dir).mkdir(parents=True, exist_ok=True)

    # initialize embedder and chroma client (no heavy work at import time)
    embedder = SentenceTransformer(EMBED_MODEL)
    client = chromadb.PersistentClient(path=persist_dir)

    # create or get collection
    collection = client.get_or_create_collection(name=collection_name)

    ids_batch = []
    docs_batch = []
    metas_batch = []
    embs_batch = []

    total = len(records)
    print(f"Indexing {total} records to Chroma collection '{collection_name}' in {persist_dir}")

    for i, rec in enumerate(tqdm(records)):
        doc_text = rec.get("summary") or rec.get("abstract") or rec.get("text") or ""
        doc_id = rec.get("id") or f"doc_{i}"

        metadata_raw = {
            "title": rec.get("title", ""),
            "year": rec.get("year", ""),
            "authors": rec.get("authors", []),
            "source": rec.get("source", ""),
            "allergens": rec.get("allergens", []),
            "food_triggers": rec.get("food_triggers", []),
            "regions": rec.get("regions", []),
            "prevalence_percent": rec.get("prevalence_percent", [])
        }

        metadata = _sanitize_metadata(metadata_raw)

        emb = embedder.encode(doc_text).tolist()

        ids_batch.append(str(doc_id))
        docs_batch.append(doc_text)
        metas_batch.append(metadata)
        embs_batch.append(emb)

        if len(ids_batch) >= BATCH_SIZE or i == total - 1:
            collection.add(
                ids=ids_batch,
                documents=docs_batch,
                metadatas=metas_batch,
                embeddings=embs_batch
            )
            ids_batch.clear()
            docs_batch.clear()
            metas_batch.clear()
            embs_batch.clear()

    # persist (PersistentClient usually persists automatically)
    try:
        client.persist()
    except Exception:
        pass

    print(f"✅ Completed indexing {total} records.")
    return True