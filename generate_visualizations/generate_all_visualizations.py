# generate_all_visualizations.py
import os
import subprocess
import sys
import config

def run_script(script_path):
    """Runs a python script as a subprocess and returns True if successful."""
    print(f"\n>>> Running: {script_path}...")
    try:
        # Run using the same python interpreter executing this orchestrator
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=False  # Allows prints from the scripts to show in real-time
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error: Script {script_path} failed with exit code {e.returncode}.")
        return False
    except Exception as e:
        print(f"Error: Failed to execute {script_path}. Reason: {e}")
        return False

def main():
    print("==================================================")
    print("   Starting All Visualizations Generation Pipeline  ")
    print("==================================================")

    # Resolve paths to the individual scripts inside the subdirectory
    latex_script = os.path.join(config.BASE_DIR, "generate_latex_table.py")
    ci_script = os.path.join(config.BASE_DIR, "generate_f1_ci_plot.py")

    # Step 1: Generate the LaTeX table
    latex_success = run_script(latex_script)
    if latex_success:
        print("Latex table successfully created.")
    else:
        print("\n[!]The latex table wasn't generated. Aborting...")
        print(f"Verify if the config files are correct: \n  - checkpoint: {config.RESULTS_CHECKPOINT_PKL}")
        return

    # Step 2: Validate that the required LaTeX output table exists
    table_exists = os.path.exists(config.RESULTS_LATEX_TXT)

    if not latex_success or not table_exists:
        print("\n[!] Execution stopped.")
        print(f"Reason: The LaTeX results table file was not generated at: {config.RESULTS_LATEX_TXT}")
        print("We cannot calculate confidence intervals without this base table.")
        sys.exit(1)

    print(f"\n[✓] LaTeX table successfully verified at: {config.RESULTS_LATEX_TXT}")

    # Step 3: Generate the F1 Score Confidence Interval Plot
    # Note: Ensure config.py or generate_f1_ci_plot.py is set to read config.RESULTS_LATEX_TXT
    ci_success = run_script(ci_script)

    if ci_success:
        print("\n==================================================")
        print("   [SUCCESS] Pipeline completed flawlessly!       ")
        print(f"   - Table: {config.RESULTS_LATEX_TXT}")
        print(f"   - Plot:  {config.F1_CI_PLOT_PNG}")
        print("==================================================")
    else:
        print("\n[!] LaTeX table was generated, but the F1 Confidence Interval script failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()