# QSVM Structure Testing — Line-by-Line Code Explanation

Every line of the testing pipeline is explained below.

---

## main.py

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `from termcolor import colored` | Import `colored` for colored terminal output (green for equivalent, red for killed/survived/crashed). |
| 2 | `from classes.default_parameters import DefaultParameters` | Import global configuration class (dataset, K-fold, feature map, MR parameters). |
| 3 | `from classes.parameters import MyParameters` | Import runtime parameters, synced from DefaultParameters and reset per mutant. |
| 4 | `from classes.time import MyTimeHelper` | Import helper for timestamps (start/end of each run). |
| 5 | `import numbers` | Import `numbers` module for `isinstance(x, numbers.Number)` checks. |
| 6 | `import math` | Import `math` for `math.floor()` used when rounding scores. |
| 7 | `import argparse` | Import `argparse` for command-line argument parsing. |
| 8 | `from classes.my_dataframe_short import MyDataFrame` | Import class that formats and appends results to CSV. |
| 9 | (blank) | Blank line. |
| 10 | `myMutations = []` | Global list of mutant IDs to test; set by `runLoopThroughAllTests` (1–10 for amplitude, 11–30 for angle; Sept-style disjoint). |
| 11 | (blank) | Blank line. |
| 12 | (blank) | Blank line. |
| 13 | `def saveToDataFrame(scoreOfOriginal, scoreOfMutant, mutantNumber, typeOfMutant, tStatistic, pValue, nullHypothesisIsRejected, all_original_scores, all_mutant_scores, n_folds, featureMap, appliedMr, MrValue, startTime='', endTime=''):` | Function signature: saves one mutant result to CSV with all listed parameters. |
| 14 | `myDataFrame = MyDataFrame()` | Create a MyDataFrame instance. |
| 15 | `formattedData = myDataFrame.formatData(scoreOfOriginal, scoreOfMutant, mutantNumber, typeOfMutant, tStatistic, pValue, nullHypothesisIsRejected, all_original_scores, all_mutant_scores, n_folds, featureMap, appliedMr, MrValue, startTime, endTime)` | Convert raw values into a row format for the dataframe. |
| 16 | `myDataFrame.processToDataFrame(formattedData)` | Append the formatted row to the CSV file. |
| 17 | (blank) | Blank line. |
| 18 | `def runScript(mrNumber, mrValue):` | Define function that runs mutation testing for one MR over all mutants in `myMutations`. `mrNumber`: MR ID (1–12). `mrValue`: scaling factor, angle, etc. |
| 19 | `print(f'runScript, mrValue: {mrValue}')` | Print the current MR value to the console. |
| 20 | `myDataFrame = MyDataFrame()` | Create MyDataFrame instance (unused in this function; leftover). |
| 21 | `allMutationsScores = []` | Initialize list to hold scores from all mutants (unused; leftover). |
| 22 | `equivalentMutants = []` | Initialize list for mutant IDs classified as Equivalent. |
| 23 | `killedMutants = []` | Initialize list for mutant IDs classified as Killed. |
| 24 | `survivedMutants = []` | Initialize list for mutant IDs classified as Survived. |
| 25 | `crashedMutants = []` | Initialize list for mutant IDs classified as Crashed. |
| 26 | `equivalentMutantsScores = []` | Initialize list for scores of equivalent mutants. |
| 27 | `killedMutantsScores = []` | Initialize list for scores of killed mutants. |
| 28 | `survivedMutantsScores = []` | Initialize list for scores of survived mutants. |
| 29 | `crashedMutantsMessages = []` | Initialize list for crash messages (exception text). |
| 30 | `originalScore = 0` | Initialize variable to hold the original (mutant 0) score. |
| 31 | `firstRun = True` | Flag: True only on first iteration of the loop. |
| 32 | (blank) | Blank line. |
| 33 | `for test in myMutations:` | Loop over each mutant ID in `myMutations`. |
| 34 | `if firstRun:` | Check if this is the first iteration. |
| 35 | `DefaultParameters.testMutation = 0` | Set current mutant to 0 (original program). |
| 36 | `MyParameters.resetParameters()` | Reset runtime parameters from DefaultParameters. |
| 37 | `from main_class_manager import MainClassManager` | Import MainClassManager (lazy import). |
| 38 | `mainClassClass = MainClassManager.getMainClass()` | Get the MainClass class for the current mutant (original or m1–m30). |
| 39 | `mainClass = mainClassClass()` | Instantiate the MainClass. |
| 40 | `originalScore = mainClass.runTest(DefaultParameters.featureMapType)` | Run QSVM for the original program and store the test accuracy. |
| 41 | `print(f'originalScore: {originalScore}')` | Print the original score. |
| 42 | `firstRun = False` | Set flag so subsequent iterations skip this block. |
| 43 | (blank) | Blank line. |
| 44 | `print(colored(f'runScript,  DefaultParameters.featureMapType: {DefaultParameters.featureMapType }', 'red'))` | Print the current feature map type in red. |
| 45 | `DefaultParameters.testMutation = test` | Set the current mutant to the one being tested. |
| 46 | `MyParameters.resetParameters()` | Reset parameters for the new mutant. |
| 47 | `from main_class_manager import MainClassManager` | Re-import MainClassManager (redundant but ensures correct mutant class). |
| 48 | `mainClassClass = MainClassManager.getMainClass()` | Get the MainClass for mutant `test`. |
| 49 | `mainClass = mainClassClass()` | Instantiate it. |
| 50 | `print(colored(f'MyParameters.testMutation: {MyParameters.testMutation}', 'blue'))` | Print the current mutant ID in blue. |
| 51 | `startTime = MyTimeHelper().getTimeNow()` | Record start time. |
| 52 | `mutantScore = ''` | Initialize mutant score (string so non-numeric indicates crash). |
| 53 | (blank) | Blank line. |
| 54 | `try:` | Begin try block to catch exceptions. |
| 55 | `startTime = MyTimeHelper().getTimeNow()` | Re-record start time (redundant). |
| 56 | `mutantScore = mainClass.runTest(DefaultParameters.featureMapType)` | Run QSVM for the mutant and get its score. |
| 57 | `roundingNumber = 1000` | Factor for rounding (3 decimal places). |
| 58 | `originalScore = math.floor(originalScore * roundingNumber) / roundingNumber` | Round original score to 3 decimal places. |
| 59 | `mutantScore = math.floor(mutantScore * roundingNumber) / roundingNumber` | Round mutant score to 3 decimal places. |
| 60 | (blank) | Blank line. |
| 61 | `if mutantScore == originalScore:` | Check if scores are equal (Equivalent mutant). |
| 62 | `equivalentMutants.append(test)` | Add mutant ID to equivalent list. |
| 63 | `equivalentMutantsScores.append(mutantScore)` | Add score to equivalent scores list. |
| 64 | `print(colored(f'for mutation: {test}, original score: {originalScore} == mutation score: {mutantScore}', 'green'))` | Print equivalent result in green. |
| 65 | `endTime = MyTimeHelper().getTimeNow()` | Record end time. |
| 66 | `saveToDataFrame(originalScore, mutantScore, test, MyParameters.mutantTypes[0], '-', '-', '-', '-', '-', 0, 0, '-', '-', startTime, endTime)` | Save result with type 'Equivalent' (index 0). |
| 67 | `elif isinstance(mutantScore, numbers.Number):` | Else if mutant score is a valid number (different from original). |
| 68 | `print(colored(f'for mutation: {test}, original score: {originalScore}!= mutation score: {mutantScore}', 'red'))` | Print that scores differ in red. |
| 69 | `print(colored(f'start statistical testing', 'red'))` | Print that statistical testing is starting. |
| 70 | `from main_statistical_class_manager import MainStatisticalClassManager` | Import MainStatisticalClassManager. |
| 71 | `mainStatisticalClassClass = MainStatisticalClassManager.getMainStatisticalClass()` | Get the MainStatisticalClass for the current mutant. |
| 72 | `mainStatisticalClass = mainStatisticalClassClass()` | Instantiate it. |
| 73 | `allScoresOfOriginal, allScoresOfMutant, tStatistic, pValue = mainStatisticalClass.runTest(mrNumber, mrValue)` | Run K-fold with MR; get original scores, mutant scores, t-statistic, p-value. |
| 74 | (blank) | Blank line. |
| 75 | `if pValue < 0.05:` | If p-value is below 0.05, reject null hypothesis → Killed. |
| 76 | `killedMutants.append(test)` | Add mutant to killed list. |
| 77 | `killedMutantsScores.append(mutantScore)` | Add score to killed scores list. |
| 78 | `endTime = MyTimeHelper().getTimeNow()` | Record end time. |
| 79 | `saveToDataFrame(originalScore, mutantScore, test, MyParameters.mutantTypes[1], tStatistic, pValue, 'Yes', allScoresOfOriginal, allScoresOfMutant, MyParameters.n_folds, 0, MyParameters.mrUsed, mrValue, startTime, endTime)` | Save with type 'Killed' (index 1). |
| 80 | `else:` | Else p-value >= 0.05 → Survived. |
| 81 | `survivedMutants.append(test)` | Add mutant to survived list. |
| 82 | `survivedMutantsScores.append(mutantScore)` | Add score to survived scores list. |
| 83 | `endTime = MyTimeHelper().getTimeNow()` | Record end time. |
| 84 | `saveToDataFrame(originalScore, mutantScore, test, MyParameters.mutantTypes[2], tStatistic, pValue, 'No', allScoresOfOriginal, allScoresOfMutant, MyParameters.n_folds, 0, MyParameters.mrUsed, MyParameters.scaleValue, startTime, endTime)` | Save with type 'Survived' (index 2). |
| 85 | `else:` | Else mutant score is not a number (e.g. exception message) → Crashed. |
| 86 | `print(colored(f'for mutation: {test}, original score: {originalScore} != crashed mutation: {mutantScore}', 'red'))` | Print crashed result in red. |
| 87 | `crashedMutants.append(test)` | Add mutant to crashed list. |
| 88 | `crashedMutantsMessages.append(mutantScore)` | Add crash message. |
| 89 | `endTime = MyTimeHelper().getTimeNow()` | Record end time. |
| 90 | `saveToDataFrame(originalScore, mutantScore, test, MyParameters.mutantTypes[3], '-', '-', '-', '-', '-', 0, 0, '-', '-', startTime, endTime)` | Save with type 'Crashed' (index 3). |
| 91 | `except Exception as error:` | Catch any exception during mutant execution. |
| 92 | `print(colored(f'for mutation: {test}, original score: {originalScore} != crashed mutation: {mutantScore}', 'red'))` | Print crashed result in red. |
| 93 | `crashedMutants.append(test)` | Add mutant to crashed list. |
| 94 | `mutantScore = error` | Store the exception as mutant score. |
| 95 | `crashedMutantsMessages.append(mutantScore)` | Add exception to crashed messages. |
| 96 | `endTime = MyTimeHelper().getTimeNow()` | Record end time. |
| 97 | `saveToDataFrame(originalScore, mutantScore, test, MyParameters.mutantTypes[3], '-', '-', '-', '-', '-', 0, 0, '-', '-', startTime, endTime)` | Save with type 'Crashed'. |
| 98 | `print(f'exception: {error}')` | Print the exception. |
| 99 | (blank) | Blank line. |
| 100 | (blank) | Blank line. |
| 101 | (blank) | Blank line. |
| 102 | `def runLoopThroughAllTests(typeOfFeatureMap, mrUsed):` | Define function. `typeOfFeatureMap`: 0=angle, 1=amplitude. `mrUsed`: MR ID (1–12). |
| 103 | `global myMutations` | Declare that we will modify the global `myMutations`. |
| 104 | `DefaultParameters.mrUsed = mrUsed` | Set the MR ID in global config. |
| 105 | `DefaultParameters.featureMapType = typeOfFeatureMap` | Set the feature map type. |
| 106 | `mrValue = 1` | Default MR parameter value. |
| 107 | (blank) | Blank line. |
| 108 | `if mrUsed == 1 or mrUsed == 3 or mrUsed == 4:` | MRs 1, 3, 4 use scaling factor. |
| 109 | `print(f'main runLoopThroughAllTests, mrUsed == 1  \| mrUsed == 3 \| mrUsed == 4')` | Print which MR branch. |
| 110 | `mrValue = MyParameters.scaleValue` | Use scale value from parameters. |
| 111 | `elif mrUsed == 2:` | MR 2 uses angle. |
| 112 | `mrValue = MyParameters.angle` | Use angle from parameters. |
| 113 | `print(f'main runLoopThroughAllTests, mrUsed == 2 mrValue = {mrValue}')` | Print angle value. |
| 114 | `elif mrUsed == 5:` | MR 5 uses input duplication. |
| 115 | `mrValue = MyParameters.inputToDuplicate` | Use input-to-duplicate index. |
| 116 | `print(f'main runLoopThroughAllTests, mrUsed == 5')` | Print MR 5 branch. |
| 117 | `else:` | MRs 6–12 (other branches). |
| 118 | `print(f'main runLoopThroughAllTests, else')` | Print else branch. |
| 119 | (blank) | Blank line. |
| 120 | `allMutants = list(range(1, 31))` | Create list [1,2,...,30] (unused variable). |
| 121 | `if typeOfFeatureMap == 0:` | If angle embedding. |
| 122 | `myMutations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` | Set mutants to amplitude mutants 1–10 (Sept-style). |
| 123 | `runScript(mrNumber=DefaultParameters.mrUsed, mrValue=mrValue)` | Run mutation testing for amplitude. |
| 124 | `else:` | If angle embedding. |
| 125 | `myMutations = [11, 12, ..., 30]` | Set mutants to angle mutants 11–30 (Sept-style, disjoint). |
| 126 | `runScript(mrNumber=DefaultParameters.mrUsed, mrValue=mrValue)` | Run mutation testing for amplitude. |
| 127 | (blank) | Blank line. |
| 128 | (blank) | Blank line. |
| 129 | `def run_tests(dataset=None, kfold=None):` | Main pipeline entry. Optional dataset (0–3) and kfold. |
| 130 | `if dataset is not None:` | If dataset was provided. |
| 131 | `DefaultParameters.dataType = dataset` | Set dataset type in config. |
| 132 | `if kfold is not None:` | If kfold was provided. |
| 133 | `DefaultParameters.n_folds = kfold` | Set K-fold in config. |
| 134 | `MyParameters.resetParameters()` | Reset runtime parameters. |
| 135 | (blank) | Blank line. |
| 136 | `for i in range(1, 13):` | Loop over MRs 1 through 12. |
| 137 | `print(f'mr number: {i}')` | Print current MR number. |
| 138 | (blank) | Blank line. |
| 139 | `if i == 6:` | MR 6: add quantum register. |
| 140 | `DefaultParameters.addQuantumRegister = True` | Enable flag. |
| 141 | `MyParameters.resetParameters()` | Reset parameters. |
| 142 | `if i == 7:` | MR 7: inject null-effect operation. |
| 143 | `DefaultParameters.injectNullEffectOperation = True` | Enable flag. |
| 144 | `MyParameters.resetParameters()` | Reset parameters. |
| 145 | `if i == 8:` | MR 8: inject parameter. |
| 146 | `DefaultParameters.injectParameter = True` | Enable flag. |
| 147 | `MyParameters.resetParameters()` | Reset parameters. |
| 148 | `if i == 9:` | MR 9: change device. |
| 149 | `DefaultParameters.changeDevice = True` | Enable flag. |
| 150 | `MyParameters.resetParameters()` | Reset parameters. |
| 151 | `if i == 10:` | MR 10: change optimization. |
| 152 | `DefaultParameters.changeOptimization = True` | Enable flag. |
| 153 | `MyParameters.resetParameters()` | Reset parameters. |
| 154 | `if i == 11:` | MR 11: reverse wires. |
| 155 | `DefaultParameters.reverseWires = True` | Enable flag. |
| 156 | `MyParameters.resetParameters()` | Reset parameters. |
| 157 | `if i == 12:` | MR 12: reverse qubit multiplication. |
| 158 | `DefaultParameters.reverseQubitsMultiplication = True` | Enable flag. |
| 159 | `MyParameters.resetParameters()` | Reset parameters. |
| 160 | `if i == 13:` | MR 13: check symmetry (not in loop range 1–12; dead code). |
| 161 | `DefaultParameters.checkSymmetry = True` | Enable flag. |
| 162 | `MyParameters.resetParameters()` | Reset parameters. |
| 163 | `if i == 14:` | MR 14: check same-input symmetry (dead code). |
| 164 | `DefaultParameters.checkSameInputSymmetry = True` | Enable flag. |
| 165 | `MyParameters.resetParameters()` | Reset parameters. |
| 166 | `if i == 15:` | MR 15: check scaling invariance (dead code). |
| 167 | `DefaultParameters.checkScalingInvariance = True` | Enable flag. |
| 168 | `MyParameters.resetParameters()` | Reset parameters. |
| 169 | `if i == 16:` | MR 16: check adding periodicity. |
| 170 | `DefaultParameters.checkAddingPeriodicity = True` | Enable flag. |
| 171 | `if i == 17:` | MR 17: check shifting invariance. |
| 172 | `DefaultParameters.checkShiftingInvariance = True` | Enable flag. |
| 173 | `MyParameters.resetParameters()` | Reset parameters. |
| 174 | (blank) | Blank line. |
| 175 | `runLoopThroughAllTests(0, i)` | Run angle embedding for MR i. |
| 176 | `runLoopThroughAllTests(1, i)` | Run amplitude embedding for MR i. |
| 177 | (blank) | Blank line. |
| 178 | `DefaultParameters.addQuantumRegister = False` | Reset MR 6 flag. |
| 179 | `DefaultParameters.injectNullEffectOperation = False` | Reset MR 7 flag. |
| 180 | `DefaultParameters.injectParameter = False` | Reset MR 8 flag. |
| 181 | `DefaultParameters.changeDevice = False` | Reset MR 9 flag. |
| 182 | `DefaultParameters.changeOptimization = False` | Reset MR 10 flag. |
| 183 | `DefaultParameters.reverseWires = False` | Reset MR 11 flag. |
| 184 | `DefaultParameters.reverseQubitsMultiplication = False` | Reset MR 12 flag. |
| 185 | `DefaultParameters.checkSymmetry = False` | Reset MR 13 flag. |
| 186 | `DefaultParameters.checkSameInputSymmetry = False` | Reset MR 14 flag. |
| 187 | `DefaultParameters.checkScalingInvariance = False` | Reset MR 15 flag. |
| 188 | `DefaultParameters.checkAddingPeriodicity = False` | Reset MR 16 flag. |
| 189 | `DefaultParameters.checkShiftingInvariance = False` | Reset MR 17 flag. |
| 190 | `MyParameters.resetParameters()` | Reset parameters. |
| 191 | (blank) | Blank line. |
| 192 | `print(f"\n{'='*60}")` | Print separator line of 60 equals signs. |
| 193 | `print("Starting Step 2: Kernel Testing (defect-based, 14 MRs)")` | Print Step 2 header. |
| 194 | `print(f"{'='*60}")` | Print separator. |
| 195 | `from step2_kernel_test import run_step2_kernel_test` | Import Step 2 function. |
| 196 | `run_step2_kernel_test()` | Execute Step 2 kernel testing. |
| 197 | (blank) | Blank line. |
| 198 | (blank) | Blank line. |
| 199 | `if __name__ == "__main__":` | Only run when script is executed directly (not imported). |
| 200 | `parser = argparse.ArgumentParser(description="QSVM Structure Testing")` | Create argument parser. |
| 201 | `parser.add_argument("--dataset", type=int, default=None, choices=[0, 1, 2, 3], help="0=Wine, 1=Load Digits, 2=Credit Card, 3=MNIST")` | Add --dataset argument. |
| 202 | `parser.add_argument("--kfold", type=int, default=None, help="K-fold value for Step 1 (default: 5)")` | Add --kfold argument. |
| 203 | `args = parser.parse_args()` | Parse command-line arguments. |
| 204 | `run_tests(dataset=args.dataset, kfold=args.kfold)` | Call main pipeline with parsed args. |

---

## main_class.py

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `import sys` | Import sys for path manipulation. |
| 2 | (blank) | Blank line. |
| 3 | `from classes.time import MyTimeHelper` | Import timestamp helper. |
| 4 | (blank) | Blank line. |
| 5 | `from pennylane import numpy as np` | Import PennyLane's numpy for quantum array ops. |
| 6 | (blank) | Blank line. |
| 7 | `from data.data_manager import DataManager` | Import data loader. |
| 8 | (blank) | Blank line. |
| 9 | `# from quantum.q_kernel import Qkernel` | Commented-out direct Qkernel import. |
| 10 | (blank) | Blank line. |
| 11 | `from quantum.q_kernel_manager import QKernelManager` | Import kernel manager (mutant-aware). |
| 12 | (blank) | Blank line. |
| 13 | `# from quantum.feature_map import FeatureMap` | Commented-out direct FeatureMap import. |
| 14 | (blank) | Blank line. |
| 15 | `from quantum.feature_map_manager import FeatureMapManager` | Import feature map manager (mutant-aware). |
| 16 | (blank) | Blank line. |
| 17 | `from sklearn.svm import SVC` | Import SVM with precomputed kernel. |
| 18 | (blank) | Blank line. |
| 19 | `from sklearn.model_selection import train_test_split` | Import train/test split. |
| 20 | (blank) | Blank line. |
| 21 | `from sklearn.model_selection import KFold` | Import K-fold (unused in MainClass). |
| 22 | (blank) | Blank line. |
| 23 | `from scipy.stats import ttest_ind` | Import t-test (unused in MainClass). |
| 24 | (blank) | Blank line. |
| 25 | (blank) | Blank line. |
| 26 | `from metamorphic.my_metamorphic_relations import MyMetamorphicRelations` | Import MR application class. |
| 27 | (blank) | Blank line. |
| 28 | `sys.path.insert(0, './data')` | Add ./data to Python path. |
| 29 | `sys.path.insert(0, './quantum')` | Add ./quantum to Python path. |
| 30 | (blank) | Blank line. |
| 31 | `class MainClass:` | Define MainClass for QSVM execution. |
| 32 | (blank) | Blank line. |
| 33 | `# qKernel = Qkernel()` | Commented-out class attribute. |
| 34 | (blank) | Blank line. |
| 35 | `# featureMap = FeatureMap()` | Commented-out class attribute. |
| 36 | (blank) | Blank line. |
| 37 | (blank) | Blank line. |
| 38 | `def run_qsvm(x_padded, y, n_qubits, scaling_factor,featureMap, featureMapType = 0):` | Static method: run QSVM. Parameters: padded features, labels, qubit count, scaling, feature map instance, type. |
| 39 | (blank) | Blank line. |
| 40 | (blank) | Blank line. |
| 41 | `#run_qsvm, MainClass.featureMap: ...` | Commented debug print. |
| 42 | `# print(f'run_qsvm, MainClass.featureMap: {MainClass.featureMap}')` | Commented debug print. |
| 43 | `# print(f'scaling_factor: {scaling_factor}')` | Commented debug print. |
| 44 | (blank) | Blank line. |
| 45 | (blank) | Blank line. |
| 46 | (blank) | Blank line. |
| 47 | `# print(f'run_qsvm, x_padded: {x_padded}')` | Commented debug print. |
| 48 | (blank) | Blank line. |
| 49 | `# x_data_to_use= MyMetamorphicRelations.useMetamorphicRelation(x_padded, 1, scaling_factor)` | Commented MR application. |
| 50 | (blank) | Blank line. |
| 51 | `x_data_to_use= x_padded` | Use padded data as-is (no MR in this path). |
| 52 | (blank) | Blank line. |
| 53 | `# y_data_to_use = MyMetamorphicRelations.useMetamorphicRelation(y, 1, scaling_factor)` | Commented label MR. |
| 54 | `y_data_to_use = y` | Use labels as-is. |
| 55 | (blank) | Blank line. |
| 56 | `# print(f'run_qsvm, x_data_to_use: {x_data_to_use}')` | Commented debug print. |
| 57 | `# print(f'run_qsvm, y_data_to_use: {y_data_to_use}')` | Commented debug print. |
| 58 | (blank) | Blank line. |
| 59 | `x_train, x_test, y_train, y_test = train_test_split(` | Begin train_test_split call. |
| 60 | `x_data_to_use, y_data_to_use, test_size=0.2,  random_state=42` | Split 80/20 with fixed seed. |
| 61 | `)` | End call. |
| 62 | (blank) | Blank line. |
| 63 | `#3 run training` | Comment: run training. |
| 64 | (blank) | Blank line. |
| 65 | `# print(f'run_qsvm, n_qubits: {n_qubits}')` | Commented debug print. |
| 66 | (blank) | Blank line. |
| 67 | `kernel_train = featureMap.compute_kernel_matrix(x_train, x_train, n_qubits, featureMapType)` | Compute kernel matrix for training data. |
| 68 | (blank) | Blank line. |
| 69 | `kernel_test = featureMap.compute_kernel_matrix(x_test, x_train, n_qubits, featureMapType)` | Compute kernel matrix for test vs train. |
| 70 | (blank) | Blank line. |
| 71 | `svm = SVC(kernel='precomputed')` | Create SVM that expects precomputed kernel. |
| 72 | `svm.fit(kernel_train, y_train)` | Train SVM on kernel and labels. |
| 73 | (blank) | Blank line. |
| 74 | `test_score = svm.score(kernel_test, y_test)` | Evaluate on test set. |
| 75 | (blank) | Blank line. |
| 76 | `return test_score` | Return test accuracy. |
| 77 | (blank) | Blank line. |
| 78 | `def runTest(self, featureMapType = 0):` | Instance method: run QSVM for current mutant. |
| 79 | (blank) | Blank line. |
| 80 | `from classes.parameters import MyParameters` | Import MyParameters (lazy import). |
| 81 | (blank) | Blank line. |
| 82 | `dataManager = DataManager()` | Create data manager. |
| 83 | (blank) | Blank line. |
| 84 | `featureMapClass = FeatureMapManager().getFeatureMap()` | Get feature map class for current mutant. |
| 85 | `featureMap = featureMapClass()` | Instantiate feature map. |
| 86 | (blank) | Blank line. |
| 87 | `qKernelClass = QKernelManager().getqKernel()` | Get kernel class for current mutant. |
| 88 | `qKernel = qKernelClass()` | Instantiate kernel. |
| 89 | (blank) | Blank line. |
| 90 | `# print(f'runTest, featureMap: {featureMap}')` | Commented debug print. |
| 91 | `#1 get Data` | Comment: get data. |
| 92 | `x,y, x_normalized = dataManager.getData(MyParameters.dataType)` | Load dataset (x, y, normalized x). |
| 93 | (blank) | Blank line. |
| 94 | `# print(f'len(x_normalized): {len(x_normalized)}')` | Commented debug print. |
| 95 | `# print(f'len(y): {len(y)}')` | Commented debug print. |
| 96 | (blank) | Blank line. |
| 97 | `y = y` | No-op (leftover). |
| 98 | (blank) | Blank line. |
| 99 | `#2 get features and nqubits and add padding` | Comment: get features and padding. |
| 100 | (blank) | Blank line. |
| 101 | `n_features, n_qubits = qKernel.getFeaturesAndNqubits(x_normalized, featureMapType)` | Get feature count and qubit count. |
| 102 | (blank) | Blank line. |
| 103 | `print(f'main_class, n_qubits: {n_qubits}')` | Print qubit count. |
| 104 | (blank) | Blank line. |
| 105 | `# np.set_printoptions(threshold=np.inf)` | Commented print options. |
| 106 | `# print(f'x: \n{x}')` | Commented debug print. |
| 107 | (blank) | Blank line. |
| 108 | `# print(f'x_normalized: \n{x_normalized}')` | Commented debug print. |
| 109 | (blank) | Blank line. |
| 110 | `x_padded = x_normalized` | Default: use normalized as padded. |
| 111 | (blank) | Blank line. |
| 112 | `if(featureMapType == 0):` | If angle embedding. |
| 113 | `x_padded = qKernel.pad_features(x_normalized, n_qubits)` | Pad features for angle encoding. |
| 114 | (blank) | Blank line. |
| 115 | `# x_data_to_use= MyMetamorphicRelations.useMetamorphicRelation(x_padded, 1, mrValue)` | Commented MR application. |
| 116 | (blank) | Blank line. |
| 117 | `MyParameters.amplitudeNQubits = n_qubits` | Store qubit count in parameters. |
| 118 | (blank) | Blank line. |
| 119 | (blank) | Blank line. |
| 120 | `score_original = MainClass.run_qsvm(x_padded, y, n_qubits, 1.0, featureMap, featureMapType)` | Run QSVM with scaling 1.0. |
| 121 | (blank) | Blank line. |
| 122 | `# score_scaled = MainClass.run_qsvm(x_padded, y, n_qubits, mrValue, featureMap, featureMapType)` | Commented scaled run. |
| 123 | (blank) | Blank line. |
| 124 | `# return score_original, score_scaled` | Commented alternative return. |
| 125 | (blank) | Blank line. |
| 126 | `return score_original` | Return single score. |
| 127 | (blank) | Blank line. |
| 128 | `print(f'score_original: {score_original}')` | Unreachable (after return). |
| 129 | (blank) | Blank line. |
| 130 | `print(f'score_scaled: {score_scaled}')` | Unreachable (after return). |

---

## main_statistical_class.py

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `import sys` | Import sys. |
| 2 | (blank) | Blank line. |
| 3 | `from classes.time import MyTimeHelper` | Import timestamp helper. |
| 4 | (blank) | Blank line. |
| 5 | `from pennylane import numpy as np` | Import PennyLane numpy. |
| 6 | (blank) | Blank line. |
| 7 | `from data.data_manager import DataManager` | Import data manager. |
| 8 | (blank) | Blank line. |
| 9 | `# from quantum.q_kernel import QKernel` | Commented import. |
| 10 | (blank) | Blank line. |
| 11 | `from quantum.q_kernel_manager import QKernelManager` | Import kernel manager. |
| 12 | (blank) | Blank line. |
| 13 | `# from quantum.feature_map import FeatureMap` | Commented import. |
| 14 | (blank) | Blank line. |
| 15 | `from quantum.feature_map_manager import FeatureMapManager` | Import feature map manager. |
| 16 | (blank) | Blank line. |
| 17 | `from sklearn.svm import SVC` | Import SVM. |
| 18 | (blank) | Blank line. |
| 19 | `from sklearn.model_selection import KFold` | Import K-fold. |
| 20 | (blank) | Blank line. |
| 21 | `from scipy.stats import ttest_ind` | Import independent t-test. |
| 22 | (blank) | Blank line. |
| 23 | `from classes.parameters import MyParameters` | Import MyParameters. |
| 24 | (blank) | Blank line. |
| 25 | `from metamorphic.my_metamorphic_relations import MyMetamorphicRelations` | Import MR class. |
| 26 | (blank) | Blank line. |
| 27 | `from termcolor import colored` | Import colored (unused). |
| 28 | (blank) | Blank line. |
| 29 | `sys.path.insert(0, './data')` | Add ./data to path. |
| 30 | `sys.path.insert(0, './quantum')` | Add ./quantum to path. |
| 31 | (blank) | Blank line. |
| 32 | `class MainStatisticalClass:` | Define statistical testing class. |
| 33 | (blank) | Blank line. |
| 34 | (blank) | Blank line. |
| 35 | `# dataManager = DataManager()` | Commented class attribute. |
| 36 | (blank) | Blank line. |
| 37 | `# qKernel = QKernel()` | Commented class attribute. |
| 38 | (blank) | Blank line. |
| 39 | (blank) | Blank line. |
| 40 | `# featureMap = FeatureMap()` | Commented class attribute. |
| 41 | (blank) | Blank line. |
| 42 | `def run_qsvm_with_kfold(x_padded, y, mrNumber, n_qubits, mrValue, featureMap):` | Static method: K-fold QSVM with MR. |
| 43 | (blank) | Blank line. |
| 44 | `print(f"\nRunning evaluation with mrValue = {mrValue}, mrNumber: {mrNumber}")` | Print evaluation params. |
| 45 | (blank) | Blank line. |
| 46 | (blank) | Blank line. |
| 47 | `# x_data_to_use = x_padded * scaling_factor` | Commented scaling. |
| 48 | (blank) | Blank line. |
| 49 | `# print(f'1-- x_data_to_use: {x_data_to_use}')` | Commented debug print. |
| 50 | (blank) | Blank line. |
| 51 | `if mrValue == 1.0:` | If no MR scaling (original). |
| 52 | `print(f'MainStatisticalClass -  run_qsvm_with_kfold, scaling_factor == 1.0')` | Print no-scaling branch. |
| 53 | `x_data_to_use = x_padded` | Use data as-is. |
| 54 | (blank) | Blank line. |
| 55 | `elif mrNumber == 4:` | MR 4: invert labels. |
| 56 | (blank) | Blank line. |
| 57 | `x_data_to_use = x_padded` | Use x as-is. |
| 58 | (blank) | Blank line. |
| 59 | `x_data_to_use, y = MyMetamorphicRelations.useMetamorphicRelation(x_padded, y, mrNumber, 2)` | Apply MR 4 with value 2. |
| 60 | (blank) | Blank line. |
| 61 | `else:` | Other MRs. |
| 62 | `print(f'MainStatisticalClass -  run_qsvm_with_kfold, else: mrNumber = {mrNumber}, mrValue{mrValue}')` | Print else branch (typo: missing space before mrValue). |
| 63 | (blank) | Blank line. |
| 64 | `x_data_to_use, y = MyMetamorphicRelations.useMetamorphicRelation(x_padded, y, mrNumber, mrValue)` | Apply MR. |
| 65 | (blank) | Blank line. |
| 66 | `# print(f'2-- x_data_to_use: {x_data_to_use}')` | Commented debug print. |
| 67 | (blank) | Blank line. |
| 68 | (blank) | Blank line. |
| 69 | `# return` | Commented early return. |
| 70 | (blank) | Blank line. |
| 71 | (blank) | Blank line. |
| 72 | `n_splits = MyParameters.n_folds` | Get K from parameters. |
| 73 | `kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)` | Create K-fold splitter. |
| 74 | (blank) | Blank line. |
| 75 | `test_scores = []` | List for fold scores. |
| 76 | `fold_number = 1` | Fold counter. |
| 77 | (blank) | Blank line. |
| 78 | `firstTime = True` | Flag: only run first fold. |
| 79 | (blank) | Blank line. |
| 80 | `for train_index, test_index in kf.split(x_data_to_use):` | Loop over K-fold splits. |
| 81 | `print(f"\n{'='*15} FOLD {fold_number}/{n_splits} {'='*15}")` | Print fold header. |
| 82 | (blank) | Blank line. |
| 83 | `if firstTime == True:` | If first fold. |
| 84 | `firstTime = False` | Set flag to False. |
| 85 | `else:` | Else (subsequent folds). |
| 86 | `continue` | Skip; only first fold is executed. |
| 87 | (blank) | Blank line. |
| 88 | `x_train, x_test = x_data_to_use[train_index], x_data_to_use[test_index]` | Split data by indices. |
| 89 | `y_train, y_test = y[train_index], y[test_index]` | Split labels. |
| 90 | (blank) | Blank line. |
| 91 | `kernel_train = featureMap.compute_kernel_matrix(x_train, x_train, n_qubits, MyParameters.featureMapType)` | Compute train kernel. |
| 92 | (blank) | Blank line. |
| 93 | `kernel_test = featureMap.compute_kernel_matrix(x_test, x_train, n_qubits, MyParameters.featureMapType)` | Compute test kernel. |
| 94 | (blank) | Blank line. |
| 95 | `print("\nTraining SVM...")` | Print training message. |
| 96 | `svm = SVC(kernel='precomputed')` | Create SVM. |
| 97 | `svm.fit(kernel_train, y_train)` | Train SVM. |
| 98 | (blank) | Blank line. |
| 99 | `test_score = svm.score(kernel_test, y_test)` | Evaluate on test fold. |
| 100 | `test_scores.append(test_score)` | Append score. |
| 101 | (blank) | Blank line. |
| 102 | `print(f"Fold {fold_number} Test Accuracy: {test_score:.4f}")` | Print fold accuracy. |
| 103 | `fold_number += 1` | Increment fold counter. |
| 104 | (blank) | Blank line. |
| 105 | `print(f"\n{'='*15} Cross-Validation Summary (mrValue={mrValue}) {'='*15}")` | Print summary header. |
| 106 | `mean_accuracy = np.mean(test_scores)` | Compute mean of fold scores. |
| 107 | `std_accuracy = np.std(test_scores)` | Compute std of fold scores. |
| 108 | (blank) | Blank line. |
| 109 | `print(f"Scores for each fold: {[f'{score:.4f}' for score in test_scores]}")` | Print fold scores. |
| 110 | `print(f"\nMean Test Accuracy: {mean_accuracy:.4f}")` | Print mean. |
| 111 | `print(f"Standard Deviation: {std_accuracy:.4f}")` | Print std. |
| 112 | (blank) | Blank line. |
| 113 | `return test_scores` | Return list of fold scores. |
| 114 | (blank) | Blank line. |
| 115 | (blank) | Blank line. |
| 116 | `def runTest(self, mrNumber, mrValue):` | Instance method: run statistical test. |
| 117 | (blank) | Blank line. |
| 118 | `# print(colored(...))` | Commented debug print. |
| 119 | (blank) | Blank line. |
| 120 | `dataManager = DataManager()` | Create data manager. |
| 121 | (blank) | Blank line. |
| 122 | `# qKernel = QKernel()` | Commented. |
| 123 | (blank) | Blank line. |
| 124 | `featureMapClass = FeatureMapManager().getFeatureMap()` | Get feature map class. |
| 125 | `featureMap = featureMapClass()` | Instantiate. |
| 126 | (blank) | Blank line. |
| 127 | `qKernelClass = QKernelManager().getqKernel()` | Get kernel class. |
| 128 | `qKernel = qKernelClass()` | Instantiate. |
| 129 | (blank) | Blank line. |
| 130 | `# print(f'featureMap: {featureMap}')` | Commented. |
| 131 | `#1 get Data` | Comment. |
| 132 | `x,y, x_normalized = dataManager.getData(MyParameters.dataType)` | Load data. |
| 133 | (blank) | Blank line. |
| 134 | `#2 get features and nqubits and add padding` | Comment. |
| 135 | (blank) | Blank line. |
| 136 | (blank) | Blank line. |
| 137 | `# return` | Commented return. |
| 138 | (blank) | Blank line. |
| 139 | `n_features, n_qubits = qKernel.getFeaturesAndNqubits(x_normalized, MyParameters.featureMapType)` | Get feature count and qubits. |
| 140 | (blank) | Blank line. |
| 141 | `# print(f'n_qubits: {n_qubits}')` | Commented. |
| 142 | (blank) | Blank line. |
| 143 | `# np.set_printoptions(threshold=np.inf)` | Commented. |
| 144 | `# print(f'x: \n{x}')` | Commented. |
| 145 | (blank) | Blank line. |
| 146 | `# print(f'x_normalized: \n{x_normalized}')` | Commented. |
| 147 | (blank) | Blank line. |
| 148 | `x_padded = x_normalized` | Default padded = normalized. |
| 149 | (blank) | Blank line. |
| 150 | `if(MyParameters.featureMapType == 0):` | If angle. |
| 151 | `x_padded = qKernel.pad_features(x_normalized, n_qubits)` | Pad for angle. |
| 152 | (blank) | Blank line. |
| 153 | `MyParameters.amplitudeNQubits = n_qubits` | Store qubit count. |
| 154 | (blank) | Blank line. |
| 155 | `#3 run tests` | Comment. |
| 156 | (blank) | Blank line. |
| 157 | `scores_original = MainStatisticalClass.run_qsvm_with_kfold(x_padded, y, mrNumber, n_qubits, 1.0, featureMap)` | Run with mrValue=1.0 (no MR). |
| 158 | (blank) | Blank line. |
| 159 | `scores_scaled = MainStatisticalClass.run_qsvm_with_kfold(x_padded, y, mrNumber, n_qubits, mrValue, featureMap)` | Run with MR applied. |
| 160 | (blank) | Blank line. |
| 161 | `t_statistic, p_value = ttest_ind(scores_original, scores_scaled)` | Independent t-test. |
| 162 | (blank) | Blank line. |
| 163 | `print(f"\nIndependent t-test results:")` | Print header. |
| 164 | `print(f"T-statistic: {t_statistic:.4f}")` | Print t-stat. |
| 165 | `print(f"P-value: {p_value:.4f}")` | Print p-value. |
| 166 | (blank) | Blank line. |
| 167 | `alpha = 0.05` | Significance level. |
| 168 | `if p_value > alpha:` | If we do not reject null. |
| 169 | `print(f"\nSince the p-value ({p_value:.4f}) is greater than {alpha}, we do not reject the null hypothesis.")` | Print interpretation. |
| 170 | `print("This suggests that there is no statistically significant difference between the accuracies of the original and scaled data.")` | Print interpretation. |
| 171 | `print("The metamorphic relation holds, as expected, because AmplitudeEmbedding normalizes the input vectors, making the kernel invariant to the input vector's norm.")` | Print MR interpretation. |
| 172 | `else:` | Else we reject null. |
| 173 | `print(f"\nSince the p-value ({p_value:.4f}) is less than {alpha}, we reject the null hypothesis.")` | Print rejection. |
| 174 | `print("This suggests that there is a statistically significant difference between the accuracies, which is unexpected and may indicate an issue.")` | Print interpretation. |
| 175 | (blank) | Blank line. |
| 176 | `return scores_original, scores_scaled, t_statistic, p_value` | Return all results. |
| 177 | (blank) | Blank line. |

---

## step2_kernel_test.py — Line-by-Line

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `"""` | Start of docstring. |
| 2 | `Step 2: Kernel Testing (February main41 logic).` | Docstring: description. |
| 3 | `Defect-based mutation testing with 14 metamorphic relations.` | Docstring: defect-based, 14 MRs. |
| 4 | `Runs after Step 1 (September-style mutant testing).` | Docstring: runs after Step 1. |
| 5 | `"""` | End of docstring. |
| 6 | (blank) | Blank line. |
| 7 | `import pennylane as qml` | Import PennyLane. |
| 8 | `from pennylane import numpy as np` | Import PennyLane numpy. |
| 9 | `import pandas as pd` | Import pandas for DataFrame. |
| 10 | `from sklearn.datasets import load_wine` | Import Wine dataset. |
| 11 | `from sklearn.preprocessing import StandardScaler, Binarizer` | Import scaler and binarizer. |
| 12 | `from sklearn.decomposition import PCA` | Import PCA. |
| 13 | `from tqdm import tqdm` | Import progress bar. |
| 14 | `import random` | Import random. |
| 15 | `import itertools` | Import itertools for combinations. |
| 16 | `import warnings` | Import warnings. |
| 17 | (blank) | Blank line. |
| 18 | `# ==========================================` | Comment: section header. |
| 19 | `# CONFIGURATION` | Comment. |
| 20 | `# ==========================================` | Comment. |
| 21 | `USE_FIXED_SEED = False` | If True, use fixed seed; else random. |
| 22 | `NUM_RUNS = 100` | Number of runs per defect combo. |
| 23 | `N_QUBITS = 4` | Number of qubits. |
| 24 | `FILE_RESULTS = "results_v41_kernel_test.csv"` | Output filename. |
| 25 | `TOL_IDEAL = 1e-6` | Tolerance for basis/angle modes. |
| 26 | `TOL_AMP = 1e-8` | Tolerance for amplitude mode. |
| 27 | (blank) | Blank line. |
| 28 | `warnings.filterwarnings("ignore")` | Suppress warnings. |
| 29 | (blank) | Blank line. |
| 30 | (blank) | Blank line. |
| 31 | `def run_step2_kernel_test():` | Main Step 2 function. |
| 32 | `"""Execute the February main41 kernel testing as Step 2."""` | Docstring. |
| 33 | `# ==========================================` | Comment: section. |
| 34 | `# 1. DATA PREPARATION` | Comment. |
| 35 | `# ==========================================` | Comment. |
| 36 | `wine = load_wine()` | Load Wine dataset. |
| 37 | `mask = wine.target != 2` | Binary: exclude class 2. |
| 38 | `x_raw, y_raw = wine.data[mask], wine.target[mask]` | Extract features and labels. |
| 39 | (blank) | Blank line. |
| 40 | `scaler = StandardScaler()` | Create scaler. |
| 41 | `x_scaled = scaler.fit_transform(x_raw)` | Standardize features. |
| 42 | (blank) | Blank line. |
| 43 | `pca = PCA(n_components=N_QUBITS)` | PCA to N_QUBITS dimensions. |
| 44 | `x_pca = pca.fit_transform(x_scaled)` | Apply PCA. |
| 45 | (blank) | Blank line. |
| 46 | `DATA_BASIS = Binarizer(threshold=0.0).fit_transform(x_pca).astype(int)` | Binarize for basis encoding. |
| 47 | `DATA_ANGLE = x_pca` | Angle encoding uses PCA output. |
| 48 | (blank) | Blank line. |
| 49 | `pad_amp = 2**N_QUBITS - x_raw.shape[1]` | Padding length for amplitude. |
| 50 | `DATA_AMP = np.hstack([x_scaled, np.zeros((x_raw.shape[0], pad_amp))])` | Pad with zeros. |
| 51 | `DATA_AMP = DATA_AMP / np.linalg.norm(DATA_AMP, axis=1)[:, np.newaxis]` | Normalize rows for amplitude. |
| 52 | (blank) | Blank line. |
| 53 | `# ==========================================` | Comment. |
| 54 | `# 2. AUTO MUTATOR` | Comment. |
| 55 | `# ==========================================` | Comment. |
| 56 | `class AutoMutator:` | Define AutoMutator class. |
| 57 | `def __init__(self, mode="basis"):` | Constructor. |
| 58 | `self.mode = mode` | Store mode (basis/angle/amplitude). |
| 59 | `self.active_defects = []` | List of active defect names. |
| 60 | `self.wire_map = list(range(N_QUBITS))` | Wire permutation (identity). |
| 61 | (blank) | Blank line. |
| 62 | `def set_defects(self, defect_list):` | Set active defects. |
| 63 | `self.active_defects = list(defect_list)` | Store defect list. |
| 64 | (blank) | Blank line. |
| 65 | `def _get_angles(self, vector):` | Convert amplitude vector to rotation angles. |
| 66 | `probs = np.abs(vector)**2` | Probabilities from amplitudes. |
| 67 | `n = int(np.log2(len(vector)))` | Number of qubits. |
| 68 | `betas = [probs]` | Initialize beta tree. |
| 69 | `for _ in range(n):` | Build tree levels. |
| 70 | `curr = betas[-1]` | Current level. |
| 71 | `betas.append(np.array([curr[k] + curr[k+1] for k in range(0, len(curr), 2)]))` | Sum pairs for parent level. |
| 72 | `alphas = []` | List for rotation angles. |
| 73 | `for i in range(n - 1, -1, -1):` | Loop levels top-down. |
| 74 | `layer = []` | Angles for this layer. |
| 75 | `parent, child = betas[i+1], betas[i]` | Parent and child levels. |
| 76 | `for k in range(len(parent)):` | Loop over parent nodes. |
| 77 | `num, den = np.sqrt(child[2*k]), np.sqrt(parent[k])` | Numerator and denominator. |
| 78 | `layer.append(0.0 if den < 1e-12 else 2 * np.arccos(num/den))` | Angle or 0 if den~0. |
| 79 | `alphas.append(np.array(layer))` | Append layer. |
| 80 | `return alphas` | Return angle tree. |
| 81 | (blank) | Blank line. |
| 82 | `def _ur_cnot(self, layer, c_wires, t_wire):` | Uniformly controlled rotation. |
| 83 | `k = len(c_wires)` | Number of control qubits. |
| 84 | `thetas = np.array(list(layer) + [0.0]*(2**k - len(layer))) / (2**k)` | Pad and scale angles. |
| 85 | `for i, th in enumerate(thetas):` | Loop over angles. |
| 86 | `qml.RY(th, wires=t_wire)` | Apply RY on target. |
| 87 | `if i < len(thetas)-1:` | If not last. |
| 88 | `ctl_idx = int(np.log2((i+1) & -(i+1)))` | Control qubit index. |
| 89 | `control_qubit = c_wires[k-1-ctl_idx]` | Get control wire. |
| 90 | `if self.mode == "amplitude" and len(self.active_defects) > 0:` | If amplitude + defects. |
| 91 | `qml.RZ(np.pi/4, wires=control_qubit)` | Defect: extra RZ. |
| 92 | `qml.RY(np.pi/8, wires=t_wire)` | Defect: extra RY. |
| 93 | `else:` | No defect. |
| 94 | `qml.CNOT(wires=[control_qubit, t_wire])` | Standard CNOT. |
| 95 | (blank) | Blank line. |
| 96 | `def apply_feature_map(self, x, wires):` | Apply feature map to encode x. |
| 97 | `mapped_wires = [wires[i] for i in self.wire_map]` | Permute wires. |
| 98 | `if self.mode == "basis":` | Basis encoding. |
| 99 | `for i in range(len(mapped_wires)):` | Loop over wires. |
| 100 | `val = x[i]` | Get feature value. |
| 101 | `if "gate_error" in self.active_defects:` | If gate_error defect. |
| 102 | `val = 1 - val` | Flip bit. |
| 103 | `if val > 0.5:` | If bit is 1. |
| 104 | `qml.PauliX(wires=mapped_wires[i])` | Apply X. |
| 105 | `elif self.mode == "angle":` | Angle encoding. |
| 106 | `for i in range(len(mapped_wires)):` | Loop. |
| 107 | `ang = x[i]` | Get angle. |
| 108 | `if "param_noise" in self.active_defects:` | If param_noise. |
| 109 | `ang += np.random.uniform(0.1, np.pi/2)` | Add noise. |
| 110 | `qml.RY(ang, wires=mapped_wires[i])` | Apply RY. |
| 111 | `elif self.mode == "amplitude":` | Amplitude encoding. |
| 112 | `layers = self._get_angles(x)` | Get angle tree. |
| 113 | `qml.RY(layers[0][0], wires=mapped_wires[0])` | Root RY. |
| 114 | `for i in range(1, len(layers)):` | Loop layers. |
| 115 | `self._ur_cnot(layers[i], mapped_wires[:i], mapped_wires[i])` | Apply UCR. |
| 116 | `n_w = len(mapped_wires)` | Number of wires. |
| 117 | `for j_idx, j in enumerate(mapped_wires):` | Post-encoding loop. |
| 118 | `if not ("remove_superposition" in self.active_defects):` | If not remove_superposition. |
| 119 | `qml.Hadamard(wires=j)` | Apply H. |
| 120 | `target = mapped_wires[(j_idx + 1) % n_w]` | Next wire (cyclic). |
| 121 | `if "swap_topology" in self.active_defects:` | If swap defect. |
| 122 | `qml.SWAP(wires=[j, target])` | Apply SWAP. |
| 123 | `elif not ("remove_entanglement" in self.active_defects):` | If not remove_entanglement. |
| 124 | `qml.CNOT(wires=[j, target])` | Apply CNOT. |
| 125 | (blank) | Blank line. |
| 126 | `# ==========================================` | Comment. |
| 127 | `# 3. KERNEL & OMNI ORACLE` | Comment. |
| 128 | `# ==========================================` | Comment. |
| 129 | `dev = qml.device("default.qubit", wires=N_QUBITS)` | Create simulator. |
| 130 | `mutator = AutoMutator()` | Create mutator. |
| 131 | (blank) | Blank line. |
| 132 | `@qml.qnode(dev)` | Decorate as PennyLane qnode. |
| 133 | `def qnode_omni(x1, x2, d1, d2):` | Kernel circuit: K(x1,x2) with defects d1,d2. |
| 134 | `mutator.set_defects(d1)` | Set defects for x1. |
| 135 | `mutator.apply_feature_map(x1, range(N_QUBITS))` | Encode x1. |
| 136 | `mutator.set_defects(d2)` | Set defects for x2. |
| 137 | `qml.adjoint(mutator.apply_feature_map)(x2, range(N_QUBITS))` | Adjoint encode x2 (inner product). |
| 138 | `return qml.probs(wires=range(N_QUBITS))` | Return measurement probs. |
| 139 | (blank) | Blank line. |
| 140 | `def get_dist(x1, x2, d1=[], d2=[]):` | Wrapper for kernel. |
| 141 | `try:` | Try block. |
| 142 | `return qnode_omni(x1, x2, d1, d2)` | Call kernel. |
| 143 | `except Exception:` | On error. |
| 144 | `return np.zeros(2**N_QUBITS)` | Return zeros. |
| 145 | (blank) | Blank line. |
| 146 | `def check_mr_omni(mr_id, x1, x2, mode, active_d):` | Check if MR mr_id is violated. |
| 147 | `p_ref = get_dist(x1, x2, active_d, [])` | Reference kernel. |
| 148 | `curr_tol = TOL_AMP if mode == "amplitude" else TOL_IDEAL` | Select tolerance. |
| 149 | (blank) | Blank line. |
| 150 | `if mr_id == 2:` | MR 2: self-similarity. |
| 151 | `p_self = get_dist(x1, x1, active_d, [])` | K(x1,x1). |
| 152 | `return np.linalg.norm(p_self - np.eye(2**N_QUBITS)[0]) > curr_tol` | Violated if not [1,0,...,0]. |
| 153 | `elif mr_id == 9:` | MR 9: perturbation. |
| 154 | `return np.linalg.norm(p_ref - get_dist(x1 + 0.1, x2, active_d, [])) > 0.05` | Compare with perturbed x1. |
| 155 | `elif mr_id == 12:` | MR 12: orthogonality. |
| 156 | `x_orth = np.roll(x1, 1) if mode == "amplitude" else x1 + np.pi/2` | Orthogonal input. |
| 157 | `p_orth = get_dist(x1, x_orth, active_d, [])` | Kernel with orthogonal. |
| 158 | `return p_orth[0] > 0.1` | Violated if overlap > 0.1. |
| 159 | `elif mr_id == 14:` | MR 14: wire permutation. |
| 160 | `mutator.wire_map = [1, 0, 3, 2]` | Permute wires. |
| 161 | `p_perm = get_dist(x1, x2, active_d, [])` | Kernel with permuted wires. |
| 162 | `mutator.wire_map = list(range(N_QUBITS))` | Restore wire map. |
| 163 | `return np.linalg.norm(p_ref - p_perm) > curr_tol` | Violated if different. |
| 164 | `elif mr_id == 3:` | MR 3: negation. |
| 165 | `p_neg = get_dist(-x1, -x2, active_d, [])` | Kernel with negated inputs. |
| 166 | `return np.linalg.norm(p_ref - p_neg) > curr_tol` | Violated if different. |
| 167 | `elif mr_id == 6:` | MR 6: cyclic shift. |
| 168 | `p_rot = get_dist(np.roll(x1, 1), np.roll(x2, 1), active_d, [])` | Kernel with rolled inputs. |
| 169 | `return np.linalg.norm(p_ref - p_rot) > curr_tol` | Violated if different. |
| 170 | `elif mr_id == 10:` | MR 10: drop last feature. |
| 171 | `x_drop = x1.copy()` | Copy x1. |
| 172 | `x_drop[-1] = 0` | Set last to 0. |
| 173 | `p_drop = get_dist(x_drop, x2, active_d, [])` | Kernel with dropped. |
| 174 | `return np.linalg.norm(p_ref - p_drop) < curr_tol` | Violated if too similar. |
| 175 | `elif mr_id == 13:` | MR 13: reversal. |
| 176 | `p_rev = get_dist(x1[::-1], x2[::-1], active_d, [])` | Kernel with reversed. |
| 177 | `return np.linalg.norm(p_ref - p_rev) > curr_tol` | Violated if different. |
| 178 | (blank) | Blank line. |
| 179 | `k_ref = p_ref[0]` | Reference kernel value (first element). |
| 180 | `if mr_id == 1:` | MR 1: symmetry K(x1,x2)=K(x2,x1). |
| 181 | `return abs(k_ref - get_dist(x2, x1, active_d, [])[0]) > curr_tol` | Violated if K(x1,x2)≠K(x2,x1). |
| 182 | `elif mr_id == 4:` | MR 4: periodicity. |
| 183 | `return abs(k_ref - get_dist(x1+0.5, x2+0.5, active_d, [])[0]) > curr_tol` | Violated if shift changes kernel. |
| 184 | `elif mr_id == 5:` | MR 5: 2π periodicity (angle only). |
| 185 | `if mode != "angle":` | Only for angle. |
| 186 | `return False` | Not applicable. |
| 187 | `return abs(k_ref - get_dist(x1 + 2*np.pi, x2, active_d, [])[0]) > curr_tol` | Violated if 2π shift changes. |
| 188 | `elif mr_id == 7:` | MR 7: reversal symmetry. |
| 189 | `return abs(k_ref - get_dist(x1[::-1], x2[::-1], active_d, [])[0]) > curr_tol` | Violated if reversal changes. |
| 190 | `elif mr_id == 8:` | MR 8: complement (basis only). |
| 191 | `if mode != "basis":` | Only for basis. |
| 192 | `return False` | Not applicable. |
| 193 | `return abs(k_ref - get_dist(1-x1, 1-x2, active_d, [])[0]) > curr_tol` | Violated if complement changes. |
| 194 | `elif mr_id == 11:` | MR 11: scaling (amplitude only). |
| 195 | `if mode != "amplitude":` | Only for amplitude. |
| 196 | `return False` | Not applicable. |
| 197 | `return abs(k_ref - get_dist(x1*2.0, x2*2.0, active_d, [])[0]) > curr_tol` | Violated if scaling changes. |
| 198 | (blank) | Blank line. |
| 199 | `return False` | Default: no violation. |
| 200 | (blank) | Blank line. |
| 201 | `# ==========================================` | Comment. |
| 202 | `# 4. EXECUTION` | Comment. |
| 203 | `# ==========================================` | Comment. |
| 204 | `ALL_MRS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]` | List of all 14 MR IDs. |
| 205 | `results = []` | List for result rows. |
| 206 | `defects = ["remove_superposition", "remove_entanglement", "gate_error", "swap_topology", "param_noise"]` | Five defect types. |
| 207 | (blank) | Blank line. |
| 208 | `combos = []` | List for defect combinations. |
| 209 | `for r in range(1, 4):` | r=1,2,3 (1 to 3 defects). |
| 210 | `combos.extend([list(c) for c in itertools.combinations(defects, r)])` | Add all combinations of r defects. |
| 211 | (blank) | Blank line. |
| 212 | `iterations = 1 if USE_FIXED_SEED else NUM_RUNS` | Number of runs per combo. |
| 213 | `if USE_FIXED_SEED:` | If fixed seed. |
| 214 | `random.seed(42)` | Set random seed. |
| 215 | `np.random.seed(42)` | Set numpy seed. |
| 216 | (blank) | Blank line. |
| 217 | `print(f"\n{'='*60}")` | Print separator. |
| 218 | `print("STEP 2: Kernel Testing (February main41)")` | Print header. |
| 219 | `print(f"{'='*60}")` | Print separator. |
| 220 | `print(f"Starting: {len(combos)} defect combos x {iterations} runs per mode")` | Print run info. |
| 221 | (blank) | Blank line. |
| 222 | `for mode in ["basis", "angle", "amplitude"]:` | Loop over feature maps. |
| 223 | `dataset = DATA_BASIS if mode == "basis" else (DATA_ANGLE if mode == "angle" else DATA_AMP)` | Select data for mode. |
| 224 | `mutator.mode = mode` | Set mutator mode. |
| 225 | (blank) | Blank line. |
| 226 | `X_gold = dataset[:5]` | First 5 samples as golden set. |
| 227 | `K_GOLD_DIST = np.array([[get_dist(X_gold[i], X_gold[j], [], []) for j in range(5)] for i in range(5)])` | Golden kernel matrix (no defects). |
| 228 | (blank) | Blank line. |
| 229 | `pbar = tqdm(combos, desc=f"V41 {mode.upper()}", ncols=140)` | Progress bar over combos. |
| 230 | `for d in pbar:` | Loop over defect combos. |
| 231 | `caught_count = 0` | Count runs where defect detected. |
| 232 | `mr_kill_counts = {f"MR_{i}": 0 for i in ALL_MRS}` | Per-MR detection counts. |
| 233 | (blank) | Blank line. |
| 234 | `for run in range(iterations):` | Loop over runs. |
| 235 | `K_MUT_DIST = np.array([[get_dist(X_gold[i], X_gold[j], d, []) for j in range(5)] for i in range(5)])` | Mutated kernel matrix. |
| 236 | `diff = np.max([np.linalg.norm(K_GOLD_DIST[i, j] - K_MUT_DIST[i, j]) for i in range(5) for j in range(5)])` | Max norm difference. |
| 237 | (blank) | Blank line. |
| 238 | `curr_tol = TOL_AMP if mode == "amplitude" else TOL_IDEAL` | Select tolerance. |
| 239 | (blank) | Blank line. |
| 240 | `if diff > curr_tol:` | If defect detected (kernel changed). |
| 241 | `caught_count += 1` | Increment caught. |
| 242 | `for mr in ALL_MRS:` | Loop over MRs. |
| 243 | `h_fail = check_mr_omni(mr, dataset[0], dataset[1], mode, [])` | Healthy: does MR fail? |
| 244 | `m_fail = check_mr_omni(mr, dataset[0], dataset[1], mode, d)` | Mutated: does MR fail? |
| 245 | (blank) | Blank line. |
| 246 | `if mr == 10:` | MR 10 has inverted logic. |
| 247 | `if m_fail and not h_fail:` | Mutated fails, healthy passes. |
| 248 | `mr_kill_counts[f"MR_{mr}"] += 1` | Count MR as detecting. |
| 249 | `else:` | Other MRs. |
| 250 | `if m_fail and not h_fail:` | Same condition. |
| 251 | `mr_kill_counts[f"MR_{mr}"] += 1` | Count. |
| 252 | (blank) | Blank line. |
| 253 | `avg_caught = caught_count / iterations` | Average caught rate. |
| 254 | `avg_mr_kills = {k: v / iterations for k, v in mr_kill_counts.items()}` | Average per-MR rates. |
| 255 | (blank) | Blank line. |
| 256 | `results.append([mode, "+".join(d), avg_caught] + list(avg_mr_kills.values()))` | Append result row. |
| 257 | (blank) | Blank line. |
| 258 | `df = pd.DataFrame(results, columns=["Mode", "Defects", "Caught_Rate"] + [f"Efficient_MR_{i}_Rate" for i in ALL_MRS])` | Build DataFrame. |
| 259 | `df.to_csv(FILE_RESULTS, index=False)` | Save to CSV. |
| 260 | `print(f"\nStep 2 complete. Results saved to {FILE_RESULTS}")` | Print completion. |
| 261 | (blank) | Blank line. |

---

## metamorphic/my_metamorphic_relations.py — Key Lines

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `import numpy as np` | Import numpy. |
| 3 | `from scipy.linalg import expm` | Matrix exponential for rotation. |
| 5 | `import pennylane as qml` | PennyLane (used in __getAmplitudeEmdedding). |
| 8 | `class MyMetamorphicRelations:` | MR application class. |
| 10 | `def useMetamorphicRelation(x_data, y_data, mrNumber, mrValue):` | Apply MR by ID. |
| 12 | `resultx = x_data` | Default: x unchanged. |
| 13 | `resulty = y_data` | Default: y unchanged. |
| 16 | `if mrNumber == 1:` | MR 1: scaling. |
| 18 | `print(...)` | Log scaling. |
| 19 | `resultx = MyMetamorphicRelations.metamorphic_feature_scaling(x_data, mrValue)` | Scale features. |
| 21 | `elif mrNumber == 2:` | MR 2: rotation. |
| 23 | `print(...)` | Log rotation. |
| 25 | `resultx = MyMetamorphicRelations.metamorphic_feature_rotation_with_angle(x_data, mrValue)` | Rotate features. |
| 27 | `elif mrNumber == 3:` | MR 3: permutation. |
| 29 | `print(...)` | Log permutation. |
| 31 | `resultx, resulty = MyMetamorphicRelations.metamorphic_feature_permutation(x_data, y_data)` | Permute rows. |
| 33 | `elif mrNumber == 4:` | MR 4: invert labels. |
| 35 | `print(...)` | Log. |
| 37 | `resulty = MyMetamorphicRelations.metamorphic_invert_all_labels_multiclass(y_data, mrValue)` | Invert labels. |
| 40 | `elif mrNumber == 5:` | MR 5: duplicate inputs. |
| 42 | `resultx, resulty = MyMetamorphicRelations.duplicateInputs(x_data, y_data, mrValue)` | Duplicate sample. |
| 46 | `return resultx, resulty` | Return transformed data. |
| 49 | `def metamorphic_feature_scaling(x_data, scaling_factor):` | MR 1 implementation. |
| 53 | `scaled_x_tr = x_data * scaling_factor` | Multiply by factor. |
| 57 | `return scaled_x_tr` | Return. |
| 61 | `def metamorphic_feature_rotation_with_angle(x, angle):` | MR 2 implementation. |
| 63 | `rotation_matrix = expm(np.eye(x.shape[1]) * 1j * angle)` | Complex rotation matrix. |
| 64 | `return np.dot(rotation_matrix, x.T).T` | Apply rotation. |
| 77 | `def metamorphic_feature_permutation(input, output):` | MR 3 implementation. |
| 81 | `permutation = np.random.permutation(input.shape[0])` | Random row permutation. |
| 89 | `input_permuted = input[permutation, :]` | Permute rows of input. |
| 91 | `output_permuted = output[permutation]` | Permute labels. |
| 94 | `return input_permuted, output_permuted` | Return. |
| 97 | `def metamorphic_invert_all_labels_multiclass(y_data, num_classes):` | MR 4 implementation. |
| 106 | `y_train_inverted = y_data` | Copy (in-place). |
| 108 | `for i in range(len(y_train_inverted)):` | Loop. |
| 109 | `y_train_inverted[i] = (y_train_inverted[i] + 1) % num_classes` | Invert label. |
| 111 | `return y_train_inverted` | Return. |
| 115 | `def duplicateInputs(self, x_data, y, inputIndex):` | MR 5 implementation. |
| 117 | `x = np.vstack([x, x[inputIndex]])` | Duplicate row (bug: x undefined, should be x_data). |
| 118 | `y = np.append(y, y[inputIndex])` | Duplicate label. |
| 119 | `return x_data, y` | Return. |

---

## data/data_manager.py

| Line | Code | Explanation |
|------|------|-------------|
| 1 | (blank) | Blank line. |
| 2 | `from sklearn.datasets import load_wine` | Import Wine (unused; datasets in submodules). |
| 3 | `from sklearn.preprocessing import StandardScaler` | Import scaler (unused here). |
| 4 | `from pennylane import numpy as np` | Import numpy (unused here). |
| 5 | (blank) | Blank line. |
| 6 | `from .load_digits import DigitsData` | Import Digits dataset class. |
| 7 | `from .credit_card import KaggleCreditCardData` | Import Credit Card class. |
| 8 | `from .mnist import MNISTData` | Import MNIST class. |
| 9 | (blank) | Blank line. |
| 10 | `# from .wine_data import WineData` | Commented Wine import. |
| 11 | (blank) | Blank line. |
| 12 | `from .wine_data_manager import WineDataManager` | Import Wine data manager. |
| 13 | (blank) | Blank line. |
| 14 | `class DataManager:` | Data loader class. |
| 15 | (blank) | Blank line. |
| 16 | (blank) | Blank line. |
| 17 | (blank) | Blank line. |
| 18 | `def getData(self, number = 0):` | Load dataset by ID. |
| 19 | (blank) | Blank line. |
| 20 | `wineDataManagerClass = WineDataManager.getWineData()` | Get Wine data class. |
| 21 | `WineData = wineDataManagerClass` | Alias. |
| 22 | (blank) | Blank line. |
| 23 | `options = {` | Dict mapping ID to data class. |
| 24 | `0 : WineData,` | 0 = Wine. |
| 25 | `1: DigitsData,` | 1 = Digits. |
| 26 | `2: KaggleCreditCardData,` | 2 = Credit Card. |
| 27 | `3: MNISTData` | 3 = MNIST. |
| 28 | `}` | End dict. |
| 29 | (blank) | Blank line. |
| 30 | `# myData = WineData()` | Commented. |
| 31 | (blank) | Blank line. |
| 32 | `# myData = DataManager.options[number]()` | Commented. |
| 33 | `data_class = options.get(number, WineData)` | Get class for number; default Wine. |
| 34 | `myData = data_class()` | Instantiate. |
| 35 | (blank) | Blank line. |
| 36 | `x,y, x_normalized = myData.getData()` | Load (x, y, normalized x). |
| 37 | (blank) | Blank line. |
| 38 | `# print(f'DataManager getData, len(x): {len(x)}')` | Commented. |
| 39 | (blank) | Blank line. |
| 40 | `return  x,y, x_normalized` | Return tuple. |
| 41 | (blank) | Blank line. |
| 42 | (blank) | Blank line. |
