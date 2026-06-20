import logging
from tools.db import get_db_connection

logger = logging.getLogger(__name__)

def get_inventory():
    """
    Retrieve all inventory items from the SQLite database.
    Returns:
        dict: A dictionary containing a list of items under the "items" key.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, quantity, unit, expiry_date FROM inventory")
        rows = cursor.fetchall()
        conn.close()
        
        items = [dict(row) for row in rows]
        return {"items": items}
    except Exception as e:
        logger.error(f"Error fetching inventory: {e}")
        return {"items": []}
