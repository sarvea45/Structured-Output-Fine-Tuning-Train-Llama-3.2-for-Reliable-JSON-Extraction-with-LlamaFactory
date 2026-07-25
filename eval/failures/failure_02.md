# Failure Analysis: Document 08

## Root Cause Analysis
- **What went wrong:** The model hallucinated the string `"Unknown"` for the `vendor` field instead of properly returning `null`, and it completely dropped the line item array, returning `[]`.
- **Why it likely failed:** Our curation log shows that we explicitly enforced missing fields for `due_date`, `tax`, and `delivery_date`. However, *every single invoice in our 80-document training dataset had a valid vendor name*. Because of this, the model learned that `vendor` is a mandatory string and tried to aggressively impute one from thin air when the receipt header was missing a company name.
- **Specific Data Change to Fix It:** Add 5 examples to the `curated_train.jsonl` dataset of generic, "nameless" receipts where the `vendor` field in the expected JSON output is explicitly mapped to `null`. This teaches the model that primary identifiers can also be null.
