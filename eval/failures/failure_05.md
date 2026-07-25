# Failure Analysis: Document 19

## Source Document Text
```text
PURCHASE ORDER
ORDER NO: PO-777
BUYER: Omega
SUPPLIER: Veritas
ORDER DATE: 2026-01-01
CURRENCY CODE: EUR
LINE ITEMS:
* Paper | QTY: 10 boxes | UNIT PRICE: €5.00
GRAND TOTAL: €50.00
```

## Expected JSON
```json
{
  "buyer": "Omega",
  "supplier": "Veritas",
  "po_number": "PO-777",
  "date": "2026-01-01",
  "delivery_date": null,
  "currency": "EUR",
  "total": 50.0,
  "items": [
    {
      "item_name": "Paper",
      "quantity": 10,
      "unit_price": 5.0
    }
  ]
}
```

## Actual Model Output
```json
{
  "buyer": "Omega",
  "supplier": "Veritas",
  "po_number": "PO-777",
  "date": "2026-01-01",
  "delivery_date": null,
  "currency": "EUR",
  "total": 50.0,
  "items": [
    {
      "item_name": "Paper",
      "quantity": "10 boxes",
      "unit_price": 5.0
    }
  ]
}
```

## Root Cause Analysis
- **What went wrong:** The `quantity` field output the string `"10 boxes"` instead of the required numerical integer or float.
- **Why it likely failed:** Our Python data generator strictly populated the `QTY` text in the raw input as integers (`QTY: 10`). We did not include any examples with Units of Measure (UOM) attached to the quantity in the raw text. The model didn't learn to strip the text to cast it to an integer.
- **Specific Data Change to Fix It:** Add 5-10 training examples where line items include string-based units (`10 boxes`, `5 hrs`, `2 pallets`) in the raw text, but map the `quantity` output strictly to the numerical value (`10`, `5`, `2`).
