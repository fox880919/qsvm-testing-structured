"""
QSVM visualization: hyperplane and data classification for live display during experiments.
Uses the experiment's data pipeline (DataManager, default_parameters PCA) and projects
to 2D for plotting only.
"""

import os
import sys
import base64
import io
from pathlib import Path

# Ensure project root is in path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


def _get_experiment_data_2d(dataset: int):
    """
    Load data using the experiment's DataManager and default_parameters.
    Applies PCA per default_parameters (alwaysUsePCA, pca_components).
    Returns 2D projection for plotting (first 2 PCs) plus full data for QSVM.
    """
    from classes.parameters import MyParameters
    from classes.default_parameters import DefaultParameters

    MyParameters.resetParameters()
    DefaultParameters.testMutation = 0

    from data.data_manager import DataManager

    dm = DataManager()
    x, y, x_normalized = dm.getData(dataset)

    # Apply PCA per default_parameters (same as experiment would use)
    if DefaultParameters.alwaysUsePCA and x_normalized.shape[1] > DefaultParameters.pca_components:
        pca_full = PCA(n_components=DefaultParameters.pca_components, random_state=42)
        x_for_qsvm = pca_full.fit_transform(x_normalized)
        # For 2D plot: use first 2 components
        x_2d = x_for_qsvm[:, :2]
    else:
        x_for_qsvm = x_normalized
        # For 2D plot: use first 2 features
        x_2d = x_for_qsvm[:, :2]

    return x_2d, x_for_qsvm, y


def _compute_kernel_and_train(x_train, x_test, y_train, feature_map_fn, n_qubits):
    """Compute kernel matrices and train SVM. Uses quantum kernel via feature_map_fn."""
    def kernel_matrix(X1, X2):
        n1, n2 = len(X1), len(X2)
        K = np.zeros((n1, n2))
        for i in range(n1):
            for j in range(n2):
                K[i, j] = feature_map_fn(X1[i], X2[j], n_qubits)
        return K

    K_train = kernel_matrix(x_train, x_train)
    K_test = kernel_matrix(x_test, x_train)
    svm = SVC(kernel="precomputed")
    svm.fit(K_train, y_train)
    return svm, K_train, K_test, kernel_matrix


def generate_qsvm_visualization(dataset: int = 0, feature_map_type: int = 0):
    """
    Generate QSVM decision boundary visualization.
    dataset: 0=Wine (others not implemented for viz)
    feature_map_type: 0=amplitude, 1=angle
    Returns base64 PNG string or None on error.
    """
    if dataset != 0:
        return None  # Only Wine supported for now

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    try:
        # Load data using experiment's pipeline (DataManager + default_parameters PCA)
        x_2d, x_for_qsvm, y = _get_experiment_data_2d(dataset)
        x_train_full, x_test_full, y_train, y_test = train_test_split(
            x_for_qsvm, y, test_size=0.2, random_state=42
        )
        # Import quantum components (same as experiment)
        from classes.parameters import MyParameters
        from classes.default_parameters import DefaultParameters

        MyParameters.resetParameters()
        DefaultParameters.testMutation = 0
        DefaultParameters.featureMapType = feature_map_type

        from quantum.q_kernel_manager import QKernelManager
        from quantum.feature_map_manager import FeatureMapManager

        qKernel = QKernelManager().getqKernel()()
        n_features, n_qubits = qKernel.getFeaturesAndNqubits(x_for_qsvm, feature_map_type)

        if feature_map_type == 0:  # amplitude: pad per experiment
            x_train_k = qKernel.pad_features(x_train_full, n_qubits)
            x_test_k = qKernel.pad_features(x_test_full, n_qubits)
        else:
            x_train_k, x_test_k = x_train_full, x_test_full

        fm_class = FeatureMapManager().getFeatureMap()
        feature_map = fm_class()

        def kernel_fn(x1, x2, nq):
            return feature_map.compute_kernel_matrix(
                np.array([x1]), np.array([x2]), nq, feature_map_type
            )[0, 0]

        svm, K_train, K_test, kernel_matrix = _compute_kernel_and_train(
            x_train_k, x_test_k, y_train, kernel_fn, n_qubits
        )

        # Create mesh for decision boundary in 2D (PC1 vs PC2)
        # Grid in 2D space; other dims fixed at training mean for prediction
        grid_res = 12
        x_min, x_max = x_2d[:, 0].min() - 0.5, x_2d[:, 0].max() + 0.5
        y_min, y_max = x_2d[:, 1].min() - 0.5, x_2d[:, 1].max() + 0.5
        xx, yy = np.meshgrid(
            np.linspace(x_min, x_max, grid_res),
            np.linspace(y_min, y_max, grid_res),
        )
        grid_2d = np.c_[xx.ravel(), yy.ravel()]
        # Build full-dim grid: PC1, PC2 from mesh; other dims = mean of training
        n_other = x_for_qsvm.shape[1] - 2
        if n_other > 0:
            other_mean = np.mean(x_train_full[:, 2:], axis=0)
            grid_full = np.hstack([
                grid_2d,
                np.tile(other_mean, (len(grid_2d), 1))
            ])
        else:
            grid_full = grid_2d
        if feature_map_type == 0:
            grid_full = qKernel.pad_features(grid_full, n_qubits)

        K_grid = np.zeros((len(grid_full), len(x_train_k)))
        for i in range(len(grid_full)):
            for j in range(len(x_train_k)):
                K_grid[i, j] = kernel_fn(grid_full[i], x_train_k[j], n_qubits)
        Z = svm.predict(K_grid)
        Z = Z.reshape(xx.shape)

        # Plot
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.contourf(xx, yy, Z, alpha=0.4, cmap="RdYlBu", levels=2)
        scatter = ax.scatter(
            x_2d[:, 0], x_2d[:, 1], c=y, cmap="RdYlBu", edgecolors="k", s=50
        )
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        emb = "Amplitude" if feature_map_type == 0 else "Angle"
        ax.set_title(f"QSVM Decision Boundary ({emb} Embedding)")
        plt.colorbar(scatter, ax=ax, label="Class")
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None
