import sqlite3
import os

# Ensure the database folder exists
if not os.path.isdir("database"):
    os.mkdir("database")

conn = sqlite3.connect("database/travel.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    cost INTEGER NOT NULL
)
""")

# Insert sample data
destinations = [
    ("Goa", "beach", 15000),
    ("Manali", "mountain", 12000),
    ("Jaipur", "culture", 10000),
    ("Kerala", "beach", 18000),
    ("Leh Ladakh", "mountain", 20000)
]

cursor.executemany("INSERT INTO destinations (name, type, cost) VALUES (?, ?, ?)", destinations)

conn.commit()
conn.close()

print("Database setup complete!")
