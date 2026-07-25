# Failure Analysis: Document 15

## Root Cause Analysis
- **What went wrong:** The model output the string `"ASAP"` for the `delivery_date` field. This violates the schema constraint that dates must be formatted as `YYYY-MM-DD` or be `null`.
- **Why it likely failed:** Our Python curation script for missing dates purely excluded the `EXPECTED DELIVERY` line entirely when simulating missing dates (resulting in `null`). We did not train the model on documents where the delivery date field is actually present in the text, but contains non-date conversational text (like "TBD", "ASAP", or "Next Week"). Therefore, the model naively copied the string instead of coercing it to `null`.
- **Specific Data Change to Fix It:** Add 5 training examples to `curated_train.jsonl` where `EXPECTED DELIVERY` exists but has informal text (e.g., `TBD` or `ASAP`), and map the expected JSON output `delivery_date` strictly to `null`.
