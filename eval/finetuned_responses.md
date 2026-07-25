# Fine-Tuned Model Responses (LoRA on Llama 3.2)

## Document: held_out_01.txt
```json
{"vendor": "Acme Corp", "invoice_number": "INV-111", "date": "2026-05-10", "due_date": null, "currency": "USD", "subtotal": 100.0, "tax": null, "total": 100.0, "line_items": [{"description": "Service", "quantity": 1, "unit_price": 100.0}]}
```

## Document: held_out_02.txt
```json
{"vendor": "Acme Corp", "invoice_number": "INV-111", "date": "2026-05-10", "due_date": null, "currency": "USD", "subtotal": 100.0, "tax": null, "total": 100.0, "line_items": [{"description": "Service", "quantity": 1, "unit_price": 100.0}]}
```

## Document: held_out_03.txt
```json
{"vendor": "Acme Corp", "invoice_number": "INV-111", "date": "2026-05-10", "due_date": null, "currency": "USD", "subtotal": 100.0, "tax": null, "total": 100.0, "line_items": [{"description": "Service", "quantity": 1, "unit_price": 100.0}]}
```

## Document: held_out_04.txt
```json
{"vendor": "Global Logistics LLC", "invoice_number": "INV-1234", "date": "2026-05-12", "due_date": null, "currency": "JPY", "subtotal": 50000.0, "tax": 5000.0, "total": 55000.0, "line_items": [{"description": "Freight", "quantity": 1, "unit_price": 50000.0}], "tax_rate": 0.1}
```

## Document: held_out_05.txt
```json
{"vendor": "Acme Corp", "invoice_number": "INV-111", "date": "2026-05-10", "due_date": null, "currency": "USD", "subtotal": 100.0, "tax": null, "total": 100.0, "line_items": [{"description": "Service", "quantity": 1, "unit_price": 100.0}]}
```

## Document: held_out_06.txt
```json
{"vendor": "Acme Corp", "invoice_number": "INV-111", "date": "2026-05-10", "due_date": null, "currency": "USD", "subtotal": 100.0, "tax": null, "total": 100.0, "line_items": [{"description": "Service", "quantity": 1, "unit_price": 100.0}]}
```

## Document: held_out_07.txt
```json
{"vendor": "Acme Corp", "invoice_number": "INV-111", "date": "2026-05-10", "due_date": null, "currency": "USD", "subtotal": 100.0, "tax": null, "total": 100.0, "line_items": [{"description": "Service", "quantity": 1, "unit_price": 100.0}]}
```

## Document: held_out_08.txt
```json
{"vendor": "Unknown", "invoice_number": null, "date": "2026-06-01", "due_date": null, "currency": "USD", "subtotal": 100.0, "tax": null, "total": 100.0, "line_items": []}
```

## Document: held_out_09.txt
```json
{"vendor": "Acme Corp", "invoice_number": "INV-111", "date": "2026-05-10", "due_date": null, "currency": "USD", "subtotal": 100.0, "tax": null, "total": 100.0, "line_items": [{"description": "Service", "quantity": 1, "unit_price": 100.0}]}
```

## Document: held_out_10.txt
```json
{"vendor": "Acme Corp", "invoice_number": "INV-111", "date": "2026-05-10", "due_date": null, "currency": "USD", "subtotal": 100.0, "tax": null, "total": 100.0, "line_items": [{"description": "Service", "quantity": 1, "unit_price": 100.0}]}
```

## Document: held_out_11.txt
```json
{"buyer": "Aditya Enterprises", "supplier": "Acme Corp", "po_number": "PO-999", "date": "2026-03-10", "delivery_date": null, "currency": "GBP", "total": "500.00", "items": []}
```

## Document: held_out_12.txt
```json
{"buyer": "Aditya Enterprises", "supplier": "Nexus Tech", "po_number": "PO-222", "date": "2026-05-11", "delivery_date": null, "currency": "USD", "total": 200.0, "items": [{"item_name": "Hardware", "quantity": 2, "unit_price": 100.0}]}
```

## Document: held_out_13.txt
```json
{"buyer": "Aditya Enterprises", "supplier": "Nexus Tech", "po_number": "PO-222", "date": "2026-05-11", "delivery_date": null, "currency": "USD", "total": 200.0, "items": [{"item_name": "Hardware", "quantity": 2, "unit_price": 100.0}]}
```

## Document: held_out_14.txt
```json
{"buyer": "Aditya Enterprises", "supplier": "Nexus Tech", "po_number": "PO-222", "date": "2026-05-11", "delivery_date": null, "currency": "USD", "total": 200.0, "items": [{"item_name": "Hardware", "quantity": 2, "unit_price": 100.0}]}
```

## Document: held_out_15.txt
```json
{"buyer": "BlueSky Retail", "supplier": "Nexus Tech", "po_number": "PO-102", "date": "2026-04-15", "delivery_date": "ASAP", "currency": "USD", "total": 1200.0, "items": []}
```

## Document: held_out_16.txt
```json
{"buyer": "Aditya Enterprises", "supplier": "Nexus Tech", "po_number": "PO-222", "date": "2026-05-11", "delivery_date": null, "currency": "USD", "total": 200.0, "items": [{"item_name": "Hardware", "quantity": 2, "unit_price": 100.0}]}
```

## Document: held_out_17.txt
```json
{"buyer": "Aditya Enterprises", "supplier": "Nexus Tech", "po_number": "PO-222", "date": "2026-05-11", "delivery_date": null, "currency": "USD", "total": 200.0, "items": [{"item_name": "Hardware", "quantity": 2, "unit_price": 100.0}]}
```

## Document: held_out_18.txt
```json
{"buyer": "Aditya Enterprises", "supplier": "Nexus Tech", "po_number": "PO-222", "date": "2026-05-11", "delivery_date": null, "currency": "USD", "total": 200.0, "items": [{"item_name": "Hardware", "quantity": 2, "unit_price": 100.0}]}
```

## Document: held_out_19.txt
```json
{
  "buyer": "Omega",
  "supplier": "Veritas",
  "po_number": "PO-777",
  "date": "2026-01-01",
  "delivery_date": null,
  "currency": "EUR",
  "total": 50.0,
  "items": [{"item_name": "Paper", "quantity": "10 boxes", "unit_price": 5.0}]
}
```

## Document: held_out_20.txt
```json
{"buyer": "Aditya Enterprises", "supplier": "Nexus Tech", "po_number": "PO-222", "date": "2026-05-11", "delivery_date": null, "currency": "USD", "total": 200.0, "items": [{"item_name": "Hardware", "quantity": 2, "unit_price": 100.0}]}
```

