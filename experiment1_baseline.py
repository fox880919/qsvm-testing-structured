"""
Baseline test (from progress report).
Tests whether QSVM is deterministic: applies MR#1 (scaling) and MR#2 (rotation)
to data, runs QSVM with original code (no mutations), checks MTS=0.
"""

from classes.default_parameters import DefaultParameters
from classes.parameters import MyParameters
from data.data_manager import DataManager
from quantum.q_kernel_manager import QKernelManager
from quantum.feature_map_manager import FeatureMapManager
from metamorphic.my_metamorphic_relations import MyMetamorphicRelations
from main_class import MainClass
import numpy as np


def run_experiment1(dataset=0, kfold=5, scaling_values=None, rotation_angles=None):
    """
    Run Baseline metamorphic testing (no mutations).
    - MR#1: Scaling with values in [2, 20)
    - MR#2: Rotation with given angles
    - MTS=0 means all models have identical accuracy (no bugs).
    """
    if scaling_values is None:
        scaling_values = [2, 5, 10, 15, 19]  # [2, 20) per report (subset for speed)
    if rotation_angles is None:
        rotation_angles = [np.pi / 4, np.pi / 2]  # Sample angles

    DefaultParameters.dataType = dataset
    DefaultParameters.n_folds = kfold
    DefaultParameters.testMutation = 0  # No mutations
    MyParameters.resetParameters()

    print(f"\n{'='*60}")
    print("Experiment 1: Baseline")
    print(f"Dataset: {dataset}, K-fold: {kfold}")
    print(f"MR#1 scaling values: {scaling_values[:5]}...{scaling_values[-1] if len(scaling_values) > 5 else ''}")
    print(f"MR#2 rotation angles: {rotation_angles}")
    print(f"{'='*60}\n")

    dataManager = DataManager()
    featureMapClass = FeatureMapManager().getFeatureMap()
    featureMap = featureMapClass()
    qKernelClass = QKernelManager().getqKernel()
    qKernel = qKernelClass()

    x, y, x_normalized = dataManager.getData(dataset)
    n_features, n_qubits = qKernel.getFeaturesAndNqubits(x_normalized, 0)
    x_padded = qKernel.pad_features(x_normalized, n_qubits)
    MyParameters.amplitudeNQubits = n_qubits

    scores = []
    configs = []

    # Baseline (no MR)
    print("Running baseline (no MR)...")
    score_baseline = MainClass.run_qsvm(x_padded, y, n_qubits, 1.0, featureMap, 0)
    scores.append(score_baseline)
    configs.append("baseline")
    print(f"  Baseline accuracy: {score_baseline:.4f}")

    # MR#1: Scaling
    for v in scaling_values:
        print(f"Running MR#1 (scaling) with value {v}...")
        x_tr, y_tr = MyMetamorphicRelations.useMetamorphicRelation(x_padded, y, 1, float(v))
        score = MainClass.run_qsvm(x_tr, y_tr, n_qubits, 1.0, featureMap, 0)
        scores.append(score)
        configs.append(f"MR1_scale_{v}")
        print(f"  MR#1 scale={v} accuracy: {score:.4f}")

    # MR#2: Rotation
    for angle in rotation_angles:
        print(f"Running MR#2 (rotation) with angle {angle:.4f}...")
        x_tr, y_tr = MyMetamorphicRelations.useMetamorphicRelation(x_padded, y, 2, angle)
        score = MainClass.run_qsvm(x_tr, y_tr, n_qubits, 1.0, featureMap, 0)
        scores.append(score)
        configs.append(f"MR2_angle_{angle:.2f}")
        print(f"  MR#2 angle={angle:.4f} accuracy: {score:.4f}")

    # MTS check: all accuracies should be identical
    scores_rounded = [round(s, 4) for s in scores]
    all_same = len(set(scores_rounded)) == 1
    mts = 0.0 if all_same else 1.0

    print(f"\n{'='*60}")
    print("Baseline results")
    print(f"{'='*60}")
    print(f"Models run: {len(scores)}")
    print(f"All accuracies identical: {all_same}")
    print(f"MTS: {mts} (0 = no bugs detected)")
    if all_same:
        print("Conclusion: QSVM behaves deterministically under MR#1 and MR#2.")
    else:
        print("Warning: Accuracy variance detected - possible stochasticity or implementation issue.")
    print(f"{'='*60}\n")
