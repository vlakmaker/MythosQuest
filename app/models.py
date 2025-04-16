import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Path to your SQLite database
DB_PATH = "users.db"

def get_db_connection():
    """
    Opens a new connection to the SQLite database.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Optional: allows dict-like access to row data
    return conn

def init_db():
    """
    Initializes the database by creating the users table if it doesn't exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def get_user(username):
    """
    Retrieves a user by username.
    Returns a row with (id, username, password) or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user(username, password):
    """
    Creates a new user with a hashed password.
    Raises an exception if the username already exists.
    """
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

def verify_user(username, password):
    """
    Verifies that the given password matches the stored hash for the username.
    Returns True if valid, False otherwise.
    """
    user = get_user(username)
    if user and check_password_hash(user["password"], password):
        return True
    return False

# Run this file directly to initialize the database
if __name__ == "__main__":
    init_db()
    print("✅ users.db initialized and ready.")
