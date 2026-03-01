import sqlite3

DB_PATH = "c:/TravelAI-Website/database/travel.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Get all destinations
cur.execute("SELECT id, name, state FROM destinations ORDER BY id")
destinations = cur.fetchall()

print("Current destinations in database:")
for dest in destinations:
    print(f"  {dest[0]}. {dest[1]} - {dest[2]}")

print(f"\nTotal destinations: {len(destinations)}")

conn.close()
