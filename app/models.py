# models.py

from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
# *** Added Integer type ***
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
import os

# SQLAlchemy base
Base = declarative_base()

# --- Defaults ---
DEFAULT_PROVIDER = 'openrouter'
DEFAULT_TEMPERATURE = 0.7
# Common default models (adjust as needed)
DEFAULT_MODEL_OPENROUTER = 'mistralai/mistral-7b-instruct'
DEFAULT_MODEL_COSMOS = 'cosmosrp-001' # Seems fixed based on cosmos_api.py
DEFAULT_CONTEXT_SIZE = 4096 # Example default context size in tokens

# --- Models --- #
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    # --- Gameplay Settings ---
    selected_provider = Column(String, nullable=True, default=DEFAULT_PROVIDER)
    selected_temperature = Column(Float, nullable=True, default=DEFAULT_TEMPERATURE)
    # *** Added selected_model column ***
    selected_model = Column(String, nullable=True) # Default set dynamically below or in logic
    # *** Added context_size column ***
    context_size = Column(Integer, nullable=True, default=DEFAULT_CONTEXT_SIZE)

class APIKey(Base):
    __tablename__ = 'api_keys'
    id = Column(Integer, primary_key=True)
    provider = Column(String, nullable=False)
    key = Column(String, nullable=False) # Encrypted key
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # *** Added api_url column for custom endpoints ***
    api_url = Column(String, nullable=True) # Store user-defined URL here

# --- SQLAlchemy setup --- #
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DB_URL = "sqlite:///" + os.path.join(basedir, '..', 'users.db')

engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
db_session = scoped_session(SessionLocal)

# --- Database Initialization Function ---
def init_db():
    """Creates database tables from SQLAlchemy models."""
    print(f"Attempting to create tables for database at: {SQLALCHEMY_DB_URL}")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully (or already exist).")
    except Exception as e:
        print(f"Error during table creation: {e}")

# --- User Management Functions --- #
def add_user(username, password):
    hashed_password = generate_password_hash(password)
    # Set appropriate default model based on default provider
    default_model = DEFAULT_MODEL_OPENROUTER if DEFAULT_PROVIDER == 'openrouter' else DEFAULT_MODEL_COSMOS
    new_user = User(
        username=username,
        password=hashed_password,
        selected_provider=DEFAULT_PROVIDER,
        selected_temperature=DEFAULT_TEMPERATURE,
        # *** Set default model and context size ***
        selected_model=default_model,
        context_size=DEFAULT_CONTEXT_SIZE
    )
    db_session.add(new_user)
    db_session.commit()
    print(f"User '{username}' added with defaults.")

def get_user(username):
    print(f"Querying for user: {username}")
    user = db_session.query(User).filter_by(username=username).first()
    print(f"Query result for {username}: {'Found' if user else 'Not Found'}")
    return user

def verify_user(username, password):
    user = get_user(username)
    return user and check_password_hash(user.password, password)

def get_current_user():
    username = session.get("user")
    # print(f"Getting current user from session: {username}") # Can be noisy
    if username:
        return get_user(username)
    # print("No user found in session.") # Can be noisy
    return None

# --- API Key Functions ---
def get_user_api_key(user_id, provider):
     # Returns the full APIKey object (including id, key, user_id, api_url)
     print(f"Querying API key object for user_id={user_id}, provider={provider}")
     key_obj = db_session.query(APIKey).filter_by(user_id=user_id, provider=provider).first()
     print(f"API Key object query result: {'Found' if key_obj else 'Not Found'}")
     return key_obj

# --- User Settings Function (Updated) ---
def update_user_gameplay_settings(user_id, provider, temperature, model, context_size):
    """Updates gameplay settings for a user."""
    print(f"Attempting to update gameplay settings for user_id={user_id}")
    user = db_session.query(User).filter_by(id=user_id).first()
    if user:
        user.selected_provider = provider
        user.selected_temperature = temperature
        user.selected_model = model # Save the selected model
        user.context_size = context_size # Save context size
        db_session.commit()
        print(f"Updated gameplay settings for user {user_id}: Provider={provider}, Temp={temperature}, Model={model}, Context={context_size}")
        return True
    print(f"Failed to find user with id={user_id} to update gameplay settings.")
    return False

# --- API Key & URL Update Function (New/Refined) ---
def upsert_api_key_and_url(user_id, provider, encrypted_key, api_url):
    """Creates or updates an API key entry, including the custom URL."""
    print(f"Upserting API key/URL for user_id={user_id}, provider={provider}")
    existing = db_session.query(APIKey).filter_by(user_id=user_id, provider=provider).first()
    if existing:
        existing.key = encrypted_key
        existing.api_url = api_url # Update URL as well
        print("Updated existing APIKey record.")
    else:
        new_key = APIKey(
            user_id=user_id,
            provider=provider,
            key=encrypted_key,
            api_url=api_url # Save URL on creation
        )
        db_session.add(new_key)
        print("Created new APIKey record.")
    db_session.commit()