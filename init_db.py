import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Student details store karne ke liye
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS students (
    roll_no TEXT PRIMARY KEY,
    name TEXT NOT NULL
)
"""
)

# Attendance store karne ke liye
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT,
    name TEXT,
    date TEXT,
    time TEXT
)
"""
)

conn.commit()
conn.close()
print("Database initialized successfully!")