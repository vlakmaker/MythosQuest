import sqlite3

# Connect (or create) SQLite database
connection = sqlite3.connect("memory.db")

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Create the table only if it doesn't already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS player_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_type TEXT NOT NULL,
    description TEXT NOT NULL,
    additional_info TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit changes and close the connection
connection.commit()
connection.close()

print("Database checked/created successfully!")
