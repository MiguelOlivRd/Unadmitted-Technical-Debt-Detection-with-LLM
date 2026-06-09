# utils.py
from pathlib import Path
from config import DATA_FOLDER_PATH, GRANULARITIES

def get_project_names_by_granularity() -> dict:
    """Discovers project names across granularities and validates consistency."""
    project_names_by_granularity = {}
    
    for granularity in GRANULARITIES:
        folder_path = DATA_FOLDER_PATH / granularity
        if not folder_path.exists():
            raise FileNotFoundError(f"Data directory missing: {folder_path}")
            
        file_names = [f.name for f in folder_path.iterdir() if f.is_file() and f.suffix == '.csv']
        
        # Extract project name (everything before the first '-')
        project_names = sorted(list({name.split("-")[0] for name in file_names}))
        project_names_by_granularity[granularity] = project_names
        
    # Assert structural integrity across granularities
    base_granularity = GRANULARITIES[0]
    base_projects = project_names_by_granularity[base_granularity]
    
    for granularity in GRANULARITIES[1:]:
        assert project_names_by_granularity[granularity] == base_projects, \
            f"Mismatched projects between {base_granularity} and {granularity}"
            
    return base_projects