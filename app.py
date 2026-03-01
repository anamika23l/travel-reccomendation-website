from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "travel_ai_secure_2026_india"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "travel.db")

# Email configuration (update with your email settings)
EMAIL_ENABLED = False  # Set to True to enable emails
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"

def send_email(to_email, subject, body):
    """Send email to user"""
    if not EMAIL_ENABLED:
        print(f"Email would be sent to {to_email}: {subject}")
        return True
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def get_db():
    """Database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ============== HOME PAGE ==============
@app.route("/")
def home():
    """Homepage - Redirect to planner if logged in, else login"""
    user = session.get("user")
    if user:
        return redirect(url_for("planner"))
    return redirect(url_for("login"))

# ============== DESTINATIONS & SEARCH ==============
@app.route("/destinations")
def destinations():
    """Browse all destinations with filters"""
    conn = get_db()
    cur = conn.cursor()
    
    category = request.args.get("category", "")
    search = request.args.get("search", "")
    sort = request.args.get("sort", "rating")
    
    if category:
        cur.execute("SELECT * FROM destinations WHERE category=? ORDER BY " + sort + " DESC", (category,))
    elif search:
        search_term = f"%{search}%"
        cur.execute("SELECT * FROM destinations WHERE name LIKE ? OR description LIKE ? OR state LIKE ? ORDER BY " + sort + " DESC", 
                   (search_term, search_term, search_term))
    else:
        cur.execute("SELECT * FROM destinations ORDER BY " + sort + " DESC")
    
    destinations = cur.fetchall()
    
    cur.execute("SELECT DISTINCT category FROM destinations ORDER BY category")
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    
    user = session.get("user")
    user_email = session.get("user_email", "")
    return render_template("destinations.html", user=user, destinations=destinations, 
                         categories=categories, selected_category=category, search=search, user_email=user_email)

# ============== DESTINATION DETAIL PAGE ==============
@app.route("/destination/<int:dest_id>")
def destination_detail(dest_id):
    """Detailed destination view with everything"""
    conn = get_db()
    cur = conn.cursor()
    
    # Get destination
    cur.execute("SELECT * FROM destinations WHERE id=?", (dest_id,))
    destination = cur.fetchone()
    
    if not destination:
        conn.close()
        return "Destination not found", 404
    
    # Get budget from session
    user_budget = session.get('trip_budget', 0)
    
    # Get hotels - order by price ascending (affordable first)
    cur.execute("SELECT * FROM hotels WHERE destination_id=? ORDER BY price_per_night", (dest_id,))
    hotels = cur.fetchall()
    
    # Get activities
    cur.execute("SELECT * FROM activities WHERE destination_id=? ORDER BY cost", (dest_id,))
    activities = cur.fetchall()
    
    # Get tips
    cur.execute("SELECT * FROM travel_tips WHERE destination_id=?", (dest_id,))
    tips = cur.fetchall()
    
    # Similar destinations
    cur.execute("SELECT * FROM destinations WHERE category=? AND id!=? LIMIT 4", 
               (destination['category'], dest_id))
    similar = cur.fetchall()
    
    conn.close()
    
    user = session.get("user")
    user_email = session.get("user_email", "")
    return render_template("destination_detail.html", user=user, destination=destination,
                         hotels=hotels, activities=activities, tips=tips, similar=similar,
                         user_budget=user_budget, user_email=user_email)

# ============== TRAVEL PLANNER (ChatGPT-like) ==============
@app.route("/planner")
def planner():
    """AI-powered travel planner"""
    user = session.get("user")
    user_email = session.get("user_email", "")
    return render_template("planner.html", user=user, user_email=user_email)

@app.route("/api/suggest-trip", methods=["POST"])
def suggest_trip():
    """Suggest trips based on preferences (ChatGPT-like)"""
    data = request.json
    budget = data.get("budget", 10000)
    duration = data.get("duration", 3)
    interest = data.get("interest", "mountain")
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get destinations matching the category (case-insensitive), ordered by rating
    interest_lower = interest.lower()
    
    # Map UI categories to database categories
    category_map = {
        "adventure": "natural",  # adventure maps to Natural in DB
    }
    
    db_category = category_map.get(interest_lower, interest_lower)
    
    cur.execute("""
        SELECT * FROM destinations 
        WHERE LOWER(category) = ? OR LOWER(category) LIKE ?
        ORDER BY rating DESC 
        LIMIT 10
    """, (db_category, f"%{db_category}%"))
    
    suggestions = cur.fetchall()
    conn.close()
    
    recommendations = []
    for dest in suggestions:
        # Calculate total cost: accommodation cost + food + misc
        total = dest['cost_per_day'] * duration + 5000  # +5000 for misc
        
        # Show all matching destinations, indicate if over budget
        recommendations.append({
            'id': dest['id'],
            'name': dest['name'],
            'state': dest['state'],
            'category': dest['category'],
            'rating': dest['rating'],
            'image_url': dest['image_url'],
            'best_season': dest['best_season'],
            'temperature': dest['temperature'],
            'daily_cost': dest['cost_per_day'],
            'estimated_cost': total,
            'within_budget': total <= budget,
            'description': dest['description'][:100] + '...',
            'attractions': dest['attractions'][:80] + '...'
        })
    
    # Sort: first show within-budget, then by rating
    recommendations.sort(key=lambda x: (not x['within_budget'], -x['rating']))
    
    # Store budget in session for hotel recommendations
    session['trip_budget'] = budget
    session['trip_duration'] = duration
    
    return jsonify({
        'status': 'success',
        'recommendations': recommendations[:5],
        'message': f'Found {len(recommendations[:5])} destinations for {interest} travel!'
    })

# ============== HOTEL FILTERING ==============
@app.route("/api/hotels/<int:dest_id>")
def get_hotels(dest_id):
    """Get hotels for a destination - prioritizes affordable options"""
    conn = get_db()
    cur = conn.cursor()
    
    min_price = request.args.get("min", 0, type=int)
    max_price = request.args.get("max", 100000, type=int)
    budget = request.args.get("budget", 0, type=int)
    
    # If budget provided, auto-adjust max price to be budget-friendly (30% of daily budget)
    if budget > 0 and max_price >= 100000:
        max_price = int(budget * 0.3)  # Hotel should be max 30% of daily budget
    
    cur.execute("""
        SELECT * FROM hotels 
        WHERE destination_id=? AND price_per_night BETWEEN ? AND ? 
        ORDER BY price_per_night ASC, rating DESC
    """, (dest_id, min_price, max_price))
    
    hotels = cur.fetchall()
    conn.close()
    
    return jsonify([dict(h) for h in hotels])

# ============== ACTIVITY FILTERING ==============
@app.route("/api/activities/<int:dest_id>")
def get_activities(dest_id):
    """Get activities for a destination"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM activities WHERE destination_id=? ORDER BY cost", (dest_id,))
    activities = cur.fetchall()
    conn.close()
    
    return jsonify([dict(a) for a in activities])

# ============== RECOMMENDATIONS ==============
@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    """Smart recommendations"""
    user = session.get("user")
    user_email = session.get("user_email", "")
    
    if request.method == "POST":
        try:
            budget = int(request.form.get("budget", 0))
            interest = request.form.get("interest", "mountain").lower()
            duration = int(request.form.get("duration", 3))
            
            conn = get_db()
            cur = conn.cursor()
            
            # Use case-insensitive category matching
            cur.execute("""
                SELECT * FROM destinations 
                WHERE LOWER(category) = ? OR LOWER(category) LIKE ?
                ORDER BY rating DESC 
                LIMIT 10
            """, (interest, f"%{interest}%"))
            
            all_dests = cur.fetchall()
            conn.close()
            
            # Format recommendations with budget info
            recommendations = []
            for dest in all_dests:
                total = dest['cost_per_day'] * duration + 5000
                recommendations.append({
                    'id': dest['id'],
                    'name': dest['name'],
                    'state': dest['state'],
                    'rating': dest['rating'],
                    'category': dest['category'],
                    'cost_per_day': dest['cost_per_day'],
                    'estimated_cost': total,
                    'within_budget': total <= budget,
                    'image_url': dest['image_url'],
                    'best_season': dest['best_season']
                })
            
            # Sort by budget first, then rating
            recommendations.sort(key=lambda x: (not x['within_budget'], -x['rating']))
            recommendations = recommendations[:5]
            
            return render_template("result.html", user=user, recommendations=recommendations,
                                 budget=budget, interest=interest, duration=duration, user_email=user_email)
        except (ValueError, TypeError):
            return render_template("recommendations.html", 
                                 user=user, error="Please enter valid numbers")
    
    return render_template("recommendations.html", user=user, error=None, user_email=user_email)

# ============== REGISTRATION ==============
@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration"""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        
        if not username or not email or not password:
            return render_template("register.html", error="All fields required!")
        
        if password != confirm:
            return render_template("register.html", error="Passwords don't match!")
        
        if len(password) < 6:
            return render_template("register.html", error="Password must be at least 6+ characters!")
        
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, generate_password_hash(password)))
            conn.commit()
            conn.close()
            
            # Send welcome email
            welcome_subject = "Welcome to TravelAI! ✈️"
            welcome_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #1a998c;">Welcome to TravelAI, {username}! 🎉</h2>
                <p>Thank you for registering with TravelAI. Your account has been created successfully!</p>
                <p>Start exploring amazing destinations across India and plan your perfect trip.</p>
                <p>Happy Travels! 🌍✈️</p>
                <br>
                <p>Best Regards,<br>The TravelAI Team</p>
            </body>
            </html>
            """
            send_email(email, welcome_subject, welcome_body)
            
            # Auto-login after registration
            session["user"] = username
            session["user_email"] = email
            return redirect(url_for("planner"))
        except sqlite3.IntegrityError:
            return render_template("register.html", error="Username or Email already exists!")
    
    return render_template("register.html")

# ============== LOGIN ==============
@app.route("/login", methods=["GET", "POST"])
def login():
    """User login"""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        conn.close()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user["password"], password):
            # Handle users without email field (backward compatibility)
            session["user"] = username
            session["user_email"] = user.get("email", "") if user else ""
            return redirect(url_for("planner"))
        
        return render_template("login.html", error="Invalid credentials!")
    
    return render_template("login.html")

# ============== FAVORITES ==============
@app.route("/api/favorites", methods=["GET"])
def get_favorites():
    """Get user's favorite destinations"""
    user = session.get("user")
    if not user:
        return jsonify({"error": "Please login first"}), 401
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id, email FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    user_id = user_row[0]
    user_email = user_row[1] if user_row[1] else ""
    
    # Get favorites
    cur.execute("""
        SELECT d.*, f.id as fav_id 
        FROM favorites f 
        JOIN destinations d ON f.destination_id = d.id 
        WHERE f.user_id = ?
    """, (user_id,))
    
    favorites = cur.fetchall()
    conn.close()
    
    return jsonify([dict(f) for f in favorites])

@app.route("/api/favorites/<int:dest_id>", methods=["POST"])
def add_favorite(dest_id):
    """Add a destination to favorites"""
    user = session.get("user")
    if not user:
        return jsonify({"error": "Please login first"}), 401
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id and email
    cur.execute("SELECT id, email FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    user_id = user_row[0]
    user_email = user_row[1] if user_row[1] else ""
    
    # Check if destination exists
    cur.execute("SELECT id, name FROM destinations WHERE id=?", (dest_id,))
    dest = cur.fetchone()
    if not dest:
        conn.close()
        return jsonify({"error": "Destination not found"}), 404
    
    # Check if already in favorites
    cur.execute("SELECT id FROM favorites WHERE user_id=? AND destination_id=?", (user_id, dest_id))
    existing = cur.fetchone()
    if existing:
        conn.close()
        return jsonify({"status": "info", "message": "Already in favorites", "already_favorited": True})
    
    # Add to favorites
    try:
        cur.execute("INSERT INTO favorites (user_id, destination_id) VALUES (?, ?)", 
                   (user_id, dest_id))
        conn.commit()
        conn.close()
        
        # Send email notification if email available
        if user_email:
            email_subject = f"❤️ {dest['name']} added to your Favorites!"
            email_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #1a998c;">Destination Added to Favorites! 🎉</h2>
                <p>Hi {user},</p>
                <p>You've added <strong>{dest['name']}</strong> to your favorites list.</p>
                <p>Start planning your trip today!</p>
                <br>
                <a href="http://127.0.0.1:5000/destination/{dest_id}" style="background: #1a998c; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Destination</a>
                <br><br>
                <p>Happy Travels! 🌍✈️</p>
                <p>Best Regards,<br>The TravelAI Team</p>
            </body>
            </html>
            """
            send_email(user_email, email_subject, email_body)
        
        return jsonify({"status": "success", "message": "Added to favorites!", "already_favorited": False})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"status": "info", "message": "Already in favorites"})

@app.route("/api/favorites/<int:dest_id>", methods=["DELETE"])
def remove_favorite(dest_id):
    """Remove a destination from favorites"""
    user = session.get("user")
    if not user:
        return jsonify({"error": "Please login first"}), 401
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    user_id = user_row[0]
    
    # Remove from favorites
    cur.execute("DELETE FROM favorites WHERE user_id=? AND destination_id=?", 
               (user_id, dest_id))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Removed from favorites!"})

@app.route("/api/favorites/check/<int:dest_id>", methods=["GET"])
def check_favorite(dest_id):
    """Check if a destination is in user's favorites"""
    user = session.get("user")
    if not user:
        return jsonify({"is_favorite": False})
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"is_favorite": False})
    
    user_id = user_row[0]
    
    # Check if in favorites
    cur.execute("SELECT id FROM favorites WHERE user_id=? AND destination_id=?", 
               (user_id, dest_id))
    is_favorite = cur.fetchone() is not None
    conn.close()
    
    return jsonify({"is_favorite": is_favorite})

# ============== LOGOUT ==============
@app.route("/logout")
def logout():
    """User logout"""
    session.pop("user", None)
    session.pop("user_email", None)
    return redirect(url_for("home"))

# ============== FAVORITES PAGE ==============
@app.route("/favorites")
def favorites_page():
    """Show user's favorite destinations"""
    user = session.get("user")
    user_email = session.get("user_email", "")
    if not user:
        return redirect(url_for("login"))
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return redirect(url_for("login"))
    
    user_id = user_row[0]
    
    # Get favorites
    cur.execute("""
        SELECT d.*, f.id as fav_id 
        FROM favorites f 
        JOIN destinations d ON f.destination_id = d.id 
        WHERE f.user_id = ?
    """, (user_id,))
    
    favorites = cur.fetchall()
    conn.close()
    
    return render_template("favorites.html", user=user, favorites=favorites, user_email=user_email)

# ============== TRANSPORT ==============
@app.route("/api/transport/<int:dest_id>")
def get_transport(dest_id):
    """Get transport options for a destination"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transport WHERE destination_id=?", (dest_id,))
    transport = cur.fetchall()
    conn.close()
    return jsonify([dict(t) for t in transport])

# ============== FOOD & CUISINE ==============
@app.route("/api/food/<int:dest_id>")
def get_food(dest_id):
    """Get local food options for a destination"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM food_cuisine WHERE destination_id=? AND must_try=1", (dest_id,))
    food = cur.fetchall()
    conn.close()
    return jsonify([dict(f) for f in food])

# ============== EMERGENCY CONTACTS ==============
@app.route("/api/emergency/<int:dest_id>")
def get_emergency(dest_id):
    """Get emergency contacts for a destination"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM emergency_contacts WHERE destination_id=?", (dest_id,))
    contacts = cur.fetchall()
    conn.close()
    return jsonify([dict(c) for c in contacts])

# ============== REVIEWS ==============
@app.route("/api/reviews/<int:dest_id>")
def get_reviews(dest_id):
    """Get reviews for a destination"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.*, u.username 
        FROM reviews r 
        LEFT JOIN users u ON r.user_id = u.id 
        WHERE r.destination_id=? 
        ORDER BY r.created_at DESC
    """, (dest_id,))
    reviews = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in reviews])

@app.route("/api/reviews/<int:dest_id>", methods=["POST"])
def add_review(dest_id):
    """Add a review for a destination"""
    user = session.get("user")
    if not user:
        return jsonify({"error": "Please login first"}), 401
    
    data = request.json
    rating = data.get("rating", 5)
    review_text = data.get("review_text", "")
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    user_id = user_row[0]
    
    # Add review
    cur.execute("""
        INSERT INTO reviews (destination_id, user_id, username, rating, review_text)
        VALUES (?, ?, ?, ?, ?)
    """, (dest_id, user_id, user, rating, review_text))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Review added!"})

# ============== ITINERARY ==============
@app.route("/api/itinerary/<int:dest_id>")
def get_itinerary(dest_id):
    """Get user's itinerary for a destination"""
    user = session.get("user")
    if not user:
        return jsonify({"error": "Please login first"}), 401
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    user_id = user_row[0]
    
    # Get itinerary
    cur.execute("""
        SELECT * FROM itineraries 
        WHERE user_id=? AND destination_id=? 
        ORDER BY day_number, activity_time
    """, (user_id, dest_id))
    itinerary = cur.fetchall()
    conn.close()
    
    return jsonify([dict(i) for i in itinerary])

@app.route("/api/itinerary/<int:dest_id>", methods=["POST"])
def add_itinerary(dest_id):
    """Add activity to itinerary"""
    user = session.get("user")
    if not user:
        return jsonify({"error": "Please login first"}), 401
    
    data = request.json
    day_number = data.get("day_number", 1)
    activity_name = data.get("activity_name", "")
    activity_time = data.get("activity_time", "")
    activity_description = data.get("activity_description", "")
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    user_id = user_row[0]
    
    # Add activity
    cur.execute("""
        INSERT INTO itineraries (user_id, destination_id, day_number, activity_name, activity_time, activity_description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, dest_id, day_number, activity_name, activity_time, activity_description))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Activity added to itinerary!"})

@app.route("/api/itinerary/<int:dest_id>/<int:activity_id>", methods=["DELETE"])
def delete_itinerary(dest_id, activity_id):
    """Remove activity from itinerary"""
    user = session.get("user")
    if not user:
        return jsonify({"error": "Please login first"}), 401
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    user_id = user_row[0]
    
    # Delete activity
    cur.execute("DELETE FROM itineraries WHERE id=? AND user_id=?", (activity_id, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Activity removed from itinerary!"})

# ============== TRIP HISTORY ==============
@app.route("/trip-history")
def trip_history():
    """Show user's trip history"""
    user = session.get("user")
    user_email = session.get("user_email", "")
    if not user:
        return redirect(url_for("login"))
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return redirect(url_for("login"))
    
    user_id = user_row[0]
    
    # Get trip history
    cur.execute("""
        SELECT th.*, d.name, d.state, d.image_url, d.rating
        FROM trip_history th
        JOIN destinations d ON th.destination_id = d.id
        WHERE th.user_id = ?
        ORDER BY th.visit_date DESC
    """, (user_id,))
    
    trips = cur.fetchall()
    conn.close()
    
    return render_template("trip_history.html", user=user, trips=trips, user_email=user_email)

@app.route("/api/trip-history", methods=["POST"])
def add_trip_history():
    """Add a trip to history"""
    user = session.get("user")
    if not user:
        return jsonify({"error": "Please login first"}), 401
    
    data = request.json
    dest_id = data.get("destination_id")
    visit_date = data.get("visit_date")
    notes = data.get("notes", "")
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    user_id = user_row[0]
    
    # Add trip
    cur.execute("""
        INSERT INTO trip_history (user_id, destination_id, visit_date, notes)
        VALUES (?, ?, ?, ?)
    """, (user_id, dest_id, visit_date, notes))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Trip added to history!"})

# ============== PRICE ALERTS ==============
@app.route("/api/price-alerts", methods=["GET"])
def get_price_alerts():
    """Get user's price alerts"""
    user = session.get("user")
    if not user:
        return jsonify({"error": "Please login first"}), 401
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    user_id = user_row[0]
    
    # Get price alerts
    cur.execute("""
        SELECT pa.*, d.name, d.state, d.cost_per_day, d.image_url
        FROM price_alerts pa
        JOIN destinations d ON pa.destination_id = d.id
        WHERE pa.user_id = ? AND pa.is_active = 1
    """, (user_id,))
    
    alerts = cur.fetchall()
    conn.close()
    
    return jsonify([dict(a) for a in alerts])

@app.route("/api/price-alerts", methods=["POST"])
def add_price_alert():
    """Add a price alert"""
    user = session.get("user")
    if not user:
        return jsonify({"error": "Please login first"}), 401
    
    data = request.json
    dest_id = data.get("destination_id")
    target_price = data.get("target_price")
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    user_id = user_row[0]
    
    # Add price alert
    cur.execute("""
        INSERT INTO price_alerts (user_id, destination_id, target_price)
        VALUES (?, ?, ?)
    """, (user_id, dest_id, target_price))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Price alert added!"})

# ============== PACKING LIST ==============
@app.route("/packing-list")
def packing_list():
    """Show user's packing lists"""
    user = session.get("user")
    user_email = session.get("user_email", "")
    if not user:
        return redirect(url_for("login"))
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return redirect(url_for("login"))
    
    user_id = user_row[0]
    
    # Get packing lists
    cur.execute("""
        SELECT pl.*, d.name as dest_name
        FROM packing_lists pl
        LEFT JOIN destinations d ON pl.destination_id = d.id
        WHERE pl.user_id = ?
        ORDER BY pl.created_at DESC
    """, (user_id,))
    
    packing_lists = cur.fetchall()
    conn.close()
    
    return render_template("packing_list.html", user=user, packing_lists=packing_lists, user_email=user_email)

@app.route("/api/packing-list", methods=["POST"])
def generate_packing_list():
    """Generate a packing list based on trip type"""
    user = session.get("user")
    if not user:
        return jsonify({"error": "Please login first"}), 401
    
    data = request.json
    dest_id = data.get("destination_id")
    trip_type = data.get("trip_type", "general")
    
    # Generate packing list items based on trip type
    packing_items = {
        "general": ["Clothes", "Toiletries", "Medications", "Phone charger", "Camera", "Sunglasses", "Hat", "Shoes"],
        "adventure": ["Hiking boots", "Rain jacket", "First aid kit", "Flashlight", "Water bottle", "Backpack", "Trekking poles", "Sunscreen"],
        "beach": ["Swimsuit", "Sunscreen", "Beach towel", "Flip flops", "Sunglasses", "Beach bag", "Hat", "Snorkeling gear"],
        "business": ["Laptop", "Business cards", "Formal clothes", "Notebook", "Pen", "Phone charger", "Power bank"],
        "honeymoon": ["Couple outfits", "Romantic dinner reservation", "Camera", "Sunglasses", "Spa booking", "Comfortable shoes"]
    }
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    user_id = user_row[0]
    
    items = ",".join(packing_items.get(trip_type, packing_items["general"]))
    
    # Save packing list
    cur.execute("""
        INSERT INTO packing_lists (user_id, destination_id, trip_type, items)
        VALUES (?, ?, ?, ?)
    """, (user_id, dest_id, trip_type, items))
    conn.commit()
    conn.close()
    
    return jsonify({
        "status": "success", 
        "message": "Packing list generated!",
        "items": packing_items.get(trip_type, packing_items["general"])
    })

# ============== BLOG ==============
@app.route("/blog")
def blog():
    """Show travel blog posts"""
    user = session.get("user")
    user_email = session.get("user_email", "")
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM blog_posts ORDER BY created_at DESC")
    posts = cur.fetchall()
    conn.close()
    
    return render_template("blog.html", user=user, posts=posts, user_email=user_email)

@app.route("/blog/<int:post_id>")
def blog_post(post_id):
    """Show single blog post"""
    user = session.get("user")
    user_email = session.get("user_email", "")
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM blog_posts WHERE id=?", (post_id,))
    post = cur.fetchone()
    conn.close()
    
    if not post:
        return "Post not found", 404
    
    return render_template("blog_post.html", user=user, post=post, user_email=user_email)

# ============== USER PROFILE ==============
@app.route("/profile", methods=["GET", "POST"])
def profile():
    """User profile page"""
    user = session.get("user")
    user_email = session.get("user_email", "")
    if not user:
        return redirect(url_for("login"))
    
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == "POST":
        new_email = request.form.get("email", "").strip()
        new_password = request.form.get("password", "")
        
        if new_email:
            cur.execute("UPDATE users SET email=? WHERE username=?", (new_email, user))
            session["user_email"] = new_email
        
        if new_password:
            cur.execute("UPDATE users SET password=? WHERE username=?", 
                       (generate_password_hash(new_password), user))
        
        conn.commit()
        conn.close()
        return redirect(url_for("profile"))
    
    cur.execute("SELECT id, username, email, created_at FROM users WHERE username=?", (user,))
    user_data = cur.fetchone()
    conn.close()
    
    return render_template("profile.html", user=user, user_data=user_data, user_email=user_email)

# ============== SHARE FAVORITES ==============
@app.route("/api/share-favorites", methods=["POST"])
def share_favorites():
    """Share favorites via email"""
    user = session.get("user")
    if not user:
        return jsonify({"error": "Please login first"}), 401
    
    data = request.json
    share_email = data.get("email", "")
    message = data.get("message", "")
    
    if not share_email:
        return jsonify({"error": "Email address required"}), 400
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get user id
    cur.execute("SELECT id, email FROM users WHERE username=?", (user,))
    user_row = cur.fetchone()
    if not user_row:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    
    user_id = user_row[0]
    user_email = user_row[1] if user_row[1] else ""
    
    # Get favorites
    cur.execute("""
        SELECT d.name, d.state, d.image_url
        FROM favorites f 
        JOIN destinations d ON f.destination_id = d.id 
        WHERE f.user_id = ?
    """, (user_id,))
    
    favorites = cur.fetchall()
    conn.close()
    
    # Build email content
    fav_list = "<br>".join([f"{f['name']} ({f['state']})" for f in favorites])
    
    email_subject = f"{user} shared their TravelAI Favorites with you!"
    email_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #1a998c;">Check out these amazing destinations! 🌍</h2>
        <p>Hi!</p>
        <p><strong>{user}</strong> has shared their favorite destinations from TravelAI with you:</p>
        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 15px 0;">
            {fav_list}
        </div>
        {f'<p>Message: {message}</p>' if message else ''}
        <br>
        <a href="http://127.0.0.1:5000/destinations" style="background: #1a998c; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Explore Destinations</a>
        <br><br>
        <p>Happy Travels! ✈️</p>
    </body>
    </html>
    """
    
    send_email(share_email, email_subject, email_body)
    
    return jsonify({"status": "success", "message": "Favorites shared successfully!"})

# ============== ERROR HANDLERS ==============
@app.errorhandler(404)
def error_404(e):
    """404 error"""
    return render_template("404.html"), 404

@app.errorhandler(500)
def error_500(e):
    """500 error"""
    return render_template("500.html"), 500

# ============== RUN ==============
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
