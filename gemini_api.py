import requests

def call_gemini_api(prompt, api_key):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    instructions = (
        "You are a helpful medical expert assistant. Out of medical Expertise you don't provide any informations, only to medical asks. Provide accurate and concise information with supporting/reference links. ",
        "using attached database of medicines of india and indian government sources , provide accurate of indian's health there food and exercise habits, suggest them there personal assistant (remeber you are not a Doctor), provide results of physicologist, physiotherapist, psychiatrist, general physician, cardiologist, dermatologist, neurologist, gynecologist, urologist, ENT specialist, pediatrician, oncologist, endocrinologist, nephrologist, gastroenterologist, pulmonologist, rheumatologist and other medical fields. ",
        "Word limit: 300. Output format: text, list, markup, links, medical references and output only.",
        "Do not use following phrases while Providing response: '**', '--', instead use arrows, emojies like '➡️', '💊', '🔗' etc. to make it more engaging and visually appealing.\n"
    )
    instructions_text = ' '.join(instructions)
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": instructions_text + prompt}]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "No valid response from Gemini API."
    else:
        return f"Gemini API error: {response.status_code} {response.text}"
