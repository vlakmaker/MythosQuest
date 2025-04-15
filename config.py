import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API Configuration ---
COSMOSRP_API_KEY = os.getenv("COSMOSRP_API_KEY")
COSMOSRP_API_URL = os.getenv("COSMOSRP_API_URL", "https://api.pawan.krd/cosmosrp-pro/v1/chat/completions")

# --- App Security ---
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "super-secret-key")  # Replace for production!

# --- Basic validation ---
if not COSMOSRP_API_KEY:
    raise ValueError("❌ COSMOSRP_API_KEY is missing from your .env file!")

# Optional: add more centralized config here later
# e.g. DEBUG_MODE = os.getenv("DEBUG", "False") == "True"
