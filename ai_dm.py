from flask import Flask, request, jsonify, render_template, Response
import ollama
import logging
import json
import requests
from memory_manager import MemoryManager
from rag_manager import RAGManager

# Initialize Flask app
app = Flask(__name__)

# Ollama connection
OLLAMA_HOST = "http://ollama_server:11434"
ollama_client = ollama.Client(host=OLLAMA_HOST)

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
    Streams the AI's response gradually to improve perceived performance.
    """
    try:
        response = ollama_client.chat(
            model="gemma:2b",
            messages=[{"role": "user", "content": prompt}],
            stream=True  # Enables streaming response
        )

        for chunk in response:
            if "message" in chunk:
                yield chunk["message"]["content"] + " "
    
    except Exception as e:
        logging.error(f"Error communicating with Ollama: {str(e)}")
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
