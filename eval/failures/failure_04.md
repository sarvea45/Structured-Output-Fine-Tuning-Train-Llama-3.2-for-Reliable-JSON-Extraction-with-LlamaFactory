# Failure Analysis: Document 15

## Source Document Text
```text
PURCHASE ORDER
ORDER NO: PO-102
BUYER: BlueSky Retail
SUPPLIER: Nexus Tech
ORDER DATE: 2026-04-15
EXPECTED DELIVERY: ASAP
CURRENCY CODE: USD
LINE ITEMS:
* Widget x10 | UNIT PRICE: $120.00
GRAND TOTAL: $1200.00
```

## Expected JSON
```json
{
  "buyer": "BlueSky Retail",
  "supplier": "Nexus Tech",
  "po_number": "PO-102",
  "date": "2026-04-15",
  "delivery_date": null,
  "currency": "USD",
  "total": 1200.0,
  "items": [
    {
      "item_name": "Widget",
      "quantity": 10,
      "unit_price": 120.0
    }
  ]
}
```

## Actual Model Output
```json
{
  "buyer": "BlueSky Retail",
  "supplier": "Nexus Tech",
  "po_number": "PO-102",
  "date": "2026-04-15",
  "delivery_date": "ASAP",
  "currency": "USD",
  "total": 1200.0,
  "items": []
}
```

## Root Cause Analysis
- **What went wrong:** The model output the string `"ASAP"` for `delivery_date`, which violates the schema constraint that dates must be `YYYY-MM-DD` or `null`.
- **Why it likely failed:** Our curation logic for missing dates purely excluded the `EXPECTED DELIVERY` line entirely when simulating missing dates. We did not train the model on documents where the delivery date field is present but contains non-date text (like "TBD", "ASAP", "Next Week"). Therefore, the model naively copied the string instead of coercing it to `null`.
- **Specific Data Change to Fix It:** Add 5 training examples where `EXPECTED DELIVERY` exists but has informal text (e.g., `TBD`), and map the output `delivery_date` strictly to `null`.
