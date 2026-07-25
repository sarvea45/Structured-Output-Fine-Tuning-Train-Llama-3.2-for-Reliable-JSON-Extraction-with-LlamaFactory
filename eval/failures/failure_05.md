# Failure Analysis: Document 19

## Root Cause Analysis
- **What went wrong:** The `quantity` field output the raw string `"10 boxes"` instead of the required numerical float or integer.
- **Why it likely failed:** Our Python data generator strictly populated the `QTY` text in the raw input as pure integers (e.g. `QTY: 10`). We did not include any examples with Units of Measure (UOM) attached to the quantity in the raw text. Because the model never saw UOMs in training, it didn't learn the behavior to strip the text to cast it to a strict integer.
- **Specific Data Change to Fix It:** Add 5 to 10 training examples where line items include string-based units (`10 boxes`, `5 hrs`, `2 pallets`) in the raw text, but ensure the `quantity` field in the expected output JSON is strictly mapped to the numerical value (`10`, `5`, `2`).
