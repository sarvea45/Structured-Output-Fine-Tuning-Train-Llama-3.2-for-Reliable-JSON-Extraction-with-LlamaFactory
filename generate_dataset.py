import json
import random
import os

# Ensure directories exist
os.makedirs("data", exist_ok=True)

vendors = ["Acme Corp", "Global Logistics LLC", "Tata Steel", "Apex Supplies", "Nexus Tech", "Veritas Media", "Zenith Electronics"]
buyers = ["Aditya Enterprises", "BlueSky Retail", "Horizon Systems", "Omega Manufacturing", "Starlight Traders"]
currencies = ["USD", "EUR", "GBP", "INR", "JPY"]

currency_symbols = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹", "JPY": "¥"}

sample_items = [
    ("Widget A", 15.00), ("Server Maintenance", 450.00), ("Cloud Hosting", 120.00),
    ("Consulting Hours", 85.00), ("Office Chairs", 150.00), ("USB-C Cables", 12.50),
    ("Monitor 27-inch", 299.99), ("Keyboard Mechanical", 89.90), ("Paper Reams", 25.00)
]

instruction_prompt = "Extract all fields and return ONLY a valid JSON object. No explanation, no markdown, no code fences."

jsonl_records = []
log_entries = []

# Helper to format numbers cleanly
def fmt(val):
    return f"{val:.2f}" if isinstance(val, float) else str(val)

# --- 1. GENERATE 50 INVOICES ---
for i in range(1, 51):
    example_id = f"inv_{i:03d}"
    vendor = random.choice(vendors)
    inv_num = f"INV-2026-{random.randint(1000, 9999)}"
    date = f"2026-0{random.randint(1,6)}-{random.randint(10,28)}"
    
    # Distribution constraints
    has_due_date = i <= 40  # 10 missing due dates
    due_date = f"2026-07-{random.randint(10,28)}" if has_due_date else None
    
    has_tax = i <= 38       # 12 missing tax
    curr = "USD" if i > 3 else currencies[i]   # 3 non-USD invoices (EUR, GBP, INR)
    sym = currency_symbols[curr]
    
    num_items = random.randint(3, 5) if i <= 7 else random.randint(1, 2) # 7 multi-item invoices
    items_selected = random.sample(sample_items, num_items)
    
    line_items = []
    subtotal = 0.0
    
    for desc, price in items_selected:
        qty = random.randint(1, 10)
        line_items.append({"description": desc, "quantity": float(qty), "unit_price": float(price)})
        subtotal += qty * price
        
    tax_amt = round(subtotal * 0.10, 2) if has_tax else None
    total = round(subtotal + (tax_amt if has_tax else 0.0), 2)
    subtotal = round(subtotal, 2)
    
    # Construct raw document text simulating OCR output
    raw_text = f"*** {vendor.upper()} ***\nINVOICE #: {inv_num}\nDATE: {date}\n"
    if due_date:
        raw_text += f"DUE DATE: {due_date}\n"
    raw_text += f"CURRENCY: {curr}\n"
    raw_text += "-------------------------------\nITEMS:\n"
    for item in line_items:
        raw_text += f"- {item['description']} x{int(item['quantity'])} @ {sym}{fmt(item['unit_price'])}\n"
    raw_text += "-------------------------------\n"
    raw_text += f"SUBTOTAL: {sym}{fmt(subtotal)}\n"
    if has_tax:
        raw_text += f"TAX (10%): {sym}{fmt(tax_amt)}\n"
    raw_text += f"TOTAL DUE: {sym}{fmt(total)}\n"
    
    # Expected JSON string output
    json_output = {
        "vendor": vendor,
        "invoice_number": inv_num,
        "date": date,
        "due_date": due_date,
        "currency": curr,
        "subtotal": subtotal,
        "tax": tax_amt,
        "total": total,
        "line_items": line_items
    }
    
    jsonl_records.append({
        "instruction": instruction_prompt,
        "input": raw_text.strip(),
        "output": json.dumps(json_output)
    })
    
    notes = []
    if not has_due_date: notes.append("Missing due_date (null)")
    if not has_tax: notes.append("Missing tax (null)")
    if num_items >= 3: notes.append(f"Multi-item ({num_items} items)")
    if curr != "USD": notes.append(f"Foreign currency ({curr})")
    
    log_entries.append((example_id, "Invoice", "Synthetic Engine", "Kept", "; ".join(notes) if notes else "Standard Invoice Layout"))

# --- 2. GENERATE 30 PURCHASE ORDERS ---
for i in range(1, 31):
    example_id = f"po_{i:03d}"
    buyer = random.choice(buyers)
    supplier = random.choice(vendors)
    po_num = f"PO-882-{random.randint(100, 999)}"
    date = f"2026-03-{random.randint(10,28)}"
    
    has_deliv = i <= 23     # 7 missing delivery dates
    deliv_date = f"2026-04-{random.randint(10,28)}" if has_deliv else None
    
    curr = "USD" if i > 2 else currencies[i+2]   # 2 non-USD POs
    sym = currency_symbols[curr]
    
    num_items = random.randint(3, 4) if i <= 4 else random.randint(1, 2) # 4 multi-item POs
    items_selected = random.sample(sample_items, num_items)
    
    po_items = []
    total = 0.0
    
    for desc, price in items_selected:
        qty = random.randint(5, 20)
        po_items.append({"item_name": desc, "quantity": float(qty), "unit_price": float(price)})
        total += qty * price
    total = round(total, 2)
    
    raw_text = f"PURCHASE ORDER\nORDER NO: {po_num}\nBUYER: {buyer}\nSUPPLIER: {supplier}\nORDER DATE: {date}\n"
    if deliv_date:
        raw_text += f"EXPECTED DELIVERY: {deliv_date}\n"
    raw_text += f"CURRENCY CODE: {curr}\n"
    raw_text += "LINE ITEMS:\n"
    for item in po_items:
        raw_text += f"* {item['item_name']} | QTY: {int(item['quantity'])} | UNIT PRICE: {sym}{fmt(item['unit_price'])}\n"
    raw_text += f"GRAND TOTAL: {sym}{fmt(total)}\n"
    
    json_output = {
        "buyer": buyer,
        "supplier": supplier,
        "po_number": po_num,
        "date": date,
        "delivery_date": deliv_date,
        "currency": curr,
        "total": total,
        "items": po_items
    }
    
    jsonl_records.append({
        "instruction": instruction_prompt,
        "input": raw_text.strip(),
        "output": json.dumps(json_output)
    })
    
    notes = []
    if not has_deliv: notes.append("Missing delivery_date (null)")
    if num_items >= 3: notes.append(f"Multi-item ({num_items} items)")
    if curr != "USD": notes.append(f"Foreign currency ({curr})")
    
    log_entries.append((example_id, "Purchase Order", "Synthetic Engine", "Kept", "; ".join(notes) if notes else "Standard PO Layout"))

# Write to curated_train.jsonl
with open("data/curated_train.jsonl", "w") as f:
    for rec in jsonl_records:
        f.write(json.dumps(rec) + "\n")

# Write to curation_log.md
with open("data/curation_log.md", "w") as f:
    f.write("# Data Curation Audit Log\n\n")
    f.write("| Example ID | Document Type | Source | Status | Schema Notes & Diversity Features |\n")
    f.write("| :--- | :--- | :--- | :--- | :--- |\n")
    for row in log_entries:
        f.write(f"| `{row[0]}` | {row[1]} | {row[2]} | {row[3]} | {row[4]} |\n")

print(f"Successfully generated {len(jsonl_records)} training records in data/curated_train.jsonl")
print("Successfully generated audit log in data/curation_log.md")
