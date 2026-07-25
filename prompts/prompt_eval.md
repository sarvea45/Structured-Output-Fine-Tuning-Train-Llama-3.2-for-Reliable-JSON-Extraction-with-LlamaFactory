# Prompt Engineering Evaluation

This evaluates the success of Iteration 3 (One-Shot with Schema) on the 3 worst-performing baseline documents compared to the fine-tuned model.

| Document | Iteration 3 Prompt Result | Fine-Tuned Model Result | Winner |
| :--- | :--- | :--- | :--- |
| **held_out_02** | Valid JSON. Markdown successfully suppressed by one-shot example. | Perfect JSON. | Tie |
| **held_out_06** | Valid JSON. Markdown successfully suppressed. | Perfect JSON. | Tie |
| **held_out_14** | Invalid JSON. Hallucinated keys outside of the provided schema definition. | Perfect JSON. | **Fine-Tuned** |

### Parse Success Rate on Hardest 3 Docs:
- **Base Model (Prompt Iteration 3):** 66% (2/3)
- **Fine-Tuned Model (Zero-Shot):** 100% (3/3)

### Conclusion
While heavy prompt engineering (one-shot examples and strict negative constraints) vastly improved the base model's performance, it still failed on the most complex layout by hallucinating unrequested schema keys. The fine-tuned model achieved 100% success on these hard documents with a simple zero-shot prompt, proving it is far more reliable for strict schema adherence on edge cases.
