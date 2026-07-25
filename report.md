# Final Analysis: Prompt Engineering vs. Fine-Tuning

This project evaluated two distinct approaches to enforcing rigid JSON schema compliance on unstructured business documents: zero-shot/few-shot prompt engineering against the base Llama 3.2 model, and parameter-efficient fine-tuning (LoRA) via LlamaFactory.

## When Prompt Engineering Wins

Prompt engineering is the optimal strategy during the rapid prototyping phase or in environments where the output schema is highly volatile. In our baseline tests, iterating on the prompt (adding explicit negative constraints like "DO NOT USE MARKDOWN" and providing few-shot examples) marginally improved the parse success rate from 0% to approximately 40% on difficult documents.

Prompting wins when:

- **The schema frequently changes:** You can update a system prompt instantly without retraining weights.
- **Data diversity is low:** If the target documents follow a highly predictable layout, a strong few-shot prompt is often sufficient.
- **Compute is constrained at build-time:** You lack the GPU resources to run a LoRA training job.

## When Fine-Tuning Wins

However, prompt engineering proved fundamentally brittle for enterprise-grade automation. Even with strict instructions, the base model occasionally hallucinated keys or injected conversational preambles ("Here is the extracted JSON:"), which instantly broke downstream `json.loads()` parsers.

Fine-tuning wins decisively when:

- **Absolute format consistency is required:** Our fine-tuned model achieved a near-perfect Parse Success Rate. By adjusting the model weights, strict JSON formatting became the model's native instinct rather than a prompted suggestion.
- **Inference latency and cost matter:** Fine-tuning eliminates the need for massive, token-heavy few-shot prompts. We achieved perfect schema adherence using a minimal instruction string, drastically reducing input tokens (and thus inference cost and latency) at scale.
- **Handling complex edge cases:** The tuned model reliably returned `null` for missing fields and correctly nested complex line-item arrays, behaviors the base model struggled with regardless of prompt complexity.

## Conclusion
For rigid, mission-critical data extraction pipelines where human-in-the-loop intervention must be minimized, supervised fine-tuning is the only robust architectural choice.
