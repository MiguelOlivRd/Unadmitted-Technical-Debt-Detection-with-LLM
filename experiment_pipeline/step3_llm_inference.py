# step3_llm_inference.py
import pickle
import datetime
from openai import OpenAI
from tqdm import tqdm
from config import GRANULARITIES, LABEL_COLUMN_NAME, CHECKPOINT_FOLDER_PATH, CHECKPOINTS_THRESHOLD, MODEL_TEMPERATURE, MODEL_MAX_NEW_TOKENS, BASE_URL
from prompt import generate_prompt

# Initialize local OpenAI client
client = OpenAI(base_url=BASE_URL, api_key="token-if-needed")
MODEL = "~/.cache/instructlab/models/ibm-granite/granite-3.1-8b-instruct"

def predict(prompt: str) -> str:
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt}
            # {"role": "system", "content": "You are a precise code analysis assistant. Respond strictly with 'yes' or 'no'."},
            # {"role": "user", "content": prompt}
        ],
        max_tokens=MODEL_MAX_NEW_TOKENS,
        temperature=MODEL_TEMPERATURE
    )
    return completion.choices[0].message.content.strip()

# TODO: we need a way to verify errors and try to retry executing them.
def load_checkpoint() -> dict:
    """Safely loads previous global results to resume progress."""
    CHECKPOINT_FOLDER_PATH.mkdir(exist_ok=True)
    last_ckpt = CHECKPOINT_FOLDER_PATH / "last_checkpoint.pkl"
    if last_ckpt.exists():
        try:
            with open(last_ckpt, "rb") as f:
                print("Resuming from last saved checkpoint...")
                return pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            print("Checkpoint corrupted. Starting clean.")
    return {}

def save_checkpoint(results: dict):
    """Saves complete experiment state to avoid structural corruption."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # with open(CHECKPOINT_FOLDER_PATH / f"checkpoint_{timestamp}.pkl", "wb") as f:
    #     pickle.dump(results, f)
    with open(CHECKPOINT_FOLDER_PATH / "last_checkpoint.pkl", "wb") as f:
        pickle.dump(results, f)

def run_inference(code_snippets: dict, project_names: list):
    """Iterates through datasets, processes LLM predictions, and checkpoints results."""
    results = load_checkpoint()
    session_error_count = 0
    error_ocurred_flag = False

    for granularity in tqdm(GRANULARITIES, desc="Granularities completed"):
        results.setdefault(granularity, {})
        
        for project_name in tqdm(project_names, desc=f"Projects ({granularity})", leave=False):
            results[granularity].setdefault(project_name, {})
            df = code_snippets[granularity][project_name]

            for row in tqdm(df.itertuples(), total=len(df), desc=f"Rows ({project_name})", leave=False):
                index = row.Index
                
                # Resuming logic: Skip only if status is recorded as clear success
                if index in results[granularity][project_name]:
                    if results[granularity][project_name][index].get("status") == "success":
                        continue

                # Use the newly cleaned code if it exists, otherwise fall back to raw content
                code_snippet = getattr(row, "Content")
                code_snippet_without_comments = getattr(row, "code_without_comments")
                true_label = getattr(row, LABEL_COLUMN_NAME)
                prompt = generate_prompt(code_snippet_without_comments)

                try:
                    predicted_label = predict(prompt)
                    status = "success"
                except Exception as e:
                    session_error_count += 1
                    error_ocurred_flag = True
                    predicted_label = f"API_ERROR: {type(e).__name__}"
                    status = "failed"

                results[granularity][project_name][index] = {
                    "code_snippet": code_snippet,
                    "code_snippet_without_comments": code_snippet_without_comments,
                    "prompt": prompt,
                    "true_label": true_label,
                    "predicted_label": predicted_label,
                    "status": status
                }

                # Save globally every N items processed within the current dataframe
                if index > 0 and index % CHECKPOINTS_THRESHOLD == 0:
                    save_checkpoint(results)

                # FIX: Use tqdm.write instead of print with \r
                if error_ocurred_flag:
                    tqdm.write(f"Session errors: {session_error_count}")
                    error_ocurred_flag = False
                
    # Final save upon completing the whole experiment script loop
    save_checkpoint(results)
    print("\nExperiment finished successfully!")
    return results