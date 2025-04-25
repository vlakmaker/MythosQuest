# stream_response.py

import logging
# *** Import User model as well to access preferences ***
from app.models import get_current_user, get_user_api_key, User
from app.crypto_utils import decrypt_api_key
# Import specific provider modules
from app.ai_providers import cosmos_api, openrouter_api
# Import specific models if needed, or handle dynamically

# --- Define Provider Configurations (Defaults/Metadata) ---
# Store details needed for each provider that AREN'T user-specific URLs
PROVIDER_METADATA = {
    "openrouter": {
        # Default URL if user hasn't specified one (Optional)
        "default_api_url": "https://openrouter.ai/api/v1/chat/completions",
        "stream_function": openrouter_api.stream,
        "requires_model": True # Does this provider need a model specified in payload?
    },
    "cosmos": {
        # Default URL if user hasn't specified one (Optional)
        "default_api_url": "https://api.pawan.krd/cosmosrp-pro/v1/chat/completions",
        "stream_function": cosmos_api.stream,
        "requires_model": False # cosmos_api.py doesn't seem to pass the model arg
    }
    # Add configuration for other providers (mistral, claude, etc.) here
}

def stream_response(prompt):
    """
    Stream AI response based on the user's selected provider and settings,
    including custom API URLs and models.
    """
    user = get_current_user()
    if not user:
        yield "⚠️ Error: No logged-in user found."
        return

    # --- Get User Preferences ---
    selected_provider = user.selected_provider or 'openrouter' # Fallback to default provider
    selected_temperature = user.selected_temperature if user.selected_temperature is not None else 0.7
    selected_model = user.selected_model # Get user's chosen model
    selected_context_size = user.context_size or 4096 # Get user's context size, fallback

    # --- Get Provider Specific Metadata ---
    metadata = PROVIDER_METADATA.get(selected_provider)
    if not metadata:
        yield f"⚠️ Error: Configuration metadata for provider '{selected_provider}' not found."
        return

    stream_function = metadata.get("stream_function")
    model_required = metadata.get("requires_model", False)

    if not stream_function:
         yield f"⚠️ Error: Incomplete configuration for provider '{selected_provider}' (missing stream function)."
         return

    # --- Get API Key AND User-Specific URL ---
    key_obj = get_user_api_key(user.id, selected_provider) # Returns the full APIKey object
    if not key_obj:
        yield f"⚠️ Error: API key for provider '{selected_provider}' not found. Please add it in Settings."
        return

    # Use the user's saved URL if it exists, otherwise fallback (or error if no fallback)
    api_url = key_obj.api_url if key_obj.api_url else metadata.get("default_api_url")
    if not api_url:
         yield f"⚠️ Error: API URL for provider '{selected_provider}' is not configured (neither saved by user nor default found). Please set it in Settings."
         return

    try:
        api_key = decrypt_api_key(key_obj.key)
    except Exception as decrypt_err:
         logging.error(f"Decryption error for user {user.id}, provider {selected_provider}: {decrypt_err}")
         yield f"⚠️ Error: Could not decrypt API key for '{selected_provider}'. Please re-save it."
         return

    # --- Model Handling ---
    # Use the user's selected model. Check if required.
    model_to_use = selected_model
    if model_required and not model_to_use:
         yield f"⚠️ Error: A model must be selected or configured for provider '{selected_provider}'."
         return

    # --- Debugging Output (Using actual values) ---
    print("\n🚀 Preparing Generation Request:")
    print(f"   User: {user.username} (ID: {user.id})")
    print(f"   Selected Provider: {selected_provider}")
    print(f"   Selected Temp: {selected_temperature}")
    print(f"   Selected Model: {model_to_use if model_to_use else 'N/A'}")
    print(f"   Selected Context Size: {selected_context_size}")
    print(f"   API Key Found: {'✓' if api_key else '❌'}")
    print(f"   Using API URL: {api_url}")
    print(f"   Model Required in Payload: {model_required}")

    # --- Execute Stream ---
    try:
        # Dynamically call the correct stream function
        # Pass parameters expected by the specific stream function
        # NOTE: You might need to adjust the arguments passed based on
        #       what each provider's stream function actually accepts.
        #       You may also need to pass context_size if the API supports it.

        if selected_provider == "openrouter":
             # Assuming openrouter_api.stream takes (prompt, model, api_key, api_url, temperature)
             yield from stream_function(prompt, model_to_use, api_key, api_url, selected_temperature)
        elif selected_provider == "cosmos":
             # Assuming cosmos_api.stream takes (prompt, api_key, api_url, temperature)
             # It seems to ignore the 'model' parameter internally based on previous code.
             yield from stream_function(prompt, api_key, api_url, selected_temperature)
        else:
             # Handle other providers if configurations are added
             yield f"⚠️ Provider '{selected_provider}' streaming is not implemented yet."

    except Exception as e:
        logging.error(f"❌ Error during streaming with {selected_provider} for user {user.id}: {e}", exc_info=True)
        yield f"❌ An error occurred while communicating with the '{selected_provider}' API."