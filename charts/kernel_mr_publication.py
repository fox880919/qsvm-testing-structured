"""
Thesis MR1–MR14 labels (v10 kernel section: Groups A/B/C).

CSV Efficient_MR_i_Rate = pipeline mr_id i. Publication MR# differs from i; see MR_MAPPING.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import pandas as pd

MR_MAPPING: Dict[str, str] = {
    "Efficient_MR_1_Rate": "MR1: Symmetry",
    "Efficient_MR_2_Rate": "MR2: Identity",
    "Efficient_MR_7_Rate": "MR3: Permutation",
    "Efficient_MR_3_Rate": "MR4: Negation",
    "Efficient_MR_10_Rate": "MR5: Feature Sensitivity",
    "Efficient_MR_9_Rate": "MR6: Noise Stability",
    "Efficient_MR_12_Rate": "MR7: Structural Orthogonality",
    "Efficient_MR_13_Rate": "MR8: Dual Consistency",
    "Efficient_MR_14_Rate": "MR9: Qubit Permutation",
    "Efficient_MR_6_Rate": "MR10: Feature Rotation",
    "Efficient_MR_4_Rate": "MR11: Shift Invariance (Angle)",
    "Efficient_MR_5_Rate": "MR12: Periodicity (Angle)",
    "Efficient_MR_8_Rate": "MR13: Bit Inversion (Basis)",
    "Efficient_MR_11_Rate": "MR14: Linear Scaling (Amplitude)",
}

ORDERED_PUBLICATION_KEYS: List[str] = [
    "Efficient_MR_1_Rate",
    "Efficient_MR_2_Rate",
    "Efficient_MR_7_Rate",
    "Efficient_MR_3_Rate",
    "Efficient_MR_10_Rate",
    "Efficient_MR_9_Rate",
    "Efficient_MR_12_Rate",
    "Efficient_MR_13_Rate",
    "Efficient_MR_14_Rate",
    "Efficient_MR_6_Rate",
    "Efficient_MR_4_Rate",
    "Efficient_MR_5_Rate",
    "Efficient_MR_8_Rate",
    "Efficient_MR_11_Rate",
]


def build_publication_heatmap_plot_df(
    df: pd.DataFrame,
    modes_order: List[str],
) -> Tuple[Optional[pd.DataFrame], List[str]]:
    """
    Build the matrix passed to sns.heatmap: rows = publication MR1..MR14 (top to bottom),
    columns = embedding modes. Reindexes columns and rows so labels always match the
    correct Efficient_MR_* series (avoids misaligned rows after rename/transpose).
    """
    present = [c for c in ORDERED_PUBLICATION_KEYS if c in df.columns]
    if not present:
        return None, present
    mat = df.groupby("Mode", sort=False)[present].mean(numeric_only=True) * 100
    mat = mat.reindex(modes_order, fill_value=0)
    mat = mat.reindex(columns=present, fill_value=0)
    labels = [MR_MAPPING[c] for c in present]
    mat.columns = labels
    plot_df = mat.T.reindex(index=labels)
    return plot_df, present
