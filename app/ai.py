import requests
import json
import logging
from config import COSMOSRP_API_KEY, COSMOSRP_API_URL

def stream_response(prompt):
    """
    Stream AI response from CosmosRP with defensive JSON handling.
    """
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
            if not line:
                continue

            decoded_line = line.decode("utf-8").strip()

            # Expecting format: data: {JSON}
            if not decoded_line.startswith("data: "):
                continue

            json_str = decoded_line[6:].strip()

            if json_str == "[DONE]":
                break

            try:
                chunk_data = json.loads(json_str)
                delta = chunk_data.get("choices", [{}])[0].get("delta", {})
                content = delta.get("content", "")

                if content:
                    buffer += content
                    if any(p in buffer for p in [".", "!", "?"]):
                        yield buffer.strip() + "\n"
                        buffer = ""

            except json.JSONDecodeError:
                logging.warning(f"Could not decode: {json_str}")

        if buffer:
            yield buffer.strip() + "\n"

    except Exception as e:
        logging.error(f"Streaming error: {str(e)}")
        yield f"⚠️ Error: {str(e)}"
