import os
import json
import csv
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import glob
from tqdm import tqdm

def calculate_metrics(predicted_str, expected_json):
    is_valid = False
    predicted_json = {}
    
    # 1. Check if it's valid JSON
    try:
        predicted_json = json.loads(predicted_str)
        is_valid = True
    except json.JSONDecodeError:
        is_valid = False

    expected_keys = set(expected_json.keys())
    predicted_keys = set(predicted_json.keys()) if is_valid else set()
    
    # 2. Check missing keys
    has_keys = expected_keys.issubset(predicted_keys) if is_valid else False
    
    # 3. Key Accuracy
    if not expected_keys:
        key_acc = 0.0
    else:
        correct_keys = expected_keys.intersection(predicted_keys)
        key_acc = len(correct_keys) / len(expected_keys)
        
    # 4. Value Accuracy
    val_acc = 0.0
    if is_valid and expected_keys:
        correct_vals = 0
        for k in expected_keys:
            if k in predicted_json and predicted_json[k] == expected_json[k]:
                correct_vals += 1
        val_acc = correct_vals / len(expected_keys)
        
    # 5. Notes / failure modes
    notes = "Perfect"
    if not is_valid:
        if "```" in predicted_str:
            notes = "Markdown fences broke parser"
        elif not predicted_str.strip().startswith("{"):
            notes = "Conversational preamble broke parser"
        else:
            notes = "Invalid JSON structure (trailing comma or unescaped quotes)"
    elif not has_keys:
        notes = "Missing required keys or hallucinated wrong keys"
    elif val_acc < 1.0:
        notes = "Values do not perfectly match expected output (type mismatch or hallucination)"
        
    return is_valid, has_keys, key_acc, val_acc, notes


def evaluate_model(model, tokenizer, dataset, output_md, output_csv):
    responses_md = f"# Model Responses\n\n"
    csv_data = [["filename", "raw_output_first_50_chars", "is_valid_json", "has_all_required_keys", "key_accuracy", "value_accuracy", "notes"]]
    
    for i, record in enumerate(tqdm(dataset, desc="Evaluating")):
        instruction = record["instruction"]
        user_input = record["input"]
        expected = json.loads(record["expected_output"])
        
        # Llama 3 Prompt Format
        prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{instruction}\n{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.1, do_sample=False)
            
        # Extract only the generated response
        generated_tokens = outputs[0][inputs.input_ids.shape[1]:]
        predicted_str = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
        
        # Compute Metrics
        is_valid, has_keys, key_acc, val_acc, notes = calculate_metrics(predicted_str, expected)
        
        filename = f"held_out_{i+1:02d}.txt"
        responses_md += f"## Document: {filename}\n```text\n{predicted_str}\n```\n\n"
        
        csv_data.append([
            filename,
            predicted_str[:50].replace('\n', ' '),
            is_valid,
            has_keys,
            key_acc,
            val_acc,
            notes
        ])
        
    with open(output_md, "w", encoding="utf-8") as f:
        f.write(responses_md)
        
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)


def main():
    os.makedirs("eval", exist_ok=True)
    
    # 1. Load Dataset
    dataset = []
    with open("data/held_out_test.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            dataset.append(json.loads(line))
            
    # 2. Load Base Model
    print("Loading Base Llama 3.2 3B Model...")
    base_model_id = "meta-llama/Llama-3.2-3B"
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id, 
        device_map="auto", 
        torch_dtype=torch.bfloat16
    )
    
    # 3. Evaluate Base Model
    print("Evaluating Base Model (this will show the failures)...")
    evaluate_model(model, tokenizer, dataset, "eval/baseline_responses.md", "eval/baseline_scores.csv")
    
    # 4. Find LoRA Adapter
    adapter_dirs = glob.glob("saves/Llama-3.2-3B/lora/train_*")
    if not adapter_dirs:
        print("ERROR: Could not find any trained adapters in saves/Llama-3.2-3B/lora/train_*")
        return
    adapter_path = max(adapter_dirs, key=os.path.getctime)
    print(f"Found latest LoRA adapter: {adapter_path}")
    
    # 5. Load LoRA Adapter onto Base Model
    print("Injecting LoRA weights into Base Model...")
    model = PeftModel.from_pretrained(model, adapter_path)
    
    # 6. Evaluate Fine-Tuned Model
    print("Evaluating Fine-Tuned Model...")
    evaluate_model(model, tokenizer, dataset, "eval/finetuned_responses.md", "eval/finetuned_scores.csv")
    
    print("DONE! Real evaluation metrics have been generated and saved to the eval/ folder.")

if __name__ == "__main__":
    main()
