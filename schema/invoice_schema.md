# Invoice JSON Schema

This document defines the strict JSON schema that the Llama 3.2 model must adhere to when extracting data from Invoice documents. 

## Schema Constraints & Null Handling
- **Absent Fields:** If a field is optional (e.g., `due_date`, `tax`) and is explicitly missing from the source document, the model MUST output a discrete `null` value without quotes. 
- **Empty Strings / Zeros:** The model must NOT use empty strings `""` or `0.0` to denote missing values. `0.0` implies the value was explicitly stated as zero on the document. `null` implies the data was completely absent.
- **Strict Adherence:** Every training example and evaluation output must perfectly match these keys.

## Required Keys

| Key | Data Type | Description | Handling when Absent |
| :--- | :--- | :--- | :--- |
| `vendor` | string | The name of the company or entity issuing the invoice. | `null` |
| `invoice_number` | string | The unique identifier or number assigned to the invoice. | `null` |
| `date` | string (YYYY-MM-DD) | The date the invoice was issued. Must strictly follow `YYYY-MM-DD` format. | `null` |
| `due_date` | string (YYYY-MM-DD) or null | The date the payment is due. Must strictly follow `YYYY-MM-DD` format. | `null` |
| `currency` | string (3-letter ISO) | The 3-letter ISO code for the currency (e.g., USD, GBP, EUR, INR, JPY). | `null` |
| `subtotal` | float | The total amount before taxes and discounts. Must be a numeric float, not a string. | `null` |
| `tax` | float or null | The total tax amount. Must be a numeric float. | `null` |
| `total` | float | The final total amount owed. Must be a numeric float. | `null` |
| `line_items` | array of objects | A list of the individual items billed. | Empty array `[]` if no items |

### `line_items` Object Structure

Every object inside the `line_items` array must contain:

| Key | Data Type | Description |
| :--- | :--- | :--- |
| `description` | string | The description of the item or service. |
| `quantity` | int or float | The number of units billed. |
| `unit_price` | float | The price per single unit. |

## Example Output
```json
{
  "vendor": "Tata Steel",
  "invoice_number": "INV-2024-001",
  "date": "2024-03-15",
  "due_date": "2024-04-15",
  "currency": "INR",
  "subtotal": 140000.00,
  "tax": 2500.00,
  "total": 142500.00,
  "line_items": [
    {
      "description": "Steel Coils Type A",
      "quantity": 10,
      "unit_price": 14000.00
    }
  ]
}
```
