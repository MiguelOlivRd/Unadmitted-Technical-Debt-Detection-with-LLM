import re
import numpy as np
import pandas as pd


def parse_evaluation_table(file_path):
    """Reads the evaluation LaTeX table from a file and parses it into a clean Pandas DataFrame."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # CRITICAL FIX: Strip invisible non-breaking spaces (\xa0) and normalize carriage returns
    content = content.replace("\xa0", " ").replace("\r\n", "\n")

    # Find the table data between \midrule and \bottomrule using a raw regex string
    table_body_match = re.search(
        r"\\midrule(.*?)\\bottomrule", content, re.DOTALL
    )
    if not table_body_match:
        raise ValueError(
            "Could not find table body between \\midrule and \\bottomrule. "
            "Please check if the file contains these exact LaTeX commands."
        )

    table_body = table_body_match.group(1)

    # Clean up LaTeX styling tags
    def clean_cell(text):
        text = text.strip()
        # Remove bold formatting: \textbf{...}
        text = re.sub(r"\\textbf\{([^}]+)\}", r"\1", text)
        # Remove cell colors: \cellcolor{...} or \cellcolor{...!num}
        text = re.sub(r"\\cellcolor\{[^}]+\}", "", text)
        # Remove multirow wrappers: \multirow{...}{...}{text}
        text = re.sub(r"\\multirow\{[^}]+\}\{[^}]+\}", "", text)
        # Strip remaining braces and whitespace
        text = text.replace("{", "").replace("}", "").strip()
        return text

    parsed_rows = []
    current_project = None

    # Expected metric layout: 4 granularities * 5 metrics = 20 metric values
    granularities = ["File", "Class", "Method", "Block"]
    metrics_names = ["P", "R", "F1", "AUC", "MCC"]
    columns = [f"{g}_{m}" for g in granularities for m in metrics_names]

    for line in table_body.split("\n"):
        line = line.strip()

        # Skip LaTeX formatting structure lines
        if (
            not line
            or line.startswith("%")
            or line.startswith("\\hline")
            or line.startswith("\\cmidrule")
        ):
            continue

        if "&" in line:
            # Strip off trailing LaTeX line breaks (\\)
            line_clean = re.sub(r"\\\\.*$", "", line)
            cells = [clean_cell(c) for c in line_clean.split("&")]

            # Filter out "Average" rows
            if any("average" in cell.lower() for cell in cells):
                continue

            # Ensure we have the Project, Technique, and at least some metrics
            if len(cells) >= 22:
                project = cells[0]
                technique = cells[1]

                # Handle multirow project propagation
                if project == "":
                    project = current_project
                else:
                    current_project = project

                # Parse the 20 metric columns
                metrics = []
                for val in cells[2:22]:
                    try:
                        metrics.append(float(val))
                    except ValueError:
                        metrics.append(np.nan)

                # Store row details
                row_dict = {"Project": project, "Technique": technique}
                for col_name, val in zip(columns, metrics):
                    row_dict[col_name] = val
                parsed_rows.append(row_dict)

    df = pd.DataFrame(parsed_rows)
    return df[0:-1]