# Evaluating an LLM Approach in Unadmitted Technical Debt Detection

This repository contains the replication code, pipeline, and analysis for evaluating a Large Language Model (Qwen2.5-7B-Instruct) against the metric-based approach proposed by Yu et al. (2025) for detecting Unadmitted Technical Debt (UTD). This project was developed for the course **"Reproducibility in Computer Science Research"** at UFCG.

---

## Paper & Publications

* **Original Paper:** *Unadmitted Technical Debt: Dataset and Detection Approaches* (IEEE TSE, Dec 2025)
  * **Authors:** Dongjin Yu, Yihang Xu, Xin Chen, Quanxin Yang, and Sixuan Wang
  * [IEEE Link](https://ieeexplore.ieee.org/document/11208161)
* **Our Final Paper:** The PDF containing our comparative evaluation and statistical analysis can be found at:  
  `./paper/Evaluating A Large Language Model Approach in Unadmitted Technical Debt Detection.pdf`

---

## Repository Structure (main files)

```text
.
├── experiment_pipeline/            # Pipeline to execute the replication experiment
│   ├── config.py                   # API and execution configurations
│   └── main.py                     # Main execution script (runs steps sequentially)
├── generate_visualizations/        # Scripts to analyze results and generate assets
│   ├── f1_ci_comparison.png        # Output 95% CI F1-Score plot
│   └── generate_all_visualizations.py # Runs both plotting and LaTeX table generation
├── paper/                          # Contains our final compiled paper PDF
└── requirements.txt                # Python package dependencies
```

## Setup & Installation

* **Prerequisites:** To execute the replication pipeline, you need access to an LLM inference API (e.g., vLLM, OpenAI-compatible endpoint, or Hugging Face TGI).
* **Environment Setup:** We recommend creating a Python virtual environment:
```{bash}
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```
## How to Configure & Run
* **1. Configuration:** 
    1. Open experiment_pipeline/config.py and set your API keys, base URL, model name, and preferred concurrency limits.

    2. Open generate_visualizations/config.py to customize output paths for the LaTeX table and the F1-Score confidence interval plot.

* **2. Execute the Pipeline:**
You can execute the entire data collection, cleaning, and inference pipeline by running:

```{bash}
cd experiment_pipeline
python main.py
```

**Note: The LLM inference step runs asynchronously. You can configure the max_concurrent_requests in config.py to balance speed and API rate limits.**

* **3. Generate Visualizations & LaTeX Tables:**
Once your experiment runs complete, generate the paper's LaTeX summary tables and the 95% Confidence Interval plot using:

```{bash}
cd ../generate_visualizations
python generate_all_visualizations.py
```

The generated LaTeX table code will be saved in generate_visualizations/latex_results_table.txt.

The 95% Confidence Interval plot will be updated at generate_visualizations/f1_ci_comparison.png.