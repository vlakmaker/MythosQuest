from flask import Flask, request, jsonify, render_template, Response
import requests
import logging
import json
from memory_manager import MemoryManager
from rag_manager import RAGManager

# Initialize Flask app
app = Flask(__name__)

# CosmosRP API Config
COSMOSRP_API_URL = "https://api.pawan.krd/cosmosrp-pro/v1/chat/completions"
API_KEY = "YOUR_COSMOSRP_API_KEY"  # Replace with your actual API Key

# Memory and RAG management
memory = MemoryManager()
rag = RAGManager()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@app.route("/")
def index():
    """Render the web-based interface"""
    return render_template("index.html")


def stream_response(prompt):
    """
    Streams the AI's response in readable chunks instead of character-by-character.
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        payload = {
            "model": "cosmosrp-001",
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }

        response = requests.post(COSMOSRP_API_URL, json=payload, headers=headers, stream=True)
        response.raise_for_status()

        full_text = ""
        buffer = ""

        for chunk in response.iter_lines():
            if chunk:
                try:
                    data = json.loads(chunk.decode("utf-8"))
                    buffer += data.get("choices", [{}])[0].get("message", {}).get("content", "")

                    # Only send data when a full sentence (ending in . ! ? ) is reached
                    if any(char in buffer for char in ".!?"):
                        yield buffer + "\n"
                        full_text += buffer + "\n"
                        buffer = ""

                except json.JSONDecodeError:
                    continue

        # Send remaining text if any
        if buffer:
            yield buffer + "\n"

    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with CosmosRP: {str(e)}")
        yield f"⚠️ Error: {str(e)}"


@app.route("/generate", methods=["POST"])
def generate_response():
    """
    Processes user input and returns a response from the AI Dungeon Master.
    """
    data = request.json
    player_input = data.get("prompt", "").strip()

    if not player_input:
        return jsonify({"error": "No prompt provided"}), 400

    # Load memory from previous actions
    last_scenario = memory.get_latest_memory_by_type('setting')
    last_character = memory.get_latest_memory_by_type('character')
    recent_memories = memory.get_recent_memories(limit=10)

    past_actions_summary = "\n".join(
        [f"- {mem['description']}" for mem in recent_memories if mem['memory_type'] == 'choice']
    )

    # If no scenario or character exists, prompt user to set it up
    if not last_scenario:
        return jsonify({"response": "📜 Choose a historical period to begin your journey."})
    if not last_character:
        return jsonify({"response": "🎭 Create your character before continuing."})

    # Save player input to memory
    memory.save_memory('choice', player_input)

    prompt = f"""
    🎲 **DM Roleplay Mode Engaged**
    
    You are the Dungeon Master for an **immersive historical RPG**. Stay in character, respond dynamically.
    
    **World Setting**: {last_scenario}
    **Player Character**: {last_character}
    
    **Recent Actions:**
    {past_actions_summary}

    🎭 **[🌆 Scene Description]**: Describe the environment, mood, and situation.
    💬 **[NPC Interaction]**: Introduce an NPC and have them interact with the player.
    🛠️ **[Action Consequences]**: Describe what happens due to the player’s last action.
    📜 **[Choices]**: Offer 3 options for the player to continue the adventure.
    
    🚨 Stay immersive, don’t break character!
    """

    return Response(stream_response(prompt), content_type='text/plain')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
