import requests
import json
import logging
from app.routes.settings_routes import load_settings
from app.ai_providers import cosmos_api, mistral_api, claude_api, openai_api


def stream_response(prompt):
    """
    Stream AI response from the selected provider: cosmos, mistral, claude, chatgpt.
    """
    settings = load_settings()
    provider = settings.get("provider", "cosmos")
    api_key = settings.get("api_keys", {}).get(provider)
    temperature = settings.get("temperature", 0.7)

    if not api_key:
        yield f"⚠️ Error: API key for {provider} is not configured."
        return

    try:
        if provider == "cosmos":
            for chunk in cosmos_api.stream(prompt, api_key, temperature):
                yield chunk

        elif provider == "mistral":
            for chunk in mistral_api.stream(prompt, api_key, temperature):
                yield chunk

        elif provider == "claude":
            for chunk in claude_api.stream(prompt, api_key, temperature):
                yield chunk

        elif provider == "chatgpt":
            for chunk in openai_api.stream(prompt, api_key, temperature):
                yield chunk

        else:
            yield f"⚠️ Error: Unsupported provider '{provider}'."

    except Exception as e:
        logging.error(f"Streaming error from {provider}: {str(e)}")
        yield f"⚠️ Error from {provider}: {str(e)}"
