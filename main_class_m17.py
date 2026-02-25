import sys

from classes.time import MyTimeHelper

from pennylane import numpy as np

from data.data_manager import DataManager

# from quantum.q_kernel import Qkernel

from quantum.q_kernel_manager import QKernelManager

# from quantum.feature_map import FeatureMap

from quantum.feature_map_manager import FeatureMapManager

from sklearn.svm import SVC

from sklearn.model_selection import train_test_split

from sklearn.model_selection import KFold

from scipy.stats import ttest_ind


from metamorphic.my_metamorphic_relations import MyMetamorphicRelations

sys.path.insert(0, './data')
sys.path.insert(0, './quantum')

class MainClass:

    # qKernel = Qkernel()

    # featureMap = FeatureMap()


    def run_qsvm(x_padded, y, n_qubits, scaling_factor,featureMap, featureMapType = 0):


        #run_qsvm, MainClass.featureMap: <quantum.feature_map.FeatureMap object at 0x10fd0e660>
        #run_qsvm, MainClass.featureMap: <class 'quantum.feature_map.FeatureMap'>
        #run_qsvm, MainClass.featureMap: <quantum.feature_map.FeatureMap object at 0x121cce900>
        # print(f'run_qsvm, MainClass.featureMap: {MainClass.featureMap}')
        # print(f'scaling_factor: {scaling_factor}')


        # print(f'run_qsvm, x_padded: {x_padded}')

        # x_data_to_use= MyMetamorphicRelations.useMetamorphicRelation(x_padded, 1, scaling_factor)

        x_data_to_use= x_padded

        # y_data_to_use = MyMetamorphicRelations.useMetamorphicRelation(y, 1, scaling_factor)
        y_data_to_use = y

        # print(f'run_qsvm, x_data_to_use: {x_data_to_use}')

        # print(f'run_qsvm, y_data_to_use: {y_data_to_use}')

        x_train, x_test, y_train, y_test = train_test_split(
        x_data_to_use, y_data_to_use, test_size=0.2,  random_state=42  
        )
        
        #3 run training

        # print(f'run_qsvm, n_qubits: {n_qubits}')

        kernel_train = featureMap.compute_kernel_matrix(x_train, x_train, n_qubits, featureMapType)
            
        #mutation #20 start
        kernel_test = featureMap.compute_kernel_matrix(x_train, x_test, n_qubits, featureMapType)
        #mutation #20 end

        svm = SVC(kernel='precomputed')
        svm.fit(kernel_train, y_train)

        test_score = svm.score(kernel_test, y_test)

        return test_score
        
    def runTest(self, featureMapType = 0):

        from classes.parameters import MyParameters
        
        dataManager = DataManager()

        featureMapClass = FeatureMapManager().getFeatureMap()

        featureMap = featureMapClass()

        qKernelClass = QKernelManager().getqKernel()

        qKernel = qKernelClass()

        print(f'runTest, featureMap: {featureMap}')
        #1 get Data 
        x,y, x_normalized = dataManager.getData(MyParameters.dataType)

        #2 get features and nqubits and add padding
        
        n_features, n_qubits = qKernel.getFeaturesAndNqubits(x_normalized, featureMapType) 
        
        # print(f'n_qubits: {n_qubits}')

        # np.set_printoptions(threshold=np.inf)    
        # print(f'x: \n{x}')

        # print(f'x_normalized: \n{x_normalized}')

        x_padded = x_normalized
        
        if(featureMapType == 0):
            x_padded = qKernel.pad_features(x_normalized, n_qubits) 

        # x_data_to_use= MyMetamorphicRelations.useMetamorphicRelation(x_padded, 1, mrValue)
        x_data_to_use= x_padded

        MyParameters.amplitudeNQubits = n_qubits


        score_original = MainClass.run_qsvm(x_data_to_use, y, n_qubits, 1.0, featureMap, featureMapType)

        # score_scaled = MainClass.run_qsvm(x_data_to_use, y, n_qubits, mrValue, featureMap, featureMapType)

        # return score_original, score_scaled

        return score_original

        print(f'score_original: {score_original}')

        print(f'score_scaled: {score_scaled}')

