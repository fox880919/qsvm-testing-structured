"""
Generate Kernel Testing charts for progress report.
Adapted from mutation_testing_feb/create_chart41_2.py.
Output: chart_v41_heatmap_omni_2.png, chart_v41_detection_omni_2.png
"""

import os
import sys

# Run from project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

FILE_INPUT = "results_v41_kernel_test.csv"
OUTPUT_DIR = "progress report/figures2"
FILE_CHART_RATE = os.path.join(OUTPUT_DIR, "chart_v41_detection_omni_2.png")
FILE_CHART_HEATMAP = os.path.join(OUTPUT_DIR, "chart_v41_heatmap_omni_2.png")

mr_mapping = {
    "Efficient_MR_1_Rate": "MR1: Symmetry",
    "Efficient_MR_2_Rate": "MR2: Identity",
    "Efficient_MR_3_Rate": "MR3: Negation Inv.",
    "Efficient_MR_4_Rate": "MR4: Shift Inv.",
    "Efficient_MR_5_Rate": "MR5: Periodicity",
    "Efficient_MR_6_Rate": "MR6: Feature Rot.",
    "Efficient_MR_7_Rate": "MR7: Permutation Inv.",
    "Efficient_MR_8_Rate": "MR8: Bit Inversion",
    "Efficient_MR_9_Rate": "MR9: Noise Stability",
    "Efficient_MR_10_Rate": "MR10: Feat. Sensitivity",
    "Efficient_MR_11_Rate": "MR11: Linear Scaling",
    "Efficient_MR_12_Rate": "MR12: Structural Ortho",
    "Efficient_MR_13_Rate": "MR13: Dual Consistency",
    "Efficient_MR_14_Rate": "MR14: Qubit Permutation",
}

ORDERED_MR_KEYS = [
    "Efficient_MR_1_Rate", "Efficient_MR_2_Rate", "Efficient_MR_7_Rate",
    "Efficient_MR_12_Rate", "Efficient_MR_14_Rate", "Efficient_MR_9_Rate",
    "Efficient_MR_5_Rate", "Efficient_MR_4_Rate", "Efficient_MR_8_Rate",
    "Efficient_MR_11_Rate",
    "Efficient_MR_3_Rate", "Efficient_MR_6_Rate", "Efficient_MR_10_Rate", "Efficient_MR_13_Rate",
]


def generate_v41_plots():
    if not os.path.exists(FILE_INPUT):
        print(f"Error: '{FILE_INPUT}' not found. Run Kernel Testing first.")
        return False
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(FILE_INPUT)
    sns.set_theme(style="whitegrid", context="talk")
    modes_order = ["basis", "angle", "amplitude"]

    # Detection Confidence
    plt.figure(figsize=(12, 6))
    detection_stats = df.groupby('Mode')['Caught_Rate'].mean() * 100
    detection_stats = detection_stats.reindex(modes_order, fill_value=0)
    ax1 = sns.barplot(x=detection_stats.index, y=detection_stats.values, palette="viridis", edgecolor="black", linewidth=1.5)
    plt.title("Statistical Detection Confidence", fontsize=18, pad=20, weight='bold')
    plt.ylabel("Avg. Detection Probability (%)", fontsize=14)
    plt.xlabel("Embedding Mode", fontsize=14)
    plt.ylim(0, 115)
    for p in ax1.patches:
        ax1.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', xytext=(0, 12), textcoords='offset points', weight='bold', fontsize=14)
    plt.tight_layout()
    plt.savefig(FILE_CHART_RATE, dpi=300)
    plt.close()
    print(f"Saved: {FILE_CHART_RATE}")

    # Heatmap
    present_mr_cols = [col for col in ORDERED_MR_KEYS if col in df.columns]
    if present_mr_cols:
        heatmap_data = df.groupby('Mode')[present_mr_cols].mean() * 100
        heatmap_data = heatmap_data.reindex(modes_order, fill_value=0)
        heatmap_data.columns = [mr_mapping[c] for c in heatmap_data.columns]
        plt.figure(figsize=(20, 12))
        ax = sns.heatmap(heatmap_data.T, annot=True, cmap="rocket_r", fmt=".0f",
                         cbar_kws={'label': 'Statistical Reliability (%)'}, linewidths=1, linecolor='white',
                         annot_kws={"size": 11, "weight": "bold"})
        ax.hlines([3, 6], *ax.get_xlim(), colors='white', linestyles='dashed', linewidths=3)
        ax2 = ax.twinx()
        ax2.set_ylim(ax.get_ylim())
        ax2.set_yticks([1.5, 4.5, 10])
        ax2.set_yticklabels(["Group A\n(General)", "Group B\n(Quantum)", "Group C\n(Embedding)"], fontsize=12, weight='bold', color='#333333')
        ax2.tick_params(right=False)
        plt.title("Metamorphic Oracle Reliability (Classified)", fontsize=18, pad=20, weight='bold')
        ax.set_xlabel("Embedding Mode", fontsize=14)
        ax.set_ylabel("Metamorphic Relation (Grouped)", fontsize=14)
        plt.tight_layout()
        plt.savefig(FILE_CHART_HEATMAP, dpi=300)
        plt.close()
        print(f"Saved: {FILE_CHART_HEATMAP}")
    return True


if __name__ == "__main__":
    generate_v41_plots()
