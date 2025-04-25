# app/init_db.py
import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = "users.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None

def create_users_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    print("✅ users table created.")

def add_test_user(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (
            "testuser",
            generate_password_hash("testpass")
        ))
        conn.commit()
        print("🧪 Test user added: testuser / testpass")
    except sqlite3.IntegrityError:
        print("ℹ️ Test user already exists.")

def main():
    if not os.path.exists(DB_PATH):
        print("📁 users.db not found, creating new database...")
    else:
        print("📁 users.db found.")

    conn = get_connection()
    if not table_exists(conn, "users"):
        print("⚠️ users table not found. Creating...")
        create_users_table(conn)
        add_test_user(conn)
    else:
        print("✅ users table already exists.")

    conn.close()

if __name__ == "__main__":
    main()
