import numpy as np

from scipy.linalg import expm

import pennylane as qml


class MyMetamorphicRelations:

    def useMetamorphicRelation(x_data, y_data, mrNumber, mrValue):
        
        result = x_data

        if mrNumber == 1:

            # print(f'useMetamorphicRelation, using metamorphic of scaling')
            result = MyMetamorphicRelations.metamorphic_feature_scaling(x_data, mrValue)
        
        elif mrNumber == 2:

            result = MyMetamorphicRelations.metamorphic_feature_rotation_with_angle(x_data, mrValue)
        
        elif mrNumber == 3:

            result = MyMetamorphicRelations.metamorphic_feature_permutation(x_data)

        elif mrNumber == 4:

            result = MyMetamorphicRelations.metamorphic_invert_all_labels_multiclass(y_data, mrValue)


        elif mrNumber == 5:

            result = MyMetamorphicRelations.perturb_parameters(x_data, mrValue)


        return result
    #1
    def metamorphic_feature_scaling(x_data, scaling_factor):

        # print(f'metamorphic_feature_scaling, x_data: {x_data[1]}')

        #mutation #22 start
        scaled_x_tr = x_data + scaling_factor
        #mutation #22 end

        # print(f'metamorphic_feature_scaling, scaled_x_tr: {scaled_x_tr[1]}')

        return scaled_x_tr

    
    #2-1
    def metamorphic_feature_rotation_with_angle(x, angle):
        # Generate a random rotation matrix
        rotation_matrix = expm(np.eye(x.shape[1]) * 1j * angle) 
        return np.dot(rotation_matrix, x.T).T
    
    #2-2 => to try later
    def metamorphic_feature_geometric_rotation_with_angle(x, angle):
        
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])
        
        # Apply the rotation to the data
        return np.dot(rotation_matrix, x.T).T

    #3
    def metamorphic_feature_permutation(input):
        # Randomly permute the feature columns
        
        # permutation = random.sample(range(input.shape[1]), input.shape[1])
        permutation = np.random.permutation(input.shape[0]) 

        #permute columns
        # input_permuted = input[:, permutation]
        # output_permuted = output[:, permutation]

        #permute rows
        input_permuted = input[permutation, :]

        return input_permuted


    #4
    def metamorphic_invert_all_labels_multiclass(y_data, num_classes):

        # y_train_inverted = y_train.copy()
        # y_test_inverted = y_test.copy()

        # print('2- y_train')
        # print(y_train)

        y_train_inverted = y_data

        for i in range(len(y_train_inverted)):
            y_train_inverted[i] = (y_train_inverted[i] + 1) % num_classes
        
      
        
        return y_train_inverted
    
    #5
    def perturb_parameters(self, x_data, delta=0.1):

        return x_data + np.random.uniform(-delta, delta, size=x_data.shape)
    
    #--
    def modify_circuit_depth(self, type):

        # print('type')
        # print(type)

        if(type == 1):

            print('type == 1')
        
            return MyMetamorphicRelations.__getAmplitudeEmdedding
        
    
    #6
    def addingAdditionalFeature(self, x_tr, x_test):

        # print('x_tr.shape: ', x_tr.shape)
        # print('x_test.shape: ', x_test.shape)

        x_tr_rows, x_tr_cols = x_tr.shape
        x_test_rows, x_test_cols = x_test.shape

        new_x_tr = np.empty((x_tr_rows,x_tr_cols+1))

        new_x_test = np.empty((x_test_rows,x_test_cols+1))

        i = 0

        for a_tr in x_tr:

            additionalFeature =  MyMetamorphicRelations.addingAdditionalFeaturePerInput(a_tr)

            new_x_tr[i] = np.append( x_tr[i], additionalFeature)

            i = i + 1

        i = 0

        for a_test in x_test:

            additionalFeature = MyMetamorphicRelations.addingAdditionalFeaturePerInput(a_test)

            new_x_test[i] = np.append( x_test[i], additionalFeature)
            i = i + 1
            # print('len(new_x_test[i])', len(new_x_test[i]))


        return new_x_tr, new_x_test
    
    #66
    def addingAdditionalFeaturePerInput(input):

        featuresNumber = len(input)
        
        featuresTotal = 0

        for feature in input:
        
            featuresTotal = featuresTotal + feature
        
        featuresAverage = featuresTotal/featuresNumber

        return featuresAverage
    
    #7
    def addingRedundantInputsAndOutputs(self, x_tr, x_test, y_tr, y_test):
        
        # print('y_tr.shape: ', y_tr.shape)

        x_y_tr_rows = y_tr.shape

        # print('x_y_tr_rows: ', x_y_tr_rows)

        new_x_tr = MyMetamorphicRelations.addExtraRowsToInputs(x_tr)

        new_x_test = MyMetamorphicRelations.addExtraRowsToInputs(x_test)
        new_y_tr = MyMetamorphicRelations.addExtraRowsToOutputs(y_tr)
        new_y_test = MyMetamorphicRelations.addExtraRowsToOutputs(y_test)

        # return x_tr, x_test, y_tr, y_test

        return new_x_tr, new_x_test, new_y_tr, new_y_test
    
    #81
    def addExtraRowsToInputs(data):

        x_data_rows, x_data_cols = data.shape

        new_data = np.empty((x_data_rows+1,x_data_cols))

        i = 0

        total = x_data_rows+1

        new_data[0] = data[0]

        while i + 1 < total:

            new_data[i+1] = data[i]

            i = i + 1
        
        return new_data
    
    def addExtraRowsToOutputs(data):

        # print('len(data): ', len(data))

        new_data = np.empty((len(data)+1))

        i = 0

        total = len(data)+1

        new_data[0] = data[0]

        while i + 1 < total:

            new_data[i+1] = data[i]

            i = i + 1
        
        return new_data

  
    # @qml.qnode(qml.device("lightning.qubit", wires = 4))
    def __getAmplitudeEmdedding(a, b, depth = 2, nqubits = 4):

        qml.AmplitudeEmbedding(
        a, wires=range(nqubits), pad_with=0, normalize=True)
        qml.adjoint(qml.AmplitudeEmbedding(
        b, wires=range(nqubits), pad_with=0, normalize=True))
        for _ in range(depth):
            for i in range(nqubits - 1):
                qml.CNOT(wires=[i, i+1])

        return qml.expval(qml.PauliZ(0))
        # return qml.probs(wires = range(nqubits))

