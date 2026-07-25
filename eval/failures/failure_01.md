# Failure Analysis: Document 04

## Source Document Text
```text
*** GLOBAL LOGISTICS LLC ***
INVOICE #: INV-1234
DATE: 2026-05-12
CURRENCY: JPY
-------------------------------
ITEMS:
- Freight x1 @ ¥50000.00
-------------------------------
SUBTOTAL: ¥50000.00
TAX RATE: 10%
TOTAL DUE: ¥55000.00
```

## Expected JSON
```json
{
  "vendor": "Global Logistics LLC",
  "invoice_number": "INV-1234",
  "date": "2026-05-12",
  "due_date": null,
  "currency": "JPY",
  "subtotal": 50000.0,
  "tax": 5000.0,
  "total": 55000.0,
  "line_items": [
    {
      "description": "Freight",
      "quantity": 1,
      "unit_price": 50000.0
    }
  ]
}
```

## Actual Model Output
```json
{
  "vendor": "Global Logistics LLC",
  "invoice_number": "INV-1234",
  "date": "2026-05-12",
  "due_date": null,
  "currency": "JPY",
  "subtotal": 50000.0,
  "tax": 5000.0,
  "total": 55000.0,
  "line_items": [
    {
      "description": "Freight",
      "quantity": 1,
      "unit_price": 50000.0
    }
  ],
  "tax_rate": 0.1
}
```

## Root Cause Analysis
- **What went wrong:** The model hallucinated an extra key (`tax_rate`) that is not present in our strict invoice schema.
- **Why it likely failed:** The source document explicitly states `TAX RATE: 10%`. While the model correctly calculated the `tax` field as 5000.0, it also tried to preserve the tax rate data by inventing a new key. Our dataset primarily handles tax as an absolute amount (`TAX (10%): $5.00`) and does not feature enough examples where a standalone percentage is mapped purely to the `tax` absolute value field without creating a new key.
- **Specific Data Change to Fix It:** We need to add at least 3 more training examples to `curated_train.jsonl` where the raw input contains a `TAX RATE` line, but the expected output completely drops it (only keeping the absolute `tax` value). This will explicitly teach the model to ignore fields that do not fit the schema.
