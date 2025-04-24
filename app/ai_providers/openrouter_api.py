# app/ai_providers/openrouter_api.py
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
        "X-Title": "MythosQuest"                  # Optional: Your app name
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "stream": True
    }

    # Log the payload being sent for easier debugging
    try:
        payload_json_for_log = json.dumps(payload)
    except TypeError:
        payload_json_for_log = "Error serializing payload for logging"
    logging.info(f"Sending OpenRouter request to {api_url} with payload: {payload_json_for_log}")


    try:
        response = requests.post(api_url.strip(), headers=headers, json=payload, stream=True, timeout=60)

        # Check for HTTP errors BEFORE trying to iterate
        response.raise_for_status() # Raises HTTPError for 4xx/5xx status codes

        buffer = ""
        # Only proceed to iterate if the status code was OK (2xx)
        for line in response.iter_lines():
            if not line:
                continue
            # Log raw chunks ONLY if really needed - can be very verbose
            # print("🧩 Raw OpenRouter chunk:", line)

            decoded_line = line.decode("utf-8").strip()
            if not decoded_line.startswith("data: "):
                continue

            json_str = decoded_line[len("data: "):].strip() # Use len() for robustness
            if json_str == "[DONE]":
                break

            try:
                chunk_data = json.loads(json_str)
                delta = chunk_data.get("choices", [{}])[0].get("delta", {})
                content = delta.get("content", "")

                if content:
                    # Choose one streaming method:
                    # Option 1: Sentence Buffering (current)
                    buffer += content
                    if any(p in buffer for p in [".", "!", "?", "\n"]): # Added newline as potential separator
                        yield buffer.strip() + "\n"
                        buffer = ""
                    # Option 2: Token Streaming (faster perception)
                    # yield content

            except json.JSONDecodeError:
                logging.warning(f"OpenRouter JSON decode error on line: {json_str}")

        # Yield any remaining buffer (for sentence buffering)
        if buffer:
            yield buffer.strip() + "\n"

    # --- Improved Error Handling ---
    except requests.exceptions.HTTPError as http_err:
        error_content = "Could not read error response body."
        error_json = None
        try:
            # Try to get the response body, first as text, then maybe as JSON
            error_content = http_err.response.text
            error_json = http_err.response.json() # Try parsing as JSON
        except Exception as parse_err:
            logging.warning(f"Could not parse error response body as JSON: {parse_err}")

        # Log detailed error information
        logging.error(f"OpenRouter HTTP error: {http_err}")
        logging.error(f"--> Status Code: {http_err.response.status_code}")
        logging.error(f"--> Response Body: {error_content}")

        # Yield a more informative message to the frontend
        detail_msg = f"Status Code: {http_err.response.status_code}."
        if error_json and 'error' in error_json:
            # Try to extract specific error message if available in JSON response
             detail_msg += f" Message: {error_json['error'].get('message', 'No specific message.')}"
        elif error_content:
             detail_msg += f" Response: {error_content[:200]}" # Limit length

        yield f"⚠️ Error from OpenRouter API: Bad Request. {detail_msg}"

    except Exception as e:
        # Catch other non-HTTP errors (network timeout, connection errors, etc.)
        logging.error(f"OpenRouter general communication error: {str(e)}", exc_info=True)
        yield f"⚠️ Error communicating with OpenRouter: {str(e)}"