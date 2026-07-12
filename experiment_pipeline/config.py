# config.py

from pathlib import Path

# The direct link to your experiment dataset archive
DATASET_URL = "https://github.com/HduDBSI/Dataset4TD/releases/download/v2/code.snippets-with-labels.metrics.7z"

# Data configuration
DATA_FOLDER_PATH = Path("./data")
GRANULARITIES = ["file", "class", "method", "block"] 

# define how many projects you want to evaluate
# The original paper's dataset contains 18 projects
PROJECT_LIMIT = 18
LABEL_COLUMN_NAME = "CommentsAssociatedLabel"

# Checkpoint configuration
CHECKPOINT_FOLDER_PATH = Path("./checkpoints")
CHECKPOINTS_THRESHOLD = 1000

# API configurations
BASE_URL = "http://localhost:8084/v1/"
MODEL_NAME = "/home/multiarq/.cache/instructlab/models/ibm-granite/granite-3.1-8b-instruct"
API_KEY="token-if-needed"

# How many requests the server can handle simultaneously
MAX_CONCURRENT_REQUESTS = 25

# Model configurations
MODEL_TEMPERATURE = 0.0
MODEL_MAX_NEW_TOKENS = 2