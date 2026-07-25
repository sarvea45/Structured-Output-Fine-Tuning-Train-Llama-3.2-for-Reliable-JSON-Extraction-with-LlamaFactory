# Prompt Engineering Ablation Study

This document details the attempts to fix the base model's formatting failures using prompt engineering alone (prior to fine-tuning).

## Prompt Iteration 1: Zero-Shot Direct

**The Prompt:**
Extract all fields from this invoice and return them as a JSON object.

**The Result:**
Failed. The model successfully identified the data but returned it wrapped in Markdown code blocks (` ```json ... ``` `), accompanied by conversational text ("Here is the extracted JSON data for the invoice you provided:"). This resulted in a 0% Parse Success Rate when passed directly to `json.loads()`.

## Prompt Iteration 2: Zero-Shot with Explicit Constraints

**The Prompt:**
Extract all fields from this invoice. You must return ONLY a valid JSON object. Do not include any explanations, preambles, or markdown formatting. Do not use code fences. Output raw JSON only.

**The Result:**
Marginal improvement. The model stopped generating conversational text, but still occasionally wrapped the output in markdown code fences. Furthermore, it began hallucinating schema keys (outputting `total_amount` instead of `total`) because the schema was not explicitly defined in the prompt.

## Prompt Iteration 3: One-Shot with Schema Definition

**The Prompt:**
```text
Extract the data from the provided invoice into a strict JSON object.
You must use exactly these keys: vendor, invoice_number, date, due_date, currency, subtotal, tax, total, line_items.
If a field is missing, output null.
Do NOT use markdown code blocks.

Example Input:
INVOICE #: 123
TOTAL: $50.00

Example Output:
{"vendor": null, "invoice_number": "123", "date": null, "due_date": null, "currency": "USD", "subtotal": null, "tax": null, "total": 50.0, "line_items": []}

Input to process: [RAW DOCUMENT TEXT]
```

**The Result:**
Significant improvement. Key hallucination stopped, and null handling improved drastically. However, the model still occasionally failed on complex, nested multi-item arrays or reverted to outputting markdown fences on highly complex documents. The parse success rate rose to ~40%, but fell far short of the deterministic reliability required for production, proving the necessity of the LoRA fine-tuning phase.
