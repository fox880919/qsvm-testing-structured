"""
Generate Statistical Testing pie chart for progress report.
Adapted from mutation_testing_sept/create_testing_efficiency.py.
Output: mutant_detection_coverage_pie_chart.png
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

FILE_INPUT = "saved_data/my_data_frame_Jan_all.csv"
OUTPUT_DIR = "progress report/figures"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "mutant_detection_coverage_pie_chart.png")
TOTAL_MUTANTS_COUNT = 30


def generate_pie_chart():
    if not os.path.exists(FILE_INPUT):
        print(f"Error: '{FILE_INPUT}' not found. Run Statistical Testing first.")
        return False
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df_long = pd.read_csv(FILE_INPUT)
    df_long['type_of_mutant'] = df_long['type_of_mutant'].astype(str).str.strip().str.lower()
    df_long = df_long[df_long['Applied_MR'].astype(str).str.strip() != '-']

    df_results = df_long.groupby(['mutant_#', 'Applied_MR'])['type_of_mutant'].agg(
        lambda x: x.mode()[0] if not x.mode().empty else np.nan
    ).reset_index(name='Outcome')
    df_results['Is_Killed'] = (df_results['Outcome'] == 'killed')

    mutants_killed_at_least_once = df_results.groupby('mutant_#')['Is_Killed'].max()
    killed_count = int(mutants_killed_at_least_once.sum())
    percentage_killed = (killed_count / TOTAL_MUTANTS_COUNT) * 100
    percentage_not_killed = 100 - percentage_killed

    data = {'Status': ['Killed at Least Once', 'Not Killed'], 'Percentage': [percentage_killed, percentage_not_killed]}
    df_pie = pd.DataFrame(data)

    plt.figure(figsize=(8, 8))
    colors = ['#2ca02c', '#d62728']
    wedges, texts, autotexts = plt.pie(
        df_pie['Percentage'], labels=df_pie['Status'], autopct='%1.1f%%',
        startangle=90, colors=colors, wedgeprops={'edgecolor': 'black', 'linewidth': 1}
    )
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
    plt.title(f'Test Suite Detection Coverage (Total Mutants: {TOTAL_MUTANTS_COUNT})', fontsize=14)
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE)
    plt.close()
    print(f"Saved: {OUTPUT_FILE}")
    print(f"Mutants Killed: {killed_count}/{TOTAL_MUTANTS_COUNT} ({percentage_killed:.2f}%)")
    return True


if __name__ == "__main__":
    generate_pie_chart()
