import logging
from tools.db import get_db_connection

logger = logging.getLogger(__name__)

def get_waste_history():
    """
    Retrieve waste history from the SQLite database.
    Returns:
        dict: A dictionary containing a list of waste items under the "waste_items" key.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, item, waste_count, waste_score FROM waste_history")
        rows = cursor.fetchall()
        conn.close()
        
        waste_items = [dict(row) for row in rows]
        return {"waste_items": waste_items}
    except Exception as e:
        logger.error(f"Error fetching waste history: {e}")
        return {"waste_items": []}
