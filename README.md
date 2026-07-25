# Structured Output Fine-Tuning with Llama 3.2

This repository contains the complete MLOps pipeline for fine-tuning the open-weights Llama 3.2 model to act as a highly reliable, deterministic JSON extraction engine for business documents (Invoices and Purchase Orders).

## Project Objective

General-purpose LLMs struggle with format consistency, frequently breaking downstream automated pipelines by wrapping JSON in Markdown, hallucinating keys, or injecting conversational text. This project solves that reliability problem via Supervised Fine-Tuning (SFT).

By fine-tuning Llama 3.2 on a carefully curated dataset, the model's native behavior is altered to output strict, machine-parseable JSON that perfectly adheres to a pre-defined schema, maximizing the Parse Success Rate.

## Methodology

- **Schema Design (`schema/`):** Defined rigid JSON schemas for Invoices and POs, establishing strict typing and rules for handling missing data (using `null`).
- **Data Curation (`data/`):** Synthesized 80 high-variance JSONL training examples featuring complex edge cases (missing fields, nested arrays, foreign currencies).
- **Baseline Evaluation (`eval/`):** Established the base model's Parse Success Rate using programmatic Python validation (`json.loads()`).
- **LoRA Fine-Tuning:** Utilized LlamaFactory to inject small, trainable adapter matrices (Rank 16, Alpha 32), modifying the model weights without catastrophic forgetting.
- **Ablation & Analysis (`eval/failures/`, `report.md`):** Measured the exact ROI of fine-tuning versus advanced prompt engineering.

## Repository Structure

- `schema/`: The binding JSON schemas used for training and evaluation.
- `data/`: The 80-example JSONL training set and manual review audit log.
- `eval/`: Baseline and post-tuning scoring matrices, plus root-cause failure analysis.
- `prompts/`: Documentation of the prompt engineering ablation study.
- `training_config.md`: Theoretical justification for LoRA hyperparameters.
- `report.md`: Final analytical comparison of Prompting vs. Fine-Tuning.

## Execution Requirements

This project was orchestrated entirely via the LlamaFactory Gradio Web UI. No custom PyTorch training scripts were utilized, ensuring the engineering focus remained entirely on data quality, schema enforcement, and rigorous evaluation.
