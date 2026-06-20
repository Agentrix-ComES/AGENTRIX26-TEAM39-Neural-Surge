# db.py
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'homeos.db')

def get_db_connection():
    """
    Establishes and returns a connection to the local SQLite database.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initializes the SQLite tables for inventory, waste history, and meal history and seeds them if empty.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create inventory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            quantity TEXT NOT NULL,
            unit TEXT NOT NULL,
            expiry_date TEXT NOT NULL
        )
    """)
    
    # Create waste_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS waste_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL UNIQUE,
            waste_count TEXT NOT NULL,
            waste_score TEXT NOT NULL
        )
    """)
    
    # Create MealHistory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MealHistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            breakfast TEXT NOT NULL,
            lunch TEXT NOT NULL,
            dinner TEXT NOT NULL
        )
    """)
    
    conn.commit()
    
    # Seed inventory
    cursor.execute("SELECT COUNT(*) FROM inventory")
    if cursor.fetchone()[0] == 0:
        seed_inventory = [
            ("Rice", "2", "kg", "2026-07-20"),
            ("Carrots", "500", "g", "2026-06-23"),
            ("Eggs", "6", "pcs", "2026-06-30"),
            ("Soy Sauce", "150", "ml", "2026-12-20")
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO inventory (name, quantity, unit, expiry_date)
            VALUES (?, ?, ?, ?)
        """, seed_inventory)
        conn.commit()
        
    # Seed waste history
    cursor.execute("SELECT COUNT(*) FROM waste_history")
    if cursor.fetchone()[0] == 0:
        seed_waste = [
            ("Carrots", "4", "0.8"),
            ("Eggs", "2", "0.5"),
            ("Rice", "1", "0.2"),
            ("Soy Sauce", "0", "0.1")
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO waste_history (item, waste_count, waste_score)
            VALUES (?, ?, ?)
        """, seed_waste)
        conn.commit()

    # Seed MealHistory with past 7 days of meals (dates 2026-06-13 to 2026-06-19)
    cursor.execute("SELECT COUNT(*) FROM MealHistory")
    if cursor.fetchone()[0] == 0:
        seed_history = [
            ("2026-06-13", "Egg Rice Bowl", "Chicken Fried Rice", "Soy Glazed Chicken"),
            ("2026-06-14", "Scrambled Eggs on Rice", "Carrot Ginger Soup", "Braised Chicken with Carrots"),
            ("2026-06-15", "Boiled Eggs with Rice", "Green Beans Stir Fry", "Chicken Fried Rice"),
            ("2026-06-16", "Garlic Rice", "Egg and Tomato Stir Fry", "Chicken and Beans Stir Fry"),
            ("2026-06-17", "Onion and Egg Omelet", "Tomato Egg Soup", "Chicken and Rice"),
            ("2026-06-18", "Steamed Rice", "Carrot Salad", "Braised Chicken with Carrots"),
            ("2026-06-19", "Scrambled Eggs on Rice", "Vegetable Rice", "Mixed Rice Bowl")
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO MealHistory (date, breakfast, lunch, dinner)
            VALUES (?, ?, ?, ?)
        """, seed_history)
        conn.commit()
        
    conn.close()
    print("Local SQLite database initialized and seeded with MealHistory.")
