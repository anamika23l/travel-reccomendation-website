import sqlite3

DB_PATH = "c:/TravelAI-Website/database/travel.db"

# Famous hotels specific to each destination with realistic prices
famous_hotels = {
    "Mumbai": [
        ("The Taj Mahal Palace", "5-Star", 15000, 4.9, "Sea View, Pool, Spa, 24/7 Restaurant", "tajhotel.com"),
        ("The Leela Palace", "5-Star", 12000, 4.8, "Ocean View, Fine Dining, Luxury Spa", "theleela.com"),
        ("Trident Hotel", "4-Star", 6500, 4.5, "Harbour View, Restaurant, Gym", "tridenthotels.com"),
        ("Hotel Marine Plaza", "3-Star", 3500, 4.2, "Near Marine Drive, Restaurant", "hotelmarineplaza.com"),
        ("Hotel Breeze Residency", "2-Star", 1800, 3.8, "Budget Friendly, Near Station", "budgethotel.in"),
    ],
    "Delhi": [
        ("The Leela Palace", "5-Star", 14000, 4.8, "Luxury Spa, Rooftop Pool, Fine Dining", "theleela.com"),
        ("Taj Palace Hotel", "5-Star", 12000, 4.7, "Diplomatic Enclave, Restaurant, Gym", "tajhotels.com"),
        ("The Metropolitan Hotel", "4-Star", 6000, 4.4, "Concierge, Restaurant, Business Center", "metropolitanhotel.com"),
        ("Hotel Bright", "3-Star", 2800, 4.0, "Near New Delhi Station, WiFi", "bright hotel.in"),
        ("Hotel Delhi Heart", "2-Star", 1500, 3.5, "Budget, Basic Amenities", "delhiheart.com"),
    ],
    "Jaipur": [
        ("Rambagh Palace", "5-Star", 25000, 4.9, "Royal Palace, Spa, Fine Dining", "tajhotels.com"),
        ("The Lalit Jaipur", "5-Star", 9000, 4.7, "City View, Pool, Restaurant", "thelalit.com"),
        ("Hotel Pearl Palace", "4-Star", 4500, 4.5, "Heritage Decor, Rooftop Restaurant", "pearlpalacehotel.com"),
        ("Hotel Arya Niwas", "3-Star", 2200, 4.2, "Budget Heritage Hotel", "aryaniwashotels.com"),
        ("Zostel Jaipur", "2-Star", 1200, 4.0, "Hostel, Social Atmosphere", "zostel.com"),
    ],
    "Agra": [
        ("Taj Hotel & Convention Centre", "5-Star", 12000, 4.9, "Taj View, Pool, Spa", "tajhotels.com"),
        ("ITC Mughal", "5-Star", 9500, 4.7, "Mughal Gardens, Pool, Spa", "itchotels.com"),
        ("Hotel Clarks Shiraz", "4-Star", 5000, 4.5, "View of Taj, Restaurant", "clarkshotels.com"),
        ("Hotel Sheela", "3-Star", 2500, 4.2, "Budget Friendly, AC Rooms", "hotelsheela.com"),
        (" Agra Hotel", "2-Star", 1200, 3.8, "Budget, Basic Amenities", "agrahotel.in"),
    ],
    "Shimla": [
        ("The Oberoi Shimla", "5-Star", 18000, 4.9, "Mountain View, Spa, Fine Dining", "oberoihotels.com"),
        ("Wildflower Hall", "5-Star", 15000, 4.8, "Luxury Retreat, Mountain View", "oberoihotels.com"),
        ("Hotel Chapslee", "4-Star", 6500, 4.6, "Heritage Property, Garden View", "chapslee.com"),
        ("Hotel White", "3-Star", 3000, 4.3, "Mall Road, Restaurant", "hotelwhite.com"),
        ("Hotel Pine View", "2-Star", 1800, 3.9, "Budget, Mountain View", "pineviewhotel.in"),
    ],
    "Manali": [
        ("The Himalayan Palace", "4-Star", 7000, 4.6, "River View, Bonfire, Restaurant", "himalayanpalace.in"),
        ("Manali Heights", "3-Star", 3500, 4.4, "Mountain View, Heated Rooms", "manaliheights.com"),
        ("Johnson Hotel", "3-Star", 2800, 4.3, "Heritage Property, Garden", "johnsonhotel.com"),
        ("Hotel Snow View", "2-Star", 1500, 4.0, "Budget, Central Location", "snowviewhotel.in"),
        ("Mountain Queen Hostel", "2-Star", 800, 3.8, "Budget Hostel, Social", "hostelmanali.in"),
    ],
    "Nainital": [
        ("The Naini Retreat", "4-Star", 6500, 4.7, "Lake View, Heritage, Restaurant", "nainiretreat.com"),
        ("Hotel The Lake City", "3-Star", 3200, 4.4, "Near Naini Lake, Restaurant", "hotellakecity.in"),
        ("Hotel Emerald Lake", "3-Star", 2500, 4.2, "Lake View, Budget Friendly", "emeraldhotel.in"),
        ("Nainital Budget Inn", "2-Star", 1200, 3.9, "Basic Amenities, Mall Road", "budgetinn.in"),
        ("Kashmir Guest House", "2-Star", 1000, 3.7, "Very Budget, Basic Rooms", "guesthouse.in"),
    ],
    "Srinagar": [
        ("Kashmir Houseboats - Dal Lake", "5-Star", 15000, 4.9, "Houseboat Experience, Shikara Ride", "kashmirhouseboats.com"),
        ("The Lalit Grand Palace", "5-Star", 12000, 4.8, "Palace Hotel, Garden View", "thelalit.com"),
        ("Centaur Lake View Hotel", "4-Star", 5000, 4.5, "Lake View, Restaurant", "centaurhotel.com"),
        ("Hotel Grand Habib", "3-Star", 2500, 4.2, "Near Dal Lake, Budget", "grandhabib.com"),
        ("Kashmir Tourist Guest House", "2-Star", 1200, 3.8, "Budget, Basic", "touristguesthouse.in"),
    ],
    "Goa": [
        ("Taj Fort Aguada Resort", "5-Star", 18000, 4.9, "Beach Front, Pool, Spa", "tajhotels.com"),
        ("The Leela Goa", "5-Star", 15000, 4.8, "Beach Front, Golf, Spa", "theleela.com"),
        ("Alila Diwa Goa", "5-Star", 11000, 4.7, "Beach View, Infinity Pool", "alilahotels.com"),
        ("Hotel Figo", "3-Star", 3500, 4.4, "Baga Beach, Budget", "hotelfigo.com"),
        ("Beach Hotel Heaven", "2-Star", 1800, 4.0, "Budget, Near Beach", "beachhotel.in"),
    ],
    "Varanasi": [
        ("Taj Ganges Varanasi", "5-Star", 9000, 4.8, "Ganges View, Pool, Spa", "tajhotels.com"),
        ("Hotel Gateway Ganges", "4-Star", 5500, 4.6, "Ganges View, Restaurant", "gatewayhotels.com"),
        ("Hotel Rivatas", "4-Star", 4500, 4.4, "River View, Modern Amenities", "rivatas.com"),
        ("Hotel Ganapati", "3-Star", 2000, 4.2, "Near Ghats, Budget", "hotelganapati.com"),
        ("Shanti Guest House", "2-Star", 1000, 3.9, "Very Budget, Basic", "shantigh.in"),
    ],
    "Udaipur": [
        ("Taj Lake Palace", "5-Star", 25000, 4.9, "Lake Palace, Island Hotel", "tajhotels.com"),
        ("The Leela Palace Udaipur", "5-Star", 18000, 4.8, "Lake View, Luxury Spa", "theleela.com"),
        ("Hotel Fateh Garh", "4-Star", 6000, 4.6, "Hill Top View, Restaurant", "fatehgarh.com"),
        ("Hotel Sarovar", "3-Star", 2500, 4.3, "Lake View, Budget", "hotelsarovar.com"),
        ("Udaipur Youth Hostel", "2-Star", 800, 3.8, "Budget, Social", "youthhostel.in"),
    ],
    "Jodhpur": [
        ("Umaid Bhawan Palace", "5-Star", 22000, 4.9, "Royal Palace, Spa, Museum", "tajhotels.com"),
        ("The Rajputana Palace", "4-Star", 5500, 4.6, "Heritage Decor, Restaurant", "rajputanapalace.com"),
        ("Hotel Haveli", "3-Star", 3000, 4.4, "Heritage Hotel, Rooftop", "havelihotel.in"),
        ("Jodhpur Budget Hotel", "2-Star", 1500, 4.0, "Budget, Basic", "budgetjodhpur.in"),
        ("Old City Guest House", "2-Star", 800, 3.7, "Very Budget", "guesthouse.in"),
    ],
    "Kerala": [
        ("Taj Malabar Resort", "5-Star", 12000, 4.8, "Backwater View, Pool, Spa", "tajhotels.com"),
        ("Kumarakom Lake Resort", "5-Star", 10000, 4.7, "Backwater, Ayurveda Spa", "kumarakom.com"),
        ("Spice Village Hotel", "4-Star", 5500, 4.6, "Spice Plantation, Eco", "spicevillage.com"),
        ("Hotel Tharavadu", "3-Star", 2500, 4.4, "Traditional, Budget", "tharavadu.com"),
        ("Kerala Youth Hostel", "2-Star", 700, 3.9, "Budget, Basic", "hostelkerala.in"),
    ],
    "Darjeeling": [
        ("The Mayfair Darjeeling", "4-Star", 8000, 4.7, "Heritage, Mountain View", "mayfairhotels.com"),
        ("Taj Tashi Darjeeling", "4-Star", 6500, 4.6, "Mountain View, Restaurant", "tajhotels.com"),
        ("Hotel Windamere", "3-Star", 4000, 4.5, "Heritage, Mountain View", "windamerehotel.com"),
        ("Hotel Seven Stars", "2-Star", 1800, 4.1, "Budget, Mall Road", "sevenstars.in"),
        ("Darjeeling Budget Stay", "2-Star", 1000, 3.8, "Basic Budget", "budgetstay.in"),
    ],
    "Leh": [
        ("The Grand Dragon Ladakh", "4-Star", 9000, 4.8, "Luxury, Mountain View", "granddragonladakh.com"),
        ("Hotel Ladakh Palace", "4-Star", 6000, 4.6, "Heritage, Restaurant", "ladakhpalace.com"),
        ("Zostel Leh", "3-Star", 2000, 4.4, "Budget Hostel, Social", "zostel.com"),
        ("Ladakh Budget Hotel", "2-Star", 1200, 4.0, "Basic Budget", "budgetladakh.in"),
        ("Mountain View Guest House", "2-Star", 1000, 3.9, "Very Budget", "guesthouse.in"),
    ],
    "Rishikesh": [
        ("Aloha on the Ganges", "4-Star", 7000, 4.7, "River View, Yoga, Spa", "aloharesorts.com"),
        ("The Tapovan Resort", "4-Star", 5500, 4.6, "River View, Adventure Sports", "tapovanresort.com"),
        ("Hotel Ganga Kinare", "3-Star", 3500, 4.4, "Riverside, Restaurant", "gangakinare.com"),
        ("Rishikesh Yogis Hostel", "2-Star", 1200, 4.2, "Budget, Yoga", "yogishostel.in"),
        ("Ganga Devi Guest House", "2-Star", 800, 3.8, "Very Budget", "gdevigh.in"),
    ],
    "Hyderabad": [
        ("Taj Falaknuma Palace", "5-Star", 25000, 4.9, "Palace Hotel, Luxury Spa", "tajhotels.com"),
        ("The Leela Hyderabad", "5-Star", 12000, 4.8, "Luxury, Fine Dining", "theleela.com"),
        ("Hotel Taj Krishna", "5-Star", 9500, 4.7, "Banquet Hall, Restaurant", "tajhotels.com"),
        ("Hotel Aditya", "3-Star", 3500, 4.4, "Bubget, Near Charminar", "adityahotels.com"),
        ("Hyderabad Budget Inn", "2-Star", 1500, 3.9, "Budget, Basic", "budgetinn.in"),
    ],
    "Chennai": [
        ("The Taj Coromandel", "5-Star", 14000, 4.9, "Luxury, Fine Dining", "tajhotels.com"),
        ("The Leela Palace Chennai", "5-Star", 12000, 4.8, "Sea View, Pool, Spa", "theleela.com"),
        ("Hotel Savera", "4-Star", 5500, 4.5, "Modern Amenities, Restaurant", "saverahotels.com"),
        ("Hotel Comfort", "3-Star", 2500, 4.2, "Budget, Near Station", "hotelcomfort.in"),
        ("Chennai Budget Stay", "2-Star", 1200, 3.8, "Very Budget", "budgetstay.in"),
    ],
    "Bangalore": [
        ("The Taj Bangalore", "5-Star", 13000, 4.9, "Luxury, Pool, Spa", "tajhotels.com"),
        ("The Leela Palace Bangalore", "5-Star", 11000, 4.8, "Luxury, Garden View", "theleela.com"),
        ("Hotel Shangri-La", "5-Star", 10000, 4.7, "Business Hotel, Restaurant", "shangri-la.com"),
        ("Hotel Aroma Circle", "3-Star", 2800, 4.3, "Budget, MG Road", "aromahotels.com"),
        ("Bangalore Backpacker Hostel", "2-Star", 900, 4.1, "Budget Hostel", "hostelbangalore.in"),
    ],
    "Kolkata": [
        ("Taj Bengal Kolkata", "5-Star", 11000, 4.8, "Luxury, Fine Dining", "tajhotels.com"),
        ("The Leela Kolkata", "5-Star", 9000, 4.7, "Modern Luxury, Pool", "theleela.com"),
        ("Hotel Hindustan International", "4-Star", 5500, 4.5, "City Center, Restaurant", "hhikolkata.com"),
        ("Hotel Emerald", "3-Star", 2500, 4.2, "Budget, Park Street", "emeraldhotel.in"),
        ("Kolkata Budget Stay", "2-Star", 1200, 3.9, "Budget, Basic", "budgetstay.in"),
    ],
    "Pune": [
        ("The Taj Hotel Pune", "5-Star", 10000, 4.8, "Luxury, Pool, Spa", "tajhotels.com"),
        ("The Leela Pune", "5-Star", 8500, 4.7, "Business Hotel, Restaurant", "theleela.com"),
        ("Hotel Sheraton", "5-Star", 7500, 4.6, "5-Star Luxury", "sheraton.com"),
        ("Hotel Aurora Towers", "4-Star", 4000, 4.4, "City View, Restaurant", "aurorahotels.com"),
        ("Pune Budget Hotel", "2-Star", 1500, 4.0, "Budget, Station", "budgetpune.in"),
    ],
    "Amritsar": [
        ("Taj Hotel Amritsar", "5-Star", 9000, 4.8, "Near Golden Temple, Luxury", "tajhotels.com"),
        ("Hotel Hyatt Amritsar", "4-Star", 6000, 4.6, "Modern Amenities", "hyatt.com"),
        ("Hotel Royal Vinayak", "3-Star", 3000, 4.4, "Near Golden Temple", "hotelroyalvinayak.com"),
        ("Amritsar Budget Inn", "2-Star", 1500, 4.1, "Budget, Basic", "budgetinn.in"),
        ("Golden Temple Guest House", "2-Star", 1000, 4.0, "Very Budget", "gtemplegh.in"),
    ],
}

# Generic hotels for destinations not in the list
default_hotels = [
    ("City Center Hotel", "4-Star", 4000, 4.3, "Central Location, Restaurant", "hotel.in"),
    ("Grand Resort", "3-Star", 2800, 4.2, "Pool, Restaurant", "resort.in"),
    ("Hotel Express", "2-Star", 1500, 4.0, "Budget, WiFi", "hotelexpress.in"),
    ("Travelers Inn", "2-Star", 1000, 3.8, "Basic Budget", "travelersinn.in"),
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Get all destinations
cur.execute("SELECT id, name FROM destinations")
destinations = cur.fetchall()

# Delete existing hotels
cur.execute("DELETE FROM hotels")
print("Cleared existing hotels...")

# Insert famous hotels for each destination
for dest_id, dest_name in destinations:
    # Try to find specific hotels for this destination
    hotels_to_add = None
    
    # Check for exact match
    if dest_name in famous_hotels:
        hotels_to_add = famous_hotels[dest_name]
    else:
        # Check for partial match
        for key in famous_hotels:
            if key.lower() in dest_name.lower() or dest_name.lower() in key.lower():
                hotels_to_add = famous_hotels[key]
                break
    
    if hotels_to_add is None:
        hotels_to_add = default_hotels
    
    # Insert hotels for this destination
    for hotel in hotels_to_add:
        cur.execute("""
            INSERT INTO hotels (destination_id, hotel_name, category, price_per_night, rating, amenities, image_url, contact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (dest_id, hotel[0], hotel[1], hotel[2], hotel[3], hotel[4], "https://source.unsplash.com/500x300/?hotel," + dest_name.lower().replace(" ", ","), hotel[5]))

conn.commit()

# Verify
cur.execute("SELECT COUNT(*) FROM hotels")
print(f"Total hotels after update: {cur.fetchone()[0]}")

# Show sample
cur.execute("""
    SELECT d.name, h.hotel_name, h.category, h.price_per_night, h.rating
    FROM hotels h
    JOIN destinations d ON h.destination_id = d.id
    LIMIT 20
""")
print("\nSample hotels after update:")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]} | {row[2]} | ₹{row[3]} | ⭐{row[4]}")

conn.close()
print("\n✓ Hotels updated successfully with famous location-specific hotels!")
