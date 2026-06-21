# config.py
from pathlib import Path

# The direct link to your experiment dataset archive
DATASET_URL = "https://github.com/HduDBSI/Dataset4TD/releases/download/v2/code.snippets-with-labels.metrics.7z"

# Data configuration
DATA_FOLDER_PATH = Path("./data")
GRANULARITIES = ["file", "class", "method", "block"] 
# define how many projects you want to evaluate
PROJECT_LIMIT = None
LABEL_COLUMN_NAME = "CommentsAssociatedLabel"

# Checkpoint configuration
CHECKPOINT_FOLDER_PATH = Path("./checkpoints")
CHECKPOINTS_THRESHOLD = 100

# API and Model configurations
BASE_URL = "http://localhost:8084/v1/"

MODEL_TEMPERATURE = 0.0
MODEL_MAX_NEW_TOKENS = 2