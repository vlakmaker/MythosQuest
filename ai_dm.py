from flask import Flask, request, jsonify, render_template, Response
import os
import json
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
COSMOSRP_API_URL = "https://api.pawan.krd/cosmosrp-pro/v1/chat/completions"
COSMOSRP_API_KEY = os.getenv("COSMOSRP_API_KEY")

# Debug log to ensure API key is loaded
if not COSMOSRP_API_KEY:
    raise ValueError("❌ COSMOSRP_API_KEY not found in .env!")

# Initialize Flask app
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/")
def index():
    return render_template("index.html")

def stream_response(prompt):
    """
    Stream AI response from CosmosRP
    """
    try:
        headers = {
            "Authorization": f"Bearer {COSMOSRP_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "cosmosrp-001",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        response = requests.post(COSMOSRP_API_URL, headers=headers, json=payload, stream=True)

        if response.status_code != 200:
            error_msg = response.json().get("error", {}).get("message", "Unknown error")
            yield f"⚠️ Error: {response.status_code} - {error_msg}"
            return

        for chunk in response.iter_lines():
            if chunk:
                chunk_data = json.loads(chunk.decode("utf-8"))
                if "choices" in chunk_data:
                    message = chunk_data["choices"][0]["message"]["content"]
                    yield message + "\n"

    except Exception as e:
        logging.error(f"Error in stream_response: {e}")
        yield f"⚠️ Error: {str(e)}"

@app.route("/generate", methods=["POST"])
def generate_response():
    """
    Handle prompt input and stream AI response.
    """
    data = request.json
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    return Response(stream_response(prompt), content_type='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
