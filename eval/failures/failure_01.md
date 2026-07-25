# Failure Analysis: Document 01 (Invoice)

## Source Document Snippet
```text
*** APEX SUPPLIES ***
INVOICE #: INV-2026-9812
DATE: 2026-05-14
CURRENCY: USD
-------------------------------
ITEMS:
- Consulting Hours x10 @ $85.00
-------------------------------
SUBTOTAL: $850.00
TOTAL DUE: $850.00
```

## Expected JSON (Ground Truth)
```json
{
  "vendor": "Apex Supplies",
  "invoice_number": "INV-2026-9812",
  "date": "2026-05-14",
  "due_date": null,
  "currency": "USD",
  "subtotal": 850.0,
  "tax": null,
  "total": 850.0,
  "line_items": [
    {
      "description": "Consulting Hours",
      "quantity": 10.0,
      "unit_price": 85.0
    }
  ]
}
```

## Actual Model Output
```json
{
  "vendor": "Apex Supplies",
  "invoice_number": "INV-2026-9812",
  "date": "2026-05-14",
  "due_date": null,
  "currency": "USD",
  "subtotal": 850.0,
  "tax": 0.0,
  "total": 850.0,
  "line_items": [
    {
      "description": "Consulting Hours",
      "quantity": 10.0,
      "unit_price": 85.0
    }
  ]
}
```

## Analysis

### 1. What went wrong?
The model failed schema compliance regarding absent fields. The source document did not mention tax. According to the strict schema rules, tax should have evaluated to `null`. Instead, the model hallucinated the value `0.0`.

### 2. Why did it likely fail?
While our training data included 12 examples of missing tax mapped to `null`, the model still retains a strong pre-trained bias to associate financial missing values with `0.0` rather than a programmatic `null` type.

### 3. Data-centric fix
Prompt engineering cannot reliably fix this deep-seated bias. To fix this at the weight level, we must increase the density of this specific edge case in `curated_train.jsonl`. We need to append 10 additional training examples of invoices lacking tax information, explicitly mapping the output to `"tax": null` to overpower the model's pre-trained assumptions.
