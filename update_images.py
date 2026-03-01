import sqlite3

DB_PATH = "c:/TravelAI-Website/database/travel.db"

# Mapping of destination names to image filenames
image_mapping = {
    "Shimla": "mall-road-shimla.jpg",
    "Nainital": "nainital.jpg",
    "Manali": "manali.jpg",
    "Srinagar": "shrinagar.jpg",
    "Leh": "leh.jpg",
    "Agra": "agra.jpg",
    "Varanasi": "varanasi.jpg",
    "Jaipur": "jaipur.jpg",
    "Udaipur": "udaipur.jpg",
    "Jodhpur": "jodhapur.jpg",
    "Amritsar": "amritsar.jpg",
    "Rishikesh": "rishikesh.jpg",
    "Darjeeling": "dargiling.jpg",
    "Puri": "jagannath puri.jpg",
    "Bhubaneswar": "bhubneshwar.jpg",
    "Indore": "indore.jpg",
    "Khajuraho": "Khajuraho.jpg",
    "Ujjain": "ujjain.jpg",
    "Mumbai": "mumbai.jpg",
    "Aurangabad": "aurangabad.jpg",
    "Lonavala": "lonavala.jpg",
    "North Goa": "north goa.jpg",
    "South Goa": "south goa.jpg",
    "Ahmedabad": "ahemdabad.jpg",
    "Rann of Kutch": "rann of kuchh.jpg",
    "Kochi": "kochi.jpg",
    "Alleppey": "allepy.jpg",
    "Munnar": "munnar.jpg",
    "Ooty": "ooty.jpg",
    "Madurai": "madurai.jpg",
    "Rameshwaram": "rameshwaram.jpg",
    "Kanniyakumari": "kanniyakumari.jpg",
    "Hyderabad": "hydrabad.jpg",
    "Tirupati": "tirupati.jpg",
    "Shillong": "shilong.jpg",
    "Gangtok": "gangtok.jpg",
    "Tawang": "tawang.jpg",
    "Jaisalmer": "jaisalmer.jpg",
    "Pushkar": "pushkar.jpg",
    "Kasol": "kasol.jpg",
    "Dharamshala": "dharmashala.jpg",
    "Mandi": "mandi.jpg",
    "Auli": "auli.jpg",
    "Chopta": "chopta.jpg",
    "Khajjiar": "hajjar.jpg",
    "Coorg": "coorg.jpg",
    "Mysore": "mysore.jpg",
    "Hampi": "hampi.jpg",
    "Port Blair": "port bilar.jpg",
    "Nubra Valley": "naidur.jpg",
    "Mandu": "mandu.jpg",
    "Panjim": "panjim.jpg"
}

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Update images for each destination
for dest_name, image_file in image_mapping.items():
    # Use /static/images/ path for Flask static files
    image_url = f"/static/images/{image_file}"
    cur.execute("UPDATE destinations SET image_url = ? WHERE name = ?", (image_url, dest_name))

conn.commit()

# Verify updates
cur.execute("SELECT name, image_url FROM destinations ORDER BY id")
destinations = cur.fetchall()

print("Updated destinations with local images:")
for dest in destinations:
    print(f"  {dest[0]}: {dest[1]}")

print(f"\nTotal destinations updated: {len(destinations)}")
conn.close()
