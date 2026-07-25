# Failure Analysis: Document 04

## Root Cause Analysis
- **What went wrong:** The fine-tuned model output an invalid schema. It hallucinated an extra key (`"tax_rate": 0.1`) that is not present in our strict invoice schema.
- **Why it likely failed:** The source document explicitly states `TAX RATE: 10%`. While the model correctly calculated the `tax` field as 5000.0, it also tried to preserve the tax rate data by inventing a new key. Our dataset primarily handles tax as an absolute amount (e.g. `TAX: $5.00`). We did not train the model on documents that feature a standalone percentage rate where it must explicitly ignore that rate in the JSON output.
- **Specific Data Change to Fix It:** Add 3-5 more training examples to `curated_train.jsonl` where the raw input contains a `TAX RATE: X%` line, but the expected JSON output completely drops it (only keeping the absolute `tax` value). This will explicitly teach the model that it must drop unmapped schema fields.
