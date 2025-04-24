# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class. Contains settings loaded from environment variables."""

    # --- App Security ---
    # REQUIRED for session management, flashing, etc.
    # Loads from FLASK_SECRET_KEY environment variable, falls back to a default (change it!).
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "you-should-really-change-this-secret")

    # --- Legacy API Configuration (Consider removing if no longer used directly) ---
    # These seem specific to one provider and might be better handled
    # within the provider logic or user settings if they vary.
    # Keeping them here for now if they are still needed globally.
    COSMOSRP_API_KEY = os.getenv("COSMOSRP_API_KEY")
    COSMOSRP_API_URL = os.getenv("COSMOSRP_API_URL", "https://api.pawan.krd/cosmosrp-pro/v1/chat/completions")

    # --- Basic validation (Optional within the class, good practice) ---
    # You might want to perform checks during app initialization instead,
    # but keeping it here is also possible.
    # if not COSMOSRP_API_KEY:
    #     print("⚠️ WARNING: COSMOSRP_API_KEY is missing from your environment/config!")
        # Consider raising an error if it's absolutely critical at startup
        # raise ValueError("❌ COSMOSRP_API_KEY is missing and required!")

    # Add other global application configurations here
    # e.g., SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///users.db'
    # e.g., DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")

# You can still define other config classes if needed for different environments
# class DevelopmentConfig(Config):
#     DEBUG = True
#
# class ProductionConfig(Config):
#     DEBUG = False
#     # Override or add production-specific settings