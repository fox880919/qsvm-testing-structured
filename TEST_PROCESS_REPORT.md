# QSVM Structure Testing — Test Process Report

This document describes the two-step testing process for the Quantum Support Vector Machine (QSVM) project, with code-level explanations.

---

## Overview

The test framework consists of two sequential steps:

| Step | Focus | Mutants | Metamorphic Relations | Statistical Testing |
|------|--------|---------|------------------------|---------------------|
| **Step 1** | Full QSVM pipeline (feature map, kernel, data, main class, statistical class, metamorphic) | 30 mutants | 12 MRs | Yes (t-test, p &lt; 0.05) |
| **Step 2** | Quantum kernel only | Defect combinations | 14 MRs | No (threshold-based) |

---

## Step 1: Mutation Testing with Metamorphic Relations

### Purpose

Step 1 evaluates the full QSVM pipeline (data → feature map → quantum kernel → SVM) by mutation testing. Each mutant is run under metamorphic relations (MRs), and differences in scores are checked via statistical testing to decide whether the mutant is **equivalent**, **killed**, **survived**, or **crashed**.

### Entry Point and Loop

```python
# main.py, line 283
for i in range(1, 13):
```

- MRs 1–12 are exercised: `i` takes values 1 through 12.
- For each MR, tests run once with **angle** embedding and once with **amplitude** embedding.

### MR-Specific Flags

Before calling the test runner, flags in `DefaultParameters` are set for the current MR:

| MR | Flag | Meaning |
|----|------|---------|
| 6 | `addQuantumRegister = True` | Add extra qubit |
| 7 | `injectNullEffectOperation = True` | Inject no-op |
| 8 | `injectParameter = True` | Inject parameter |
| 9 | `changeDevice = True` | Switch device |
| 10 | `changeOptimization = True` | Change optimization |
| 11 | `reverseWires = True` | Reverse wire order |
| 12 | `reverseQubitsMultiplication = True` | Reverse qubit multiplication |

Each MR activates its flag; after the run, all flags are reset to `False`.

### Embedding Types and Mutant Sets

```python
# main.py, lines 175-176
runLoopThroughAllTests(0, i)   # Amplitude embedding
runLoopThroughAllTests(1, i)   # Angle embedding
```

- `runLoopThroughAllTests(typeOfFeatureMap, mrUsed)`:
  - `typeOfFeatureMap`:
    - `0` → amplitude embedding
    - `1` → angle embedding
  - `mrUsed` → current MR number (1–12).

Inside `runLoopThroughAllTests` (Sept-style sequential mapping, disjoint sets):

```python
# main.py, lines 121-126
if typeOfFeatureMap == 0:
    myMutations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]   # Amplitude: 10 mutants
else:
    myMutations = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]   # Angle: 20 mutants
```

- **Amplitude** tests use mutants 1–10 (disjoint set).
- **Angle** tests use mutants 11–30 (disjoint set, no overlap with amplitude).

### Mutant Organization (from `default_parameters.py`)

| Subsystem | Mutant IDs | Files |
|-----------|------------|-------|
| Feature Map | 1, 2, 3, 4, 5, 6, 11, 12, 13, 16, 20, 22–30 | `quantum/feature_map_m*.py` |
| Quantum Kernel | 7, 8, 9, 10 | `quantum/q_kernel_m*.py` |
| Main Class | 14, 17 | `main_class_m14.py`, `main_class_m17.py` |
| Statistical Class | 18, 21 | `main_statistical_class_m18.py`, `main_statistical_class_m21.py` |
| Data | 15 | `data/wine_data_m15.py` |
| Metamorphic | 19 | `metamorphic/my_metamorphic_relations_m19.py` |

### Core Test Logic: `runScript`

`runScript(mrNumber, mrValue)` is the main driver for Step 1.

1. **Initialization**  
   First iteration runs the original program (mutant 0) and stores its score.

2. **Mutant execution**  
   For each mutant ID in `myMutations`, `DefaultParameters.testMutation` is set and the main class is resolved dynamically:

   ```python
   # main.py, lines 70-76
   DefaultParameters.testMutation = 0  # First run: original
   mainClassClass = MainClassManager.getMainClass()  # Resolves MainClass or main_class_m14/17
   mainClass = mainClassClass()
   originalScore = mainClass.runTest(DefaultParameters.featureMapType)
   ```

   `MainClassManager.getMainClass()` loads either the base `MainClass` or a mutant (e.g. `main_class_m14`) depending on `MyParameters.testMutation`.

3. **Classification**  
   `mainClass.runTest()` returns a test score; this score is compared to the original:

   - **Equivalent**: score unchanged → equivalent mutant.
   - **Different** (numeric): statistical testing.
   - **Exception / non-numeric**: crashed mutant.

4. **Statistical testing (when scores differ)**

   ```python
   # main.py, lines 156-168
   mainStatisticalClass = MainStatisticalClassManager.getMainStatisticalClass()
   allScoresOfOriginal, allScoresOfMutant, tStatistic, pValue = mainStatisticalClass.runTest(mrNumber, mrValue)
   if pValue < 0.05:
       # Killed
   else:
       # Survived
   ```

   `MainStatisticalClass` repeats multiple runs with K-fold cross-validation, collects scores, and runs a two-sample t-test. If `p < 0.05`, the mutant is killed; otherwise it survives.

5. **Data recording**  
   For each outcome, `saveToDataFrame()` writes: original/mutant scores, mutant ID, type (equivalent/killed/survived/crashed), t-statistic, p-value, and metadata (e.g. feature map, MR).

### MR Value Selection

```python
# main.py, lines 237-258
if mrUsed == 1 or mrUsed == 3 or mrUsed == 4:
    mrValue = MyParameters.scaleValue
elif mrUsed == 2:
    mrValue = MyParameters.angle
elif mrUsed == 5:
    mrValue = MyParameters.inputToDuplicate
else:
    mrValue = 1
```

Different MRs use different parameters (scaling, angle, input duplication, etc.) via `mrValue`.

---

## Step 2: Quantum Kernel Testing

### Purpose

Step 2 isolates the quantum kernel and feature map, without the full SVM. It uses defect-based mutations and 14 metamorphic relations to evaluate how well MRs detect kernel-level bugs.

### Entry Point

```python
# main.py, lines 387-392
from step2_kernel_test import run_step2_kernel_test
run_step2_kernel_test()
```

### Data Preparation

```python
# step2_kernel_test.py, lines 36-51
wine = load_wine()
mask = wine.target != 2  # Binary classification
x_raw, y_raw = wine.data[mask], wine.target[mask]
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x_raw)
pca = PCA(n_components=N_QUBITS)
x_pca = pca.fit_transform(x_scaled)

DATA_BASIS = Binarizer(threshold=0.0).fit_transform(x_pca).astype(int)
DATA_ANGLE = x_pca
DATA_AMP = ...  # Normalized amplitude encoding
```

Three encodings are produced:

- **Basis**: Binarized PCA
- **Angle**: PCA components as angles
- **Amplitude**: Normalized amplitude vectors (padded to 2^n qubits)

### AutoMutator and Defects

`AutoMutator` applies a feature map under an optional defect set:

```python
# step2_kernel_test.py, lines 61-62, 99-123
def set_defects(self, defect_list):
    self.active_defects = list(defect_list)

def apply_feature_map(self, x, wires):
    if self.mode == "basis":
        if "gate_error" in self.active_defects:
            val = 1 - val  # Flip bit
    elif self.mode == "angle":
        if "param_noise" in self.active_defects:
            ang += np.random.uniform(0.1, np.pi/2)
    elif self.mode == "amplitude":
        if "remove_superposition" in self.active_defects:
            # Skip Hadamard
        if "remove_entanglement" in self.active_defects:
            # Skip CNOT
        if "swap_topology" in self.active_defects:
            qml.SWAP(...)
```

Defects: `remove_superposition`, `remove_entanglement`, `gate_error`, `swap_topology`, `param_noise`. Combinations of 1–3 defects are used.

### Quantum Kernel Computation

```python
# step2_kernel_test.py, lines 131-143
@qml.qnode(dev)
def qnode_omni(x1, x2, d1, d2):
    mutator.set_defects(d1)
    mutator.apply_feature_map(x1, range(N_QUBITS))
    mutator.set_defects(d2)
    qml.adjoint(mutator.apply_feature_map)(x2, range(N_QUBITS))
    return qml.probs(wires=range(N_QUBITS))

def get_dist(x1, x2, d1=[], d2=[]):
    return qnode_omni(x1, x2, d1, d2)
```

The kernel is implemented as: feature map on `x1`, adjoint feature map on `x2`, then measurement probabilities. This yields kernel distances without training an SVM.

### 14 Metamorphic Relations

`check_mr_omni(mr_id, x1, x2, mode, active_d)` checks whether a defect causes a violation of a given MR:

| MR | Property | Check |
|----|----------|--------|
| 1 | Symmetry | K(x1,x2) ≈ K(x2,x1) |
| 2 | Self-similarity | K(x1,x1) ≈ 1 |
| 3 | Negation | K(-x1,-x2) ≈ K(x1,x2) |
| 4 | Shift | K(x1+c,x2+c) ≈ K(x1,x2) |
| 5 | Periodicity (angle) | K(x1+2π,x2) ≈ K(x1,x2) |
| 6 | Rotation | K(roll(x1),roll(x2)) ≈ K(x1,x2) |
| 7 | Reversal | K(x1[::-1],x2[::-1]) ≈ K(x1,x2) |
| 8 | Complement (basis) | K(1-x1,1-x2) ≈ K(x1,x2) |
| 9 | Perturbation | K(x1+0.1,x2) ≠ K(x1,x2) (large change) |
| 10 | Drop dimension | K(x_drop,x2) vs K(x1,x2) |
| 11 | Scaling (amplitude) | K(2x1,2x2) ≈ K(x1,x2) |
| 12 | Orthogonality | K(x1,x_orth) small |
| 13 | Reversal (full vector) | K(x1[::-1],x2[::-1]) ≈ K(x1,x2) |
| 14 | Permutation | K(x1,x2) invariant under wire permutation |

Some MRs are mode-specific (e.g. MR 5 for angle, MR 8 for basis, MR 11 for amplitude).

### Execution Loop

```python
# step2_kernel_test.py, lines 204, 209-210, 222-256
ALL_MRS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
defects = ["remove_superposition", "remove_entanglement", "gate_error", "swap_topology", "param_noise"]
combos = itertools.combinations(defects, r) for r in 1..3

for mode in ["basis", "angle", "amplitude"]:
    for d in combos:
        for run in range(iterations):  # 100 runs (or 1 if fixed seed)
            K_MUT_DIST = [[get_dist(...) for ...]]  # Kernel with defects
            diff = max(norm(K_GOLD - K_MUT))
            if diff > tol:
                caught_count += 1
                for mr in ALL_MRS:
                    if check_mr_omni detects violation: mr_kill_counts[MR] += 1
```

- For each mode and defect combo, compute gold vs mutated kernel distances.
- If the maximum distance exceeds a tolerance, the defect is “caught”.
- For each MR, count how often that MR detects the violation.

### Output

Results are written to `results_v41_kernel_test.csv` with columns for mode, defect combination, caught rate, and per-MR detection rates.

---

## Summary Flow Diagram

```
main.py
    │
    ├─ for i in range(1, 13):                    # MRs 1–12
    │       │
    │       ├─ Set MR-specific flags (e.g. addQuantumRegister for MR6)
    │       │
    │       ├─ runLoopThroughAllTests(0, i)      # Amplitude embedding
    │       │       └─ myMutations = [1..10]
    │       │       └─ runScript → MainClass.runTest → statistical test
    │       │
    │       ├─ runLoopThroughAllTests(1, i)     # Angle embedding
    │       │       └─ myMutations = [11..30]
    │       │       └─ runScript → MainClass.runTest → statistical test
    │       │
    │       └─ Reset all MR flags
    │
    └─ run_step2_kernel_test()
            └─ For basis, angle, amplitude:
                └─ For each defect combo:
                    └─ Compute kernel matrices with defects
                    └─ Check 14 MRs via check_mr_omni
                    └─ Record caught rates and MR effectiveness
```

---

## Files Reference

| File | Role |
|------|-----|
| `main.py` | Step 1 entry point, MR loop, `runLoopThroughAllTests`, `runScript`, statistical decision |
| `step2_kernel_test.py` | Step 2 kernel-only testing, 14 MRs, defect-based mutations |
| `classes/default_parameters.py` | MR flags, mutant lists, feature-map type |
| `main_class_manager.py` | Loads `MainClass` or mutant `main_class_m*` |
| `main_statistical_class_manager.py` | Loads `MainStatisticalClass` or mutant variant |
| `quantum/feature_map_manager.py` | Loads feature map or `feature_map_m*` mutants |
| `quantum/q_kernel_manager.py` | Loads quantum kernel or `q_kernel_m*` mutants |
| `classes/my_dataframe_short.py` | Persists test results to CSV |
