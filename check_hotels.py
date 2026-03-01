import sqlite3

DB_PATH = "c:/TravelAI-Website/database/travel.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Get all hotels with destination names
cur.execute("""
    SELECT d.name, h.hotel_name, h.category, h.price_per_night, h.rating
    FROM hotels h
    JOIN destinations d ON h.destination_id = d.id
    ORDER BY d.name
""")

hotels = cur.fetchall()

print("Current hotels in database:")
current_dest = ""
for hotel in hotels:
    if hotel[0] != current_dest:
        print(f"\n📍 {hotel[0]}:")
        current_dest = hotel[0]
    print(f"   - {hotel[1]} | {hotel[2]} | ₹{hotel[3]} | ⭐{hotel[4]}")

print(f"\nTotal hotels: {len(hotels)}")
conn.close()
