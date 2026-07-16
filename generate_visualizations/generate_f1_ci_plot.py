# generating_visualizations/generate_f1_ci_plot.py
import sys
import os
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Add parent directory to path so we can import config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

try:
    from utils import parse_evaluation_table
except ImportError:
    print("Warning: 'utils' module not found. Ensure utils.py is accessible.")
    def parse_evaluation_table(path):
        raise FileNotFoundError("Could not import parse_evaluation_table.")

def calculate_confidence_intervals(df, metric_col, confidence=0.95):
    results = []
    grouped = df.groupby("Technique")
    for tech_name, group in grouped:
        data = group[metric_col].dropna().values
        n = len(data)
        if n < 2:
            continue
        mean = np.mean(data)
        sem = stats.sem(data)
        h = sem * stats.t.ppf((1 + confidence) / 2.0, n - 1)
        results.append({
            "Technique": tech_name,
            "Sample Size (N)": n,
            "Mean": round(mean, 2),
            "95% CI Lower": round(mean - h, 2),
            "95% CI Upper": round(mean + h, 2),
            "Margin of Error": round(h, 2),
        })
    return pd.DataFrame(results)

def main():
    # Use config path for results file
    if not os.path.exists(config.RESULTS_TXT):
        print(f"Error: Results file not found at: {config.RESULTS_TXT}")
        return

    print(f"Parsing evaluation table from: {config.RESULTS_TXT}...")
    df = parse_evaluation_table(config.RESULTS_TXT)

    plot_data = []
    for target_metric in config.TARGET_METRICS:
        ci_summary = calculate_confidence_intervals(df, target_metric)
        granularity = target_metric.split('_')[0]
        
        for idx, row in ci_summary.iterrows():
            mean_val = row['Mean']
            lower_val = row['95% CI Lower']
            upper_val = row['95% CI Upper']
            plot_data.append({
                "Granularity": granularity,
                "Technique": row['Technique'],
                "Mean": mean_val,
                "Error_Minus": mean_val - lower_val,
                "Error_Plus": upper_val - mean_val
            })

    ci_plot_df = pd.DataFrame(plot_data)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))

    techniques = list(ci_plot_df["Technique"].unique())
    if len(techniques) > 1:
        techniques = techniques[1:] + [techniques[0]]

    granularities = [m.split('_')[0] for m in config.TARGET_METRICS]
    x_coords = np.arange(len(granularities))
    width = 0.18

    colors = ["#1f77b4", "#e65c00", "#b30000", "#cca300"]
    markers = ["o", "s", "^", "D"]

    for i, tech in enumerate(techniques):
        tech_data = ci_plot_df[ci_plot_df["Technique"] == tech]
        means = [tech_data[tech_data["Granularity"] == g]["Mean"].values[0] for g in granularities]
        err_low = [tech_data[tech_data["Granularity"] == g]["Error_Minus"].values[0] for g in granularities]
        err_high = [tech_data[tech_data["Granularity"] == g]["Error_Plus"].values[0] for g in granularities]
        y_errors = [err_low, err_high]
        
        pos = x_coords + (i - len(techniques)/2 + 0.5) * width
        ax.errorbar(pos, means, yerr=y_errors, fmt=markers[i % len(markers)], 
                    color=colors[i % len(colors)], capsize=6, capthick=1.5, 
                    elinewidth=1.8, ms=8, label=tech)

    ax.set_xticks(x_coords)
    ax.set_xticklabels(granularities, fontsize=12, fontweight='bold')
    ax.set_ylabel("F1-Score Mean & 95% CI", fontsize=12, fontweight='bold')
    ax.set_xlabel("Code Granularity", fontsize=12, fontweight='bold')
    ax.set_title("95% Confidence Intervals for F1-Score Across Granularities", fontsize=14, fontweight='bold', pad=15)
    ax.legend(title="Technique", fontsize=11, title_fontsize=12, frameon=True, shadow=True)

    plt.tight_layout()
    
    # Save output plot using config path
    plt.savefig(config.F1_CI_PLOT_PNG, dpi=300)
    print(f"Visualization successfully saved to: {config.F1_CI_PLOT_PNG}")

if __name__ == "__main__":
    main()