# Structured Output Fine-Tuning (Llama 3.2)

## Project Overview
This repository contains the complete data engineering, fine-tuning configuration, and evaluation pipeline for training a Llama 3.2 (3B) model to reliably extract strict JSON payloads from unstructured business documents (Invoices and Purchase Orders).

The goal of this project was to transition a general-purpose, chatty LLM into a deterministic data extraction engine using **Parameter-Efficient Fine-Tuning (LoRA)** via the **LlamaFactory** framework.

## Methodology

### 1. Schema Design
Strict JSON schemas were defined for both Invoices and Purchase Orders (`schema/`). Crucially, we enforced rigorous null-handling rules: absent optional fields must output a discrete `null` rather than omitting the key or utilizing empty strings.

### 2. Data Curation
We curated 80 highly diverse training examples (`data/curated_train.jsonl`) mimicking OCR output. The curation prioritized format diversity and explicitly targeted edge cases (missing fields, foreign currencies, multi-item arrays) to prevent model overfitting and hallucination. An audit trail of curation decisions is available in `data/curation_log.md`.

### 3. Fine-Tuning 
The model was fine-tuned using LoRA. Hyperparameters were strictly justified to avoid catastrophic forgetting and overfitting given the small dataset size (Rank 16, Alpha 32, 3 Epochs). See `training_config.md` for full details.

### 4. Evaluation & Failure Analysis
The model was evaluated against a held-out set of 20 documents before and after fine-tuning. 
- **Baseline Parse Success Rate:** 0% (Failed due to markdown fences and hallucinations).
- **Post-Tuning Parse Success Rate:** 75% (Massive improvement in strict schema adherence).

A deep dive into the 5 remaining failure cases (`eval/failures/`) proved that all post-tuning errors were rooted in data representation issues (e.g., missing UOM string examples in the training set), validating the axiom that fine-tuning is fundamentally a data engineering problem.

## Repository Structure
- `schema/`: JSON constraint documentation.
- `data/`: Curated JSONL dataset and audit logs.
- `eval/`: Baseline and post-tuning scoring matrices, responses, and failure analysis.
- `prompts/`: A comparative study on Prompt Engineering vs Fine-Tuning.
- `screenshots/`: LlamaFactory configuration and loss curves.
- `training_config.md`: Hyperparameter justifications.
- `report.md`: Final analytical report on extraction methodologies.
