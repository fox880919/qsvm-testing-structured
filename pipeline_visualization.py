"""
Pipeline visualization: data extraction, PCA, feature map circuits, training,
accuracy, mutation analysis, golden matrix and kernel testing.
"""

import os
import sys
import base64
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


def get_pipeline_summary(dataset: int = 0):
    """Get data extraction and PCA summary for the experiment pipeline."""
    from classes.parameters import MyParameters
    from classes.default_parameters import DefaultParameters

    MyParameters.resetParameters()
    DefaultParameters.testMutation = 0

    from data.data_manager import DataManager

    dm = DataManager()
    x, y, x_normalized = dm.getData(dataset)

    summary = {
        "dataset": dataset,
        "dataset_name": ["Wine", "Load Digits", "Credit Card", "MNIST"][dataset] if dataset < 4 else "Custom",
        "n_samples": int(len(x)),
        "n_features_raw": int(x.shape[1]),
        "n_classes": int(len(set(y))),
        "always_use_pca": DefaultParameters.alwaysUsePCA,
        "pca_components": DefaultParameters.pca_components,
        "pca_applied": False,
        "n_features_after_pca": int(x_normalized.shape[1]),
    }

    if DefaultParameters.alwaysUsePCA and x_normalized.shape[1] > DefaultParameters.pca_components:
        from sklearn.decomposition import PCA
        pca = PCA(n_components=DefaultParameters.pca_components, random_state=42)
        x_pca = pca.fit_transform(x_normalized)
        summary["pca_applied"] = True
        summary["n_features_after_pca"] = DefaultParameters.pca_components
        summary["pca_explained_variance_ratio"] = pca.explained_variance_ratio_.tolist()

    return summary


def get_circuit_diagram(feature_map_type: int, n_qubits: int = 3):
    """Generate circuit diagram for amplitude (0) or angle (1) embedding. Returns base64 PNG."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import pennylane as qml
        from pennylane import numpy as np

        dev = qml.device("default.qubit", wires=n_qubits)

        if feature_map_type == 0:  # amplitude
            @qml.qnode(dev)
            def circuit_amp(x1, x2):
                qml.AmplitudeEmbedding(features=x1, wires=range(n_qubits), normalize=True)
                qml.adjoint(qml.AmplitudeEmbedding)(features=x2, wires=range(n_qubits), normalize=True)
                return qml.probs(wires=range(n_qubits))

            x1 = np.ones(2**n_qubits) / np.sqrt(2**n_qubits)
            x2 = np.ones(2**n_qubits) / np.sqrt(2**n_qubits)
            fig, _ = qml.draw_mpl(circuit_amp)(x1, x2)
        else:  # angle
            @qml.qnode(dev)
            def circuit_ang(x1, x2):
                qml.AngleEmbedding(features=x1, wires=range(n_qubits), rotation="Y")
                qml.adjoint(qml.AngleEmbedding)(features=x2, wires=range(n_qubits), rotation="Y")
                return qml.probs(wires=range(n_qubits))

            x1 = np.zeros(n_qubits)
            x2 = np.zeros(n_qubits)
            fig, _ = qml.draw_mpl(circuit_ang)(x1, x2)

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")
    except Exception:
        import traceback
        traceback.print_exc()
        return None


def get_step1_analysis(csv_path: Path):
    """Parse Step 1 CSV for mutation analysis. Returns counts and chart data."""
    if not csv_path.exists():
        return None
    try:
        import pandas as pd
        df = pd.read_csv(csv_path)
        if df.empty or "type_of_mutant" not in df.columns:
            return {"equivalent": 0, "killed": 0, "survived": 0, "crashed": 0, "total": 0, "rows": []}

        counts = df["type_of_mutant"].value_counts()
        result = {
            "equivalent": int(counts.get("Equivalent", 0)),
            "killed": int(counts.get("Killed", 0)),
            "survived": int(counts.get("Survived", 0)),
            "crashed": int(counts.get("Crashed", 0)),
            "total": len(df),
            "rows": df.head(50).to_dict(orient="records"),
        }
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None


def get_step2_analysis(csv_path: Path):
    """Parse Step 2 CSV for golden matrix and kernel testing. Returns summary and table."""
    if not csv_path.exists():
        return None
    try:
        import pandas as pd
        df = pd.read_csv(csv_path)
        if df.empty:
            return {"modes": [], "defect_combos": [], "caught_rates": [], "rows": []}

        result = {
            "modes": df["Mode"].unique().tolist() if "Mode" in df.columns else [],
            "defect_combos": df["Defects"].tolist() if "Defects" in df.columns else [],
            "caught_rates": df["Caught_Rate"].tolist() if "Caught_Rate" in df.columns else [],
            "rows": df.head(30).to_dict(orient="records"),
        }
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None
