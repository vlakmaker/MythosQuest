from app.models import APIKey, db_session
from app.crypto_utils import encrypt_api_key, decrypt_api_key

def login(client, username="testuser", password="password"):
    client.post("/register", data={"username": username, "password": password})
    client.post("/login", data={"username": username, "password": password})

def test_save_and_get_api_key(test_client):
    login(test_client)

    # Save a new key
    response = test_client.post("/api/keys", json={
        "provider": "openrouter",
        "key": "my_secret_key_123"
    })
    assert response.status_code == 200

    # Fetch the key again
    response = test_client.get("/api/keys/openrouter")
    data = response.get_json()
    assert data["key"] == "my_secret_key_123"

    # Double-check it's encrypted in DB
    key_obj = db_session.query(APIKey).filter_by(provider="openrouter").first()
    assert key_obj is not None
    assert key_obj.key != "my_secret_key_123"  # Should be encrypted
    assert decrypt_api_key(key_obj.key) == "my_secret_key_123"
