# Failure Analysis: Document 02 (Purchase Order)

## Source Document Snippet
```text
PURCHASE ORDER
ORDER NO: PO-882-411
BUYER: Horizon Systems
SUPPLIER: Global Logistics LLC
ORDER DATE: 2026-03-22
EXPECTED DELIVERY: TBD
CURRENCY CODE: EUR
LINE ITEMS:
* Server Maintenance | QTY: 2 | UNIT PRICE: €450.00
GRAND TOTAL: €900.00
```

## Expected JSON (Ground Truth)
```json
{
  "buyer": "Horizon Systems",
  "supplier": "Global Logistics LLC",
  "po_number": "PO-882-411",
  "date": "2026-03-22",
  "delivery_date": null,
  "currency": "EUR",
  "total": 900.0,
  "items": [
    {
      "item_name": "Server Maintenance",
      "quantity": 2.0,
      "unit_price": 450.0
    }
  ]
}
```

## Actual Model Output
```json
{
  "buyer": "Horizon Systems",
  "supplier": "Global Logistics LLC",
  "po_number": "PO-882-411",
  "date": "2026-03-22",
  "delivery_date": "TBD",
  "currency": "EUR",
  "total": 900.0,
  "items": [
    {
      "item_name": "Server Maintenance",
      "quantity": 2.0,
      "unit_price": 450.0
    }
  ]
}
```

## Analysis

### 1. What went wrong?
Type mismatch error resulting in a schema violation. The `delivery_date` key requires a strict `YYYY-MM-DD` string or a `null` value. The model extracted the exact text `"TBD"` from the document, violating the date formatting constraint.

### 2. Why did it likely fail?
This is a classic out-of-distribution error. Our `curated_train.jsonl` file handled missing delivery dates by completely omitting them from the input text and mapping them to `null` in the output. However, we did not include any training examples where a date field was present but contained non-standard/ambiguous text like "TBD", "ASAP", or "Pending".

### 3. Data-centric fix
The model learned to map missing text to `null`, but it did not learn to map invalid text to `null`. We must modify the dataset. We need to replace 3 of our standard PO examples in `curated_train.jsonl` with POs that contain strings like "EXPECTED DELIVERY: ASAP", and ensure the corresponding JSON output strictly maps `"delivery_date": null`.
