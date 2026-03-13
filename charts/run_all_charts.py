"""
Run all chart generation scripts to produce progress report figures.
Run after Statistical Testing and/or Kernel Testing complete.

Usage:
    python -m charts.run_all_charts
    # or
    cd qsvm_structure_testing && python charts/run_all_charts.py
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)


def main():
    from charts.create_chart_mutant_heatmap import generate_mutant_heatmap
    from charts.create_chart_pie import generate_pie_chart
    from charts.create_chart_v41_2_ordered import generate_v41_plots

    print("Generating progress report charts...")
    ok1 = generate_mutant_heatmap()
    ok2 = generate_pie_chart()
    ok3 = generate_v41_plots()
    print("\nDone.")
    if ok1 and ok2:
        print("Statistical Testing charts: heatmap + pie chart")
    if ok3:
        print("Kernel Testing charts: detection + heatmap")
    if not (ok1 or ok2 or ok3):
        print("No charts generated. Run Statistical Testing and/or Kernel Testing first.")


if __name__ == "__main__":
    main()
