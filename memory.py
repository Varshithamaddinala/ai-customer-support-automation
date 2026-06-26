"""
memory.py
SQLite-based memory for storing and retrieving customer history.
Task 7: Memory Management
"""

import sqlite3
from datetime import datetime

DB_PATH = "memory.db"


def init_db():
    """Creates the conversations table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            query TEXT NOT NULL,
            intent TEXT,
            response TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_interaction(customer_name: str, query: str, intent: str, response: str):
    """Saves one customer interaction to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (customer_name, query, intent, response, timestamp) VALUES (?, ?, ?, ?, ?)",
        (customer_name, query, intent, response, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_history(customer_name: str, limit: int = 5) -> str:
    """Retrieves past interactions for a customer."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT query, intent, response, timestamp FROM conversations WHERE customer_name = ? ORDER BY id DESC LIMIT ?",
        (customer_name, limit)
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return ""

    history_lines = []
    for query, intent, response, timestamp in rows:
        history_lines.append(
            f"- On {timestamp}, asked: \"{query}\" (Category: {intent}). Reply: \"{response}\""
        )
    return "\n".join(history_lines)