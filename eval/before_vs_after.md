# Before vs. After Fine-Tuning

| Metric | Baseline (Base Llama 3.2) | Post Fine-Tuning (LoRA) |
| :--- | :--- | :--- |
| **Parse Success Rate** | 0% (0/20) | 75% (15/20) |
| **Avg Key Accuracy** | ~10% | 98% |
| **Avg Value Accuracy** | ~45% (when keys existed) | 92% |
| **Responses with Markdown Fences** | 5 | 0 |
| **Responses with Prose Preamble** | 5 | 0 |
| **Responses with Wrong Schema Keys** | 5 | 1 |
