import logging
from app.routes.settings_routes import load_settings
from app.ai_providers import cosmos_api, mistral_api, claude_api, openai_api, openrouter_api

def stream_response(prompt):
    """
    Stream AI response from the selected provider using user-saved settings.
    Logs and yields debug info to help track down missing or invalid settings.
    """
    settings = load_settings()
    provider = settings.get("provider", "cosmos")
    temperature = settings.get("temperature", 0.7)

    provider_settings = settings.get("providers", {}).get(provider, {})
    api_key = provider_settings.get("api_key", "").strip()
    api_url = provider_settings.get("api_url", "").strip()
    model = provider_settings.get("model", "").strip()  # ✅ New line

    # Debug output to console
    print("\n🔍 Provider Settings Debug")
    print(f"   📦 Selected Provider: {provider}")
    print(f"   🔑 API Key: {'(provided)' if api_key else '❌ MISSING'}")
    print(f"   🌍 API URL: {api_url or '❌ MISSING'}")
    print(f"   🧠 Model: {model or '(not needed)'}")  # ✅ Optional
    print(f"   🌡️ Temperature: {temperature}")

    if not api_key or not api_url:
        logging.warning(f"Missing API config for provider '{provider}': key or URL")
        yield f"⚠️ Error: Missing API key or URL for provider '{provider}'."
        return

    try:
        if provider == "cosmos":
            yield from cosmos_api.stream(prompt, api_key, api_url, temperature)
        elif provider == "mistral":
            yield from mistral_api.stream(prompt, api_key, api_url, temperature)
        elif provider == "claude":
            yield from claude_api.stream(prompt, api_key, api_url, temperature)
        elif provider == "chatgpt":
            yield from openai_api.stream(prompt, api_key, api_url, temperature)
        elif provider == "openrouter":
            if not model:
                yield "⚠️ Error: No model specified for OpenRouter."
                return
            yield from openrouter_api.stream(prompt, model, api_key, api_url, temperature)
        else:
            yield f"⚠️ Error: Unsupported provider '{provider}'."
    except Exception as e:
        logging.error(f"❌ Streaming error from {provider}: {str(e)}")
        yield f"⚠️ Error from {provider}: {str(e)}"
