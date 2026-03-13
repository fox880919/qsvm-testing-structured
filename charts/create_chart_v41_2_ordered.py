"""
Generate Kernel Testing charts for progress report (ordered MR numbering).
Source: mutation_testing_feb/create_chart41_2_ordered.py.
Output: chart_v41_detection_omni_2_ordered.png, chart_v41_heatmap_omni_2_ordered.png
"""

import os
import sys

# Run from project root (qsvm_structure_testing)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. LOAD DATA
# ==========================================
FILE_INPUT = "results_v41_kernel_test.csv"
OUTPUT_DIR = "progress report/figures2"
FILE_CHART_RATE = os.path.join(OUTPUT_DIR, "chart_v41_detection_omni_2_ordered.png")
FILE_CHART_HEATMAP = os.path.join(OUTPUT_DIR, "chart_v41_heatmap_omni_2_ordered.png")

# Full Mapping for ALL 14 Metamorphic Relations
mr_mapping = {
    "Efficient_MR_1_Rate": "MR1: Symmetry",
    "Efficient_MR_2_Rate": "MR2: Identity",
    "Efficient_MR_7_Rate": "MR3: Permutation",
    "Efficient_MR_9_Rate": "MR4: Noise Stability",
    "Efficient_MR_12_Rate": "MR5: Structural Orthogonality",
    "Efficient_MR_13_Rate": "MR6: Dual Consistency",
    "Efficient_MR_14_Rate": "MR7: Qubit Permutation",
    "Efficient_MR_4_Rate": "MR8: Shift Invariance",
    "Efficient_MR_5_Rate": "MR9: Angle Periodicity",
    "Efficient_MR_8_Rate": "MR10: Bit Inversion (Basis)",
    "Efficient_MR_11_Rate": "MR11: Linear Scaling (Amplitude)",
    "Efficient_MR_3_Rate": "MR12: Negation",
    "Efficient_MR_6_Rate": "MR13: Feature Rotation",
    "Efficient_MR_10_Rate": "MR14: Feature Sensitivity"
}

# Explicit Order: MR1 through MR14 in new sequential numbering
# Group A: General Mathematical (MR1, MR2, MR3)
# Group B: Quantum-Specific (MR4, MR5, MR6)
# Group C: Feature-Embedding Specific (MR7–MR14)
ORDERED_MR_KEYS = [
    "Efficient_MR_1_Rate",   # MR1: Symmetry
    "Efficient_MR_2_Rate",   # MR2: Identity
    "Efficient_MR_7_Rate",   # MR3: Permutation
    "Efficient_MR_9_Rate",   # MR4: Noise Stability
    "Efficient_MR_12_Rate",  # MR5: Structural Orthogonality
    "Efficient_MR_13_Rate",  # MR6: Dual Consistency
    "Efficient_MR_14_Rate",  # MR7: Qubit Permutation
    "Efficient_MR_4_Rate",   # MR8: Shift Invariance
    "Efficient_MR_5_Rate",   # MR9: Angle Periodicity
    "Efficient_MR_8_Rate",   # MR10: Bit Inversion (Basis)
    "Efficient_MR_11_Rate",  # MR11: Linear Scaling (Amplitude)
    "Efficient_MR_3_Rate",   # MR12: Negation
    "Efficient_MR_6_Rate",   # MR13: Feature Rotation
    "Efficient_MR_10_Rate",  # MR14: Feature Sensitivity
]


def generate_v41_plots():
    # 1. Check if file exists
    if not os.path.exists(FILE_INPUT):
        print(f"Error: '{FILE_INPUT}' not found.")
        print("Please ensure the V41 simulation has completed successfully.")
        return False

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 2. Load Data
    print(f"Loading Omni-Suite data from {FILE_INPUT}...")
    try:
        df = pd.read_csv(FILE_INPUT)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return False

    # Setup Visual Theme
    sns.set_theme(style="whitegrid", context="talk")
    modes_order = ["basis", "angle", "amplitude"]

    # ==========================================
    # 3. PLOT 1: DETECTION CONFIDENCE (Bar Chart)
    # ==========================================
    print("Generating Detection Confidence Chart...")
    plt.figure(figsize=(12, 6))

    # Calculate mean detection rate per mode
    detection_stats = df.groupby('Mode')['Caught_Rate'].mean() * 100
    detection_stats = detection_stats.reindex(modes_order, fill_value=0)

    ax1 = sns.barplot(
        x=detection_stats.index,
        y=detection_stats.values,
        palette="viridis",
        edgecolor="black",
        linewidth=1.5
    )

    plt.title("Statistical Detection Confidence", fontsize=18, pad=20, weight='bold')
    plt.ylabel("Avg. Detection Probability (%)", fontsize=14)
    plt.xlabel("Embedding Mode", fontsize=14)
    plt.ylim(0, 115)

    # Add labels
    for p in ax1.patches:
        ax1.annotate(
            f'{p.get_height():.1f}%',
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center', va='center',
            xytext=(0, 12),
            textcoords='offset points',
            weight='bold',
            fontsize=14
        )

    plt.tight_layout()
    plt.savefig(FILE_CHART_RATE, dpi=300)
    print(f"Saved: {FILE_CHART_RATE}")
    plt.close()

    # ==========================================
    # 4. PLOT 2: OMNI-SUITE HEATMAP
    # ==========================================
    print("Generating Omni-Suite Heatmap...")

    # Filter and Sort columns based on the new Report Groups
    present_mr_cols = [col for col in ORDERED_MR_KEYS if col in df.columns]

    if present_mr_cols:
        # Calculate mean efficiency per mode
        heatmap_data = df.groupby('Mode')[present_mr_cols].mean() * 100
        heatmap_data = heatmap_data.reindex(modes_order, fill_value=0)

        # Rename columns using the mapping
        heatmap_data.columns = [mr_mapping[c] for c in heatmap_data.columns]

        # Large Figure for 14 Columns
        plt.figure(figsize=(20, 12))

        # 'rocket_r' colormap: Light = Low, Dark/Black = High Efficiency
        ax = sns.heatmap(
            heatmap_data.T,
            annot=True,
            cmap="rocket_r",
            fmt=".0f",
            cbar_kws={'label': 'Statistical Reliability (%)'},
            linewidths=1,
            linecolor='white',
            annot_kws={"size": 11, "weight": "bold"}
        )

        # Add Visual Separators for Groups A, B, C
        ax.hlines([3, 6], *ax.get_xlim(), colors='white', linestyles='dashed', linewidths=3)

        # Add Group Labels on the Right Y-Axis
        ax2 = ax.twinx()
        ax2.set_ylim(ax.get_ylim())
        ax2.set_yticks([1.5, 4.5, 10])
        ax2.set_yticklabels(["Group A\n(General)", "Group B\n(Quantum)", "Group C\n(Embedding)"],
                            fontsize=12, weight='bold', color='#333333')
        ax2.tick_params(right=False)

        plt.title("Metamorphic Oracle Reliability (Classified)", fontsize=18, pad=20, weight='bold')
        ax.set_xlabel("Embedding Mode", fontsize=14)
        ax.set_ylabel("Metamorphic Relation (Grouped)", fontsize=14)

        plt.tight_layout()
        plt.savefig(FILE_CHART_HEATMAP, dpi=300)
        print(f"Saved: {FILE_CHART_HEATMAP}")
        plt.close()
    else:
        print("Warning: No MR columns found in the CSV.")
        return False

    return True


if __name__ == "__main__":
    generate_v41_plots()
