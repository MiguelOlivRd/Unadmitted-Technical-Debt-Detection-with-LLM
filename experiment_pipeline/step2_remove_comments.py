# step2_remove_comments.py
import pandas as pd
from tqdm import tqdm
from config import GRANULARITIES
import re

def verify_and_get_comment_columns(code_snippets: dict, project_names: list) -> list:
    """Verifies all granularities share identical comment columns and returns them."""
    # Establish a baseline using the first project
    first_df = code_snippets[GRANULARITIES[0]][project_names[0]]
    baseline_cols = [
        col for col in first_df.columns 
        if "comment" in col.lower() and "each" not in col.lower()
    ]
    
    for granularity in GRANULARITIES:
        for project in project_names:
            df = code_snippets[granularity][project]
            current_cols = [
                col for col in df.columns 
                if "comment" in col.lower() and "each" not in col.lower()
            ]
            assert current_cols == baseline_cols, \
                f"Mismatch in {granularity}/{project}. Expected {baseline_cols}, got {current_cols}"
                
    print("Verification complete: Comment columns match across all granularities.")
    return baseline_cols

def remove_comments(code: str, comments_row: pd.Series) -> str:
    """Removes found comments from a single code snippet string."""
    if not isinstance(code, str):
        return ""
        
    for comments in comments_row:
        if isinstance(comments, str) and comments.strip() != "":
            comments_list = comments.split("[[SEP]]")
            for comment in comments_list:
                for line in comment.split("\n"):
                    code = code.replace(line.strip(), "", 1)

    # Fix: Replace 3 or more consecutive newlines with just 2 newlines
    code = re.sub(r'\n\s{1,}\n', '\n', code)

    code = code.replace("@Deprecated", "")
    code = code.replace("@deprecated", "")

    return code

def clean_comments_pipeline(code_snippets: dict, project_names: list) -> dict:
    """Applies comment stripping across the entire dataset structure."""
    comment_cols = verify_and_get_comment_columns(code_snippets, project_names)
    
    for granularity in tqdm(GRANULARITIES, desc="Removing comments"):
        for project_name in project_names:
            df = code_snippets[granularity][project_name]
            
            # Use axis=1 to evaluate rows dynamically
            df["code_without_comments"] = df.apply(
                lambda row: remove_comments(row["Content"], row[comment_cols]), 
                axis=1
            )
            
    return code_snippets