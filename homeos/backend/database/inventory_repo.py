from db import get_connection

def get_inventory():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_waste_scores():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM waste_scores")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]