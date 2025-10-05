# Gemini Medicine Assistant (Python Flask)

A Flask web app that provides a RAG-enabled medical assistant using ChromaDB and Google Gemini. Includes a Material 3 dark-mode UI and an indexer to load structured allergy data for context-rich answers.

---

## Quick overview
- RAG pipeline: structured CSV/JSON -> SentenceTransformer embeddings -> ChromaDB -> Gemini for generation.
- Main files:
  - `app.py` — Flask app / UI
  - `build_index.py` — builds ChromaDB from CSV/JSON
  - `gemini_api.py` — Gemini RAG call
  - `templates/` — HTML/CSS/JS UI
  - `.env.example` — contains `GEMINI_API_KEY` variable

---

## Prerequisites
- Python 3.9+ (3.11 recommended)
- Docker (optional)
- Official ngrok binary if you want public tunnels (download from https://ngrok.com)

---

## Setup — Windows (recommended flow)
1. Create and activate venv (PowerShell):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
   Or Command Prompt:
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
   If you prefer manual:
   ```powershell
   pip install chromadb flask sentence-transformers python-dotenv
   ```
3. Configure environment:
   ```powershell
   copy .env.example .env
   # open .env and paste your GEMINI_API_KEY
   ```
4. Build the index (first run, after populating CSV/JSON):
   ```powershell
   python build_index.py
   ```
5. Run the app:
   ```powershell
   python app.py
   ```
6. Open: http://127.0.0.1:5000

---

## Setup — Linux / WSL
1. Create and activate venv:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or install core packages individually:
   ```bash
   pip install chromadb flask sentence-transformers python-dotenv
   ```
3. Configure environment:
   ```bash
   cp .env.example .env
   # edit .env and set GEMINI_API_KEY
   ```
4. Build index:
   ```bash
   python3 build_index.py
   ```
5. Run:
   ```bash
   python3 app.py
   ```
6. Open: http://127.0.0.1:5000

---

## Docker (optional)
1. Create `Dockerfile` (project root) — example:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```
2. Build and run:
```bash
docker build -t medical-assistant .
docker run -d -p 5000:5000 --env-file .env medical-assistant
```
3. Visit `http://<host-ip>:5000`

---

## Sharing publicly (quick)
- ngrok (recommended for quick demos):
  1. Download official ngrok, sign in, set authtoken.
  2. Run locally then:
     ```bash
     ngrok http 5000
     ```
  3. Share the provided `https://...ngrok.io` URL.
- For production, deploy Docker on a cloud VM (Azure/AWS/GCP), open firewall port, and use a reverse proxy + HTTPS.

---

## Environment variables
- Copy `.env.example` -> `.env` and set:
  ```
  GEMINI_API_KEY=your_gemini_api_key_here
  ```
- `app.py` reads `GEMINI_API_KEY` and passes it to `gemini_api.call_gemini_api`.

---

## Troubleshooting
- Module not found: ensure VS Code / terminal uses the same Python interpreter as your venv.
  - Windows: `where python`
  - Linux: `which python3`
- If `chromadb` or `sentence-transformers` installation fails, install system build tools (Linux).
- If Gemini requests fail, verify `GEMINI_API_KEY` and network access.
- If UI input disappears or messages not visible, clear browser cache and confirm `app.py` is the running process.

---

## Next steps & tips
- Add authentication and rate limiting before public deployment.
- Use a managed vector DB for scale (Pinecone, Weaviate) for production.
- Replace in-memory demo data with a proper DB and secure secrets (Vault/Azure KeyVault).
