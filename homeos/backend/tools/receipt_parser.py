import re
import os
import json
import requests

def parse_receipt_regex(text: str):
    """
    Fallback Regex parser logic for raw receipt text.
    """
    print(f"[DEBUG] parse_receipt_regex invoked with text length: {len(text)}")
    valid_items = []
    warnings = []
    
    qty_end_pattern = re.compile(r'([\d\.]+)\s*([a-zA-Z]*)$')
    qty_start_pattern = re.compile(r'^([\d\.]+)\s*([a-zA-Z]+)?(.*)')
    
    for line_raw in text.splitlines():
        line = line_raw.strip()
        if not line:
            continue
            
        parts = re.split(r'[-–—]', line)
        if len(parts) < 2:
            warning_msg = f"Invalid format (missing price separator '-'): {line}"
            print(f"[DEBUG] Regex parse warning: {warning_msg}")
            warnings.append(warning_msg)
            continue
            
        left_part = '-'.join(parts[:-1]).strip()
        price_str = parts[-1].strip()
        
        clean_price = re.sub(r'[^\d\.]', '', price_str)
        try:
            if not clean_price:
                raise ValueError("Empty price")
            price = float(clean_price)
        except ValueError:
            warning_msg = f"Invalid price format: {line}"
            print(f"[DEBUG] Regex parse warning: {warning_msg}")
            warnings.append(warning_msg)
            continue
            
        match_end = qty_end_pattern.search(left_part)
        if match_end and match_end.start() > 0:
            qty = match_end.group(1)
            unit = match_end.group(2) or "pieces"
            name = left_part[:match_end.start()].strip()
            item = {"name": name, "quantity": qty, "unit": unit, "price": price}
            print(f"[DEBUG] Regex parsed (end match): {item}")
            valid_items.append(item)
            continue
            
        match_start = qty_start_pattern.search(left_part)
        if match_start:
            qty = match_start.group(1)
            unit_guess = match_start.group(2) or ""
            rest = match_start.group(3).strip()
            if rest:
                unit = unit_guess
                name = rest
            else:
                unit = "pieces"
                name = unit_guess
            if name:
                item = {"name": name, "quantity": qty, "unit": unit, "price": price}
                print(f"[DEBUG] Regex parsed (start match): {item}")
                valid_items.append(item)
                continue
            
        if left_part:
            item = {"name": left_part, "quantity": "1", "unit": "pieces", "price": price}
            print(f"[DEBUG] Regex parsed (fallback): {item}")
            valid_items.append(item)
            continue
            
        warning_msg = f"Could not parse quantity and name: {line}"
        print(f"[DEBUG] Regex parse warning: {warning_msg}")
        warnings.append(warning_msg)
        
    print(f"[DEBUG] parse_receipt_regex finished. Parsed items: {valid_items}, Warnings: {warnings}")
    return valid_items, warnings

def parse_receipt_text(text: str):
    """
    Parses raw receipt text into a list of structured items.
    Tries to use Groq API first if GROQ_API_KEY is available.
    Falls back to regex if it fails or if the key is missing.
    Returns:
        valid_items: list of dicts {"name": str, "quantity": str, "unit": str, "price": float}
        warnings: list of strings indicating lines that failed to parse
    """
    print(f"[DEBUG] parse_receipt_text invoked. Text length: {len(text)}")
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("XAI_API_KEY")
    
    if api_key:
        print("[DEBUG] GROQ_API_KEY found, attempting Groq API request...")
        try:
            prompt = (
                "You are a grocery receipt parser. Extract the items from the following receipt text "
                "and return ONLY a valid JSON array of objects. Do not include markdown blocks or any other text. "
                "Each object must have these exactly keys: 'name' (string), 'quantity' (string), 'unit' (string), and 'price' (number). "
                "If a unit or quantity is missing, infer it logically (e.g. quantity '1', unit 'pieces').\n\n"
                f"Receipt Text:\n{text}"
            )
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1
                },
                timeout=15
            )
            
            print(f"[DEBUG] Groq API HTTP Status: {response.status_code}")
            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                print(f"[DEBUG] Raw Groq API response content: {content}")
                
                # Clean up any potential markdown formatting the LLM might have added despite instructions
                content = content.replace("```json", "").replace("```", "").strip()
                
                # Robust extraction of JSON array from content
                json_match = re.search(r'\[\s*\{.*\}\s*\]', content, re.DOTALL)
                if json_match:
                    content = json_match.group(0)
                    print(f"[DEBUG] Extracted JSON array from response content: {content}")
                
                try:
                    valid_items = json.loads(content)
                except Exception as json_err:
                    print(f"[DEBUG] Failed to parse Groq response JSON: {json_err}. Falling back to regex.")
                    raise json_err
                
                # Validate the structure returned by Groq
                clean_items = []
                for idx, item in enumerate(valid_items):
                    if "name" in item and "price" in item:
                        clean_items.append({
                            "name": str(item["name"]),
                            "quantity": str(item.get("quantity", "1")),
                            "unit": str(item.get("unit", "pieces")),
                            "price": float(item["price"])
                        })
                    else:
                        print(f"[DEBUG] Validation failed for Groq parsed item index {idx}: {item} (missing 'name' or 'price')")
                
                print(f"[DEBUG] Successfully parsed {len(clean_items)} items from Groq API.")
                return clean_items, [] # Return clean items and no warnings if LLM succeeds
            else:
                print(f"[DEBUG] Groq API Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[DEBUG] Groq API Parsing failed, falling back to regex: {e}")
            pass # Fallback to regex below
            
    else:
        print("[DEBUG] No GROQ_API_KEY or XAI_API_KEY found. Falling back to regex parser directly.")
        
    # Fallback to Regex Parser
    return parse_receipt_regex(text)
