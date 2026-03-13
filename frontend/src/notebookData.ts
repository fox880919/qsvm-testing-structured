/** Default notebook sections — used when no custom data is saved. */

export interface NotebookCell {
  id: string
  type: 'markdown' | 'code'
  content: string
}

export interface NotebookSection {
  id: string
  title: string
  experiment?: 1 | 2 | 3
  cells: NotebookCell[]
}

export const DEFAULT_NOTEBOOK_SECTIONS: NotebookSection[] = [
  {
    id: 'intro',
    title: 'Overview',
    cells: [
      {
        id: 'intro',
        type: 'markdown',
        content: `## QSVM Structure Testing — Interactive Notebook

This notebook documents and runs the full QSVM mutation and metamorphic testing pipeline, aligned with **TEST_PROCESS_REPORT.md**. Each code cell can be executed with the **Run** button.

### Three Experiments

| Experiment | Focus | Mutants | Metamorphic Relations | Statistical Testing |
|------------|--------|---------|------------------------|---------------------|
| **1. Baseline** | MR#1 (scaling) + MR#2 (rotation) on data, no mutations. MTS=0 check. | 0 | 2 | No |
| **2. Statistical Testing** | Full QSVM pipeline (feature map, kernel, data, main class, statistical class, metamorphic) | 10 amplitude / 20 angle | 12 MRs | Yes (t-test, p < 0.05) |
| **3. Kernel Testing** | Quantum kernel only | Defect combinations | 14 MRs | No (threshold-based) |

Run all: \`main.run_tests(dataset=0, kfold=5, experiment='all')\` or run individual experiments (1, 2, or 3).`,
      },
      {
        id: 'run-all-code',
        type: 'code',
        content: `# Run all three experiments (takes several minutes)
import main
main.run_tests(dataset=0, kfold=5, experiment='all')`,
      },
    ],
  },
  {
    id: 'exp1',
    title: 'Baseline',
    experiment: 1,
    cells: [
      {
        id: 'exp1-desc',
        type: 'markdown',
        content: `## 1. Baseline

Applies **MR#1** (scaling) and **MR#2** (rotation) to data, runs QSVM with original code (no mutations). Verifies **MTS=0**: all models have identical accuracy (deterministic, no bugs).

**Execution:** 1 baseline + 5 scaling values + 2 rotation angles = **8 QSVM runs**.`,
      },
      {
        id: 'exp1-full-code',
        type: 'markdown',
        content: `### Full Implementation (experiment1_baseline.py)

The complete \`run_experiment1\` function: loads data, creates feature map and kernel, runs baseline (no MR), then MR#1 with 5 scaling values, then MR#2 with 2 rotation angles. Each run calls \`MainClass.run_qsvm\` (train_test_split → kernel matrix → SVM fit → score). MTS=0 if all accuracies identical.`,
      },
      {
        id: 'exp1-code-full',
        type: 'code',
        content: `from classes.default_parameters import DefaultParameters
from classes.parameters import MyParameters
from data.data_manager import DataManager
from quantum.q_kernel_manager import QKernelManager
from quantum.feature_map_manager import FeatureMapManager
from metamorphic.my_metamorphic_relations import MyMetamorphicRelations
from main_class import MainClass
import numpy as np

def run_experiment1(dataset=0, kfold=5, scaling_values=None, rotation_angles=None):
    if scaling_values is None:
        scaling_values = [2, 5, 10, 15, 19]
    if rotation_angles is None:
        rotation_angles = [np.pi / 4, np.pi / 2]

    DefaultParameters.dataType = dataset
    DefaultParameters.n_folds = kfold
    DefaultParameters.testMutation = 0
    MyParameters.resetParameters()

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
    # Baseline (no MR)
    score_baseline = MainClass.run_qsvm(x_padded, y, n_qubits, 1.0, featureMap, 0)
    scores.append(score_baseline)
    # MR#1: Scaling
    for v in scaling_values:
        x_tr, y_tr = MyMetamorphicRelations.useMetamorphicRelation(x_padded, y, 1, float(v))
        score = MainClass.run_qsvm(x_tr, y_tr, n_qubits, 1.0, featureMap, 0)
        scores.append(score)
    # MR#2: Rotation
    for angle in rotation_angles:
        x_tr, y_tr = MyMetamorphicRelations.useMetamorphicRelation(x_padded, y, 2, angle)
        score = MainClass.run_qsvm(x_tr, y_tr, n_qubits, 1.0, featureMap, 0)
        scores.append(score)

    scores_rounded = [round(s, 4) for s in scores]
    all_same = len(set(scores_rounded)) == 1
    mts = 0.0 if all_same else 1.0
    print(f"Models run: {len(scores)}, MTS: {mts} (0=no bugs)")
    return mts

run_experiment1(dataset=0, kfold=5)`,
      },
    ],
  },
  {
    id: 'exp2',
    title: 'Statistical Testing',
    experiment: 2,
    cells: [
      {
        id: 'exp2-desc',
        type: 'markdown',
        content: `## 2. Statistical Testing (Full QSVM Pipeline)

30 mutants (10 amplitude, 20 angle), 12 metamorphic relations. Statistical t-test (p < 0.05) for Killed/Survived. Output: \`saved_data/my_data_frame_Jan_all.csv\`.`,
      },
      {
        id: 'config',
        type: 'markdown',
        content: `## 3. Configuration (DefaultParameters)

\`DefaultParameters\` holds dataset type, K-fold, feature map (0=amplitude, 1=angle), MR flags, and mutant lists.`,
      },
      {
        id: 'config-code',
        type: 'code',
        content: `from classes.default_parameters import DefaultParameters

print("Dataset:", DefaultParameters.dataType, "(0=Wine, 1=Digits, 2=Credit, 3=MNIST)")
print("K-fold:", DefaultParameters.n_folds)
print("Feature map:", DefaultParameters.featureMapType, "(0=amplitude, 1=angle)")
print("MR used:", DefaultParameters.mrUsed)
print("Scale value:", DefaultParameters.scaleValue)
print("Feature map mutants:", DefaultParameters.featureMapMutationList[:10], "...")`,
      },
      {
        id: 'mr-flags',
        type: 'markdown',
        content: `## 4. MR-Specific Flags (Statistical Testing)

Before each test run, flags in \`DefaultParameters\` are set for the current MR:

| MR | Flag | Meaning |
|----|------|---------|
| 6 | addQuantumRegister | Add extra qubit |
| 7 | injectNullEffectOperation | Inject no-op |
| 8 | injectParameter | Inject parameter |
| 9 | changeDevice | Switch device |
| 10 | changeOptimization | Change optimization |
| 11 | reverseWires | Reverse wire order |
| 12 | reverseQubitsMultiplication | Reverse qubit multiplication |

Each MR activates its flag; after the run, all flags are reset to False.`,
      },
      {
        id: 'mr-flags-code',
        type: 'code',
        content: `from classes.default_parameters import DefaultParameters

# Example: MR 6 adds quantum register
DefaultParameters.addQuantumRegister = True
print("addQuantumRegister:", DefaultParameters.addQuantumRegister)

# Reset
DefaultParameters.addQuantumRegister = False

# MR value selection
from classes.parameters import MyParameters
MyParameters.resetParameters()
mrValue = MyParameters.scaleValue if DefaultParameters.mrUsed in [1,3,4] else MyParameters.angle if DefaultParameters.mrUsed == 2 else 1
print("mrValue for MR1:", DefaultParameters.mrUsed, "->", mrValue)`,
      },
      {
        id: 'data',
        type: 'markdown',
        content: `## 5. Data Loading

\`DataManager.getData(n)\` loads dataset n and returns (x, y, x_normalized). PCA is applied for dimensionality reduction.`,
      },
      {
        id: 'data-code',
        type: 'code',
        content: `from data.data_manager import DataManager

dm = DataManager()
x, y, x_norm = dm.getData(0)
print("Wine - Shape:", x.shape, y.shape)
print("Classes:", set(y))`,
      },
      {
        id: 'metamorphic',
        type: 'markdown',
        content: `## 6. Metamorphic Relations (MyMetamorphicRelations)

\`MyMetamorphicRelations.useMetamorphicRelation\` applies MRs to data:
- **MR1**: Feature scaling
- **MR2**: Rotation with angle
- **MR3**: Permutation
- **MR4**: Label inversion
- **MR5**: Input duplication`,
      },
      {
        id: 'metamorphic-code',
        type: 'code',
        content: `from metamorphic.my_metamorphic_relations import MyMetamorphicRelations
import numpy as np

x = np.array([[1, 2], [3, 4]])
y = np.array([0, 1])
x_scaled, y_out = MyMetamorphicRelations.useMetamorphicRelation(x, y, 1, 2.0)
print("MR1 scaling x2:", x_scaled)`,
      },
      {
        id: 'mutant-org',
        type: 'markdown',
        content: `## 7. Mutant Organization

From \`default_parameters.py\`:

| Subsystem | Mutant IDs | Files |
|-----------|------------|-------|
| Feature Map | 1, 2, 3, 4, 5, 6, 11, 12, 13, 16, 20, 22–30 | quantum/feature_map_m*.py |
| Quantum Kernel | 7, 8, 9, 10 | quantum/q_kernel_m*.py |
| Main Class | 14, 17 | main_class_m14.py, main_class_m17.py |
| Statistical Class | 18, 21 | main_statistical_class_m18.py, main_statistical_class_m21.py |
| Data | 15 | data/wine_data_m15.py |
| Metamorphic | 19 | metamorphic/my_metamorphic_relations_m19.py |`,
      },
      {
        id: 'mainclass',
        type: 'markdown',
        content: `## 8. MainClass — QSVM Execution (Full Logic)

\`MainClass.runTest(featureMapType)\` loads data, builds the quantum kernel via the feature map, trains an SVM, and returns the test score. \`MainClassManager.getMainClass()\` selects the mutant (original or m1–m30) based on \`testMutation\`.

**run_qsvm (static, ~40 lines):**
\`\`\`python
x_train, x_test, y_train, y_test = train_test_split(x_padded, y, test_size=0.2, random_state=42)
kernel_train = featureMap.compute_kernel_matrix(x_train, x_train, n_qubits, featureMapType)
kernel_test = featureMap.compute_kernel_matrix(x_test, x_train, n_qubits, featureMapType)
svm = SVC(kernel='precomputed')
svm.fit(kernel_train, y_train)
return svm.score(kernel_test, y_test)
\`\`\`

**runTest (instance):** getData → getFeaturesAndNqubits → pad_features → run_qsvm → return score`,
      },
      {
        id: 'mainclass-code',
        type: 'code',
        content: `from main_class_manager import MainClassManager
from classes.default_parameters import DefaultParameters

DefaultParameters.testMutation = 0
mc_class = MainClassManager.getMainClass()
mc = mc_class()
score = mc.runTest(0)
print("Original (mutant 0) score:", score)`,
      },
      {
        id: 'statistical',
        type: 'markdown',
        content: `## 9. Statistical Testing (MainStatisticalClass)

When mutant score ≠ original, \`MainStatisticalClass.runTest(mrNumber, mrValue)\` runs K-fold with t-test. If **p < 0.05** → **Killed**; else → **Survived**.`,
      },
      {
        id: 'statistical-code',
        type: 'code',
        content: `from main_statistical_class_manager import MainStatisticalClassManager
from classes.default_parameters import DefaultParameters
from classes.parameters import MyParameters

MyParameters.resetParameters()
DefaultParameters.testMutation = 1
DefaultParameters.dataType = 0
DefaultParameters.n_folds = 3
DefaultParameters.mrUsed = 1
msc_class = MainStatisticalClassManager.getMainStatisticalClass()
msc = msc_class()
all_orig, all_mut, t, p = msc.runTest(1, 5.0)
print("t-statistic:", round(t, 4), "p-value:", round(p, 4))`,
      },
      {
        id: 'runscript',
        type: 'markdown',
        content: `## 10. runScript — Core Test Driver (Full Implementation)

\`runScript(mrNumber, mrValue)\` is the main driver for Statistical Testing:

1. **Initialization**: First run executes mutant 0 (original) and stores its score.
2. **Mutant execution**: For each mutant in \`myMutations\`, sets \`testMutation\`, loads \`MainClass\` via \`MainClassManager\`, runs \`runTest\`.
3. **Classification**: Equivalent (score unchanged) | Killed (p < 0.05) | Survived (p ≥ 0.05) | Crashed (exception).
4. **Data recording**: \`saveToDataFrame\` writes results to CSV.

**Execution:** 12 MRs × (10 amplitude + 20 angle mutants) = **384 runTest calls** (+ statistical K-fold when scores differ).`,
      },
      {
        id: 'runscript-code',
        type: 'markdown',
        content: `### runScript full source (main.py lines 19–100)

\`\`\`python
def runScript(mrNumber, mrValue):
    for test in myMutations:
        if firstRun:
            DefaultParameters.testMutation = 0
            mainClass = MainClassManager.getMainClass()()
            originalScore = mainClass.runTest(DefaultParameters.featureMapType)
            firstRun = False
        DefaultParameters.testMutation = test
        mainClass = MainClassManager.getMainClass()()
        mutantScore = mainClass.runTest(DefaultParameters.featureMapType)
        if mutantScore == originalScore:
            saveToDataFrame(..., 'Equivalent', ...)
        elif isinstance(mutantScore, numbers.Number):
            msc = MainStatisticalClassManager.getMainStatisticalClass()()
            allScoresOfOriginal, allScoresOfMutant, tStatistic, pValue = msc.runTest(mrNumber, mrValue)
            if pValue < 0.05: saveToDataFrame(..., 'Killed', ...)
            else: saveToDataFrame(..., 'Survived', ...)
        else:
            saveToDataFrame(..., 'Crashed', ...)
\`\`\``,
      },
      {
        id: 'runloop',
        type: 'markdown',
        content: `## 11. runLoopThroughAllTests — Embedding & Mutant Sets

\`runLoopThroughAllTests(typeOfFeatureMap, mrUsed)\`:
- **typeOfFeatureMap == 0** (amplitude): \`myMutations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\` — 10 mutants (Sept-style, disjoint)
- **typeOfFeatureMap == 1** (angle): \`myMutations = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]\` — 20 mutants (Sept-style, disjoint)

MRs 1–12 are exercised: \`for i in range(1, 13)\`. For each MR, tests run once with amplitude and once with angle embedding.`,
      },
      {
        id: 'runloop-code',
        type: 'code',
        content: `import main
from classes.default_parameters import DefaultParameters

print("runLoopThroughAllTests:", hasattr(main, "runLoopThroughAllTests"))
print("Amplitude (0): [1..10] | Angle (1): [11..30] (disjoint, Sept-style)")
print("MRs 1-12: scaling, rotation, permutation, labels, duplication, addQuantumRegister, etc.")`,
      },
      {
        id: 'step1-flow',
        type: 'markdown',
        content: `## 12. runLoopThroughAllTests & run_tests (Statistical Testing) — Full Source

\`\`\`python
def runLoopThroughAllTests(typeOfFeatureMap, mrUsed):
    global myMutations
    DefaultParameters.mrUsed = mrUsed
    DefaultParameters.featureMapType = typeOfFeatureMap
    mrValue = MyParameters.scaleValue if mrUsed in [1,3,4] else MyParameters.angle if mrUsed == 2 else 1
    if typeOfFeatureMap == 0:
        myMutations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # amplitude: 10 mutants
    else:
        myMutations = [11, 12, ..., 30]  # angle: 20 mutants
    runScript(mrNumber=mrUsed, mrValue=mrValue)

# Statistical Testing loop in run_tests (main.py lines 154-216):
for i in range(1, 13):
    if i == 6: DefaultParameters.addQuantumRegister = True
    if i == 7: DefaultParameters.injectNullEffectOperation = True
    # ... MR 8-17 flags ...
    runLoopThroughAllTests(0, i)   # Amplitude: 10 mutants
    runLoopThroughAllTests(1, i)    # Angle: 20 mutants
    # Reset all flags
\`\`\``,
      },
      {
        id: 'run-tests',
        type: 'markdown',
        content: `## 13. Full Pipeline: run_tests (Statistical Testing only)

\`run_tests(dataset, kfold, experiment='2')\` runs only Statistical Testing. Outputs: \`saved_data/my_data_frame_Jan_all.csv\`. **Note:** Full run takes several minutes.

**Full Statistical Testing loop (main.py lines 154-216):**
\`\`\`python
for i in range(1, 13):  # MRs 1-12
    if i == 6: DefaultParameters.addQuantumRegister = True
    if i == 7: DefaultParameters.injectNullEffectOperation = True
    if i == 8: DefaultParameters.injectParameter = True
    if i == 9: DefaultParameters.changeDevice = True
    if i == 10: DefaultParameters.changeOptimization = True
    if i == 11: DefaultParameters.reverseWires = True
    if i == 12: DefaultParameters.reverseQubitsMultiplication = True
    runLoopThroughAllTests(0, i)  # Amplitude: 10 mutants
    runLoopThroughAllTests(1, i)  # Angle: 20 mutants
    # Reset all 12 flags
\`\`\``,
      },
      {
        id: 'run-tests-code',
        type: 'code',
        content: `from classes.default_parameters import DefaultParameters
from classes.parameters import MyParameters
import main

DefaultParameters.dataType = 0
DefaultParameters.n_folds = 5
MyParameters.resetParameters()

main.run_tests(dataset=0, kfold=5, experiment='2')`,
      },
    ],
  },
  {
    id: 'exp3',
    title: 'Kernel Testing',
    experiment: 3,
    cells: [
      {
        id: 'step2-intro',
        type: 'markdown',
        content: `## 14. Kernel Testing — Purpose

Kernel Testing isolates the quantum kernel and feature map, without the full SVM. It uses defect-based mutations and 14 metamorphic relations to evaluate how well MRs detect kernel-level bugs.`,
      },
      {
        id: 'step2-data',
        type: 'markdown',
        content: `## 15. Step 2: Data Preparation

\`step2_kernel_test.py\` loads Wine, applies StandardScaler, PCA, and produces three encodings:
- **Basis**: Binarized PCA (threshold 0)
- **Angle**: PCA components as angles
- **Amplitude**: Normalized amplitude vectors (padded to 2^n qubits)`,
      },
      {
        id: 'step2-data-code',
        type: 'code',
        content: `from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler, Binarizer
from sklearn.decomposition import PCA
import numpy as np

wine = load_wine()
mask = wine.target != 2
x_raw, y_raw = wine.data[mask], wine.target[mask]
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x_raw)
pca = PCA(n_components=4)
x_pca = pca.fit_transform(x_scaled)

DATA_BASIS = Binarizer(threshold=0.0).fit_transform(x_pca).astype(int)
DATA_ANGLE = x_pca
print("Basis shape:", DATA_BASIS.shape, "Angle shape:", DATA_ANGLE.shape)`,
      },
      {
        id: 'step2-defects',
        type: 'markdown',
        content: `## 16. Step 2: AutoMutator & Defects

\`AutoMutator\` applies a feature map under an optional defect set:
- **remove_superposition**: Skip Hadamard
- **remove_entanglement**: Skip CNOT
- **gate_error**: Flip bit (basis)
- **swap_topology**: Use SWAP instead of CNOT
- **param_noise**: Add noise to angles (angle mode)

Combinations of 1–3 defects are used.`,
      },
      {
        id: 'step2-kernel',
        type: 'markdown',
        content: `## 17. Step 2: Kernel Computation

\`qnode_omni(x1, x2, d1, d2)\`: Applies feature map on x1 with defects d1, adjoint feature map on x2 with defects d2, returns measurement probabilities. \`get_dist(x1, x2, d1, d2)\` wraps this for kernel distance.`,
      },
      {
        id: 'step2-mrs',
        type: 'markdown',
        content: `## 18. Step 2: 14 Metamorphic Relations

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
| 9 | Perturbation | K(x1+0.1,x2) ≠ K(x1,x2) |
| 10 | Drop dimension | K(x_drop,x2) vs K(x1,x2) |
| 11 | Scaling (amplitude) | K(2x1,2x2) ≈ K(x1,x2) |
| 12 | Orthogonality | K(x1,x_orth) small |
| 13 | Reversal (full) | K(x1[::-1],x2[::-1]) ≈ K(x1,x2) |
| 14 | Permutation | K invariant under wire permutation |`,
      },
      {
        id: 'step2',
        type: 'markdown',
        content: `## 19. Step 2: Execute — Full Implementation

\`run_step2_kernel_test()\` runs for basis, angle, amplitude; for each defect combo, computes gold vs mutated kernel distances; if max distance > tolerance, defect is "caught"; records per-MR detection rates. Output: \`results_v41_kernel_test.csv\`.

**Execution:** 3 modes × 25 defect combos × 100 runs = **7,500** kernel-matrix computations (or 75 if USE_FIXED_SEED). Each run: 5×5 = 25 \`get_dist\` calls.`,
      },
      {
        id: 'step2-full-impl',
        type: 'markdown',
        content: `### Full run_step2_kernel_test structure (step2_kernel_test.py ~261 lines)

**1. Data prep (lines 36-51):**
\`\`\`python
wine = load_wine()
mask = wine.target != 2
x_raw, y_raw = wine.data[mask], wine.target[mask]
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x_raw)
pca = PCA(n_components=N_QUBITS)
x_pca = pca.fit_transform(x_scaled)
DATA_BASIS = Binarizer(threshold=0.0).fit_transform(x_pca).astype(int)
DATA_ANGLE = x_pca
DATA_AMP = normalized amplitude (padded to 2^n qubits)
\`\`\`

**2. AutoMutator (lines 56-124):** apply_feature_map with defects: gate_error, param_noise, remove_superposition, remove_entanglement, swap_topology

**3. qnode_omni & get_dist (lines 131-144):** feature map on x1, adjoint on x2, return qml.probs

**4. check_mr_omni (lines 146-201):** 14 MR checks (symmetry, self-similarity, negation, shift, periodicity, rotation, reversal, complement, perturbation, drop dim, scaling, orthogonality, permutation)

**5. Execution loop (lines 223-261):**
\`\`\`python
for mode in ["basis", "angle", "amplitude"]:
    for d in combos:  # 25 defect combos
        for run in range(iterations):  # 100 or 1
            K_MUT_DIST = 5x5 get_dist matrix
            diff = max |K_GOLD - K_MUT|
            if diff > tol: caught_count += 1; check each of 14 MRs
\`\`\``,
      },
      {
        id: 'step2-code-full',
        type: 'code',
        content: `# Full Kernel Testing: inline implementation (abbreviated - run step2_kernel_test for full)
import pennylane as qml
from pennylane import numpy as np
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler, Binarizer
from sklearn.decomposition import PCA
import itertools

N_QUBITS = 4
defects = ["remove_superposition", "remove_entanglement", "gate_error", "swap_topology", "param_noise"]
combos = []
for r in range(1, 4):
    combos.extend([list(c) for c in itertools.combinations(defects, r)])
print(f"Defect combos: {len(combos)}")  # 25
print(f"Modes: basis, angle, amplitude")
print(f"Runs per mode×combo: 100 (or 1 if USE_FIXED_SEED)")
print("Execute full run: from step2_kernel_test import run_step2_kernel_test; run_step2_kernel_test()")`,
      },
      {
        id: 'step2-code',
        type: 'code',
        content: `from step2_kernel_test import run_step2_kernel_test

run_step2_kernel_test()`,
      },
    ],
  },
]

export const DEFAULT_NOTEBOOK_TABS = [
  { id: 'intro', label: 'Overview' },
  { id: 'exp1', label: 'Baseline' },
  { id: 'exp2', label: 'Statistical Testing' },
  { id: 'exp3', label: 'Kernel Testing' },
]
