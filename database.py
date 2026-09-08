import sqlite3

DB_NAME = "secure_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            encrypted_data TEXT NOT NULL,
            capability_code TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, encrypted_data, capability_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Parameterized query prevents SQL Injection
    cursor.execute(
        "INSERT INTO users (username, encrypted_data, capability_code) VALUES (?, ?, ?)",
        (username, encrypted_data, capability_code)
    )
    conn.commit()
    conn.close()

def fetch_user_data(username, capability_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Parameterized query + capability code check (Double-layer protection)
    cursor.execute(
        "SELECT encrypted_data FROM users WHERE username = ? AND capability_code = ?",
        (username, capability_code)
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None