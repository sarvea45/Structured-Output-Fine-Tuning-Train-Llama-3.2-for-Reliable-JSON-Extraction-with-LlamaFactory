import os
import json
import csv
import sys

def print_status(message, passed):
    """Prints a formatted status message."""
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"{status} | {message}")

def validate_project():
    print("\n--- Starting Project Structure & Data Validation ---\n")
    all_passed = True

    required_dirs = [
        "schema", "data", "eval", "eval/failures", "prompts", "screenshots"
    ]
    print("Checking Directories:")
    for d in required_dirs:
        exists = os.path.isdir(d)
        print_status(f"Directory '{d}' exists", exists)
        if not exists: all_passed = False

    print("\nChecking Required Files:")
    required_files = [
        "README.md", "report.md", "training_config.md", ".gitignore",
        "schema/invoice_schema.md", "schema/po_schema.md",
        "data/curation_log.md", "data/curated_train.jsonl",
        "eval/baseline_responses.md", "eval/baseline_scores.csv", "eval/summary.md",
        "eval/finetuned_responses.md", "eval/finetuned_scores.csv", "eval/before_vs_after.md",
        "prompts/prompt_iterations.md", "prompts/prompt_eval.md"
    ]
    for f in required_files:
        exists = os.path.isfile(f)
        print_status(f"File '{f}' exists", exists)
        if not exists: all_passed = False

    print("\nChecking Data Engine (curated_train.jsonl):")
    jsonl_path = "data/curated_train.jsonl"
    if os.path.isfile(jsonl_path):
        try:
            with open(jsonl_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Check exact count
            is_80_lines = len(lines) == 80
            print_status(f"Contains exactly 80 examples (Found: {len(lines)})", is_80_lines)
            if not is_80_lines: all_passed = False

            # Check JSON structure and required keys
            valid_json = True
            keys_present = True
            for i, line in enumerate(lines):
                try:
                    obj = json.loads(line)
                    if not all(k in obj for k in ["instruction", "input", "output"]):
                        keys_present = False
                except json.JSONDecodeError:
                    valid_json = False
                    print(f"   -> JSON Error on line {i+1}")
                    break
            
            print_status("All lines are valid JSON objects", valid_json)
            print_status("All lines contain 'instruction', 'input', 'output' keys", keys_present)
            if not (valid_json and keys_present): all_passed = False

        except Exception as e:
            print_status(f"Could not read JSONL file: {e}", False)
            all_passed = False
    else:
        print_status("JSONL file missing, skipping data validation.", False)
        all_passed = False

    print("\nChecking Evaluation CSV Schemas:")
    csv_files = ["eval/baseline_scores.csv", "eval/finetuned_scores.csv"]
    expected_headers = ["filename", "raw_output_first_50_chars", "is_valid_json", "has_all_required_keys", "key_accuracy", "value_accuracy", "notes"]
    
    for csv_file in csv_files:
        if os.path.isfile(csv_file):
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    headers = next(reader, [])
                    # Check if expected headers are a subset of actual headers (to allow flexibility)
                    has_headers = all(h in headers for h in expected_headers)
                    print_status(f"{csv_file} has correct headers", has_headers)
                    if not has_headers: all_passed = False
            except Exception:
                print_status(f"Error reading {csv_file}", False)
                all_passed = False

    print("\n========================================")
    if all_passed:
        print("🎉 ALL CORE REQUIREMENTS PASSED! Your repository is structurally perfect.")
    else:
        print("⚠️ SOME REQUIREMENTS FAILED. Please fix the missing files or data errors above.")
    print("========================================\n")

if __name__ == "__main__":
    validate_project()
