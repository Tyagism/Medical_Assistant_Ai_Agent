
import json
import csv
import chromadb
from sentence_transformers import SentenceTransformer

# Load JSON data
with open("structured_allergy_data.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Load CSV data
csv_data = []
with open("structured_allergy_data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Combine title, summary, and text for richer context
        text = f"{row.get('title', '')} {row.get('summary', '')} {row.get('text', '')}"
        csv_data.append(text)

# Combine all texts
all_texts = [item["text"] for item in json_data] + csv_data

# Create embeddings model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Chroma
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("allergy")

# Insert docs
for i, text in enumerate(all_texts):
    emb = embedder.encode(text).tolist()
    collection.add(documents=[text], embeddings=[emb], ids=[str(i)])

print("✅ Combined dataset stored in ChromaDB")
