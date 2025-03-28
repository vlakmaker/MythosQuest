from flask import Flask, request, jsonify, render_template, redirect, url_for, Response, session
import os
import json
import requests
import logging
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_user, add_user

# Load environment variables
load_dotenv()
COSMOSRP_API_URL = "https://api.pawan.krd/cosmosrp-pro/v1/chat/completions"
COSMOSRP_API_KEY = os.getenv("COSMOSRP_API_KEY")

# Debug log to ensure API key is loaded
if not COSMOSRP_API_KEY:
    raise ValueError("❌ COSMOSRP_API_KEY not found in .env!")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key")  # Use a real secret in production
logging.basicConfig(level=logging.INFO)

# 🏠 Home (Protected)
@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session["user"])

# 🎲 Generate AI response (Protected)
@app.route("/generate", methods=["POST"])
def generate_response():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    return Response(stream_response(prompt), content_type='text/plain')

# 🔐 Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if not username or not password:
            return render_template("register.html", error="Please enter both a username and password.")

        if get_user(username):
            return render_template("register.html", error="Username already exists.")

        add_user(username, password)
        return redirect(url_for("login"))

    return render_template("register.html")

# 🔑 Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        user = get_user(username)  # Returns a tuple: (id, username, hashed_password)

        # Use index-based access since user is a tuple
        if user and check_password_hash(user[2], password):  
            session["user"] = user[1]  # Store the username from the tuple
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# 🚪 Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# 🌐 CosmosRP AI streaming
def stream_response(prompt):
    if not COSMOSRP_API_KEY:
        yield "⚠️ Error: AI Service API Key is not configured."
        return

    try:
        headers = {
            "Authorization": f"Bearer {COSMOSRP_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "cosmosrp-001",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "stream": True
        }

        response = requests.post(COSMOSRP_API_URL, headers=headers, json=payload, stream=True, timeout=60)
        response.raise_for_status()

        buffer = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")

                if decoded_line.startswith("data: "):
                    json_str = decoded_line[6:].strip()

                    if json_str == "[DONE]":
                        break

                    try:
                        chunk_data = json.loads(json_str)
                        delta = chunk_data.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            buffer += content
                            # Check for complete sentence
                            if any(p in buffer for p in [".", "!", "?"]):
                                yield buffer.strip() + "\n"
                                buffer = ""

                    except json.JSONDecodeError:
                        logging.warning(f"Could not decode: {decoded_line}")

        # Flush remaining buffer
        if buffer:
            yield buffer.strip() + "\n"

    except Exception as e:
        logging.error(f"Streaming error: {str(e)}")
        yield f"⚠️ Error: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
