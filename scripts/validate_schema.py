import sqlite3
import os
import sys

BASE = os.path.dirname(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE, "database")
DB_PATH = os.path.join(DB_DIR, "validate_temp.db")
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")

if not os.path.isfile(SCHEMA_PATH):
    print("schema.sql not found at", SCHEMA_PATH)
    sys.exit(1)

with open(SCHEMA_PATH, "rb") as f:
    raw = f.read()

if raw.startswith(b"SQLite format 3"):
    print("ERROR: schema.sql contains a binary SQLite header. Replace with plain SQL text.")
    sys.exit(1)

try:
    sql = raw.decode("utf-8")
except UnicodeDecodeError:
    print("ERROR: schema.sql is not valid UTF-8. Re-save as UTF-8 without BOM.")
    sys.exit(1)

try:
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(sql)
    conn.commit()
    conn.close()
    os.remove(DB_PATH)
    print("schema.sql validated successfully.")
except sqlite3.Error as e:
    print("SQLite error while executing schema.sql:")
    print(e)
    sys.exit(1)
