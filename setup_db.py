import sqlite3

conn = sqlite3.connect('db/restaurant.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_type TEXT,
    items TEXT,
    total REAL,
    gst REAL,
    discount REAL,
    payment_method TEXT,
    timestamp TEXT
)
''')

conn.commit()
conn.close()