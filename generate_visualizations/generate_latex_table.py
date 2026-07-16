# generating_visualizations/generate_latex_table.py
import sys
import os
import pickle
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, matthews_corrcoef

# Add parent directory to path so we can import config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def compute_metrics(true_labels: list, pred_labels: list) -> list:
    if not true_labels or not pred_labels:
        return [0.0] * 4

    def binarize(label):
        if str(label).strip().lower() in ["1", "true", "yes", "positive"]:
            return 1
        return 0

    y_true = np.array([binarize(l) for l in true_labels])
    y_pred = np.array([binarize(l) for l in pred_labels])

    p = precision_score(y_true, y_pred, zero_division=0)
    r = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    mcc = matthews_corrcoef(y_true, y_pred)
    
    return [float(p), float(r), float(f1), float(mcc)]

# (LITEM_MANUAL_DATA - This step was necessary to compare the results with the sames obtained on the original UTD paper)
LITEM_MANUAL_DATA = {'antlr4': {'file': [0.39, 0.31, 0.34, 0.82, 0.27],
  'class': [0.43, 0.35, 0.38, 0.78, 0.29],
  'method': [0.28, 0.21, 0.23, 0.7, 0.21],
  'block': [0.04, 0.12, 0.06, 0.53, 0.03]},
 'dbeaver': {'file': [0.28, 0.24, 0.25, 0.77, 0.22],
  'class': [0.29, 0.32, 0.3, 0.77, 0.26],
  'method': [0.16, 0.26, 0.2, 0.65, 0.16],
  'block': [0.44, 0.12, 0.14, 0.63, 0.18]},
 'elasticsearch': {'file': [0.38, 0.36, 0.36, 0.8, 0.31],
  'class': [0.35, 0.33, 0.34, 0.73, 0.26],
  'method': [0.33, 0.23, 0.15, 0.7, 0.16],
  'block': [0.08, 0.31, 0.12, 0.62, 0.09]},
 'exoplayer': {'file': [0.5, 0.46, 0.47, 0.76, 0.36],
  'class': [0.44, 0.42, 0.43, 0.75, 0.32],
  'method': [0.87, 0.46, 0.6, 0.86, 0.62],
  'block': [0.66, 0.33, 0.44, 0.77, 0.46]},
 'fastjson': {'file': [0.5, 0.23, 0.29, 0.78, 0.3],
  'class': [0.35, 0.21, 0.24, 0.77, 0.23],
  'method': [0.8, 0.68, 0.71, 0.92, 0.7],
  'block': [0.86, 0.78, 0.81, 0.91, 0.81]},
 'flink': {'file': [0.27, 0.34, 0.3, 0.79, 0.25],
  'class': [0.28, 0.35, 0.31, 0.8, 0.27],
  'method': [0.19, 0.36, 0.17, 0.73, 0.18],
  'block': [0.51, 0.15, 0.14, 0.58, 0.19]},
 'guava': {'file': [0.66, 0.6, 0.63, 0.81, 0.48],
  'class': [0.62, 0.58, 0.59, 0.82, 0.48],
  'method': [0.57, 0.39, 0.42, 0.78, 0.4],
  'block': [0.92, 0.57, 0.7, 0.93, 0.7]},
 'jenkins': {'file': [0.64, 0.55, 0.59, 0.79, 0.44],
  'class': [0.56, 0.5, 0.53, 0.76, 0.37],
  'method': [0.31, 0.4, 0.35, 0.7, 0.24],
  'block': [0.15, 0.26, 0.18, 0.59, 0.11]},
 'libgdx': {'file': [0.41, 0.32, 0.34, 0.8, 0.32],
  'class': [0.35, 0.31, 0.32, 0.8, 0.28],
  'method': [0.83, 0.46, 0.59, 0.82, 0.61],
  'block': [0.82, 0.33, 0.44, 0.77, 0.49]},
 'logstash': {'file': [0.19, 0.1, 0.12, 0.66, 0.08],
  'class': [0.5, 0.27, 0.33, 0.69, 0.3],
  'method': [0.3, 0.18, 0.2, 0.71, 0.19],
  'block': [0.11, 0.32, 0.17, 0.69, 0.14]},
 'mockito': {'file': [0.37, 0.25, 0.29, 0.7, 0.23],
  'class': [0.32, 0.3, 0.31, 0.67, 0.21],
  'method': [0.39, 0.22, 0.27, 0.77, 0.25],
  'block': [0.2, 0.23, 0.14, 0.65, 0.14]},
 'openrefine': {'file': [0.45, 0.38, 0.4, 0.82, 0.34],
  'class': [0.49, 0.4, 0.44, 0.75, 0.31],
  'method': [0.54, 0.3, 0.36, 0.74, 0.34],
  'block': [0.33, 0.32, 0.31, 0.77, 0.26]},
 'presto': {'file': [0.35, 0.33, 0.34, 0.75, 0.29],
  'class': [0.38, 0.31, 0.34, 0.66, 0.21],
  'method': [0.23, 0.32, 0.27, 0.7, 0.18],
  'block': [0.12, 0.38, 0.18, 0.67, 0.13]},
 'quarkus': {'file': [0.42, 0.39, 0.4, 0.77, 0.33],
  'class': [0.45, 0.39, 0.41, 0.77, 0.35],
  'method': [0.22, 0.4, 0.29, 0.73, 0.24],
  'block': [0.22, 0.3, 0.2, 0.64, 0.16]},
 'questdb': {'file': [0.32, 0.23, 0.23, 0.8, 0.23],
  'class': [0.42, 0.25, 0.28, 0.69, 0.26],
  'method': [0.52, 0.22, 0.29, 0.76, 0.31],
  'block': [0.47, 0.28, 0.29, 0.7, 0.31]},
 'redisson': {'file': [0.58, 0.42, 0.47, 0.89, 0.47],
  'class': [0.57, 0.33, 0.35, 0.87, 0.39],
  'method': [0.66, 0.66, 0.64, 0.97, 0.64],
  'block': [0.92, 0.78, 0.83, 0.9, 0.82]},
 'rxjava': {'file': [0.59, 0.49, 0.51, 0.88, 0.5],
  'class': [0.59, 0.44, 0.48, 0.89, 0.47],
  'method': [0.87, 0.63, 0.72, 0.94, 0.73],
  'block': [0.73, 0.45, 0.53, 0.87, 0.55]},
 'tink': {'file': [0.73, 0.7, 0.71, 0.85, 0.64],
  'class': [0.74, 0.66, 0.69, 0.87, 0.63],
  'method': [0.75, 0.58, 0.64, 0.88, 0.63],
  'block': [0.16, 0.31, 0.2, 0.64, 0.2]},
#  'average': {'file': [0.45, 0.37, 0.39, 0.79, 0.34],
#   'class': [0.45, 0.37, 0.39, 0.77, 0.33],
#   'method': [0.49, 0.39, 0.39, 0.78, 0.38],
#   'block': [0.43, 0.35, 0.33, 0.71, 0.32]}
} 

# Remove AUC metric
for project in LITEM_MANUAL_DATA.keys():
    for granularity in LITEM_MANUAL_DATA[project].keys():
        if len(LITEM_MANUAL_DATA[project][granularity]) == 5:
            LITEM_MANUAL_DATA[project][granularity].pop(3)

def generate_latex_table(data_granite, model_name="Qwen2.5-7B-Instruct"):
    granularities = config.GRANULARITIES
    techniques = [model_name, "LiteM"]
    
    projects = sorted(list(data_granite["block"].keys())) if data_granite["block"] else sorted(list(LITEM_MANUAL_DATA.keys()))
    metrics_data = {proj: {tech: {} for tech in techniques} for proj in projects}
    
    for proj in projects:
        for gran in granularities:
            proj_gran_data = data_granite.get(gran, {}).get(proj, {})
            true_labels = [proj_gran_data[idx]["true_label"] for idx in sorted(proj_gran_data.keys())]
            pred_labels = [proj_gran_data[idx]["predicted_label"] for idx in sorted(proj_gran_data.keys())]
            metrics_data[proj][model_name][gran] = compute_metrics(true_labels, pred_labels)
            metrics_data[proj]["LiteM"][gran] = LITEM_MANUAL_DATA.get(proj, {}).get(gran, [0.0] * 4)
                
    averages = {tech: {gran: [0.0] * 4 for gran in granularities} for tech in techniques}
    for tech in techniques:
        for gran in granularities:
            project_metrics = [metrics_data[proj][tech][gran] for proj in projects]
            if project_metrics:
                averages[tech][gran] = np.mean(project_metrics, axis=0).tolist()

    def format_val(val, max_val):
        val_str = f"{val:.2f}"
        if abs(val - max_val) < 1e-9:
            return f"\\textbf{{{val_str}}}"
        return val_str

        # 3. Construct Table Lines
    latex_lines = []
    latex_lines.append(r"\begin{table*}[t]")
    latex_lines.append(r"\centering")
    latex_lines.append(r"\caption{Comprehensive evaluation results comparing Qwen2.5-7B-Instruct and LiteM across four distinct code granularities (File, Class, Method, and Block) on four subject projects. Performance is measured using Precision (P), Recall (R) and Matthews Correlation Coefficient (MCC). The highest values for each metric within a project and granularity are highlighted in bold.}")
    latex_lines.append(r"\label{tab:evaluation_results}")
    latex_lines.append(r"\resizebox{\textwidth}{!}{% Resize table to fit within text width if necessary")
    latex_lines.append(r"\begin{tabular}{ll" + "|cccc" * (len(granularities)) + "}")
    latex_lines.append(r"\toprule")
    
    # Header Row 1
    header1 = r"\multirow{2}{*}{Project} & \multirow{2}{*}{Technique}"
    for gran in granularities:
        header1 += f" & \\multicolumn{{4}}{{c}}{{{gran.capitalize()}}}"
    header1 += r" \\"
    latex_lines.append(header1)
    
    # Midrules for each granularity group
    midrules = r"\cmidrule(lr){3-6} \cmidrule(lr){7-10} \cmidrule(lr){11-14} \cmidrule(lr){15-18}"
    latex_lines.append(midrules)
    
    # Header Row 2
    header2 = r" & & " + " & ".join(["P & R & F1 & MCC"] * len(granularities)) + r" \\"
    latex_lines.append(header2)
    latex_lines.append(r"\midrule")
    
    # Populate project rows
    for proj in projects:
        for tech_name in techniques:
            row_str = ""
            # Checks if it's the first model in the list dynamically
            if tech_name == model_name:
                row_str += f"\\multirow{{2}}{{*}}{{{proj}}}"
            else:
                row_str += " "
                
            row_str += f" & {tech_name}"
            
            for gran in granularities:
                vals = metrics_data[proj][tech_name][gran]
                # Dynamic toggle for finding the counterpart model's data
                other_tech = "LiteM" if tech_name == model_name else model_name
                other_vals = metrics_data[proj][other_tech][gran]
                
                for m_idx in range(4):
                    max_val = max(vals[m_idx], other_vals[m_idx])
                    row_str += f" & {format_val(vals[m_idx], max_val)}"
            
            row_str += r" \\"
            latex_lines.append(row_str)
            
        if proj != projects[-1]:
            latex_lines.append(r"\hline")
        
    # Populate Summary Average Rows at the bottom
    # Populate Summary Average Rows at the bottom
    latex_lines.append(r"\midrule")
    for tech_name in techniques:
        row_str = ""

        # Color both cells, but put the multirow text on the LAST row with a negative index
        if tech_name == model_name:
            row_str += r"\cellcolor{gray!15}"
        else:
            row_str += r"\cellcolor{gray!15}\multirow{-2}{*}{Average}"

        row_str += f" & \\cellcolor{{gray!15}} {tech_name}"

        for gran in granularities:
            vals = averages[tech_name][gran]
            other_tech = "LiteM" if tech_name == model_name else model_name
            other_vals = averages[other_tech][gran]

            for m_idx in range(4):
                max_val = max(vals[m_idx], other_vals[m_idx])
                row_str += f" & \\cellcolor{{gray!15}} {format_val(vals[m_idx], max_val)}"

        row_str += r" \\"
        latex_lines.append(row_str)
        
    latex_lines.append(r"\bottomrule")
    latex_lines.append(r"\end{tabular}")
    latex_lines.append(r"}")
    latex_lines.append(r"\end{table*}")

    return "\n".join(latex_lines)

if __name__ == "__main__":
    # Load pickle using config path
    try:
        with open(config.RESULTS_CHECKPOINT_PKL, "rb") as file:
            data = pickle.load(file)
    except FileNotFoundError:
        print(f"Warning: Checkpoint not found at {config.RESULTS_CHECKPOINT_PKL}. Running with empty data.")
        data = {g: {} for g in config.GRANULARITIES}

    # (Data cleaning code remains exactly the same as before)
    ...

    latex_table = generate_latex_table(data)
    
    # Save output using config path
    with open(config.RESULTS_LATEX_TXT, "w", encoding="utf-8") as f:
        f.write(latex_table)
        
    print(f"LaTeX Table successfully saved to {config.RESULTS_LATEX_TXT}")