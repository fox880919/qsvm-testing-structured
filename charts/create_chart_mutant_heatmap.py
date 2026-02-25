"""
Generate Statistical Testing heatmap for progress report.
Adapted from mutation_testing_sept/createchart2_3d_9_4.py.
Output: mutant_outcome_fully_hierarchical_heatmap_sequential_labels_fixed_data.png
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import ListedColormap
import matplotlib.gridspec as gridspec

FILE_INPUT = "saved_data/my_data_frame_Jan_all.csv"
OUTPUT_DIR = "progress report/figures"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "mutant_outcome_fully_hierarchical_heatmap_sequential_labels_fixed_data.png")

DESCRIPTIVE_MR_LABELS = [
    'Scaling', 'Rotating', 'Feature Permutation', 'Invert Labels', 'Duplicating Inputs',
    'Add Quantum Register', 'Inject Null Effect Operations', 'Inject Parameters',
    'Change Back-End Service', 'Change of Optimization Level',
    'Reverse QC Wires', 'Switch Q-Kernel Inner Product Inputs',
]

MR_NUM_TO_LABEL = {i + 1: DESCRIPTIVE_MR_LABELS[i] for i in range(12)}


def generate_mutant_heatmap():
    if not os.path.exists(FILE_INPUT):
        print(f"Error: '{FILE_INPUT}' not found. Run Statistical Testing first.")
        return False
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df_long = pd.read_csv(FILE_INPUT)
    outcome_col = 'type_of_mutant'
    df_long[outcome_col] = df_long[outcome_col].astype(str).str.strip().str.lower()
    df_long = df_long[df_long['Applied_MR'].astype(str).str.strip() != '-']
    df_long['mutant_#'] = df_long['mutant_#'].astype(str)

    df_aggregated = df_long.groupby(['mutant_#', 'Applied_MR'])[outcome_col].agg(
        lambda x: x.mode()[0] if not x.mode().empty else np.nan
    ).reset_index(name=outcome_col)

    df_results_wide = df_aggregated.pivot(index='mutant_#', columns='Applied_MR', values=outcome_col)

    # Map numeric MR columns to descriptive labels
    rename_map = {}
    for col in df_results_wide.columns:
        try:
            n = int(float(col))
            if n in MR_NUM_TO_LABEL:
                rename_map[col] = MR_NUM_TO_LABEL[n]
        except (ValueError, TypeError):
            pass
    df_results_wide = df_results_wide.rename(columns=rename_map)
    # Reorder columns to match DESCRIPTIVE_MR_LABELS
    existing_cols = [c for c in DESCRIPTIVE_MR_LABELS if c in df_results_wide.columns]
    df_results_wide = df_results_wide[existing_cols]

    mutant_ids_unsorted = df_results_wide.index.tolist()
    sorted_mutant_ids = sorted(mutant_ids_unsorted, key=lambda x: int(x) if str(x).isdigit() else 0)
    df_results_wide = df_results_wide.reindex(sorted_mutant_ids)
    sequential_mutant_labels = [str(i) for i in range(1, len(sorted_mutant_ids) + 1)]
    df_results_annot = df_results_wide.fillna('N/A').astype(str)

    # Mutant embedding: 1-10 amplitude, 11-30 angle (per main.py)
    MUTANT_EMBEDDING_COLORS_HEX = {'Amplitude Embedding': '#fdb462', 'Angle Embedding': '#b3de69', 'Other': 'gray'}
    mutant_category_list = []
    for mutant_id in sorted_mutant_ids:
        try:
            mid = int(mutant_id)
            if 1 <= mid <= 10:
                mutant_category_list.append('Amplitude Embedding')
            elif 11 <= mid <= 30:
                mutant_category_list.append('Angle Embedding')
            else:
                mutant_category_list.append('Other')
        except ValueError:
            mutant_category_list.append('Other')

    unique_mutant_categories = sorted(list(set(mutant_category_list)))
    mutant_category_to_int = {cat: i for i, cat in enumerate(unique_mutant_categories)}
    mutant_int_array = np.array([mutant_category_to_int[cat] for cat in mutant_category_list])
    mutant_category_cmap = ListedColormap([MUTANT_EMBEDDING_COLORS_HEX.get(cat, 'gray') for cat in unique_mutant_categories])

    CATEGORY_COLORS_HEX = {'SVM Related': '#FFD700', 'Quantum Circuit Related': '#800080'}
    n_mrs = len(df_results_wide.columns)
    category_list = ['SVM Related'] * min(5, n_mrs) + ['Quantum Circuit Related'] * max(0, n_mrs - 5)
    unique_categories = sorted(list(set(category_list)))
    category_to_int = {cat: i for i, cat in enumerate(unique_categories)}
    category_int_array = np.array([category_to_int[cat] for cat in category_list]).reshape(1, -1)
    category_cmap_top = ListedColormap([CATEGORY_COLORS_HEX.get(cat, 'gray') for cat in unique_categories])

    ORDERED_OUTCOMES = ['killed', 'survived', 'equivalent', 'crashed']
    OUTCOME_COLORS = {'killed': '#2ca02c', 'survived': '#ff7f0e', 'equivalent': '#1f77b4', 'crashed': '#d62728'}
    outcome_to_numeric = {name: i for i, name in enumerate(ORDERED_OUTCOMES)}
    pivot_table_numeric = df_results_wide.apply(lambda col: col.map(outcome_to_numeric))
    outcome_cmap = ListedColormap([OUTCOME_COLORS[name] for name in ORDERED_OUTCOMES])

    sns.set_style("white")
    fig = plt.figure(figsize=(18, 12))
    gs = gridspec.GridSpec(1, 2, width_ratios=[0.05, 1], wspace=0.05)

    ax_row_anno = fig.add_subplot(gs[0, 0])
    ax_row_anno.imshow(mutant_int_array.reshape(-1, 1), aspect='auto', cmap=mutant_category_cmap)
    ax_row_anno.set_xticks([])
    ax_row_anno.set_yticks(np.arange(len(sorted_mutant_ids)))
    ax_row_anno.set_yticklabels(sequential_mutant_labels, rotation=0, fontsize=9)
    ax_row_anno.set_ylabel('Embedding Type', rotation=90, fontsize=12, labelpad=10)
    ax_row_anno.yaxis.set_label_position("left")
    ax_row_anno.yaxis.tick_left()

    ax_main = fig.add_subplot(gs[0, 1])
    divider = make_axes_locatable(ax_main)
    sns.heatmap(pivot_table_numeric, cmap=outcome_cmap, vmin=0, vmax=3,
                linewidths=0.5, linecolor='lightgray', cbar=False, annot=df_results_annot.to_numpy(),
                fmt='s', ax=ax_main, annot_kws={"size": 6, "rotation": 45, "color": "black", "va": "center", "ha": "center"})
    ax_main.set_yticklabels(sequential_mutant_labels, rotation=0, fontsize=9)
    ax_main.set_ylabel('Mutant Index', fontsize=12, labelpad=10)

    cax_col_anno = divider.append_axes("top", size="3%", pad=0.1)
    cax_col_anno.imshow(category_int_array, aspect='auto', cmap=category_cmap_top)
    cax_col_anno.set_xticks(np.arange(len(category_int_array[0])))
    cax_col_anno.set_xticklabels(df_results_wide.columns.tolist(), rotation=45, ha='left', fontsize=10)
    cax_col_anno.tick_params(left=False, right=False, top=True, bottom=False, labelleft=False, labelright=False, labeltop=True, labelbottom=False)

    ax_main.vlines(5, *ax_main.get_ylim(), color='white', linewidth=4, linestyle='solid')
    ax_main.set_xlabel('QSVM Metamorphic Testing with Statistical Testing', fontsize=14)
    ax_main.set_xticks([])

    outcome_legend_patches = [plt.plot([], [], marker="s", ms=10, mec=None, color=OUTCOME_COLORS[name], label=name.capitalize())[0] for name in ORDERED_OUTCOMES]
    mr_group_legend_patches = [plt.plot([], [], marker="s", ms=10, mec=None, color=CATEGORY_COLORS_HEX[name], label=name)[0] for name in sorted(CATEGORY_COLORS_HEX.keys())]
    mutant_group_legend_patches = [plt.plot([], [], marker="s", ms=10, mec=None, color=MUTANT_EMBEDDING_COLORS_HEX[name], label=name)[0] for name in sorted(MUTANT_EMBEDDING_COLORS_HEX.keys())]
    full_legend_handles = outcome_legend_patches + mr_group_legend_patches + mutant_group_legend_patches
    full_legend_labels = [h.get_label() for h in full_legend_handles]
    fig.legend(full_legend_handles, full_legend_labels, bbox_to_anchor=(1.03, 1), loc='upper left', title="Legend", fontsize=10)

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, bbox_inches='tight')
    plt.close()
    print(f"Saved: {OUTPUT_FILE}")
    return True


if __name__ == "__main__":
    generate_mutant_heatmap()
