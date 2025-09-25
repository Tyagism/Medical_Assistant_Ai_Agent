from flask import Flask, render_template, request, jsonify




import os
from dotenv import load_dotenv
from gemini_api import call_gemini_api
load_dotenv()
app = Flask(__name__)


# Temporary in-memory medicine data
temp_medicine_db = {
    "paracetamol": {"name": "Paracetamol", "usage": "Pain relief", "dosage": "500mg"},
    "ibuprofen": {"name": "Ibuprofen", "usage": "Anti-inflammatory", "dosage": "200mg"}
}

# Gemini API key (now loaded from environment variable)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    user_prompt = data.get("prompt", "")
    # Try Gemini API first
    gemini_response = call_gemini_api(user_prompt, GEMINI_API_KEY)
    # If user asked for a medicine, try to add medicine info
    medicine = temp_medicine_db.get(user_prompt.lower())
    if medicine:
        med_info = f"{medicine['name']} is used for {medicine['usage']}. Recommended dosage: {medicine['dosage']}."
        response = f"{gemini_response}\n\n{med_info}"
    else:
        response = gemini_response
    return jsonify({"result": response})

if __name__ == "__main__":
    app.run(debug=True)
