# main.py
from step0_download_data import ensure_data_is_ready
from step1_load_data import load_code_snippets, get_project_names
from step2_remove_comments import clean_comments_pipeline
from step3_llm_inference import run_inference

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
    cleaned_snippets = clean_comments_pipeline(snippets, project_names)
    print("Comments processed and stripped successfully.\n")

    print("=== Phase 3: Executing LLM Inference ===")
    final_results = run_inference(cleaned_snippets, project_names)

if __name__ == "__main__":
    main()