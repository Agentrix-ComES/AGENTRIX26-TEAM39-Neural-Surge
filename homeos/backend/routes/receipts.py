from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tools.receipt_parser import parse_receipt_text
from tools.db import get_db_connection
from datetime import datetime, timedelta

router = APIRouter()

class ReceiptRequest(BaseModel):
    raw_text: str
    purchase_date: str
    store_name: str

def clean_and_convert_quantity(receipt_qty_str: str, receipt_unit: str, target_unit: str) -> float:
    import re
    # Extract numeric part (e.g., "5.5" or "5")
    nums = re.findall(r'[\d\.]+', receipt_qty_str)
    if not nums:
        qty = 1.0
    else:
        try:
            qty = float(nums[0])
        except ValueError:
            qty = 1.0
            
    qty_lower = receipt_qty_str.lower()
    unit_lower = receipt_unit.lower().strip()
    
    is_kg = "kg" in qty_lower or unit_lower == "kg" or unit_lower == "kilogram" or unit_lower == "kilograms"
    is_liter = "l" in qty_lower or unit_lower == "l" or unit_lower == "liter" or unit_lower == "liters" or unit_lower == "litre" or unit_lower == "litres"
    
    target_lower = target_unit.lower().strip()
    if target_lower == "g":
        if is_kg:
            qty *= 1000.0
    elif target_lower == "ml":
        if is_liter:
            qty *= 1000.0
            
    return qty

def normalize_ingredient_name(name: str) -> str:
    name = name.lower().strip()
    if name == "egg":
        return "eggs"
    if name == "carrot":
        return "carrots"
    if name == "tomato":
        return "tomatoes"
    if name == "bean":
        return "beans"
    if name == "onion":
        return "onions"
    return name

@router.post("/")
def add_receipt(req: ReceiptRequest):
    print("[DEBUG] POST /api/receipts/ invoked.")
    print(f"[DEBUG] Incoming request payload (parsed request body): {req}")
    print(f"[DEBUG] raw_text: {req.raw_text}")
    print(f"[DEBUG] purchase_date: {req.purchase_date}")
    print(f"[DEBUG] store_name: {req.store_name}")
    
    valid_items, warnings = parse_receipt_text(req.raw_text)
    
    print(f"[DEBUG] parse_receipt_text returned items: {valid_items}, warnings: {warnings}")
    
    if not valid_items:
        err_msg = "No valid items parsed from receipt."
        print(f"[DEBUG] Raising HTTP 400 Bad Request: {err_msg}. Warnings: {warnings}")
        raise HTTPException(status_code=400, detail={"message": err_msg, "warnings": warnings})
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Insert receipt
        print(f"[DEBUG] Inserting receipt record for store: {req.store_name}, date: {req.purchase_date}...")
        cursor.execute("INSERT INTO receipts (purchase_date, store_name) VALUES (?, ?)", (req.purchase_date, req.store_name))
        receipt_id = cursor.lastrowid
        print(f"[DEBUG] Receipt inserted with ID: {receipt_id}")
        
        total_expense = 0.0
        
        # Calculate expiry (default 7 days from purchase)
        try:
            p_date = datetime.strptime(req.purchase_date, "%Y-%m-%d")
        except ValueError:
            p_date = datetime.now()
            
        expiry_date = (p_date + timedelta(days=7)).strftime("%Y-%m-%d")
        
        for item in valid_items:
            # Insert receipt_item
            print(f"[DEBUG] Inserting receipt item: {item['name']}, qty: {item['quantity']}, price: {item['price']}...")
            cursor.execute("""
                INSERT INTO receipt_items (receipt_id, name, quantity, unit, price)
                VALUES (?, ?, ?, ?, ?)
            """, (receipt_id, item['name'], item['quantity'], item['unit'], item['price']))
            
            total_expense += item['price']
            
            norm_name = normalize_ingredient_name(item['name'])
            
            # Update inventory
            print(f"[DEBUG] Updating Inventory for ingredient: {norm_name}...")
            cursor.execute("SELECT quantity, original_quantity, unit FROM Inventory WHERE LOWER(ingredient) = LOWER(?)", (norm_name,))
            row = cursor.fetchone()
            if row:
                try:
                    old_qty = float(row[0])
                    old_orig_qty = float(row[1])
                    target_unit = row[2]
                    added_qty = clean_and_convert_quantity(item['quantity'], item['unit'], target_unit)
                    new_qty = old_qty + added_qty
                    new_orig_qty = old_orig_qty + added_qty
                    print(f"[DEBUG] Existing stock found. Ingredient: {norm_name}, old qty: {old_qty}, old original: {old_orig_qty}. Added qty after conversion: {added_qty} {target_unit}...")
                    cursor.execute("UPDATE Inventory SET quantity = ?, original_quantity = ? WHERE LOWER(ingredient) = LOWER(?)", (new_qty, new_orig_qty, norm_name))
                except Exception as ve:
                    print(f"[DEBUG] Error updating quantity for existing item {norm_name}: {ve}")
                    pass
            else:
                qty_val = clean_and_convert_quantity(item['quantity'], item['unit'], item['unit'])
                print(f"[DEBUG] Ingredient {norm_name} not found in Inventory. Inserting new record with qty: {qty_val} {item['unit']}...")
                cursor.execute("""
                    INSERT INTO Inventory (ingredient, quantity, original_quantity, unit, expiry_date)
                    VALUES (?, ?, ?, ?, ?)
                """, (norm_name, qty_val, qty_val, item['unit'], expiry_date))
                
        # Update monthly expenses
        month_year = p_date.strftime("%Y-%m")
        print(f"[DEBUG] Updating monthly expenses for month: {month_year}...")
        cursor.execute("SELECT total_expense FROM monthly_expenses WHERE month_year = ?", (month_year,))
        row = cursor.fetchone()
        if row:
            new_expense = row[0] + total_expense
            print(f"[DEBUG] Existing expense found: {row[0]}. New total: {new_expense}")
            cursor.execute("UPDATE monthly_expenses SET total_expense = ? WHERE month_year = ?", (new_expense, month_year))
        else:
            print(f"[DEBUG] No existing expense for {month_year}. Inserting expense: {total_expense}")
            cursor.execute("INSERT INTO monthly_expenses (month_year, total_expense) VALUES (?, ?)", (month_year, total_expense))
            
        conn.commit()
        print("[DEBUG] DB transaction committed successfully.")
        
    except Exception as db_err:
        conn.rollback()
        print(f"[DEBUG] Database write error occurred: {db_err}")
        raise HTTPException(status_code=500, detail=f"Database write error: {str(db_err)}")
    finally:
        conn.close()
        
    return {
        "message": "Receipt processed successfully.",
        "receipt_id": receipt_id,
        "parsed_items": len(valid_items),
        "total_expense": total_expense,
        "warnings": warnings
    }

@router.get("/pantry")
def get_pantry():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ingredient FROM Inventory")
    rows = cursor.fetchall()
    conn.close()
    
    names = [row['ingredient'] for row in rows]
    return names

@router.get("/inventory")
def get_inventory():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, ingredient as name, quantity as current_stock, unit, expiry_date FROM Inventory")
    rows = cursor.fetchall()
    conn.close()
    
    # Optional: fetch average price from receipt_items
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, AVG(price) as avg_price FROM receipt_items GROUP BY name")
    avg_prices = {row['name'].lower(): row['avg_price'] for row in cursor.fetchall()}
    conn.close()
    
    inventory_items = []
    for row in rows:
        item = dict(row)
        item['avg_price'] = avg_prices.get(item['name'].lower(), 0.0)
        inventory_items.append(item)
        
    return inventory_items
