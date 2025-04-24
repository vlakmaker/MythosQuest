# models.py

from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
import os # Import os

# SQLAlchemy base
Base = declarative_base()

# --- Models --- #
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    selected_provider = Column(String, nullable=True, default='openrouter')
    selected_temperature = Column(Float, nullable=True, default=0.7)

class APIKey(Base):
    __tablename__ = 'api_keys'
    id = Column(Integer, primary_key=True)
    provider = Column(String, nullable=False)
    key = Column(String, nullable=False) # Encrypted key
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

# --- SQLAlchemy setup --- #
basedir = os.path.abspath(os.path.dirname(__file__))
# Place DB in project root (one level up from 'app' folder)
SQLALCHEMY_DB_URL = "sqlite:///" + os.path.join(basedir, '..', 'users.db')

engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
db_session = scoped_session(SessionLocal)


# --- Database Initialization Function (Moved Here) ---
def init_db():
    """Creates database tables from SQLAlchemy models."""
    print(f"Attempting to create tables for database at: {SQLALCHEMY_DB_URL}")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully (or already exist).")
    except Exception as e:
        print(f"Error during table creation: {e}")


# *** REMOVED create_all from module level ***
# Base.metadata.create_all(bind=engine)


# --- User Management Functions --- #
def add_user(username, password):
    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        password=hashed_password,
        selected_provider='openrouter',
        selected_temperature=0.7
    )
    db_session.add(new_user)
    db_session.commit()
    print(f"User '{username}' added.")

def get_user(username):
    # Add a check/log before querying
    print(f"Querying for user: {username}")
    user = db_session.query(User).filter_by(username=username).first()
    print(f"Query result for {username}: {'Found' if user else 'Not Found'}")
    return user


def verify_user(username, password):
    user = get_user(username)
    return user and check_password_hash(user.password, password)

def get_current_user():
    username = session.get("user")
    print(f"Getting current user from session: {username}")
    if username:
        return get_user(username)
    print("No user found in session.")
    return None

# --- API Key Functions ---
def get_user_api_key(user_id, provider):
     print(f"Querying API key for user_id={user_id}, provider={provider}")
     key = db_session.query(APIKey).filter_by(user_id=user_id, provider=provider).first()
     print(f"API Key query result: {'Found' if key else 'Not Found'}")
     return key

# --- User Settings Function ---
def update_user_gameplay_settings(user_id, provider, temperature):
    """Updates the selected provider and temperature for a user."""
    print(f"Attempting to update settings for user_id={user_id}")
    user = db_session.query(User).filter_by(id=user_id).first()
    if user:
        user.selected_provider = provider
        user.selected_temperature = temperature
        db_session.commit()
        print(f"Updated settings for user {user_id}: Provider={provider}, Temp={temperature}")
        return True
    print(f"Failed to find user with id={user_id} to update settings.")
    return False