from termcolor import colored
from classes.default_parameters import DefaultParameters
from classes.parameters import MyParameters
from classes.time import MyTimeHelper
import numbers
import math
import argparse
from classes.my_dataframe_short import MyDataFrame

myMutations = []

def saveToDataFrame(scoreOfOriginal, scoreOfMutant, mutantNumber, typeOfMutant, tStatistic, pValue, nullHypothesisIsRejected, all_original_scores, all_mutant_scores, n_folds, featureMap, appliedMr, MrValue, startTime='', endTime=''):
    myDataFrame = MyDataFrame()
    formattedData = myDataFrame.formatData(scoreOfOriginal, scoreOfMutant, mutantNumber, typeOfMutant, tStatistic, pValue, nullHypothesisIsRejected, all_original_scores, all_mutant_scores, n_folds, featureMap, appliedMr, MrValue, startTime, endTime)
    myDataFrame.processToDataFrame(formattedData)


def runScript(mrNumber, mrValue):
    print(f'runScript, mrValue: {mrValue}')
    myDataFrame = MyDataFrame()
    allMutationsScores = []
    equivalentMutants = []
    killedMutants = []
    survivedMutants = []
    crashedMutants = []
    equivalentMutantsScores = []
    killedMutantsScores = []
    survivedMutantsScores = []
    crashedMutantsMessages = []
    originalScore = 0
    firstRun = True

    for test in myMutations:
        if firstRun:
            DefaultParameters.testMutation = 0
            MyParameters.resetParameters()
            from main_class_manager import MainClassManager
            mainClassClass = MainClassManager.getMainClass()
            mainClass = mainClassClass()
            originalScore = mainClass.runTest(DefaultParameters.featureMapType)
            print(f'originalScore: {originalScore}')
            firstRun = False

        print(colored(f'runScript,  DefaultParameters.featureMapType: {DefaultParameters.featureMapType }', 'red'))
        DefaultParameters.testMutation = test
        MyParameters.resetParameters()
        from main_class_manager import MainClassManager
        mainClassClass = MainClassManager.getMainClass()
        mainClass = mainClassClass()
        print(colored(f'MyParameters.testMutation: {MyParameters.testMutation}', 'blue'))
        startTime = MyTimeHelper().getTimeNow()
        mutantScore = ''

        try:
            startTime = MyTimeHelper().getTimeNow()
            mutantScore = mainClass.runTest(DefaultParameters.featureMapType)
            roundingNumber = 1000
            originalScore = math.floor(originalScore * roundingNumber) / roundingNumber
            mutantScore = math.floor(mutantScore * roundingNumber) / roundingNumber

            if mutantScore == originalScore:
                equivalentMutants.append(test)
                equivalentMutantsScores.append(mutantScore)
                print(colored(f'for mutation: {test}, original score: {originalScore} == mutation score: {mutantScore}', 'green'))
                endTime = MyTimeHelper().getTimeNow()
                saveToDataFrame(originalScore, mutantScore, test, MyParameters.mutantTypes[0], '-', '-', '-', '-', '-', 0, 0, '-', '-', startTime, endTime)
            elif isinstance(mutantScore, numbers.Number):
                print(colored(f'for mutation: {test}, original score: {originalScore}!= mutation score: {mutantScore}', 'red'))
                print(colored(f'start statistical testing', 'red'))
                from main_statistical_class_manager import MainStatisticalClassManager
                mainStatisticalClassClass = MainStatisticalClassManager.getMainStatisticalClass()
                mainStatisticalClass = mainStatisticalClassClass()
                allScoresOfOriginal, allScoresOfMutant, tStatistic, pValue = mainStatisticalClass.runTest(mrNumber, mrValue)

                if pValue < 0.05:
                    killedMutants.append(test)
                    killedMutantsScores.append(mutantScore)
                    endTime = MyTimeHelper().getTimeNow()
                    saveToDataFrame(originalScore, mutantScore, test, MyParameters.mutantTypes[1], tStatistic, pValue, 'Yes', allScoresOfOriginal, allScoresOfMutant, MyParameters.n_folds, 0, MyParameters.mrUsed, mrValue, startTime, endTime)
                else:
                    survivedMutants.append(test)
                    survivedMutantsScores.append(mutantScore)
                    endTime = MyTimeHelper().getTimeNow()
                    saveToDataFrame(originalScore, mutantScore, test, MyParameters.mutantTypes[2], tStatistic, pValue, 'No', allScoresOfOriginal, allScoresOfMutant, MyParameters.n_folds, 0, MyParameters.mrUsed, MyParameters.scaleValue, startTime, endTime)
            else:
                print(colored(f'for mutation: {test}, original score: {originalScore} != crashed mutation: {mutantScore}', 'red'))
                crashedMutants.append(test)
                crashedMutantsMessages.append(mutantScore)
                endTime = MyTimeHelper().getTimeNow()
                saveToDataFrame(originalScore, mutantScore, test, MyParameters.mutantTypes[3], '-', '-', '-', '-', '-', 0, 0, '-', '-', startTime, endTime)
        except Exception as error:
            print(colored(f'for mutation: {test}, original score: {originalScore} != crashed mutation: {mutantScore}', 'red'))
            crashedMutants.append(test)
            mutantScore = error
            crashedMutantsMessages.append(mutantScore)
            endTime = MyTimeHelper().getTimeNow()
            saveToDataFrame(originalScore, mutantScore, test, MyParameters.mutantTypes[3], '-', '-', '-', '-', '-', 0, 0, '-', '-', startTime, endTime)
            print(f'exception: {error}')


def runLoopThroughAllTests(typeOfFeatureMap, mrUsed):
    global myMutations
    DefaultParameters.mrUsed = mrUsed
    DefaultParameters.featureMapType = typeOfFeatureMap
    mrValue = 1

    if mrUsed == 1 or mrUsed == 3 or mrUsed == 4:
        print(f'main runLoopThroughAllTests, mrUsed == 1  | mrUsed == 3 | mrUsed == 4')
        mrValue = MyParameters.scaleValue
    elif mrUsed == 2:
        mrValue = MyParameters.angle
        print(f'main runLoopThroughAllTests, mrUsed == 2 mrValue = {mrValue}')
    elif mrUsed == 5:
        mrValue = MyParameters.inputToDuplicate
        print(f'main runLoopThroughAllTests, mrUsed == 5')
    else:
        print(f'main runLoopThroughAllTests, else')

    # Sept-style sequential mapping: amplitude 1-10, angle 11-30 (disjoint)
    if typeOfFeatureMap == 0:
        myMutations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # amplitude: 10 mutants
        runScript(mrNumber=DefaultParameters.mrUsed, mrValue=mrValue)
    else:
        myMutations = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]  # angle: 20 mutants
        runScript(mrNumber=DefaultParameters.mrUsed, mrValue=mrValue)


def run_tests(dataset=None, kfold=None, experiment="all"):
    if dataset is not None:
        DefaultParameters.dataType = dataset
    else:
        dataset = DefaultParameters.dataType
    if kfold is not None:
        DefaultParameters.n_folds = kfold
    else:
        kfold = DefaultParameters.n_folds
    MyParameters.resetParameters()

    run_exp1 = experiment in ("all", "1")
    run_exp2 = experiment in ("all", "2")
    run_exp3 = experiment in ("all", "3")

    if run_exp1:
        print(f"\n{'='*60}")
        print("Experiment 1: Baseline")
        print(f"{'='*60}")
        from experiment1_baseline import run_experiment1
        run_experiment1(dataset=dataset, kfold=kfold)

    if run_exp2:
        print(f"\n{'='*60}")
        print("Experiment 2: Statistical Testing (12 MRs, 30 mutants)")
        print(f"{'='*60}")
        for i in range(1, 13):
            print(f'mr number: {i}')

            if i == 6:
                DefaultParameters.addQuantumRegister = True
                MyParameters.resetParameters()
            if i == 7:
                DefaultParameters.injectNullEffectOperation = True
                MyParameters.resetParameters()
            if i == 8:
                DefaultParameters.injectParameter = True
                MyParameters.resetParameters()
            if i == 9:
                DefaultParameters.changeDevice = True
                MyParameters.resetParameters()
            if i == 10:
                DefaultParameters.changeOptimization = True
                MyParameters.resetParameters()
            if i == 11:
                DefaultParameters.reverseWires = True
                MyParameters.resetParameters()
            if i == 12:
                DefaultParameters.reverseQubitsMultiplication = True
                MyParameters.resetParameters()
            if i == 13:
                DefaultParameters.checkSymmetry = True
                MyParameters.resetParameters()
            if i == 14:
                DefaultParameters.checkSameInputSymmetry = True
                MyParameters.resetParameters()
            if i == 15:
                DefaultParameters.checkScalingInvariance = True
                MyParameters.resetParameters()
            if i == 16:
                DefaultParameters.checkAddingPeriodicity = True
            if i == 17:
                DefaultParameters.checkShiftingInvariance = True
                MyParameters.resetParameters()

            runLoopThroughAllTests(0, i)
            runLoopThroughAllTests(1, i)

            DefaultParameters.addQuantumRegister = False
            DefaultParameters.injectNullEffectOperation = False
            DefaultParameters.injectParameter = False
            DefaultParameters.changeDevice = False
            DefaultParameters.changeOptimization = False
            DefaultParameters.reverseWires = False
            DefaultParameters.reverseQubitsMultiplication = False
            DefaultParameters.checkSymmetry = False
            DefaultParameters.checkSameInputSymmetry = False
            DefaultParameters.checkScalingInvariance = False
            DefaultParameters.checkAddingPeriodicity = False
            DefaultParameters.checkShiftingInvariance = False
            MyParameters.resetParameters()

    if run_exp3:
        print(f"\n{'='*60}")
        print("Experiment 3: Kernel Testing (defect-based, 14 MRs)")
        print(f"{'='*60}")
        from step2_kernel_test import run_step2_kernel_test
        run_step2_kernel_test()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QSVM Structure Testing")
    parser.add_argument("--dataset", type=int, default=None, choices=[0, 1, 2, 3], help="0=Wine, 1=Load Digits, 2=Credit Card, 3=MNIST")
    parser.add_argument("--kfold", type=int, default=None, help="K-fold value for Step 1 (default: 5)")
    parser.add_argument("--experiment", type=str, default="all", choices=["all", "1", "2", "3"], help="all=run all, 1=Baseline only, 2=Statistical Testing only, 3=Kernel Testing only")
    args = parser.parse_args()
    run_tests(dataset=args.dataset, kfold=args.kfold, experiment=args.experiment)
