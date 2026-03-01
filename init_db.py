#!/usr/bin/env python3
"""
Initialize the Travel AI database with tables and sample data
"""
import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "travel.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")

def init_db():
    """Initialize the database with schema and sample data"""
    try:
        # Remove existing database if it exists
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print(f"Removed existing database: {DB_PATH}")
        
        # Create connection
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Read and execute schema
        with open(SCHEMA_PATH, 'r') as f:
            schema = f.read()
        
        cursor.executescript(schema)
        conn.commit()
        conn.close()
        
        print("\n✅ Database initialized successfully!")
        print(f"📁 Database location: {DB_PATH}")
        print("\n📊 Sample data inserted:")
        
        # Display inserted data
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM destinations")
        count = cursor.fetchone()['count']
        print(f"   - {count} destinations added")
        
        cursor.execute("SELECT name, type, cost FROM destinations LIMIT 5")
        print("\n   Sample destinations:")
        for row in cursor.fetchall():
            print(f"      • {row['name']} ({row['type']}) - ₹{row['cost']}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        raise

if __name__ == "__main__":
    init_db()
