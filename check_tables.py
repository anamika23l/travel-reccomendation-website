import sqlite3

DB_PATH = "c:/TravelAI-Website/database/travel.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Get all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("Tables in database:", tables)

# Check favorites table structure
if 'favorites' in tables:
    cur.execute("PRAGMA table_info(favorites)")
    print("\nFavorites table structure:")
    for col in cur.fetchall():
        print(f"  {col[1]} {col[2]}")

conn.close()
