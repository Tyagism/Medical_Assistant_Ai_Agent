# Gemini Medicine Assistant (Python Flask)

This is a modern, minimalist web application that integrates with the Google Gemini API and provides a beautiful interface for users to ask about medicines and health topics. It uses Python Flask and can be run locally, in Docker, or deployed to the cloud. Medicine data is indexed for Retrieval-Augmented Generation (RAG) using ChromaDB and Gemini API.

## Features
* Modern, vibrant UI with Material 3 and dark mode
* Loader and "Thinking..." indicator while waiting for answers
* Gemini API integration for real-time, AI-powered responses
* RAG workflow with ChromaDB for context-rich answers
* Pre-asked onboarding questions
* Scrollable chat history, hidden scrollbars
* Easily extensible for real medical data


## How to Run
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and add your Gemini API key:
   ```sh
   copy .env.example .env  # On Windows
   # Then edit .env and set your GEMINI_API_KEY
   ```
3. Start the Flask app:
   ```sh
   python app.py
   ```
4. Open your browser at http://127.0.0.1:5000/

## Run with Docker
1. Create a `Dockerfile` in your project root:
   ```Dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["python", "app.py"]
   ```
2. Make sure `app.py` has:
   ```python
   if __name__ == "__main__":
       app.run(host="0.0.0.0", port=5000)
   ```
3. Build and run:
   ```sh
   docker build -t medical-assistant .
   docker run -d -p 5000:5000 medical-assistant
   ```
4. Access at `http://localhost:5000` (or your server's public IP)

## VS Code Port Forwarding
If using VS Code Remote (SSH/WSL/Codespaces), you can forward port 5000 and access the app at `localhost:5000` on your local machine. This is for development only and not public sharing.

## Public Sharing
To share your app on the internet:
* Deploy to a cloud VM (Azure, AWS, GCP) and open port 5000
* Or use a tunneling service like [ngrok](https://ngrok.com/):
   ```sh
   ngrok http 5000
   ```
* For production, use HTTPS and a reverse proxy (Nginx, Caddy)
## Sharing & Security

* The `.env` file is in `.gitignore` and will NOT be uploaded to GitHub.
* Share `.env.example` so others know what variables to set.
* Each user must create their own `.env` with their own API key.

## Customization
* Update your Gemini API key in `.env`.
* Edit `gemini_api.py` to change prompt instructions or output style.
* Update the UI in `templates/index.html` for further design tweaks.

## Next Steps
* Replace in-memory data with a real database
* Add authentication and more advanced features as needed
* Expand prompt logic for more use cases
