import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "users.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    """
    Create users table if it doesn't exist.
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
    Retrieve a user by username.
    Returns tuple: (id, username, hashed_password) or None.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user(username, password):
    """
    Add a new user with hashed password.
    """
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized.")
