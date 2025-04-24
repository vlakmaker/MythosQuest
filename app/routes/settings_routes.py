# settings_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
# *** Import User model and update function ***
from app.models import db_session, User, APIKey, get_current_user, update_user_gameplay_settings
from app.crypto_utils import encrypt_api_key, decrypt_api_key
from functools import wraps
import logging # Import logging

settings_bp = Blueprint("settings", __name__)

# --------- Auth Decorator --------- #
# (Keep existing login_required decorator)
def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)
    return wrapper

# --------- Settings UI --------- #
@settings_bp.route("/settings", methods=["GET"])
@login_required
def settings():
    user = get_current_user()
    # Pass current settings to the template
    return render_template(
        "settings.html",
        provider=user.selected_provider if user else 'openrouter',
        temperature=user.selected_temperature if user else 0.7
    )

# --------- API: Save Gameplay Settings (New) --------- #
@settings_bp.route("/gameplay", methods=["POST"])
@login_required
def save_gameplay_settings():
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 401 # Should be caught by login_required, but good practice

    data = request.json
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    provider = data.get("provider")
    temperature_str = data.get("temperature")

    # --- Validation ---
    valid_providers = ["openrouter", "cosmos"] # Define valid providers
    if not provider or provider not in valid_providers:
        return jsonify({"error": f"Invalid provider specified. Choose from: {', '.join(valid_providers)}"}), 400

    try:
        temperature = float(temperature_str)
        if not (0.0 <= temperature <= 2.0): # Allow slightly wider range if needed
             raise ValueError("Temperature out of range")
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid temperature value. Must be a number between 0.0 and 2.0."}), 400
    # --- End Validation ---

    try:
        if update_user_gameplay_settings(user.id, provider, temperature):
            return jsonify({"status": "ok", "message": "Gameplay settings saved successfully."})
        else:
            # This case shouldn't happen if get_current_user worked, but handle defensively
            return jsonify({"error": "Failed to find user to update settings"}), 500
    except Exception as e:
        db_session.rollback() # Rollback in case of unexpected error during commit
        logging.error(f"Database error saving gameplay settings for user {user.id}: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred while saving settings."}), 500


# --------- API: Save API Key --------- #
# (Keep existing save_api_key route)
@settings_bp.route("/api/keys", methods=["POST"])
@login_required
def save_api_key():
    data = request.json
    user = get_current_user()
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    provider = data.get("provider")
    key = data.get("key")

    if not provider or not key:
         return jsonify({"error": "Provider and key are required."}), 400

    try:
        encrypted_key = encrypt_api_key(key)
        existing = db_session.query(APIKey).filter_by(user_id=user.id, provider=provider).first()

        if existing:
            existing.key = encrypted_key
            print(f"Updated API key for user {user.id}, provider {provider}") # Added log
        else:
            new_key = APIKey(user_id=user.id, provider=provider, key=encrypted_key)
            db_session.add(new_key)
            print(f"Added new API key for user {user.id}, provider {provider}") # Added log

        db_session.commit()
        return jsonify({"status": "ok"})
    except Exception as e:
        db_session.rollback()
        logging.error(f"Error saving API key for user {user.id}, provider {provider}: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred while saving the API key."}), 500


# --------- API: Retrieve API Key --------- #
# (Keep existing get_api_key route)
@settings_bp.route("/api/keys/<provider>", methods=["GET"])
@login_required
def get_api_key(provider):
    user = get_current_user()
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    key_obj = db_session.query(APIKey).filter_by(user_id=user.id, provider=provider).first()
    decrypted_key = ""
    if key_obj:
        try:
            decrypted_key = decrypt_api_key(key_obj.key)
        except Exception as e:
            logging.error(f"Failed to decrypt key for user {user.id}, provider {provider}: {e}")
            # Return empty string but maybe log an error or flash a message later
            # Don't return the encrypted key
    return jsonify({"key": decrypted_key})