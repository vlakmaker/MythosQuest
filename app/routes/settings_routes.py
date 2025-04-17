from flask import Blueprint, render_template, request, redirect, url_for
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
        json.dump(data, f, indent=2)

def initialize_settings_if_missing():
    if not os.path.exists(SETTINGS_FILE):
        default_settings = {
            "provider": "cosmos",
            "temperature": 0.7,
            "providers": {
                "cosmos": {"api_key": "", "api_url": ""},
                "claude": {"api_key": "", "api_url": ""},
                "mistral": {"api_key": "", "api_url": ""},
                "chatgpt": {"api_key": "", "api_url": ""},
                "openrouter": {"api_key": "", "api_url": "", "model": ""}
            }
        }
        save_settings(default_settings)

@settings_bp.route("/settings", methods=["GET", "POST"])
def settings():
    initialize_settings_if_missing()
    settings = load_settings()

    if request.method == "POST":
        provider = request.form.get("provider")
        temperature = float(request.form.get("temperature", 0.7))

        providers = {
            "cosmos": {
                "api_key": request.form.get("cosmos_api_key", "").strip(),
                "api_url": request.form.get("cosmos_api_url", "").strip()
            },
            "claude": {
                "api_key": request.form.get("claude_api_key", "").strip(),
                "api_url": request.form.get("claude_api_url", "").strip()
            },
            "mistral": {
                "api_key": request.form.get("mistral_api_key", "").strip(),
                "api_url": request.form.get("mistral_api_url", "").strip()
            },
            "chatgpt": {
                "api_key": request.form.get("chatgpt_api_key", "").strip(),
                "api_url": request.form.get("chatgpt_api_url", "").strip()
            },
            "openrouter": {
                "api_key": request.form.get("openrouter_api_key", "").strip(),
                "api_url": request.form.get("openrouter_api_url", "").strip(),
                "model": request.form.get("openrouter_model", "").strip()
            }
        }

        new_settings = {
            "provider": provider,
            "temperature": temperature,
            "providers": providers
        }

        save_settings(new_settings)
        return redirect(url_for("game.index"))

    return render_template(
        "settings.html",
        provider=settings.get("provider", "cosmos"),
        providers=settings.get("providers", {}),
        temperature=settings.get("temperature", 0.7)
    )
