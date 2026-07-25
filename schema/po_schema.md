# Purchase Order JSON Schema

This document defines the strict JSON schema that the Llama 3.2 model must adhere to when extracting data from Purchase Order (PO) documents. 

## Schema Constraints & Null Handling
- **Absent Fields:** If a field is optional (e.g., `delivery_date`) and is explicitly missing from the source document, the model MUST output a discrete `null` value without quotes. 
- **Empty Strings / Zeros:** The model must NOT use empty strings `""` or `0.0` to denote missing values. `0.0` implies the value was explicitly stated as zero on the document. `null` implies the data was completely absent.
- **Strict Adherence:** Every training example and evaluation output must perfectly match these keys.

## Required Keys

| Key | Data Type | Description | Handling when Absent |
| :--- | :--- | :--- | :--- |
| `buyer` | string | The name of the company or entity placing the order. | `null` |
| `supplier` | string | The name of the company or entity fulfilling the order. | `null` |
| `po_number` | string | The unique identifier or number assigned to the purchase order. | `null` |
| `date` | string (YYYY-MM-DD) | The date the purchase order was issued. Must strictly follow `YYYY-MM-DD` format. | `null` |
| `delivery_date` | string (YYYY-MM-DD) or null | The requested or expected date of delivery. Must strictly follow `YYYY-MM-DD` format. | `null` |
| `currency` | string (3-letter ISO) | The 3-letter ISO code for the currency (e.g., USD, GBP, EUR, INR, JPY). | `null` |
| `total` | float | The final total amount for the purchase order. Must be a numeric float, not a string. | `null` |
| `items` | array of objects | A list of the individual items ordered. | Empty array `[]` if no items |

### `items` Object Structure

Every object inside the `items` array must contain:

| Key | Data Type | Description |
| :--- | :--- | :--- |
| `item_name` | string | The name or description of the item ordered. |
| `quantity` | int or float | The number of units ordered. |
| `unit_price` | float | The price per single unit. |

## Example Output
```json
{
  "buyer": "Acme Corp",
  "supplier": "Global Supplies Inc",
  "po_number": "PO-99452",
  "date": "2024-05-10",
  "delivery_date": null,
  "currency": "USD",
  "total": 5200.50,
  "items": [
    {
      "item_name": "Office Chairs",
      "quantity": 25,
      "unit_price": 208.02
    }
  ]
}
```
