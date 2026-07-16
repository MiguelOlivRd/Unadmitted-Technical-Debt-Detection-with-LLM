# config.py
import os

# Base directory of the project (absolute path of this config file's parent folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data file paths
# For default, we use the last checkpoint as the results.
# On our drive, there is a .pkl file with the results from our experiment execution.
RESULTS_CHECKPOINT_PKL = os.path.join(BASE_DIR, "../experiment_pipeline/checkpoints/last_checkpoint.pkl")
RESULTS_LATEX_TXT = os.path.join(BASE_DIR, "latex_results_table.txt")

# results (used by the F1 CI script as input)
RESULTS_TXT = RESULTS_LATEX_TXT

# Example of other files
# RESULTS_TXT = os.path.join(BASE_DIR, "latex_results_table.txt")

# Output visualization path
F1_CI_PLOT_PNG = os.path.join(BASE_DIR, "f1_ci_comparison.png")

# Metric Configurations
GRANULARITIES = ["file", "class", "method", "block"]
TARGET_METRICS = ["File_F1", "Class_F1", "Method_F1", "Block_F1"]