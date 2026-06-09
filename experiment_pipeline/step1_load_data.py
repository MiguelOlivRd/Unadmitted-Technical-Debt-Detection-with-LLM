# step1_load_data.py
import pandas as pd
from tqdm import tqdm
from config import DATA_FOLDER_PATH, GRANULARITIES

def get_project_names(code_snippets: dict) -> list:
    """Helper to extract project names from the loaded keys."""
    return list(code_snippets[GRANULARITIES[0]].keys())

def load_code_snippets() -> dict:
    """Loads all CSV datasets into a nested dictionary structure."""
    code_snippets = {}
    
    for granularity in tqdm(GRANULARITIES, desc="Loading granularities"):
        folder_path = DATA_FOLDER_PATH / granularity
        if not folder_path.exists():
            raise FileNotFoundError(f"Missing directory: {folder_path}")
            
        project_files = [f for f in folder_path.iterdir() if f.is_file() and f.suffix == '.csv']
        code_snippets[granularity] = {}
        
        for file_path in project_files:
            project_name = file_path.name.split("-")[0]
            code_snippets[granularity][project_name] = pd.read_csv(file_path)
            
    return code_snippets