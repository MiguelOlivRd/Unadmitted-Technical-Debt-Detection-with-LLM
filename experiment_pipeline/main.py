# main.py
from step0_download_data import ensure_data_is_ready
from step1_load_data import load_code_snippets, get_project_names
from step2_remove_comments import clean_comments_pipeline
from step3_llm_inference import run_inference
from config import PROJECT_LIMIT
import json

def main():
    print("=== Phase 0: Verifying Data Source ===")
    # This checks if files exist, downloads the .7z file if missing, and extracts it
    ensure_data_is_ready()
    print("\n")

    print("=== Phase 1: Loading Code Snippets ===")
    snippets = load_code_snippets()
    project_names = get_project_names(snippets)
    print(f"Discovered {len(project_names)} projects: {project_names}\n")

    print("=== Phase 2: Removing Code Comments ===")
    cleaned_snippets = clean_comments_pipeline(snippets, project_names[0:PROJECT_LIMIT])
    print("Comments processed and stripped successfully.\n")

    print("=== Phase 3: Executing LLM Inference ===")
    final_results = run_inference(cleaned_snippets, project_names[0:PROJECT_LIMIT])

    # === Phase 4: Saving the Results ===
    print("=== Phase 4: Saving Final Results ===")
    output_filename = "./llm_inference_results.json"
    
    # Option A: Save as JSON (Best for nested structures/text generation)
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=4, ensure_ascii=False)
    
    print(f"Success! Results saved to {output_filename}")


if __name__ == "__main__":
    main()