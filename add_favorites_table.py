import sqlite3

DB_PATH = "c:/TravelAI-Website/database/travel.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Check if favorites table exists
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='favorites'")
table_exists = cur.fetchone()

if table_exists:
    print("Favorites table already exists!")
else:
    # Create favorites table
    cur.execute("""
        CREATE TABLE favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            destination_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(destination_id) REFERENCES destinations(id),
            UNIQUE(user_id, destination_id)
        )
    """)
    conn.commit()
    print("Favorites table created successfully!")

# Verify table exists
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='favorites'")
if cur.fetchone():
    print("✓ Favorites table exists in database")
else:
    print("✗ Favorites table NOT found!")

conn.close()
