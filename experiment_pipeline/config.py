# config.py
from pathlib import Path

DATA_FOLDER_PATH = Path("./data")
CHECK_POINT_FOLDER_PATH = Path("./checkpoints")
GRANULARITIES = ["file", "class", "method", "block"] 

LABEL_COLUMN_NAME = "CommentsAssociatedLabel"
CHECK_POINTS_THRESHOLD = 100

# The direct link to your experiment dataset archive
DATASET_URL = "https://github.com/HduDBSI/Dataset4TD/releases/download/v2/code.snippets-with-labels.metrics.7z"