PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS favorites;
DROP TABLE IF EXISTS travel_tips;
DROP TABLE IF EXISTS activities;
DROP TABLE IF EXISTS hotels;
DROP TABLE IF EXISTS destinations;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS trip_history;
DROP TABLE IF EXISTS price_alerts;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS packing_lists;
DROP TABLE IF EXISTS blog_posts;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    state TEXT NOT NULL,
    category TEXT NOT NULL,
    best_season TEXT,
    cost_per_day INTEGER,
    description TEXT,
    attractions TEXT,
    image_url TEXT,
    rating REAL DEFAULT 4.5,
    temperature TEXT,
    how_to_reach TEXT,
    nearby_cities TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hotels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER NOT NULL,
    hotel_name TEXT NOT NULL,
    category TEXT,
    price_per_night INTEGER,
    rating REAL,
    amenities TEXT,
    image_url TEXT,
    contact TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(destination_id) REFERENCES destinations(id)
);

CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER NOT NULL,
    activity_name TEXT NOT NULL,
    category TEXT,
    duration TEXT,
    cost INTEGER,
    description TEXT,
    best_time TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(destination_id) REFERENCES destinations(id)
);

CREATE TABLE travel_tips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER NOT NULL,
    tip_category TEXT,
    title TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(destination_id) REFERENCES destinations(id)
);

-- Favorites table for user favorites
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    destination_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(destination_id) REFERENCES destinations(id),
    UNIQUE(user_id, destination_id)
);

-- Trip History - track visited destinations
CREATE TABLE trip_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    destination_id INTEGER NOT NULL,
    visit_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(destination_id) REFERENCES destinations(id)
);

-- Price Alerts - notify when prices drop
CREATE TABLE price_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    destination_id INTEGER NOT NULL,
    target_price INTEGER,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(destination_id) REFERENCES destinations(id)
);

-- Reviews table
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    username TEXT,
    rating INTEGER,
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(destination_id) REFERENCES destinations(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Packing Lists
CREATE TABLE packing_lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    destination_id INTEGER,
    trip_type TEXT,
    items TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(destination_id) REFERENCES destinations(id)
);

-- Blog Posts
CREATE TABLE blog_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    author TEXT,
    image_url TEXT,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert 52 Indian destinations (UPDATED IMAGE URLS)

  INSERT INTO destinations 
(name, state, category, best_season, cost_per_day, description, attractions, image_url, rating, temperature, how_to_reach, nearby_cities) 
VALUES 

('Shimla','Himachal Pradesh','Mountain','April-June, September-November',5000,
'Queen of Hill Stations with colonial charm, toy train, and panoramic views',
'Jakhoo Temple, The Ridge, Kalka-Shimla Railway, Christ Church',
'c:\TravelAI-Website\images\mall-road-shimla.jpg',4.7,'10-20°C',
'Flight to Delhi, then 7-8 hrs drive/train','Manali, Kasol, Mandi'),

('Nainital','Uttarakhand','Mountain','March-May, September-November',4000,
'Lake town nestled in Himalayan foothills, perfect for adventure and nature',
'Naini Lake, China Peak, Tiffin Top, Naina Devi Temple, Zoo',
'https://source.unsplash.com/500x300/?nainital,lake,mountains',4.6,'8-18°C',
'Flight to Delhi, then 6-7 hrs drive','Ranikhet, Bhimtal, Mussoorie'),

('Manali','Himachal Pradesh','Mountain','March-June, September-November',6000,
'Adventure hub with trekking, paragliding, rafting and stunning views',
'Solang Valley, Rohtang Pass, Beas River, Old Manali, Hadimba Temple',
'https://source.unsplash.com/500x300/?manali,snow,mountains',4.8,'5-20°C',
'Flight to Delhi, then 13-14 hrs drive','Shimla, Kasol, Khajjiar'),

('Srinagar','Jammu & Kashmir','Mountain','April-October',7000,
'Paradise on Earth with houseboats, gardens, and snow-capped peaks',
'Dal Lake, Mughal Gardens, Nagin Lake, Shankaracharya Temple',
'c:\TravelAI-Website\images\shrinagar.jpg',4.9,'-5 to 20°C',
'Flight to Srinagar Airport, 30 mins to city','Gulmarg, Pahalgam, Leh'),

('Leh','Ladakh','Mountain','June-September',8000,
'High altitude desert with stunning monasteries and breathtaking landscapes',
'Thiksey Monastery, Pangong Tso Lake, Khardung La Pass, Hemis Monastery',
'https://source.unsplash.com/500x300/?leh,ladakh,mountains',4.9,'-20 to 15°C',
'Flight to Leh, direct from major cities','Nubra Valley, Pangong Lake, Khardung La'),

('Agra','Uttar Pradesh','Culture','October-March',4000,
'Home to Taj Mahal, one of the seven wonders of the world',
'Taj Mahal, Agra Fort, Fatehpuri Sikri, I.T. Park, Mehtab Bagh',
'https://source.unsplash.com/500x300/?taj mahal,agra',4.9,'15-30°C',
'Flight to Delhi, then 3-4 hrs drive','Delhi, Mathura, Gwalior'),

('Varanasi','Uttar Pradesh','Religious','October-March',3000,
'Holiest city on Earth, spiritual heart of India with sacred Ganges ghats',
'Ghat Rituals, Kashi Vishwanath Temple, Ganges Aarti, Assi Ghat',
'https://source.unsplash.com/500x300/?varanasi,ghats,ganga aarti',4.7,'15-30°C',
'Flight to Varanasi, trains from Delhi','Allahabad, Jaunpur, Ghazipur'),

('Jaipur','Rajasthan','Culture','October-March',5000,
'Pink City of India with magnificent forts and palaces',
'City Palace, Jantar Mantar, Hawa Mahal, Albert Hall Museum',
'https://source.unsplash.com/500x300/?jaipur,hawa mahal',4.6,'15-35°C',
'Flight to Jaipur, train from Delhi','Delhi, Udaipur, Jodhpur'),

('Udaipur','Rajasthan','Culture','October-March',6000,
'City of Lakes with romantic palaces overlooking turquoise waters',
'Lake Palace, City Palace, Jag Mandir, Sajjangarh Fort, Pichola Lake',
'https://source.unsplash.com/500x300/?udaipur,lake palace',4.8,'15-35°C',
'Flight to Udaipur, train from Jaipur','Jodhpur, Pushkar, Chittorgarh'),

('Jodhpur','Rajasthan','Culture','October-March',4000,
'Blue City with majestic Mehrangarh Fort and vibrant markets',
'Mehrangarh Fort, Umaid Bhawan Palace, Mandore Gardens',
'https://source.unsplash.com/500x300/?jodhpur,mehrangarh fort',4.7,'15-35°C',
'Flight to Jodhpur, train from Jaipur','Jaisalmer, Udaipur, Pali');

-- Updated Hotel Images

INSERT INTO hotels 
(destination_id, hotel_name, category, price_per_night, rating, amenities, image_url, contact) 
VALUES

(6,'Taj View Hotel','5-Star',15000,4.9,
'Swimming Pool, Restaurant, Taj View, AC Rooms',
'https://source.unsplash.com/500x300/?luxury hotel,taj mahal view',
'agra@hotels.com'),

(6,'Amar Vilas','4-Star',10000,4.8,
'Rooftop Restaurant, Taj View, Spa',
'https://source.unsplash.com/500x300/?agra luxury hotel',
'amarvilas@hotels.com'),

(6,'Hotel Sheela','3-Star',4000,4.2,
'Budget Friendly, AC Rooms, Restaurant',
'https://source.unsplash.com/500x300/?budget hotel,agra',
'sheela@budget.com'),

(8,'Rambagh Palace','5-Star',20000,4.9,
'Palace Hotel, Spa, Multiple Restaurants',
'https://source.unsplash.com/500x300/?rambagh palace jaipur',
'rambagh@palace.com'),

(8,'Hotel Pearl','3-Star',5000,4.4,
'Central Location, Restaurant, AC Rooms',
'https://source.unsplash.com/500x300/?hotel room,jaipur',
'pearl@jaipur.com'),

(4,'Houseboats Dal Lake','5-Star',12000,4.9,
'Houseboat Experience, Meals, Stunning Views',
'https://source.unsplash.com/500x300/?dal lake houseboat',
'houseboat@srinagar.com'),

(4,'Centaur Hotel','4-Star',8000,4.6,
'Lake View, Garden, Restaurant',
'https://source.unsplash.com/500x300/?hotel srinagar lake view',
'centaur@srinagar.com');

-- Insert sample blog posts
INSERT INTO blog_posts (title, content, author, category, image_url) VALUES
('Top 10 Hill Stations in India', 'Discover the most beautiful hill stations in India...', 'TravelAI Team', 'Travel Guide', 'https://source.unsplash.com/500x300/?hill station,india'),
('Best Time to Visit Kerala', 'A complete guide to planning your Kerala trip...', 'TravelAI Team', 'Travel Guide', 'https://source.unsplash.com/500x300/?kerala,backwaters'),
('Rajasthan on a Budget', 'How to explore the royal state without breaking the bank...', 'TravelAI Team', 'Budget Travel', 'https://source.unsplash.com/500x300/?rajasthan,fort');
