# nlp_extract.py
import re
import spacy
from collections import defaultdict

# Try scispaCy; fallback to spaCy general model
try:
    nlp = spacy.load("en_core_sci_sm")
except Exception:
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        raise RuntimeError("Install a spaCy model: python -m spacy download en_core_web_sm")

# predefine allergen & food keyword lexicons (extendable)
ALLERGEN_KEYWORDS = [
    "nickel", "potassium dichromate", "chromate", "paraphenylenediamine", "ppd", "fragrance",
    "neomycin", "colophony", "methylisothiazolinone", "mci/mi", "thiuram", "mercaptobenzothiazole",
    "rubber", "latex", "parthenium", "potassium dichromate", "cobalt", "formaldehyde", "cement",
    "garlic", "seafood", "milk", "dairy", "egg", "peanut", "tree nut", "wheat", "soy", "sesame"
]

FOOD_KEYWORDS = [
    "seafood", "fish", "shellfish", "dairy", "milk", "egg", "peanut", "nuts", "spice", "chili",
    "mustard", "sesame", "curry", "milk", "dairy", "yogurt", "curd"
]

REGION_KEYWORDS = ["India", "Delhi", "Kashmir", "Kerala", "Tamil Nadu", "Andhra", "Bengal", "Maharashtra", "Rajasthan", "Karnataka", "Punjab", "Gujarat"]

CONDITION_KEYWORDS = ["atopic dermatitis", "contact dermatitis", "urticaria", "eczema", "allergic contact dermatitis", "food allergy", "drug reaction", "fixed drug eruption"]

PERCENT_PATTERN = re.compile(r'(\d{1,2}(?:\.\d+)?)[\s]?(?:%|percent|per cent)|(\d{1,3}\/\d{1,3})')

def find_allergens(text):
    text_l = text.lower()
    found = set()
    for kw in ALLERGEN_KEYWORDS:
        if kw in text_l:
            found.add(kw)
    # also try to catch hyphenated or capitalized words using NER nouns
    doc = nlp(text)
    for ent in doc.ents:
        ent_text = ent.text.lower()
        if ent_text in ALLERGEN_KEYWORDS:
            found.add(ent_text)
    return list(found)

def find_food_triggers(text):
    text_l = text.lower()
    found = set()
    for kw in FOOD_KEYWORDS:
        if kw in text_l:
            found.add(kw)
    return list(found)

def find_conditions(text):
    text_l = text.lower()
    found = set()
    for kw in CONDITION_KEYWORDS:
        if kw in text_l:
            found.add(kw)
    return list(found)

def find_regions(text):
    text_l = text
    found = []
    for kw in REGION_KEYWORDS:
        if re.search(r'\b' + re.escape(kw) + r'\b', text_l, re.IGNORECASE):
            found.append(kw)
    return found

def extract_percentages(text):
    """Return list of numerical prevalence findings found in text as floats or fractions."""
    results = []
    for match in re.finditer(r'(\d{1,3}(?:\.\d+)?)\s*(%|percent|per cent)', text, re.IGNORECASE):
        try:
            val = float(match.group(1))
            results.append(val)
        except:
            continue
    # fractions like 1/3 -> convert to percent
    for m in re.finditer(r'(\d{1,3})\s*/\s*(\d{1,3})', text):
        a,b = int(m.group(1)), int(m.group(2))
        if b!=0:
            results.append(round(a/b*100,2))
    return results

def extract_authors_and_year(metadata_text):
    # try to extract year
    ymatch = re.search(r'\b(20(1[5-9]|2[0-5]))\b', metadata_text)
    year = ymatch.group(0) if ymatch else None
    # authors: heuristic: line before "Abstract" or comma-separated names near title
    # This will be replaced by real metadata when available
    return {"year": year, "authors": []}

def summarize_text(text, max_chars=1000):
    # Simple trimming summary: first 1000 chars; replace with abstractive summary model if needed
    s = text.strip().replace("\n", " ")
    return s[:max_chars] + ("..." if len(s) > max_chars else "")

def extract_features_from_doc(doc):
    """
    doc: dict with keys: title, abstract, text (full text optional), year, authors, source
    returns structured record
    """
    text = (doc.get("abstract") or "") + "\n\n" + (doc.get("text") or "")
    features = {}
    features["title"] = doc.get("title")
    features["year"] = doc.get("year") or extract_authors_and_year(doc.get("title", ""))["year"]
    features["authors"] = doc.get("authors", [])
    features["source"] = doc.get("source", "")
    features["summary"] = summarize_text(text)
    features["conditions"] = find_conditions(text)
    features["allergens"] = find_allergens(text)
    features["food_triggers"] = find_food_triggers(text)
    features["regions"] = find_regions(text)
    features["prevalence_percent"] = extract_percentages(text)
    return features
