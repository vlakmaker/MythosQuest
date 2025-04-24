from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env values

FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise ValueError("FERNET_KEY not found in .env file!")

fernet = Fernet(FERNET_KEY.encode())


def encrypt_api_key(plain_text: str) -> str:
    """Encrypts the API key."""
    return fernet.encrypt(plain_text.encode()).decode()


def decrypt_api_key(cipher_text: str) -> str:
    """Decrypts the API key."""
    return fernet.decrypt(cipher_text.encode()).decode()
