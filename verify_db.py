import sqlite3

DB_PATH = "c:/TravelAI-Website/database/travel.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Get all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("Tables in database:", tables)

# Check favorites table
if 'favorites' in tables:
    print("\n✓ Favorites table exists")
    
    # Get favorites table structure
    cur.execute("PRAGMA table_info(favorites)")
    columns = cur.fetchall()
    print("  Columns:", [c[1] for c in columns])
else:
    print("\n✗ Favorites table NOT found")

# Check destinations
cur.execute("SELECT COUNT(*) FROM destinations")
count = cur.fetchone()[0]
print(f"\n✓ Total destinations: {count}")

# Check a sample image URL
cur.execute("SELECT name, image_url FROM destinations LIMIT 3")
for dest in cur.fetchall():
    print(f"  {dest[0]}: {dest[1]}")

conn.close()
print("\n✓ Database verification complete!")
