import sys
import sys

from classes.time import MyTimeHelper

from pennylane import numpy as np

from data.data_manager import DataManager

# from quantum.q_kernel import QKernel

from quantum.q_kernel_manager import QKernelManager

# from quantum.feature_map import FeatureMap

from quantum.feature_map_manager import FeatureMapManager

from sklearn.svm import SVC

from sklearn.model_selection import KFold

from scipy.stats import ttest_ind

from classes.parameters import MyParameters

from metamorphic.my_metamorphic_relations import MyMetamorphicRelations

from termcolor import colored

sys.path.insert(0, './data')
sys.path.insert(0, './quantum')

class MainStatisticalClass:


    # dataManager = DataManager()

    # qKernel = QKernel()

    
    # featureMap = FeatureMap()

    def run_qsvm_with_kfold(x_padded, y, mrNumber, n_qubits, scaling_factor, featureMap):
    
        print(f"\nRunning evaluation with scaling_factor = {scaling_factor}, mrNumber: {mrNumber}")


        # x_data_to_use = x_padded * scaling_factor

        # print(f'1-- x_data_to_use: {x_data_to_use}')

        if scaling_factor == 1.0:

            # print(f'MainStatisticalClass -  run_qsvm_with_kfold, scaling_factor == 1.0')
            x_data_to_use = x_padded

        elif mrNumber == 4:
            

            x_data_to_use = x_padded 
            y = MyMetamorphicRelations.useMetamorphicRelation(x_padded, y, mrNumber, 2)

        else:

            x_data_to_use= MyMetamorphicRelations.useMetamorphicRelation(x_padded, y, mrNumber, scaling_factor)

        # print(f'2-- x_data_to_use: {x_data_to_use}')

        # return 


        n_splits = MyParameters.n_folds
        kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
        
        test_scores = []
        fold_number = 1

        #mutation #25 start
        for train_index, test_index in kf.split(x_padded):
        #mutation #25 end

            print(f"\n{'='*15} FOLD {fold_number}/{n_splits} {'='*15}")
            
            x_train, x_test = x_data_to_use[train_index], x_data_to_use[test_index]
            y_train, y_test = y[train_index], y[test_index]

            kernel_train = featureMap.compute_kernel_matrix(x_train, x_train, n_qubits, MyParameters.featureMapType)
            
            kernel_test = featureMap.compute_kernel_matrix(x_test, x_train, n_qubits, MyParameters.featureMapType)

            print("\nTraining SVM...")
            svm = SVC(kernel='precomputed')
            svm.fit(kernel_train, y_train)

            test_score = svm.score(kernel_test, y_test)
            test_scores.append(test_score)
            
            print(f"Fold {fold_number} Test Accuracy: {test_score:.4f}")
            fold_number += 1

        print(f"\n{'='*15} Cross-Validation Summary (scaling_factor={scaling_factor}) {'='*15}")
        mean_accuracy = np.mean(test_scores)
        std_accuracy = np.std(test_scores)
        
        print(f"Scores for each fold: {[f'{score:.4f}' for score in test_scores]}")
        print(f"\nMean Test Accuracy: {mean_accuracy:.4f}")
        print(f"Standard Deviation: {std_accuracy:.4f}")
        
        return test_scores


    def runTest(self, mrNumber, mrValue):

        # print(colored(f'MainStatisticalClass, MyParameters.testMutation: {MyParameters.testMutation}', 'blue'))

        dataManager = DataManager()

        # qKernel = QKernel()

        featureMapClass = FeatureMapManager().getFeatureMap()

        featureMap = featureMapClass()

        qKernelClass = QKernelManager().getqKernel()

        qKernel = qKernelClass()
        # print(f'featureMap: {featureMap}')
        #1 get Data 
        x,y, x_normalized = dataManager.getData(MyParameters.dataType)

        #2 get features and nqubits and add padding
        
        n_features, n_qubits = qKernel.getFeaturesAndNqubits(x_normalized, MyParameters.featureMapType) 
        
        # print(f'n_qubits: {n_qubits}')

        # np.set_printoptions(threshold=np.inf)    
        # print(f'x: \n{x}')

        # print(f'x_normalized: \n{x_normalized}')

        x_padded = x_normalized

        if(MyParameters.featureMapType == 0):
            x_padded = qKernel.pad_features(x_normalized, n_qubits) 

        # x_padded = x_normalized
        # print(f'x_padded: {x_padded}')

        # return

        MyParameters.amplitudeNQubits = n_qubits

        #3 run tests
        
        scores_original = MainStatisticalClass.run_qsvm_with_kfold(x_padded, y, mrNumber, n_qubits, 1.0, featureMap)

        scores_scaled = MainStatisticalClass.run_qsvm_with_kfold(x_padded, y, mrNumber, n_qubits, mrValue, featureMap)

        t_statistic, p_value = ttest_ind(scores_original, scores_scaled)

        print(f"\nIndependent t-test results:")
        print(f"T-statistic: {t_statistic:.4f}")
        print(f"P-value: {p_value:.4f}")

        alpha = 0.05
        if p_value > alpha:
            print(f"\nSince the p-value ({p_value:.4f}) is greater than {alpha}, we do not reject the null hypothesis.")
            print("This suggests that there is no statistically significant difference between the accuracies of the original and scaled data.")
            print("The metamorphic relation holds, as expected, because AmplitudeEmbedding normalizes the input vectors, making the kernel invariant to the input vector's norm.")
        else:
            print(f"\nSince the p-value ({p_value:.4f}) is less than {alpha}, we reject the null hypothesis.")
            print("This suggests that there is a statistically significant difference between the accuracies, which is unexpected and may indicate an issue.")

        return scores_original, scores_scaled, t_statistic, p_value

