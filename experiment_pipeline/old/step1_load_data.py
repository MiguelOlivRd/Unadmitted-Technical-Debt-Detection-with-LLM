# step1_load_data.py

from pathlib import Path
import pandas as pd
from tqdm.notebook import tqdm
from .config import GRANULARITIES, DATA_FOLDER_PATH

def load_code_snippets() -> dict:
       
    code_snippets = {}
    # Iterates over the directory and prints only files
    for granularity in tqdm(GRANULARITIES):
        folder_path = f"{DATA_FOLDER_PATH}/{granularity}"
        path = Path(folder_path)
        projects_file_names = [f.name for f in path.iterdir() if f.is_file()]

        code_snippets[granularity] = {}
        for project_file_name in projects_file_names:
            project_name = project_file_name.split("-")[0]
            
            code_snippets[granularity][project_name] = pd.read_csv(f"{folder_path}/{project_file_name}")

    return code_snippets