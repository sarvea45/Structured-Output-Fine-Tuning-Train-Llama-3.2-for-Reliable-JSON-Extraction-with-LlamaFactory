import json
import random

invoices = [
    {
        "input": "Invoice 901 from Global Tech. Date: 2026-08-01. Due: 2026-08-15. Total: 1500.50 USD. Subtotal 1400. Tax 100.50. 2x Monitors at 700 each.",
        "expected": {"vendor": "Global Tech", "invoice_number": "901", "date": "2026-08-01", "due_date": "2026-08-15", "currency": "USD", "subtotal": 1400.0, "tax": 100.5, "total": 1500.5, "line_items": [{"description": "Monitors", "quantity": 2.0, "unit_price": 700.0}]}
    },
    {
        "input": "From: PaperCo. Inv# PC-12. Date: Oct 2nd, 2026. No due date specified. We shipped 10 boxes of A4 paper for 50 EUR total. Tax was 5 EUR. Total 55 EUR.",
        "expected": {"vendor": "PaperCo", "invoice_number": "PC-12", "date": "2026-10-02", "due_date": None, "currency": "EUR", "subtotal": 50.0, "tax": 5.0, "total": 55.0, "line_items": [{"description": "A4 paper boxes", "quantity": 10.0, "unit_price": 5.0}]}
    },
    {
        "input": "Invoice from Delta Services. Date 2026-09-10. Amount: 5000 JPY. Just consulting services, no tax.",
        "expected": {"vendor": "Delta Services", "invoice_number": None, "date": "2026-09-10", "due_date": None, "currency": "JPY", "subtotal": 5000.0, "tax": None, "total": 5000.0, "line_items": [{"description": "consulting services", "quantity": 1.0, "unit_price": 5000.0}]}
    },
    {
        "input": "Here is invoice #99. Vendor: Office Depot. Date 2026-01-05. Due 2026-01-20. Total is 100 USD. Subtotal 90, tax 10. 5 pens at 2.0 each, 10 notebooks at 8.0 each.",
        "expected": {"vendor": "Office Depot", "invoice_number": "99", "date": "2026-01-05", "due_date": "2026-01-20", "currency": "USD", "subtotal": 90.0, "tax": 10.0, "total": 100.0, "line_items": [{"description": "pens", "quantity": 5.0, "unit_price": 2.0}, {"description": "notebooks", "quantity": 10.0, "unit_price": 8.0}]}
    },
    {
        "input": "Acme Corp bill. 2026-12-12. No invoice number. Subtotal 200 GBP. Tax 40 GBP. Total 240 GBP. 1x Server repair at 200 GBP.",
        "expected": {"vendor": "Acme Corp", "invoice_number": None, "date": "2026-12-12", "due_date": None, "currency": "GBP", "subtotal": 200.0, "tax": 40.0, "total": 240.0, "line_items": [{"description": "Server repair", "quantity": 1.0, "unit_price": 200.0}]}
    },
    {
        "input": "Monthly subscription invoice 88-A from SaaS Inc. Date: 2026-04-01. Due: 2026-04-15. Amount 99.99 USD. No tax.",
        "expected": {"vendor": "SaaS Inc", "invoice_number": "88-A", "date": "2026-04-01", "due_date": "2026-04-15", "currency": "USD", "subtotal": 99.99, "tax": None, "total": 99.99, "line_items": [{"description": "Monthly subscription", "quantity": 1.0, "unit_price": 99.99}]}
    },
    {
        "input": "Invoice INV-001 from Local Plumber. Fixed the sink. Date: May 5th 2026. Subtotal 150. Tax 15. Total 165 USD.",
        "expected": {"vendor": "Local Plumber", "invoice_number": "INV-001", "date": "2026-05-05", "due_date": None, "currency": "USD", "subtotal": 150.0, "tax": 15.0, "total": 165.0, "line_items": [{"description": "Fixed the sink", "quantity": 1.0, "unit_price": 150.0}]}
    },
    {
        "input": "Supplier: FastDelivery. Inv 1002. Date 2026-03-03. Due 2026-03-10. Total 500 EUR. Subtotal 500. 10x pallets at 50 each.",
        "expected": {"vendor": "FastDelivery", "invoice_number": "1002", "date": "2026-03-03", "due_date": "2026-03-10", "currency": "EUR", "subtotal": 500.0, "tax": None, "total": 500.0, "line_items": [{"description": "pallets", "quantity": 10.0, "unit_price": 50.0}]}
    },
    {
        "input": "Invoice from Amazon AWS. ID: AWS-99. 2026-11-01. Due 2026-11-30. 1x EC2 usage at 1200 USD. 1x S3 usage at 300 USD. Subtotal 1500. Tax 150. Total 1650 USD.",
        "expected": {"vendor": "Amazon AWS", "invoice_number": "AWS-99", "date": "2026-11-01", "due_date": "2026-11-30", "currency": "USD", "subtotal": 1500.0, "tax": 150.0, "total": 1650.0, "line_items": [{"description": "EC2 usage", "quantity": 1.0, "unit_price": 1200.0}, {"description": "S3 usage", "quantity": 1.0, "unit_price": 300.0}]}
    },
    {
        "input": "Bill from IT Support Bros. Inv #444. 2026-02-28. 20 hours of support at 50 GBP/hr. Total 1000 GBP.",
        "expected": {"vendor": "IT Support Bros", "invoice_number": "444", "date": "2026-02-28", "due_date": None, "currency": "GBP", "subtotal": 1000.0, "tax": None, "total": 1000.0, "line_items": [{"description": "hours of support", "quantity": 20.0, "unit_price": 50.0}]}
    }
]

pos = [
    {
        "input": "PO Number: PO-1001. Buyer: TechCorp. Supplier: Hardware Store. Date: 2026-07-01. Delivery expected 2026-07-10. Items: 5x Keyboards at 20 USD. Total 100 USD. Tax 10. Final 110 USD.",
        "expected": {"buyer": "TechCorp", "supplier": "Hardware Store", "po_number": "PO-1001", "date": "2026-07-01", "delivery_date": "2026-07-10", "currency": "USD", "total": 110.0, "items": [{"item_name": "Keyboards", "quantity": 5.0, "unit_price": 20.0}]}
    },
    {
        "input": "Order PO-99. Buyer: Startup Inc. Supplier: WeWork. Date 2026-01-01. 1x Office rent at 5000 USD. Tax 500. Total 5500 USD. Delivery date TBD.",
        "expected": {"buyer": "Startup Inc", "supplier": "WeWork", "po_number": "PO-99", "date": "2026-01-01", "delivery_date": None, "currency": "USD", "total": 5500.0, "items": [{"item_name": "Office rent", "quantity": 1.0, "unit_price": 5000.0}]}
    },
    {
        "input": "Purchase order from BigRetail to ShoeCo. PO# 555. Date: 2026-02-15. Deliver by 2026-03-01. 100x Sneakers at 50 EUR. Total 5000 EUR. Tax 500. Final 5500 EUR.",
        "expected": {"buyer": "BigRetail", "supplier": "ShoeCo", "po_number": "555", "date": "2026-02-15", "delivery_date": "2026-03-01", "currency": "EUR", "total": 5500.0, "items": [{"item_name": "Sneakers", "quantity": 100.0, "unit_price": 50.0}]}
    },
    {
        "input": "PO 77. Buyer: Hospital. Supplier: MedSupply. Date 2026-11-20. 50x Bandages at 2 GBP. Total 100 GBP. No tax. No delivery date specified.",
        "expected": {"buyer": "Hospital", "supplier": "MedSupply", "po_number": "77", "date": "2026-11-20", "delivery_date": None, "currency": "GBP", "total": 100.0, "items": [{"item_name": "Bandages", "quantity": 50.0, "unit_price": 2.0}]}
    },
    {
        "input": "Order 888. Buyer Uni. Supplier BookStore. Date 2026-08-05. Deliver 2026-08-20. 200x Textbooks at 100 USD. Total 20000 USD.",
        "expected": {"buyer": "Uni", "supplier": "BookStore", "po_number": "888", "date": "2026-08-05", "delivery_date": "2026-08-20", "currency": "USD", "total": 20000.0, "items": [{"item_name": "Textbooks", "quantity": 200.0, "unit_price": 100.0}]}
    },
    {
        "input": "PO-12. Buyer: AutoShop. Supplier: TiresRUs. 2026-09-09. Deliver ASAP. 40x Tires at 100 USD. Tax 400. Total 4400 USD.",
        "expected": {"buyer": "AutoShop", "supplier": "TiresRUs", "po_number": "PO-12", "date": "2026-09-09", "delivery_date": None, "currency": "USD", "total": 4400.0, "items": [{"item_name": "Tires", "quantity": 40.0, "unit_price": 100.0}]}
    },
    {
        "input": "Buyer: GovDept. Supplier: Cleaners. PO 001. Date 2026-01-10. 1x Janitorial Services at 1000 JPY. Total 1000 JPY.",
        "expected": {"buyer": "GovDept", "supplier": "Cleaners", "po_number": "001", "date": "2026-01-10", "delivery_date": None, "currency": "JPY", "total": 1000.0, "items": [{"item_name": "Janitorial Services", "quantity": 1.0, "unit_price": 1000.0}]}
    },
    {
        "input": "Order 333. Buyer: Cafe. Supplier: Coffee Beans Inc. Date 2026-10-10. Deliver 2026-10-12. 20x Espresso Bags at 15 EUR. Total 300 EUR.",
        "expected": {"buyer": "Cafe", "supplier": "Coffee Beans Inc", "po_number": "333", "date": "2026-10-10", "delivery_date": "2026-10-12", "currency": "EUR", "total": 300.0, "items": [{"item_name": "Espresso Bags", "quantity": 20.0, "unit_price": 15.0}]}
    },
    {
        "input": "PO-X. Buyer: Movie Studio. Supplier: Camera Rentals. Date 2026-05-01. Deliver 2026-05-15. 2x Red Cameras at 2000 USD. 5x Lenses at 500 USD. Total 6500 USD.",
        "expected": {"buyer": "Movie Studio", "supplier": "Camera Rentals", "po_number": "PO-X", "date": "2026-05-01", "delivery_date": "2026-05-15", "currency": "USD", "total": 6500.0, "items": [{"item_name": "Red Cameras", "quantity": 2.0, "unit_price": 2000.0}, {"item_name": "Lenses", "quantity": 5.0, "unit_price": 500.0}]}
    },
    {
        "input": "Buyer: Gym. Supplier: WeightsCo. PO 44. Date 2026-12-01. Deliver 2026-12-10. 10x Dumbbells at 50 GBP. Total 500 GBP.",
        "expected": {"buyer": "Gym", "supplier": "WeightsCo", "po_number": "44", "date": "2026-12-01", "delivery_date": "2026-12-10", "currency": "GBP", "total": 500.0, "items": [{"item_name": "Dumbbells", "quantity": 10.0, "unit_price": 50.0}]}
    }
]

with open("data/held_out_test.jsonl", "w") as f:
    for item in invoices:
        f.write(json.dumps({
            "instruction": "Extract the data into a strict JSON object adhering to the Invoice schema. Do not output markdown.",
            "input": item["input"],
            "expected_output": json.dumps(item["expected"])
        }) + "\n")
    for item in pos:
        f.write(json.dumps({
            "instruction": "Extract the data into a strict JSON object adhering to the Purchase Order schema. Do not output markdown.",
            "input": item["input"],
            "expected_output": json.dumps(item["expected"])
        }) + "\n")

print("Generated data/held_out_test.jsonl with 20 real test cases.")
