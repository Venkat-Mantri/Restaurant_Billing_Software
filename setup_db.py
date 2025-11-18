import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "restaurant.db")

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_type TEXT,
            items TEXT,
            subtotal REAL,
            gst REAL,
            total REAL,
            payment_method TEXT,
            timestamp TEXT
        );
    """)

    conn.commit()
    conn.close()
    print("Database created successfully at:", DB_PATH)

if __name__ == "__main__":
    create_tables()
