# settings_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from app.models import (
    db_session, User, APIKey, get_current_user,
    update_user_gameplay_settings, upsert_api_key_and_url, get_user_api_key
)
from app.crypto_utils import encrypt_api_key, decrypt_api_key
from functools import wraps
import logging

settings_bp = Blueprint("settings", __name__)

VALID_PROVIDERS = ["openrouter", "cosmos"]

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login"))
        user = get_current_user()
        if not user:
             flash("User not found, please log in again.", "error")
             session.clear()
             return redirect(url_for("auth.login"))
        kwargs['current_user'] = user
        return view_func(*args, **kwargs)
    return wrapper

@settings_bp.route("/settings", methods=["GET"])
@login_required
def settings(current_user):
    return render_template(
        "settings.html",
        provider=current_user.selected_provider,
        temperature=current_user.selected_temperature,
        selected_model=current_user.selected_model,
        context_size=current_user.context_size
    )

@settings_bp.route("/gameplay", methods=["POST"])
@login_required
def save_gameplay_settings(current_user):
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    provider = data.get("provider")
    temperature_str = data.get("temperature")
    model = data.get("model") # Get selected model
    context_size_str = data.get("context_size") # Get context size

    if not provider or provider not in VALID_PROVIDERS:
        return jsonify({"error": f"Invalid provider specified. Choose from: {', '.join(VALID_PROVIDERS)}"}), 400
    if not model:
        return jsonify({"error": "Model selection cannot be empty."}), 400

    try:
        temperature = float(temperature_str)
        if not (0.0 <= temperature <= 2.0):
             raise ValueError("Temperature out of range")
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid temperature value. Must be a number between 0.0 and 2.0."}), 400

    try:
        context_size = int(context_size_str)
        if not (1 <= context_size <= 32768):
             raise ValueError("Context size out of range")
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid context size value. Must be a whole number (e.g., 4096)."}), 400

    try:
        # *** CORRECTED CALL: Pass model and context_size ***
        if update_user_gameplay_settings(current_user.id, provider, temperature, model, context_size):
            return jsonify({"status": "ok", "message": "Gameplay settings saved successfully."})
        else:
            return jsonify({"error": "Failed to find user to update settings"}), 500
    except Exception as e:
        db_session.rollback()
        logging.error(f"Database error saving gameplay settings for user {current_user.id}: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred while saving settings."}), 500

@settings_bp.route("/api/keys", methods=["POST"])
@login_required
def save_api_key_and_url(current_user):
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    provider = data.get("provider")
    key = data.get("key")
    api_url = data.get("apiUrl")

    if not provider or provider not in VALID_PROVIDERS:
         return jsonify({"error": f"Invalid provider specified. Choose from: {', '.join(VALID_PROVIDERS)}"}), 400
    if not key:
         return jsonify({"error": "API key is required."}), 400

    try:
        encrypted_key = encrypt_api_key(key)
        upsert_api_key_and_url(current_user.id, provider, encrypted_key, api_url)
        return jsonify({"status": "ok", "message": f"{provider.capitalize()} API key and URL saved."})
    except Exception as e:
        db_session.rollback()
        logging.error(f"Error saving API key/URL for user {current_user.id}, provider {provider}: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred while saving the API key/URL."}), 500

@settings_bp.route("/api/keys/<provider>", methods=["GET"])
@login_required
def get_api_key_and_url(current_user, provider):
    if provider not in VALID_PROVIDERS:
         return jsonify({"error": f"Invalid provider specified."}), 400

    key_obj = get_user_api_key(current_user.id, provider)
    decrypted_key = ""
    api_url = ""

    if key_obj:
        api_url = key_obj.api_url or ""
        try:
            decrypted_key = decrypt_api_key(key_obj.key)
        except Exception as e:
            logging.error(f"Failed to decrypt key for user {current_user.id}, provider {provider}: {e}")

    return jsonify({"key": decrypted_key, "api_url": api_url})