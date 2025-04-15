import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE = "users.db"

# Ensure table exists
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add a new user
def add_user(username, password):
    password_hash = generate_password_hash(password)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
    conn.commit()
    conn.close()

# Get user by username
def get_user(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

# Validate password
def verify_password(stored_hash, provided_password):
    return check_password_hash(stored_hash, provided_password)


# Initialize database on first run
if __name__ == "__main__":
    init_db()
    print("✅ Database initialized!")
