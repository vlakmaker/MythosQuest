import sqlite3
import json

class MemoryManager:
    def __init__(self, db_path='memory.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)  # Allow multiple calls
        self.cursor = self.connection.cursor()
        self.setup_db()

    def setup_db(self):
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS player_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_type TEXT NOT NULL,
                description TEXT NOT NULL,
                additional_info TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def save_memory(self, memory_type, description, additional_info=None):
        """
        Prevents duplicate memory entries for 'character' and 'setting'
        """
        existing_memory = self.cursor.execute(
            "SELECT * FROM player_memory WHERE memory_type = ? AND description = ?",
            (memory_type, description)
        ).fetchone()

        if existing_memory:
            print(f"DEBUG: Memory already exists - {memory_type}: {description}")
            return  # Do NOT save a duplicate

        print(f"DEBUG: Saving {memory_type} -> {description}")  # Debugging
        self.cursor.execute(
            'INSERT INTO player_memory (memory_type, description, additional_info) VALUES (?, ?, ?)',
            (memory_type, description, json.dumps(additional_info) if additional_info else None)
        )
        self.connection.commit()  # Ensure data is stored

    def get_recent_memories(self, limit=5):
        cursor = self.cursor.execute(
            'SELECT memory_type, description, additional_info, timestamp FROM player_memory ORDER BY timestamp DESC LIMIT ?',
            (limit,)
        )
        results = cursor.fetchall()
        return [{
            'memory_type': mtype,
            'description': desc,
            'additional_info': json.loads(info) if info else {},
            'timestamp': timestamp
        } for mtype, desc, info, timestamp in results]

    def close(self):
        self.connection.close()
