"""
Golden-matrix charts; publication MR1--MR14 (kernel_mr_publication).
Output: chart_v41_detection_golden_labeled.png, chart_v41_heatmap_golden_labeled.png
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, SCRIPT_DIR)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from kernel_mr_publication import build_publication_heatmap_plot_df

FILE_INPUT = "results_v41_kernel_test_golden_labeled.csv"
OUTPUT_DIR = "progress report/figures2"
FILE_CHART_RATE = os.path.join(OUTPUT_DIR, "chart_v41_detection_golden_labeled.png")
FILE_CHART_HEATMAP = os.path.join(OUTPUT_DIR, "chart_v41_heatmap_golden_labeled.png")


def _golden_matrix_caught_series(df: pd.DataFrame) -> pd.Series:
    col = "Golden_Matrix_Caught_Rate" if "Golden_Matrix_Caught_Rate" in df.columns else "Caught_Rate"
    if col not in df.columns:
        raise ValueError("CSV must contain Golden_Matrix_Caught_Rate or Caught_Rate")
    return df.groupby("Mode")[col].mean() * 100


def generate_v41_plots_golden_labeled():
    if not os.path.exists(FILE_INPUT):
        print(f"Error: '{FILE_INPUT}' not found. Run step2_kernel_test_golden_labeled.py or add the CSV.")
        return False
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(FILE_INPUT)
    sns.set_theme(style="white", context="talk")
    modes_order = ["basis", "angle", "amplitude"]

    plt.figure(figsize=(12, 7))
    detection_stats = _golden_matrix_caught_series(df)
    detection_stats = detection_stats.reindex(modes_order, fill_value=0)
    ax1 = sns.barplot(x=detection_stats.index, y=detection_stats.values, palette="viridis", edgecolor="black", linewidth=1.5)
    plt.title(
        "Golden-matrix caught rate\n"
        "(mean of column Golden_Matrix_Caught_Rate over defect combinations; kernel deviation > ε on golden samples)",
        fontsize=15,
        pad=18,
        weight="bold",
    )
    plt.ylabel("Mean golden-matrix caught rate (%)", fontsize=14)
    plt.xlabel("Embedding Mode", fontsize=14)
    plt.ylim(0, 115)
    for p in ax1.patches:
        ax1.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='center', xytext=(0, 12), textcoords='offset points', weight='bold', fontsize=14)
    plt.tight_layout()
    plt.savefig(FILE_CHART_RATE, dpi=300)
    plt.close()
    print(f"Saved: {FILE_CHART_RATE}")

    plot_df, present_mr_cols = build_publication_heatmap_plot_df(df, modes_order)
    if present_mr_cols and plot_df is not None:
        plt.figure(figsize=(20, 12))
        ax = sns.heatmap(plot_df, annot=True, cmap="rocket_r", fmt=".0f",
                         cbar_kws={'label': 'Statistical Reliability (%)'}, linewidths=0,
                         annot_kws={"size": 11, "weight": "bold"})
        ax.grid(False)
        ax2 = ax.twinx()
        ax2.set_ylim(ax.get_ylim())
        ax2.set_yticks([2.5, 7.5, 12.0])
        ax2.set_yticklabels(["Group A\n(General)", "Group B\n(Quantum)", "Group C\n(Embedding)"], fontsize=12, weight='bold', color='#333333')
        ax2.tick_params(right=False)
        plt.title("Metamorphic Oracle Reliability (Classified)", fontsize=18, pad=20, weight='bold')
        ax.set_xlabel("Embedding Mode", fontsize=14)
        plt.tight_layout()
        plt.savefig(FILE_CHART_HEATMAP, dpi=300)
        plt.close()
        print(f"Saved: {FILE_CHART_HEATMAP}")
    return True


if __name__ == "__main__":
    generate_v41_plots_golden_labeled()
