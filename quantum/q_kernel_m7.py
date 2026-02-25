from pennylane import numpy as np

from classes.parameters import MyParameters
# from classes.default_parameters import DefaultParameters

class QKernel:

    def getFeaturesAndNqubits(self, x_normalized, featureMap):

        print(f'len(x_normalized): {len(x_normalized)}')

        print(f'x_normalized.shape[1]: {x_normalized.shape[1]}')
        

        #mutation #7 start
        n_features = x_normalized.shape[1] + 5
        #mutation #7 end

        n_qubits = n_features

        if( featureMap == 0):
            n_qubits = int(np.ceil(np.log2(n_features)))

        print(f'n_features: {n_features}')

        print(f'n_qubits: {n_qubits}')

        if MyParameters.featureMapType == 0:

            MyParameters.amplitudeNQubits = n_qubits
        else:
            MyParameters.angleNQubits = n_qubits

        print(f'DefaultParameters.: {MyParameters.amplitudeNQubits}')
        print(f'DefaultParameters.angleNQubits: {MyParameters.angleNQubits}')

        # print(f'n_qubits): {n_qubits}')

        return n_features, n_qubits
    
    def pad_features(self, x, n_qubits):
        """Pads features of a dataset to make the length a power of 2."""
        target_length = 2**n_qubits
        if x.shape[1] < target_length:

            padding = np.zeros((x.shape[0], target_length - x.shape[1]))

            return np.hstack([x, padding])
        return x


