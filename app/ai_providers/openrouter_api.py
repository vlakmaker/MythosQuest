import requests
import json
import logging

def stream(prompt, model, api_key, api_url, temperature):
    """
    Streams a response from OpenRouter using dynamic model selection.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",  # Change to your domain in production
        "X-Title": "MythosQuest"
    }

    payload = {
        "model": model,  # ✅ now dynamic
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "stream": True
    }

    try:
        response = requests.post(api_url.strip(), headers=headers, json=payload, stream=True, timeout=60)
        response.raise_for_status()

        buffer = ""
        for line in response.iter_lines():
            if not line:
                continue
            print("🧩 OpenRouter chunk:", line)

            decoded_line = line.decode("utf-8").strip()
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
                logging.warning(f"OpenRouter decode error: {json_str}")

        if buffer:
            yield buffer.strip() + "\n"

    except Exception as e:
        logging.error(f"OpenRouter API error: {str(e)}")
        yield f"⚠️ Error from OpenRouter API: {str(e)}"
