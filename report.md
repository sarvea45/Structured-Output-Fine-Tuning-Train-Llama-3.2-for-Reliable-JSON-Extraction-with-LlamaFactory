# Prompting vs. Fine-Tuning Analysis

This analysis evaluates under what conditions prompt engineering outperforms fine-tuning, and vice versa, in the context of structured data extraction in production systems.

## When Prompt Engineering Wins
Prompting wins for rapid prototyping, when your data schema changes frequently, or when you lack the resources to manually curate a perfectly clean dataset. Setting up a prompt is instantaneous. If the business suddenly requires a new `tax_ID` field on invoices, updating a prompt takes seconds. Updating a fine-tuned model requires curating dozens of new examples containing `tax_ID` and running a completely new LoRA training job. Furthermore, for highly capable, expensive frontier models, few-shot prompting often achieves near-perfect parsing without any fine-tuning overhead, making it the ideal choice for low-volume, high-variance tasks.

## When Fine-Tuning Wins
Fine-Tuning wins for rigid, unchanging schemas where absolute consistency is required and latency/cost are critical factors. It guarantees a much higher Parse Success Rate on smaller, faster, open-weights models (like Llama 3.2 3B). 

Fine-tuning structurally forces the model to learn that returning anything other than JSON is mathematically incorrect. It completely eliminates Markdown artifacts, prevents conversational preambles, and forces the model to respect edge cases (like mapping missing fields to `null`) perfectly if the data is curated well. 

Crucially, fine-tuning saves money and reduces latency at inference time. You do not have to send massive, token-heavy few-shot instruction prompts containing schema definitions every single time you query the model. You simply pass the raw document text and let the adapter weights handle the formatting implicitly. 

## Conclusion
If the schema is fluid and you are exploring, use prompting. If the schema is locked and you are building a high-volume, reliable, automated production pipeline with an open-source model, fine-tuning on a highly-curated JSONL dataset is unequivocally the superior engineering approach.
