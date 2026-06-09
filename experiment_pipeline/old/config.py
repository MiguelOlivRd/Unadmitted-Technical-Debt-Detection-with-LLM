# config.py

# Hand defined variables
DATA_FOLDER_PATH = "./data"

GRANULARITIES = ["file", "class", "method", "block"] 


# Dynamically defined variables
from pathlib import Path

def _get_project_names():
    project_names_by_granularity = {}
    for granularity in GRANULARITIES:
        folder_path = f"{DATA_FOLDER_PATH}/{granularity}"
        path = Path(folder_path)
        projects_file_names = [f.name for f in path.iterdir() if f.is_file()]

        projects_names = []
        for project_file_name in projects_file_names:
            project_name = project_file_name.split("-")[0]
            projects_names.append(project_name)
        
        project_names_by_granularity[granularity] = projects_names
        
    # assert that all the granularities have the same projects:
    base_granularity = "file"
    for granularity in GRANULARITIES[1:]:
        assert project_names_by_granularity[base_granularity] == project_names_by_granularity[granularity]

    return projects_names

PROJECTS_NAMES = 
