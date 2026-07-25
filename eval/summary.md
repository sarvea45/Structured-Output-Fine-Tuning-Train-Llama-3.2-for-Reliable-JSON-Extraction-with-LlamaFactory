# Baseline Evaluation Summary

## Parse Success Rate
**0.0% (0 / 20)**

### Analysis
The base Llama 3.2 model completely failed to achieve a parseable success rate. The primary failure modes were:
1. Wrapping JSON in markdown code blocks.
2. Conversational preamble ('Here is the extracted data...').
3. Hallucinating different key names than requested.
4. Emitting trailing commas which break `json.loads()`.
