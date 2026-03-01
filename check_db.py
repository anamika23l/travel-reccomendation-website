import sqlite3

conn = sqlite3.connect("database/travel.db")
cur = conn.cursor()

print("Tables:", cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
print("Destinations:", cur.execute("SELECT name, type, cost FROM destinations").fetchall())

conn.close()
