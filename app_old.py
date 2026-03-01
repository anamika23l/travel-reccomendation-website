from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "your_secure_secret_key_2026"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "travel.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM destinations ORDER BY cost ASC")
    destinations = cur.fetchall()
    conn.close()
    
    user = session.get("user")
    return render_template("index.html", user=user, destinations=destinations)

@app.route("/destinations")
def destinations():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM destinations ORDER BY cost ASC")
    destinations = cur.fetchall()
    conn.close()
    
    user = session.get("user")
    return render_template("destinations.html", user=user, destinations=destinations)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form.get("confirm_password", "")
        
        if not username or not password:
            return render_template("register.html", error="Username and password required!")
        
        if password != confirm_password:
            return render_template("register.html", error="Passwords don't match!")
        
        if len(password) < 6:
            return render_template("register.html", error="Password must be at least 6 characters!")
        
        hashed_password = generate_password_hash(password)

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", error="Username already exists!")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid credentials!")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    if request.method == "POST":
        budget = int(request.form.get("budget", 0))
        interest = request.form.get("interest", "").lower()

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM destinations WHERE type=? AND cost<=? ORDER BY cost ASC",
            (interest, budget)
        )
        recommendations = cur.fetchall()
        conn.close()

        user = session.get("user")
        return render_template("result.html", recommendations=recommendations, interest=interest, budget=budget, user=user)
    
    user = session.get("user")
    return render_template("recommendations.html", user=user)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
