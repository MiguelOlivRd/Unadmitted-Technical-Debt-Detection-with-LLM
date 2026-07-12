# step3_llm_inference.py

import asyncio
import pickle
from openai import AsyncOpenAI  # Changed to Async client
from tqdm.asyncio import tqdm   # Async-compatible tqdm
from prompt import generate_prompt


from config import GRANULARITIES, LABEL_COLUMN_NAME, CHECKPOINT_FOLDER_PATH,\
     CHECKPOINTS_THRESHOLD, MODEL_TEMPERATURE, MODEL_MAX_NEW_TOKENS, BASE_URL, \
     MODEL_NAME, MAX_CONCURRENT_REQUESTS


# Initialize local Async OpenAI client
client = AsyncOpenAI(base_url=BASE_URL, api_key="token-if-needed")


async def predict(prompt: str, semaphore: asyncio.Semaphore) -> str:
    """Wrapped with a semaphore to control concurrency."""
    async with semaphore:
        try:
            completion = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "system", "content": prompt}],
                max_tokens=MODEL_MAX_NEW_TOKENS,
                temperature=MODEL_TEMPERATURE
            )
            return completion.choices[0].message.content.strip(), "success"
        except Exception as e:
            return f"API_ERROR: {type(e).__name__}", "failed"

def load_checkpoint() -> dict:
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
    with open(CHECKPOINT_FOLDER_PATH / "last_checkpoint.pkl", "wb") as f:
        pickle.dump(results, f)

async def run_inference_async(code_snippets: dict, project_names: list):
    results = load_checkpoint()
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    
    # 1. Flatten tasks so we can process them concurrently
    tasks_to_run = []
    
    for granularity in GRANULARITIES:
        results.setdefault(granularity, {})
        for project_name in project_names:
            results[granularity].setdefault(project_name, {})
            df = code_snippets[granularity][project_name]

            for row in df.itertuples():
                index = row.Index
                
                # Skip if already successfully completed
                if index in results[granularity][project_name]:
                    if results[granularity][project_name][index].get("status") == "success":
                        continue

                code_snippet = getattr(row, "Content")
                code_snippet_without_comments = getattr(row, "code_without_comments")
                true_label = getattr(row, LABEL_COLUMN_NAME)
                prompt = generate_prompt(code_snippet_without_comments)

                # Store metadata and the coroutine task
                tasks_to_run.append({
                    "granularity": granularity,
                    "project_name": project_name,
                    "index": index,
                    # "code_snippet": code_snippet,
                    # "code_snippet_without_comments": code_snippet_without_comments,
                    "true_label": true_label,
                    "prompt": prompt,
                    "coro": predict(prompt, semaphore)
                })

    if not tasks_to_run:
        print("All tasks already completed!")
        return results

    print(f"Starting inference for {len(tasks_to_run)} items...")
    session_error_count = 0
    
    # 1. Map coroutines back to their original metadata dictionaries so we know who is who when they finish
    # We pass a tuple of (task_meta, coro) into a wrapper task
    async def wrapped_predict(task_meta):
        predicted_label, status = await task_meta["coro"]
        return task_meta, predicted_label, status

    wrapped_tasks = [wrapped_predict(t) for t in tasks_to_run]

    # 2. Process tasks as they complete (keeps checkpointing and progress bar alive)
    for i, future in enumerate(tqdm(asyncio.as_completed(wrapped_tasks), total=len(wrapped_tasks), desc="Processing prompts")):
        task_meta, predicted_label, status = await future
        
        if status == "failed":
            session_error_count += 1
            tqdm.write(f"Session errors: {session_error_count} | Error: {predicted_label}")

        # Save back into our results dict
        g, p, idx = task_meta["granularity"], task_meta["project_name"], task_meta["index"]
        results[g][p][idx] = {
            "prompt": task_meta["prompt"],
            "true_label": task_meta["true_label"],
            "predicted_label": predicted_label,
            "status": status
        }

        # Checkpoint every N items (Works perfectly now!)
        if i > 0 and i % CHECKPOINTS_THRESHOLD == 0:
            save_checkpoint(results)

    # Final save
    save_checkpoint(results)
    print(f"\nExperiment finished! Total session errors: {session_error_count}")
    return results