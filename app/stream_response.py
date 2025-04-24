# stream_response.py

import logging
from app.models import get_current_user, get_user_api_key # User model needed for prefs
from app.crypto_utils import decrypt_api_key
# Import specific provider modules
from app.ai_providers import cosmos_api, openrouter_api
# Import specific models if needed, or handle dynamically

# --- Define Provider Configurations ---
# Store details needed for each provider
PROVIDER_CONFIG = {
    "openrouter": {
        "api_url": "https://openrouter.ai/api/v1/chat/completions",
        # You might want to store preferred model per user too later
        "default_model": "mistralai/mistral-7b-instruct",
        "stream_function": openrouter_api.stream,
        "requires_model": True # Does this provider need a model specified in payload?
    },
    "cosmos": {
        # Get URL from config or hardcode. For production, use config.
        "api_url": "https://api.pawan.krd/cosmosrp-pro/v1/chat/completions",
        "default_model": "cosmosrp-001", # Model seems fixed in payload for cosmos_api.py
        "stream_function": cosmos_api.stream,
        "requires_model": False # cosmos_api.py doesn't seem to pass the model arg
    }
    # Add configuration for other providers (mistral, claude, etc.) here
}

def stream_response(prompt):
    """
    Stream AI response based on the user's selected provider and settings.
    """
    user = get_current_user()
    if not user:
        yield "⚠️ Error: No logged-in user found."
        return

    # --- Get User Preferences ---
    selected_provider = user.selected_provider or 'openrouter' # Fallback to default
    selected_temperature = user.selected_temperature if user.selected_temperature is not None else 0.7 # Fallback

    # --- Get Provider Specific Config ---
    config = PROVIDER_CONFIG.get(selected_provider)
    if not config:
        yield f"⚠️ Error: Configuration for provider '{selected_provider}' not found."
        return

    api_url = config.get("api_url")
    stream_function = config.get("stream_function")
    model_required = config.get("requires_model", False)
    # Use user's preferred model later if implemented, otherwise default
    model = config.get("default_model") # Will be None if not defined

    if not api_url or not stream_function:
         yield f"⚠️ Error: Incomplete configuration for provider '{selected_provider}' (missing URL or stream function)."
         return

    # --- Get API Key ---
    key_obj = get_user_api_key(user.id, selected_provider)
    if not key_obj:
        yield f"⚠️ Error: API key for provider '{selected_provider}' not found. Please add it in Settings."
        return

    try:
        api_key = decrypt_api_key(key_obj.key)
    except Exception as decrypt_err:
         logging.error(f"Decryption error for user {user.id}, provider {selected_provider}: {decrypt_err}")
         yield f"⚠️ Error: Could not decrypt API key for '{selected_provider}'. Please re-save it."
         return

    # --- Debugging Output (Using actual values) ---
    print("\n🚀 Preparing Generation Request:")
    print(f"   User: {user.username} (ID: {user.id})")
    print(f"   Selected Provider: {selected_provider}")
    print(f"   Selected Temp: {selected_temperature}")
    print(f"   API Key Found: {'✓' if api_key else '❌'}")
    print(f"   Using API URL: {api_url}")
    print(f"   Using Model: {model if model else 'N/A'}")
    print(f"   Model Required in Payload: {model_required}")

    # --- Execute Stream ---
    try:
        # Dynamically call the correct stream function
        # Check function signature and pass appropriate args
        if selected_provider == "openrouter":
             if model_required and not model:
                  yield f"⚠️ Error: Model identifier is required for {selected_provider} but is missing."
                  return
             yield from stream_function(prompt, model, api_key, api_url, selected_temperature)
        elif selected_provider == "cosmos":
             # Assuming cosmos_api.stream takes (prompt, api_key, api_url, temperature)
             yield from stream_function(prompt, api_key, api_url, selected_temperature)
        else:
             # Handle other providers if configurations are added
             yield f"⚠️ Provider '{selected_provider}' streaming is not implemented yet."

    except Exception as e:
        logging.error(f"❌ Error during streaming with {selected_provider} for user {user.id}: {e}", exc_info=True)
        # Provide a more generic error to the user, details are logged
        yield f"❌ An error occurred while communicating with the '{selected_provider}' API."