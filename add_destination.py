import sqlite3

conn = sqlite3.connect("database/travel.db")
cursor = conn.cursor()

# Add a new destination
cursor.execute("INSERT INTO destinations (name, type, cost) VALUES (?, ?, ?)", 
               ("Shimla", "mountain", 14000))

conn.commit()
conn.close()

print("New destination added!")

