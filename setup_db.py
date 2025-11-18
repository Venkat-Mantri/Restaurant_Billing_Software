import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "restaurant.db")

# Full desired schema for the orders table
TABLE_DEFINITION = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "customer_type": "TEXT",
    "items": "TEXT",
    "subtotal": "REAL",
    "gst": "REAL",
    "total": "REAL",
    "payment_method": "TEXT",
    "timestamp": "TEXT"
}

def create_or_migrate():
    """
    Create the orders table if it doesn't exist.
    Add any missing columns (idempotent).
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create table with minimal id column if table doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        );
    """)
    conn.commit()

    # Get existing columns
    cur.execute("PRAGMA table_info(orders);")
    existing_rows = cur.fetchall()
    existing_cols = [row[1] for row in existing_rows]  # name is at index 1

    # Add missing columns
    for col, col_type in TABLE_DEFINITION.items():
        if col not in existing_cols:
            if col == "id":
                # id already ensured in the initial create
                continue
            alter_sql = f"ALTER TABLE orders ADD COLUMN {col} {col_type};"
            try:
                cur.execute(alter_sql)
                conn.commit()
                print(f"Added missing column: {col} {col_type}")
            except Exception as e:
                print(f"Failed to add column {col}: {e}")

    conn.close()
    print("Database ready at:", DB_PATH)

if __name__ == "__main__":
    create_or_migrate()
