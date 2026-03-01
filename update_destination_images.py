import sqlite3

# Dictionary of proper image URLs for each destination
destination_images = {
    'Shimla': 'https://images.unsplash.com/photo-1566552183938-caa92328e3a9?w=800&h=500&fit=crop',
    'Nainital': 'https://images.unsplash.com/photo-1559526323-cb2f2fe2591b?w=800&h=500&fit=crop',
    'Manali': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=500&fit=crop',
    'Srinagar': 'c:\TravelAI-Website\images\shrinagar.jpg',
    'Leh': 'https://images.unsplash.com/photo-1566522650166-411cd84d37b7?w=800&h=500&fit=crop',
    'Agra': 'https://images.unsplash.com/photo-1564507592333-c60657eea523?w=800&h=500&fit=crop',
    'Varanasi': 'https://images.unsplash.com/photo-1560993541-37a98f5d7fa9?w=800&h=500&fit=crop',
    'Jaipur': 'https://images.unsplash.com/photo-1599661046289-f90a57d21438?w=800&h=500&fit=crop',
    'Udaipur': 'https://images.unsplash.com/photo-1596270766778-c3db89f9e381?w=800&h=500&fit=crop',
    'Jodhpur': 'https://images.unsplash.com/photo-1567359781514-3b974c5a3fb5?w=800&h=500&fit=crop',
    'Amritsar': 'https://images.unsplash.com/photo-1608779029276-c9075fbd9bf0?w=800&h=500&fit=crop',
    'Rishikesh': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=500&fit=crop',
    'Darjeeling': 'https://images.unsplash.com/photo-1606552183938-ffa5faf0e8cc?w=800&h=500&fit=crop',
    'Puri': 'https://images.unsplash.com/photo-1545652711-491a7fb17da5?w=800&h=500&fit=crop',
    'Bhubaneswar': 'https://images.unsplash.com/photo-1588286840104-8957b019727f?w=800&h=500&fit=crop',
    'Indore': 'https://images.unsplash.com/photo-1570394768868-0e6c26b43b6b?w=800&h=500&fit=crop',
    'Khajuraho': 'https://images.unsplash.com/photo-1577890752751-60a46184c0d1?w=800&h=500&fit=crop',
    'Ujjain': 'https://images.unsplash.com/photo-1578926288207-a90a5366759d?w=800&h=500&fit=crop',
    'Mumbai': 'https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=800&h=500&fit=crop',
    'Aurangabad': 'https://images.unsplash.com/photo-1568871282623-e4ee24b75f69?w=800&h=500&fit=crop',
    'Goa': 'https://images.unsplash.com/photo-1519046904884-53103b34b206?w=800&h=500&fit=crop',
    'Kerala': 'https://images.unsplash.com/photo-1602216055496-273a63b29b89?w=800&h=500&fit=crop',
    'Ooty': 'https://images.unsplash.com/photo-1587117714728-03ddf94823ba?w=800&h=500&fit=crop',
    'Munnar': 'https://images.unsplash.com/photo-1591310737658-7564f5d5a5e4?w=800&h=500&fit=crop',
    'Coorg': 'https://images.unsplash.com/photo-1604099412774-0c59c2fc71e7?w=800&h=500&fit=crop',
    'Mysore': 'https://images.unsplash.com/photo-1562603974-9e7f0828f69b?w=800&h=500&fit=crop',
    'Hyderabad': 'https://images.unsplash.com/photo-1586864387789-628af9feed72?w=800&h=500&fit=crop',
    'Chennai': 'https://images.unsplash.com/photo-1588465043766-5d4f7a1df30c?w=800&h=500&fit=crop',
    'Bangalore': 'https://images.unsplash.com/photo-1599084993091-1cb5c0721cc6?w=800&h=500&fit=crop',
    'Kolkata': 'https://images.unsplash.com/photo-1580913428706-c311ab527eb3?w=800&h=500&fit=crop',
}

# Connect to database
conn = sqlite3.connect('database/travel.db')
cur = conn.cursor()

# Update images for each destination
updated_count = 0
for dest_name, image_url in destination_images.items():
    cur.execute("UPDATE destinations SET image_url = ? WHERE name = ?", (image_url, dest_name))
    if cur.rowcount > 0:
        print(f"✓ Updated {dest_name}")
        updated_count += cur.rowcount

conn.commit()
conn.close()

print(f"\n✅ Successfully updated {updated_count} destination images!")
