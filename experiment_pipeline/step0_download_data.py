# step0_download_data.py
import urllib.request
from pathlib import Path
import py7zr  # Extra requirement needed for .7z files
from config import DATA_FOLDER_PATH, GRANULARITIES, DATASET_URL

def check_data_exists() -> bool:
    """Checks if the data directories are populated with files."""
    if not DATA_FOLDER_PATH.exists():
        return False
        
    for granularity in GRANULARITIES:
        granularity_path = DATA_FOLDER_PATH / granularity
        if not granularity_path.exists():
            return False
            
        # Ensure there is at least one data file in each subdirectory
        files = list(granularity_path.glob("*"))
        if not files:
            return False
            
    return True

def download_and_extract_data():
    """Downloads the 7z dataset from GitHub and decompresses it."""
    print("Dataset missing or incomplete. Initializing download...")
    
    DATA_FOLDER_PATH.mkdir(parents=True, exist_ok=True)
    archive_path = DATA_FOLDER_PATH / "dataset.7z"
    
    try:
        # 1. Download file
        print(f"Downloading archive from GitHub Releases...")
        urllib.request.urlretrieve(DATASET_URL, archive_path)
        print("Download successful!")
        
        # 2. Extract .7z archive
        print("Extracting 7z archive contents (this may take a minute)...")
        with py7zr.SevenZipFile(archive_path, mode='r') as archive:
            archive.extractall(path=DATA_FOLDER_PATH)
            
        # 3. Clean up archive file
        archive_path.unlink()
        print("Dataset extracted and cleaned up successfully!")
        
    except Exception as e:
        print(f"\n[!] Failed to pull or extract dataset: {e}")
        print("Please download it manually and place the extracted folders under your data directory.")
        raise SystemExit(1)

def ensure_data_is_ready():
    """Orchestrator function called by main.py."""
    print("Evaluating dataset footprint...")
    if check_data_exists():
        print("Dataset integrity verified! All granularities are present.")
    else:
        download_and_extract_data()

if __name__ == "__main__":
    ensure_data_is_ready()