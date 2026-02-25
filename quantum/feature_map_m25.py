
import pennylane as qml

from classes.parameters import MyParameters

from quantum.feature_map import _progress_print

from pennylane import numpy as np

import time

from classes.my_dataframe_short import MyDataFrame

from classes.default_parameters import DefaultParameters

import math


class FeatureMap:

    embedding_call_count = 0

    oneInputKilled = False

    inputsNumber = 0

    def quantum_amplitude_embedding(x1, x2, n_qubits):

        FeatureMap.inputsNumber = FeatureMap.inputsNumber + 1
    

         #mr#11
        if MyParameters.reverseWires == True:

            qml.AmplitudeEmbedding(features=x1, wires=list(reversed(range(n_qubits))), normalize=True)

            qml.adjoint(qml.AmplitudeEmbedding(features=x2, wires=list(reversed(range(n_qubits))), normalize=True))
        
        else:
            qml.AmplitudeEmbedding(features=x1, wires=range(n_qubits), normalize=True)

            qml.adjoint(qml.AmplitudeEmbedding(features=x2, wires=range(n_qubits), normalize=True))

        if FeatureMap.embedding_call_count == 0:
            
            FeatureMap.embedding_call_count += 1
            
            #mr#7
            if MyParameters.injectParameter == True:

                qml.PauliX(wires=0) 
                qml.PauliX(wires=0) 

            #mr#8
            if MyParameters.injectNullEffectOperation == True:

                qml.RX(np.pi, wires=0) 
                qml.PauliX(wires=0) 
            
            #mr#6
            if MyParameters.addQuantumRegister == True:
                
                # Apply an X gate to the extra wire (wire n_qubits)                
                qml.PauliX(wires=n_qubits) 

                return qml.probs(wires=range(n_qubits+1))
            
        return qml.probs(wires=range(n_qubits))
    
    def quantum_angle_embedding(x1, x2, n_qubits):

        FeatureMap.inputsNumber = FeatureMap.inputsNumber + 1

          #mr#11
        if MyParameters.reverseWires == True:

            qml.AngleEmbedding(features=x1,  wires=list(reversed(range(n_qubits))), rotation='Y')

            qml.adjoint(qml.AngleEmbedding(features=x2,wires=list(reversed(range(n_qubits))), rotation='Y'))

        else:
            # Embed the first feature vector
            qml.AngleEmbedding(features=x1, wires=range(n_qubits), rotation='Y')
            
            # Apply the inverse of the second feature vector's embedding
            qml.adjoint(qml.AngleEmbedding(features=x2, wires=range(n_qubits), rotation='Y'))
            
        if FeatureMap.embedding_call_count == 0:
            
            FeatureMap.embedding_call_count += 1
            
            #mr#7
            if MyParameters.injectParameter == True:

                qml.PauliX(wires=0) 
                qml.PauliX(wires=0) 

            #mr#8
            if MyParameters.injectNullEffectOperation == True:

                qml.RX(np.pi, wires=0) 
                qml.PauliX(wires=0) 
            
            #mr#6
            if MyParameters.addQuantumRegister == True:
                
                # Apply an X gate to the extra wire (wire n_qubits)                
                qml.PauliX(wires=n_qubits) 

                return qml.probs(wires=range(n_qubits+1))
            
        return qml.probs(wires=range(n_qubits))
    
    def shot_based_kernel1(x1, x2, n_qubits):

        dev = MyParameters.getDevice()

        if MyParameters.changeOptimization == True:

            dev = FeatureMap.changeOptimizationLevel(dev)

        quantum_amplitude_embedding_qnode = qml.QNode(FeatureMap.quantum_amplitude_embedding, dev)

        probabilities = quantum_amplitude_embedding_qnode(x1, x2, n_qubits)

        if DefaultParameters.testMutation != 0:
            #mr13
            if MyParameters.checkSymmetry == True:

                # mutantNumber = DefaultParameters.testMutation
                # print(f'mutantNumber is: {mutantNumber}')

                tempProbabilities = quantum_amplitude_embedding_qnode(x2, x1, n_qubits)   

                FeatureMap.doSymmetryChecking(probabilities[0], tempProbabilities[0])

            #mr14
            if MyParameters.checkSameInputSymmetry == True:

                tempProbabilities1 = quantum_amplitude_embedding_qnode(x1, x1, n_qubits)   

                tempProbabilities2 = quantum_amplitude_embedding_qnode(x2, x2, n_qubits)   

                FeatureMap.doSameInputsSymmetryChecking(tempProbabilities1[0], tempProbabilities2[0])

            #mr15
            if MyParameters.checkScalingInvariance == True:

                scaleValue = MyParameters.scaleValue 
                
                tempX1 = scaleValue * x1

                tempX2 = scaleValue * x2

                tempProbabilities = quantum_amplitude_embedding_qnode(tempX1, tempX2, n_qubits)   

                FeatureMap.checkScalingInvariance(probabilities[0], tempProbabilities[0], True)

            #mr16
            if MyParameters.checkAddingPeriodicity == True:

                period = 2 * np.pi

                x1_shifted = x1 + period

                tempProbabilities = quantum_amplitude_embedding_qnode(x1_shifted, x2, n_qubits)   

                FeatureMap.checkAddingPeriodicity(probabilities[0], tempProbabilities[0], False)        
    
        #mutation #25 start
        return probabilities[-1]
        #mutation #25 start

    def shot_based_kernel2(x1, x2, n_qubits):

        dev = MyParameters.getDevice()

        if MyParameters.changeOptimization == True:

            dev = FeatureMap.changeOptimizationLevel(dev)

        quantum_angle_embedding_qnode = qml.QNode(FeatureMap.quantum_angle_embedding, dev)

        probabilities = quantum_angle_embedding_qnode(x1, x2, n_qubits)

        if DefaultParameters.testMutation != 0:

            #mr13
            if MyParameters.checkSymmetry == True:

                tempProbabilities = quantum_angle_embedding_qnode(x2, x1, n_qubits)   

                FeatureMap.doSymmetryChecking(probabilities[0], tempProbabilities[0])

            #mr14
            if MyParameters.checkSameInputSymmetry == True:

                tempProbabilities1 = quantum_angle_embedding_qnode(x1, x1, n_qubits)   

                tempProbabilities2 = quantum_angle_embedding_qnode(x2, x2, n_qubits)   

                FeatureMap.doSameInputsSymmetryChecking(tempProbabilities1[0], tempProbabilities2[0])

            #mr15
            if MyParameters.checkScalingInvariance == True:

                scaleValue = MyParameters.scaleValue 
                
                tempX1 = scaleValue * x1

                tempX2 = scaleValue * x2

                tempProbabilities = quantum_angle_embedding_qnode(tempX1, tempX2, n_qubits)   

                FeatureMap.checkScalingInvariance(probabilities[0], tempProbabilities[0], False)

            #mr16
            if MyParameters.checkAddingPeriodicity == True:

                period = 2 * np.pi

                x1_shifted = x1 + period

                tempProbabilities = quantum_angle_embedding_qnode(x1_shifted, x2, n_qubits)   

                FeatureMap.checkAddingPeriodicity(probabilities[0], tempProbabilities[0], True)        

        #mutation #25 start
        return probabilities[-1]
        #mutation #25 start

    def changeOptimizationLevel(qnode):

        transformed_qnode = qnode

        if MyParameters.allOptimizationLevels[MyParameters.selectedOptimizationLevel] == 1:

            transformed_qnode = qml.transforms.merge_rotations(qnode)
        
        elif MyParameters.allOptimizationLevels[MyParameters.selectedOptimizationLevel] == 2:

            transformed_qnode = qml.transforms.commute_controlled(qml.transforms.merge_rotations(qnode))

        return transformed_qnode

    def compute_kernel_matrix(self, X1, X2, n_qubits, featureMap):

        # print(f'compute_kernel_matrix, n_qubits: {n_qubits}')

        # print(f'compute_kernel_matrix, featureMap: {featureMap}')
        shot_based_kernel = FeatureMap.shot_based_kernel1
        if(featureMap == 1):
            shot_based_kernel = FeatureMap.shot_based_kernel2


        n_samples1 = len(X1)
        n_samples2 = len(X2)
        kernel_mat = np.zeros((n_samples1, n_samples2))
        
        print(f"Computing kernel matrix of size {n_samples1}x{n_samples2} using {MyParameters.shots} shots...")
        start_time = time.time()
        
        for i in range(n_samples1):
            for j in range(n_samples2):

                if FeatureMap.oneInputKilled == True:
                    continue
               
                if MyParameters.reverseQubitsMultiplication:

                    kernel_mat[i, j] = shot_based_kernel(X2[j], X1[i], n_qubits)
                    # kernel_mat[i, j] = shot_based_kernel(X2[i], X1[j], n_qubits)
                else:

                    kernel_mat[i, j] = shot_based_kernel(X1[i], X2[j], n_qubits)
            
            elapsed_time = time.time() - start_time
            avg_time_per_row = elapsed_time / (i + 1)
            est_remaining_time = avg_time_per_row * (n_samples1 - (i + 1))
            _progress_print(f'Computed row {i+1}/{n_samples1} | Est. time remaining: {est_remaining_time:.2f}s')

            FeatureMap.oneInputKilled = False
            FeatureMap.inputsNumber = 0

        print("\nKernel matrix computation complete.                      ")
        return kernel_mat
    
    def saveToaMiniDataFrame(mutantNumber, MrNumber, value1, value2, inputNumber):

        FeatureMap.oneInputKilled = True

        myDataFrame = MyDataFrame()

        formattedData = myDataFrame.formatMiniData(mutantNumber, MrNumber, value1, value2, inputNumber)

        myDataFrame.processToMiniDataFrame(formattedData)

    def doSymmetryChecking(probability1, probability2):

        mutantNumber = DefaultParameters.testMutation

        # if probability1 != probability2:
        if not math.isclose(probability1, probability2):
            
            intputNumber = FeatureMap.inputsNumber 

            FeatureMap.saveToaMiniDataFrame(mutantNumber, 13, probability1, probability2, intputNumber)

    def doSameInputsSymmetryChecking(probability1, probability2):

        mutantNumber = DefaultParameters.testMutation

        # if probability1 != 1 or probability2 != 1:
        if not math.isclose(probability1, 1) or not math.isclose(probability2, 1):

            inputNumber = FeatureMap.inputsNumber 
            
            FeatureMap.saveToaMiniDataFrame(mutantNumber, 14, probability1, probability2, inputNumber)

    def checkScalingInvariance(probability1, probability2, shouldBeEqual):

        mutantNumber = DefaultParameters.testMutation

        if shouldBeEqual:

            # if probability1 != probability2:
            if not math.isclose(probability1, probability2):

                inputNumber = FeatureMap.inputsNumber 

                FeatureMap.saveToaMiniDataFrame(mutantNumber, 15, probability1, probability2, inputNumber)
        else:

            # if probability1 == probability2:
            if math.isclose(probability1, probability2):

                inputNumber = FeatureMap.inputsNumber

                FeatureMap.saveToaMiniDataFrame(mutantNumber, 15, probability1, probability2, inputNumber)

    def checkAddingPeriodicity(probability1, probability2, shouldBeEqual):
        
        mutantNumber = DefaultParameters.testMutation

        if shouldBeEqual:

            # if probability1 != probability2:
            if not math.isclose(probability1, probability2):

                inputNumber = FeatureMap.inputsNumber

                FeatureMap.saveToaMiniDataFrame(mutantNumber, 16, probability1, probability2, inputNumber)
        else:

            # if probability1 == probability2:
            if math.isclose(probability1, probability2):
                
                inputNumber = FeatureMap.inputsNumber

                FeatureMap.saveToaMiniDataFrame(mutantNumber, 16, probability1, probability2, inputNumber)


        

