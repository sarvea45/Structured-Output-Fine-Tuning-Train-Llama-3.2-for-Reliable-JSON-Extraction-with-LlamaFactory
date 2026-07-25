# Failure Analysis: Document 11

## Source Document Text
```text
PURCHASE ORDER
ORDER NO: PO-999
BUYER: Aditya Enterprises
SUPPLIER: Acme Corp
ORDER DATE: 2026-03-10
CURRENCY CODE: GBP
LINE ITEMS:
* Consulting x1 | UNIT PRICE: £500.00
GRAND TOTAL: £500.00
```

## Expected JSON
```json
{
  "buyer": "Aditya Enterprises",
  "supplier": "Acme Corp",
  "po_number": "PO-999",
  "date": "2026-03-10",
  "delivery_date": null,
  "currency": "GBP",
  "total": 500.0,
  "items": [
    {
      "item_name": "Consulting",
      "quantity": 1,
      "unit_price": 500.0
    }
  ]
}
```

## Actual Model Output
```json
{
  "buyer": "Aditya Enterprises",
  "supplier": "Acme Corp",
  "po_number": "PO-999",
  "date": "2026-03-10",
  "delivery_date": null,
  "currency": "GBP",
  "total": "500.00",
  "items": []
}
```

## Root Cause Analysis
- **What went wrong:** The model output the total as a string (`"500.00"`) instead of a float (`500.0`). It also failed to extract the line items.
- **Why it likely failed:** The GBP currency symbol `£` is relatively rare in the dataset (only 2-3 examples). The base model has a tendency to wrap numbers with unfamiliar prefixes into strings. The fine-tuning wasn't strong enough to override this behavior for GBP specifically.
- **Specific Data Change to Fix It:** We need to increase the representation of foreign currencies (GBP, EUR, JPY) in the dataset from 5 examples up to at least 15 examples, ensuring the output is always mapped strictly to a float.
