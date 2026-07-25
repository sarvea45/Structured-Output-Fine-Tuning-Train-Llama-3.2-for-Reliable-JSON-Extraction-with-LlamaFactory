# Prompt Engineering Iterations

This document tracks the iterative prompt engineering process used to fix the base Llama 3.2 model's formatting issues on the 3 hardest baseline documents.

## Iteration 1: Zero-Shot Naive
**Prompt:**
```text
Extract the fields from the following invoice into JSON:
[DOCUMENT TEXT]
```
**Hypothesis:** The base model might just work if asked simply.
**Result:** Failed. Model output markdown fences (```json) and added a conversational preamble ("Here is the JSON data you requested:"). The JSON parser failed immediately.

## Iteration 2: Zero-Shot Strict Constraints
**Prompt:**
```text
You are a strict data extraction bot. Extract the invoice fields into JSON.
CRITICAL RULES:
1. Return ONLY valid JSON.
2. DO NOT use markdown code fences (```json).
3. DO NOT include any explanations or conversational text.
[DOCUMENT TEXT]
```
**Hypothesis:** Adding explicit negative constraints will force the model to drop the markdown and preamble.
**Result:** Failed. The model ignored the negative constraint about markdown fences in 2 out of 3 cases. Negative constraints are notoriously difficult for smaller base models to follow, as they tend to focus on the tokens mentioned (like "markdown").

## Iteration 3: One-Shot with Schema Definition
**Prompt:**
```text
Extract data from the document into a strict JSON object. 
Do not use markdown. Return only the raw JSON.

Output Schema:
{
  "vendor": string,
  "subtotal": float,
  "total": float
}

Example Input:
Vendor: Acme Corp. Sub: 100. Total: 100.
Example Output:
{
  "vendor": "Acme Corp",
  "subtotal": 100.0,
  "total": 100.0
}

Actual Input:
[DOCUMENT TEXT]
Actual Output:
```
**Hypothesis:** Providing an explicit schema and a one-shot example showing the exact desired format (without markdown fences) will force the model's pattern matching to continue the pattern correctly.
**Result:** Success on 2 out of 3 documents. The one-shot example successfully suppressed the markdown fences. However, on the most complex document, the model still hallucinated an extra key not defined in the schema.
