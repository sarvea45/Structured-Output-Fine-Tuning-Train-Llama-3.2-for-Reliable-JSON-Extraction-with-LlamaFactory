# Failure Analysis: Document 08

## Source Document Text
```text
RECEIPT
DATE: 2026-06-01
CURRENCY: USD
-------------------------------
ITEMS:
- Software License x1 @ $100.00
-------------------------------
SUBTOTAL: $100.00
TOTAL DUE: $100.00
```

## Expected JSON
```json
{
  "vendor": null,
  "invoice_number": null,
  "date": "2026-06-01",
  "due_date": null,
  "currency": "USD",
  "subtotal": 100.0,
  "tax": null,
  "total": 100.0,
  "line_items": [
    {
      "description": "Software License",
      "quantity": 1,
      "unit_price": 100.0
    }
  ]
}
```

## Actual Model Output
```json
{
  "vendor": "Unknown",
  "invoice_number": null,
  "date": "2026-06-01",
  "due_date": null,
  "currency": "USD",
  "subtotal": 100.0,
  "tax": null,
  "total": 100.0,
  "line_items": []
}
```

## Root Cause Analysis
- **What went wrong:** The model hallucinated the string `"Unknown"` for the vendor field instead of returning `null`, and completely dropped the line item.
- **Why it likely failed:** Our curation log shows that we enforced missing fields for `due_date`, `tax`, and `delivery_date`, but *every single invoice in our training dataset had a vendor*. The model learned that `vendor` is a mandatory string and tried to impute one.
- **Specific Data Change to Fix It:** Add 5 examples to the training dataset of "nameless" receipts where the `vendor` field in the JSON output is explicitly mapped to `null`.
