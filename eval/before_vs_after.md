# Before vs. After Fine-Tuning (Authentic GPU Evaluation)

This report details the exact performance jump achieved by applying the trained LoRA adapter to the Llama 3.2 3B base model, evaluated across 20 unseen, highly unstructured test documents on an NVIDIA T4 GPU.

| Metric | Baseline (Base Llama 3.2) | Post Fine-Tuning (LoRA) |
| :--- | :--- | :--- |
| **Parse Success Rate** | 0% (0/20) | **100% (20/20)** |
| **Avg Key Accuracy** | 0.0% | **64.0%** |
| **Avg Value Accuracy** | 0.0% | **51.7%** |
| **Responses with Markdown Fences** | 20 | **0** |
| **Responses with Prose Preamble** | 20 | **0** |

## Analysis
The fine-tuning was an overwhelming success in terms of structural compliance. The Base model completely failed to output parseable JSON (0% success rate), primarily due to conversational preambles ("Here is the extracted data:") and Markdown code blocks (````json ... ````). 

After injecting the LoRA weights, the Parse Success Rate jumped to **100%**. The model completely unlearned its conversational tendencies and strictly emitted raw JSON objects, perfectly ready for `json.loads()`. While the value accuracy (51.7%) reflects the limitations of a 3B parameter model handling complex, zero-shot entity extraction without a larger dataset, the absolute structural reliability achieved the primary goal of the pipeline.
