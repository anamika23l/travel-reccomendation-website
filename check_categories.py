import sqlite3
conn = sqlite3.connect('database/travel.db')
cur = conn.cursor()
cur.execute("SELECT DISTINCT category FROM destinations ORDER BY category")
categories = cur.fetchall()
print("Categories in database:")
for c in categories:
    print(f"  - {c[0]}")
conn.close()
