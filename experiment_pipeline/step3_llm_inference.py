# step3_llm_inference.py
import pickle
import datetime
from openai import OpenAI
from tqdm import tqdm
from config import GRANULARITIES, LABEL_COLUMN_NAME, CHECK_POINT_FOLDER_PATH, CHECK_POINTS_THRESHOLD

# Initialize local OpenAI client
client = OpenAI(base_url="http://localhost:8084/v1/", api_key="token-if-needed")
MODEL_PATH = "/home/multiarq/.cache/instructlab/models/ibm-granite/granite-3.1-8b-instruct"

def generate_prompt(code_snippet: str) -> str:
    return (
        f"Given the following code snippet, tell \"yes\" if it contains a Technical Debt "
        f"or \"no\" if it does not contain a Technical Debt.\n"
        f"You only can answer \"yes\" or \"no\". Do not provide any explanation.\n\n"
        f"Here is the code snippet:\n\"\"\"\n{code_snippet}\n\"\"\""
    )

def predict(prompt: str) -> str:
    completion = client.chat.completions.create(
        model=MODEL_PATH,
        messages=[
            {"role": "system", "content": "You are a precise code analysis assistant. Respond strictly with 'yes' or 'no'."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2,
        temperature=0.0
    )
    return completion.choices[0].message.content.strip()

def load_checkpoint() -> dict:
    """Safely loads previous global results to resume progress."""
    CHECK_POINT_FOLDER_PATH.mkdir(exist_ok=True)
    last_ckpt = CHECK_POINT_FOLDER_PATH / "last_checkpoint.pkl"
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
    
    with open(CHECK_POINT_FOLDER_PATH / f"checkpoint_{timestamp}.pkl", "wb") as f:
        pickle.dump(results, f)
    with open(CHECK_POINT_FOLDER_PATH / "last_checkpoint.pkl", "wb") as f:
        pickle.dump(results, f)

def run_inference(code_snippets: dict, project_names: list):
    """Iterates through datasets, processes LLM predictions, and checkpoints results."""
    results = load_checkpoint()
    session_error_count = 0

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
                code_snippet = getattr(row, "code_without_comments", getattr(row, "Content"))
                true_label = getattr(row, LABEL_COLUMN_NAME)
                prompt = generate_prompt(code_snippet)

                try:
                    predicted_label = predict(prompt)
                    status = "success"
                except Exception as e:
                    session_error_count += 1
                    predicted_label = f"API_ERROR: {type(e).__name__}"
                    status = "failed"

                results[granularity][project_name][index] = {
                    "code_snippet": code_snippet,
                    "prompt": prompt,
                    "true_label": true_label,
                    "predicted_label": predicted_label,
                    "status": status
                }

                # Save globally every N items processed within the current dataframe
                if index > 0 and index % CHECK_POINTS_THRESHOLD == 0:
                    save_checkpoint(results)
                    
                print(f"Session errors: {session_error_count}\r", end="")
                
    # Final save upon completing the whole experiment script loop
    save_checkpoint(results)
    print("\nExperiment finished successfully!")
    return results