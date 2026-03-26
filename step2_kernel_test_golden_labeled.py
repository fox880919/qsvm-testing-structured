"""
Step 2 (golden-labeled export): same logic as step2_kernel_test.py but writes
results_v41_kernel_test_golden_labeled.csv with column Golden_Matrix_Caught_Rate
(fraction of runs where max kernel deviation on golden samples exceeds ε).

Use step2_kernel_test.py for the default Caught_Rate CSV used by the app.
"""

import os
import pennylane as qml
from pennylane import numpy as np
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler, Binarizer
from sklearn.decomposition import PCA
from tqdm import tqdm
import random
import itertools
import warnings

# ==========================================
# CONFIGURATION
# ==========================================
USE_FIXED_SEED = False
NUM_RUNS = int(os.environ.get("QSVM_STEP2_NUM_RUNS", "100"))
N_QUBITS = 4
FILE_RESULTS = "results_v41_kernel_test_golden_labeled.csv"
# MR / oracle comparisons inside check_mr_omni
TOL_IDEAL = 1e-6
TOL_AMP = 1e-8
# Golden-matrix catch rule only (independent of MR tolerances)
GOLDEN_TOL_IDEAL = 1e-3
GOLDEN_TOL_AMP = 1e-5

warnings.filterwarnings("ignore")


def run_step2_kernel_test_golden_labeled():
    """Same as run_step2_kernel_test but saves Golden_Matrix_Caught_Rate column."""
    # ==========================================
    # 1. DATA PREPARATION
    # ==========================================
    wine = load_wine()
    mask = wine.target != 2
    x_raw, y_raw = wine.data[mask], wine.target[mask]

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x_raw)

    pca = PCA(n_components=N_QUBITS)
    x_pca = pca.fit_transform(x_scaled)

    DATA_BASIS = Binarizer(threshold=0.0).fit_transform(x_pca).astype(int)
    DATA_ANGLE = x_pca

    pad_amp = 2**N_QUBITS - x_raw.shape[1]
    DATA_AMP = np.hstack([x_scaled, np.zeros((x_raw.shape[0], pad_amp))])
    DATA_AMP = DATA_AMP / np.linalg.norm(DATA_AMP, axis=1)[:, np.newaxis]

    # ==========================================
    # 2. AUTO MUTATOR
    # ==========================================
    class AutoMutator:
        def __init__(self, mode="basis"):
            self.mode = mode
            self.active_defects = []
            self.wire_map = list(range(N_QUBITS))

        def set_defects(self, defect_list):
            self.active_defects = list(defect_list)

        def _get_angles(self, vector):
            probs = np.abs(vector)**2
            n = int(np.log2(len(vector)))
            betas = [probs]
            for _ in range(n):
                curr = betas[-1]
                betas.append(np.array([curr[k] + curr[k+1] for k in range(0, len(curr), 2)]))
            alphas = []
            for i in range(n - 1, -1, -1):
                layer = []
                parent, child = betas[i+1], betas[i]
                for k in range(len(parent)):
                    num, den = np.sqrt(child[2*k]), np.sqrt(parent[k])
                    layer.append(0.0 if den < 1e-12 else 2 * np.arccos(num/den))
                alphas.append(np.array(layer))
            return alphas

        def _ur_cnot(self, layer, c_wires, t_wire):
            k = len(c_wires)
            thetas = np.array(list(layer) + [0.0]*(2**k - len(layer))) / (2**k)
            for i, th in enumerate(thetas):
                qml.RY(th, wires=t_wire)
                if i < len(thetas)-1:
                    ctl_idx = int(np.log2((i+1) & -(i+1)))
                    control_qubit = c_wires[k-1-ctl_idx]
                    if self.mode == "amplitude" and len(self.active_defects) > 0:
                        qml.RZ(np.pi/4, wires=control_qubit)
                        qml.RY(np.pi/8, wires=t_wire)
                    else:
                        qml.CNOT(wires=[control_qubit, t_wire])

        def apply_feature_map(self, x, wires):
            mapped_wires = [wires[i] for i in self.wire_map]
            if self.mode == "basis":
                for i in range(len(mapped_wires)):
                    val = x[i]
                    if "gate_error" in self.active_defects:
                        val = 1 - val
                    if val > 0.5:
                        qml.PauliX(wires=mapped_wires[i])
            elif self.mode == "angle":
                for i in range(len(mapped_wires)):
                    ang = x[i]
                    if "param_noise" in self.active_defects:
                        ang += np.random.uniform(0.1, np.pi/2)
                    qml.RY(ang, wires=mapped_wires[i])
            elif self.mode == "amplitude":
                layers = self._get_angles(x)
                qml.RY(layers[0][0], wires=mapped_wires[0])
                for i in range(1, len(layers)):
                    self._ur_cnot(layers[i], mapped_wires[:i], mapped_wires[i])
            n_w = len(mapped_wires)
            for j_idx, j in enumerate(mapped_wires):
                if not ("remove_superposition" in self.active_defects):
                    qml.Hadamard(wires=j)
                target = mapped_wires[(j_idx + 1) % n_w]
                if "swap_topology" in self.active_defects:
                    qml.SWAP(wires=[j, target])
                elif not ("remove_entanglement" in self.active_defects):
                    qml.CNOT(wires=[j, target])

    # ==========================================
    # 3. KERNEL & OMNI ORACLE
    # ==========================================
    dev = qml.device("default.qubit", wires=N_QUBITS)
    mutator = AutoMutator()

    @qml.qnode(dev)
    def qnode_omni(x1, x2, d1, d2):
        mutator.set_defects(d1)
        mutator.apply_feature_map(x1, range(N_QUBITS))
        mutator.set_defects(d2)
        qml.adjoint(mutator.apply_feature_map)(x2, range(N_QUBITS))
        return qml.probs(wires=range(N_QUBITS))

    def get_dist(x1, x2, d1=[], d2=[]):
        try:
            return qnode_omni(x1, x2, d1, d2)
        except Exception:
            return np.zeros(2**N_QUBITS)

    def check_mr_omni(mr_id, x1, x2, mode, active_d):
        p_ref = get_dist(x1, x2, active_d, [])
        curr_tol = TOL_AMP if mode == "amplitude" else TOL_IDEAL

        if mr_id == 2:
            p_self = get_dist(x1, x1, active_d, [])
            return np.linalg.norm(p_self - np.eye(2**N_QUBITS)[0]) > curr_tol
        elif mr_id == 9:
            return np.linalg.norm(p_ref - get_dist(x1 + 0.1, x2, active_d, [])) > 0.05
        elif mr_id == 12:
            x_orth = np.roll(x1, 1) if mode == "amplitude" else x1 + np.pi/2
            p_orth = get_dist(x1, x_orth, active_d, [])
            return p_orth[0] > 0.1
        elif mr_id == 14:
            mutator.wire_map = [1, 0, 3, 2]
            p_perm = get_dist(x1, x2, active_d, [])
            mutator.wire_map = list(range(N_QUBITS))
            return np.linalg.norm(p_ref - p_perm) > curr_tol
        elif mr_id == 3:
            p_neg = get_dist(-x1, -x2, active_d, [])
            return np.linalg.norm(p_ref - p_neg) > curr_tol
        elif mr_id == 6:
            p_rot = get_dist(np.roll(x1, 1), np.roll(x2, 1), active_d, [])
            return np.linalg.norm(p_ref - p_rot) > curr_tol
        elif mr_id == 10:
            x_drop = x1.copy()
            x_drop[-1] = 0
            p_drop = get_dist(x_drop, x2, active_d, [])
            return np.linalg.norm(p_ref - p_drop) < curr_tol
        elif mr_id == 13:
            p_rev = get_dist(x1[::-1], x2[::-1], active_d, [])
            return np.linalg.norm(p_ref - p_rev) > curr_tol

        k_ref = p_ref[0]
        if mr_id == 1:
            return abs(k_ref - get_dist(x2, x1, active_d, [])[0]) > curr_tol
        elif mr_id == 4:
            return abs(k_ref - get_dist(x1+0.5, x2+0.5, active_d, [])[0]) > curr_tol
        elif mr_id == 5:
            if mode != "angle":
                return False
            return abs(k_ref - get_dist(x1 + 2*np.pi, x2, active_d, [])[0]) > curr_tol
        elif mr_id == 7:
            return abs(k_ref - get_dist(x1[::-1], x2[::-1], active_d, [])[0]) > curr_tol
        elif mr_id == 8:
            if mode != "basis":
                return False
            return abs(k_ref - get_dist(1-x1, 1-x2, active_d, [])[0]) > curr_tol
        elif mr_id == 11:
            if mode != "amplitude":
                return False
            return abs(k_ref - get_dist(x1*2.0, x2*2.0, active_d, [])[0]) > curr_tol

        return False

    # ==========================================
    # 4. EXECUTION
    # ==========================================
    ALL_MRS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    results = []
    defects = ["remove_superposition", "remove_entanglement", "gate_error", "swap_topology", "param_noise"]

    combos = []
    for r in range(1, 4):
        combos.extend([list(c) for c in itertools.combinations(defects, r)])

    iterations = 1 if USE_FIXED_SEED else NUM_RUNS
    if USE_FIXED_SEED:
        random.seed(42)
        np.random.seed(42)

    print(f"\n{'='*60}")
    print("STEP 2 (golden-labeled CSV): Kernel Testing (February main41)")
    print(f"{'='*60}")
    print(f"Starting: {len(combos)} defect combos x {iterations} runs per mode")

    for mode in ["basis", "angle", "amplitude"]:
        dataset = DATA_BASIS if mode == "basis" else (DATA_ANGLE if mode == "angle" else DATA_AMP)
        mutator.mode = mode

        X_gold = dataset[:5]
        K_GOLD_DIST = np.array([[get_dist(X_gold[i], X_gold[j], [], []) for j in range(5)] for i in range(5)])

        pbar = tqdm(combos, desc=f"V41 {mode.upper()}", ncols=140)
        for d in pbar:
            caught_count = 0
            mr_kill_counts = {f"MR_{i}": 0 for i in ALL_MRS}

            for run in range(iterations):
                K_MUT_DIST = np.array([[get_dist(X_gold[i], X_gold[j], d, []) for j in range(5)] for i in range(5)])
                diff = np.max([np.linalg.norm(K_GOLD_DIST[i, j] - K_MUT_DIST[i, j]) for i in range(5) for j in range(5)])

                golden_tol = GOLDEN_TOL_AMP if mode == "amplitude" else GOLDEN_TOL_IDEAL

                if diff > golden_tol:
                    caught_count += 1
                    for mr in ALL_MRS:
                        h_fail = check_mr_omni(mr, dataset[0], dataset[1], mode, [])
                        m_fail = check_mr_omni(mr, dataset[0], dataset[1], mode, d)

                        if mr == 10:
                            if m_fail and not h_fail:
                                mr_kill_counts[f"MR_{mr}"] += 1
                        else:
                            if m_fail and not h_fail:
                                mr_kill_counts[f"MR_{mr}"] += 1

            avg_golden_matrix_caught = caught_count / iterations
            avg_mr_kills = {k: v / iterations for k, v in mr_kill_counts.items()}

            results.append([mode, "+".join(d), avg_golden_matrix_caught] + list(avg_mr_kills.values()))

    df = pd.DataFrame(
        results,
        columns=["Mode", "Defects", "Golden_Matrix_Caught_Rate"] + [f"Efficient_MR_{i}_Rate" for i in ALL_MRS],
    )
    df.to_csv(FILE_RESULTS, index=False)
    print(f"\nStep 2 (golden-labeled) complete. Results saved to {FILE_RESULTS}")


if __name__ == "__main__":
    run_step2_kernel_test_golden_labeled()
