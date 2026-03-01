import sqlite3

DB_PATH = "c:/TravelAI-Website/database/travel.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Check if tables exist
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]

# Create reviews table
if 'reviews' not in tables:
    cur.execute("""
        CREATE TABLE reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination_id INTEGER NOT NULL,
            user_id INTEGER,
            username TEXT,
            rating REAL NOT NULL,
            review_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(destination_id) REFERENCES destinations(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    print("✓ Created reviews table")

# Create transport table
if 'transport' not in tables:
    cur.execute("""
        CREATE TABLE transport (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination_id INTEGER NOT NULL,
            transport_type TEXT NOT NULL,
            from_city TEXT,
            approximate_cost INTEGER,
            duration TEXT,
            description TEXT,
            FOREIGN KEY(destination_id) REFERENCES destinations(id)
        )
    """)
    print("✓ Created transport table")

# Create food_cuisine table
if 'food_cuisine' not in tables:
    cur.execute("""
        CREATE TABLE food_cuisine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination_id INTEGER NOT NULL,
            dish_name TEXT NOT NULL,
            cuisine_type TEXT,
            description TEXT,
            must_try BOOLEAN DEFAULT 1,
            FOREIGN KEY(destination_id) REFERENCES destinations(id)
        )
    """)
    print("✓ Created food_cuisine table")

# Create emergency_contacts table
if 'emergency_contacts' not in tables:
    cur.execute("""
        CREATE TABLE emergency_contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination_id INTEGER NOT NULL,
            contact_type TEXT NOT NULL,
            contact_number TEXT,
            description TEXT,
            FOREIGN KEY(destination_id) REFERENCES destinations(id)
        )
    """)
    print("✓ Created emergency_contacts table")

# Create packing_checklist table
if 'packing_checklist' not in tables:
    cur.execute("""
        CREATE TABLE packing_checklist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination_id INTEGER NOT NULL,
            season TEXT,
            item_category TEXT,
            item_name TEXT,
            is_essential BOOLEAN DEFAULT 0,
            FOREIGN KEY(destination_id) REFERENCES destinations(id)
        )
    """)
    print("✓ Created packing_checklist table")

# Create itineraries table for trip planning
if 'itineraries' not in tables:
    cur.execute("""
        CREATE TABLE itineraries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            destination_id INTEGER NOT NULL,
            day_number INTEGER NOT NULL,
            activity_name TEXT,
            activity_time TEXT,
            activity_description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(destination_id) REFERENCES destinations(id)
        )
    """)
    print("✓ Created itineraries table")

conn.commit()

# Add sample data for transport
print("\nAdding sample transport data...")
sample_transport = [
    # Mumbai
    (1, "Flight", "Delhi", 5000, "2 hours", "Direct flights from major cities"),
    (1, "Train", "Delhi", 1500, "16 hours", "Mumbai Rajdhani Express"),
    (1, "Bus", "Delhi", 1200, "24 hours", "Volvo AC buses"),
    # Delhi
    (6, "Flight", "Mumbai", 5000, "2 hours", "Direct flights"),
    (6, "Train", "Mumbai", 1500, "16 hours", "Rajdhani Express"),
    # Agra
    (6, "Train", "Delhi", 500, "3 hours", "Shatabdi Express"),
    (6, "Road", "Delhi", 400, "4 hours", "Via Yamuna Expressway"),
    # Jaipur
    (8, "Flight", "Delhi", 3000, "1 hour", "Direct flights"),
    (8, "Train", "Delhi", 600, "5 hours", "Jaipur Express"),
    (8, "Road", "Delhi", 500, "6 hours", "AC Bus available"),
]

for t in sample_transport:
    cur.execute("""
        INSERT OR IGNORE INTO transport (destination_id, transport_type, from_city, approximate_cost, duration, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, t)

# Add sample food data
print("Adding sample food data...")
sample_food = [
    (1, "Vada Pav", "Street Food", "Mumbai's signature snack", 1),
    (1, "Pav Bhaji", "Street Food", "Spiced potato curry with bread", 1),
    (1, "Bhelpuri", "Street Food", "Tangy puffed rice snack", 1),
    (6, "Petha", "Sweets", "Famous Agra sweet", 1),
    (6, "Bedai", "Breakfast", "Deep-fried bread with spicy potato", 1),
    (8, "Dal Baati Churma", "Rajasthani", "Traditional Rajasthani dish", 1),
    (8, "Laal Maas", "Rajasthani", "Spicy red meat curry", 1),
    (8, "Ghewar", "Sweets", "Sweet disc dessert", 1),
    (7, "Chaat", "Street Food", "Tangy snack", 1),
    (7, "Lassi", "Beverage", "Yogurt drink", 1),
]

for f in sample_food:
    cur.execute("""
        INSERT OR IGNORE INTO food_cuisine (destination_id, dish_name, cuisine_type, description, must_try)
        VALUES (?, ?, ?, ?, ?)
    """, f)

# Add sample emergency contacts
print("Adding sample emergency contacts...")
sample_emergency = [
    (1, "Police", "100", "Mumbai Police"),
    (1, "Ambulance", "102", "Medical Emergency"),
    (1, "Tourist Police", "1363", "Tourist Helpline"),
    (6, "Police", "100", "Uttar Pradesh Police"),
    (6, "Ambulance", "102", "Medical Emergency"),
    (8, "Police", "100", "Rajasthan Police"),
    (8, "Ambulance", "102", "Medical Emergency"),
    (8, "Tourist Helpline", "1363", "Tourist Assistance"),
]

for e in sample_emergency:
    cur.execute("""
        INSERT OR IGNORE INTO emergency_contacts (destination_id, contact_type, contact_number, description)
        VALUES ((1, "Police", "100", "Mumbai Police"),
    (1, "Ambulance", "102", "Medical Emergency"),
    (1, "Tourist Police", "1363", "Tourist Helpline"),
    (6, "Police", "100", "Uttar Pradesh Police"),
    (6, "Ambulance", "102", "Medical Emergency"),
    (8, "Police", "100", "Rajasthan Police"),
    (8, "Ambulance", "102", "Medical Emergency"),
    (8, "Tourist Helpline", "1363", "Tourist Assistance"),)
    """, )

conn.commit()

# Verify all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("\n✓ All tables in database:")
for table in cur.fetchall():
    print(f"  - {table[0]}")

conn.close()
print("\n✓ Interactive features tables created successfully!")
