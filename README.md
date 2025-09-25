# Gemini Medicine Assistant (Python Flask)

This is a modern, minimalist web application that integrates with the Google Gemini API and provides a beautiful interface for users to ask about medicines and health topics. It uses a temporary in-memory database for medicine data, ready for future extension to a real database.

## Features
- Modern, neon-gradient, minimalist UI with dark mode
- Loader and "Responding..." indicator while waiting for answers
- Gemini API integration for real-time, AI-powered responses
- Temporary in-memory medicine data (can be replaced with a real database)
- Pill emoji in header for a friendly touch


## How to Run
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and add your Gemini API key:
   ```sh
   cp .env.example .env  # On Windows, use: copy .env.example .env
   # Then edit .env and set your GEMINI_API_KEY
   ```
3. Start the Flask app:
   ```sh
   python app.py
   ```
4. Open your browser at http://127.0.0.1:5000/
## Sharing & Security

- The `.env` file is in `.gitignore` and will NOT be uploaded to GitHub.
- Share `.env.example` so others know what variables to set.
- Each user must create their own `.env` with their own API key.

## Customization
- Update your Gemini API key in `app.py` or set it as an environment variable `GEMINI_API_KEY`.
- Edit `gemini_api.py` to change the prompt instructions or output style.
- Update the UI in `templates/index.html` for further design tweaks.

## Next Steps
- Replace in-memory data with a real database
- Add authentication and more advanced features as needed
- Expand prompt logic for more use cases
