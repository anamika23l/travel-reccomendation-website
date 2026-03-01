import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "travel.db")
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")

def ensure_db_dir():
    if not os.path.isdir(DB_DIR):
        os.makedirs(DB_DIR)
        print("Created database directory:", DB_DIR)

def init_db():
    if not os.path.isfile(SCHEMA_PATH):
        raise FileNotFoundError(f"Schema file not found at {SCHEMA_PATH}")
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        sql = f.read()
    conn.executescript(sql)
    conn.commit()
    conn.close()
    print("Database initialized at", DB_PATH)

if __name__ == "__main__":
    ensure_db_dir()
    init_db()
