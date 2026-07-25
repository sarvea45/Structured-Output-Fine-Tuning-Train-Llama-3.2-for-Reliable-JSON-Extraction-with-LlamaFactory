# Failure Analysis: Document 11

## Root Cause Analysis
- **What went wrong:** The model output the total as a string (`"500.00"`) instead of a numerical float (`500.0`), and it completely failed to extract the line items array.
- **Why it likely failed:** The GBP currency symbol (`£`) is relatively rare in the dataset (only 2-3 examples exist in the 80 documents). The base model has a deep tendency to wrap numbers with unfamiliar currency prefixes into strings. The LoRA fine-tuning adapter wasn't strong enough on this specific edge case to override the base model's behavior for GBP.
- **Specific Data Change to Fix It:** We need to increase the representation of foreign currencies (GBP, EUR, JPY) in the dataset from 5 combined examples up to at least 15 examples, ensuring the output for `total` and `unit_price` is always strictly mapped to a float to reinforce the typing.
