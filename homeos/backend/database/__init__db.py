from db import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Inventory table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        quantity REAL NOT NULL,
        unit TEXT,
        expiry_days INTEGER
    )
    """)

    # Waste score table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS waste_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        risk_score INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()

#------------Insert Data-----------------


def seed():
    conn = get_connection()
    cursor = conn.cursor()

    # Inventory data
    cursor.executemany("""
    INSERT INTO inventory (item_name, quantity, unit, expiry_days)
    VALUES (?, ?, ?, ?)
    """, [
        ("Chicken", 500, "g", 1),
        ("Milk", 1, "L", 2),
        ("Tomato", 4, "pcs", 1)
    ])

    # Waste scores
    cursor.executemany("""
    INSERT INTO waste_scores (item_name, risk_score)
    VALUES (?, ?)
    """, [
        ("Chicken", 95),
        ("Milk", 70),
        ("Tomato", 88)
    ])

    conn.commit()
    conn.close()



if __name__ == "__main__":
    create_tables()
    print("Database initialized! and Seed data inserted")