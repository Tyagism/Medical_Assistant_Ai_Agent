# fetchers.py
import requests
import time
from Bio import Entrez
from tqdm import tqdm

# Set your email for NCBI Entrez
Entrez.email = "techtimesminatipid01@gmail.com"

SEMANTIC_SCHOLAR_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"

def fetch_semantic_scholar(query, limit=100, fields="title,abstract,year,authors,externalIds,url,venue"):
    results = []
    params = {"query": query, "limit": min(limit, 100), "fields": fields}
    # Semantic Scholar free tier rate-limits; do not hammer
    resp = requests.get(SEMANTIC_SCHOLAR_SEARCH, params=params)
    resp.raise_for_status()
    data = resp.json()
    for item in data.get("data", []):
        results.append({
            "source": "semantic_scholar",
            "paperId": item.get("paperId"),
            "title": item.get("title"),
            "abstract": item.get("abstract"),
            "year": item.get("year"),
            "venue": item.get("venue"),
            "authors": [a.get("name") for a in item.get("authors", [])],
            "url": item.get("url"),
            "externalIds": item.get("externalIds", {})
        })
    return results

def fetch_pubmed(query, retmax=100):
    """Use Entrez to search PubMed and fetch metadata + links (2015-2025)"""
    # restrict to 2015-2025 in query
    q = f"({query}) AND (2015:2025[dp])"
    handle = Entrez.esearch(db="pubmed", term=q, retmax=retmax)
    record = Entrez.read(handle)
    ids = record["IdList"]
    papers = []
    for pmid in tqdm(ids):
        handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
        rec = Entrez.read(handle)
        try:
            article = rec['PubmedArticle'][0]['MedlineCitation']['Article']
            title = article.get('ArticleTitle', '')
            abstract = ''
            if article.get('Abstract'):
                abstract = ' '.join([t.strip() for t in article['Abstract'].get('AbstractText', [])])
            year = article.get('Journal', {}).get('JournalIssue', {}).get('PubDate', {}).get('Year', '')
            authors = []
            for a in article.get('AuthorList', []):
                name = ''
                if 'LastName' in a and 'ForeName' in a:
                    name = f"{a['ForeName']} {a['LastName']}"
                elif 'LastName' in a:
                    name = a['LastName']
                authors.append(name)
            papers.append({
                "source": "pubmed",
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "year": year,
                "authors": authors,
            })
        except Exception as e:
            # skip problematic records
            continue
        time.sleep(0.34)  # polite delay
    return papers
