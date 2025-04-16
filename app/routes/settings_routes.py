from flask import Blueprint, render_template, request, redirect, url_for, session
import json
import os

settings_bp = Blueprint('settings', __name__)

SETTINGS_FILE = "app/user_settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f)

@settings_bp.route("/settings", methods=["GET", "POST"])
def settings():
    settings = load_settings()
    if request.method == "POST":
        provider = request.form.get("provider")
        temperature = float(request.form.get("temperature", 0.7))
        api_keys = {
            "cosmos": request.form.get("api_key_cosmos", ""),
            "claude": request.form.get("api_key_claude", ""),
            "mistral": request.form.get("api_key_mistral", ""),
            "chatgpt": request.form.get("api_key_chatgpt", "")
        }
        new_settings = {
            "provider": provider,
            "temperature": temperature,
            "api_keys": api_keys
        }
        save_settings(new_settings)
        return redirect(url_for('game.index'))

    return render_template("settings.html",
        provider=settings.get("provider", "cosmos"),
        api_keys=settings.get("api_keys", {}),
        temperature=settings.get("temperature", 0.7)
    )
