# inventory_tool.py
from .db import get_db_connection

def get_inventory():
    """
    Queries the SQLite database and returns the current pantry inventory.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, quantity, unit, expiry_date FROM inventory")
    rows = cursor.fetchall()
    conn.close()
    
    items = []
    for r in rows:
        items.append({
            "name": r["name"],
            "quantity": r["quantity"],
            "unit": r["unit"],
            "expiry_date": r["expiry_date"]
        })
        
    return {"items": items}
