import importlib

from termcolor import colored


class FeatureMapManager: 
    def getFeatureMap(self):

        print(f'in Feature_map_manager')
        from classes.parameters import MyParameters

        print(f'Feature_map_manager getFeatureMap, MyParameters.testMutation: {MyParameters.testMutation}')
        # print(f'getFeatureMap, MyParameters.featureMapMutation == 0: {MyParameters.featureMapMutation == 0}')

        featureMapMutation = f'quantum.feature_map_m{MyParameters.testMutation}'

        # print(f'getFeatureMap, featureMapMutation: {featureMapMutation}')
        module = ''

        # print(f'getFeatureMap, featureMapMutation: {featureMapMutation}')
        try:
        # The standard and safest way to do dynamic imports in Python
            
            

            # if MyParameters.featureMapMutation == 0:
            if MyParameters.testMutation in MyParameters.featureMapMutationList:

                module = importlib.import_module(featureMapMutation)
                # print(f'getFeatureMap, module: {module}')

                # print(f'getFeatureMap, MyParameters.featureMapMutation == 0')

            # elif MyParameters.addQuantumRegister == True:
                
            #     featureMapMutation = 'quantum.feature_map_with_mr6'
            #     print(colored('in MyParameters.addQuantumRegister == True', 'red'))

            #     module = importlib.import_module(featureMapMutation)
        
            else:

                module = importlib.import_module('quantum.feature_map')


            print(colored(f'getFeatureMap, MyPmodule: {module}', 'green') )

            return module.FeatureMap
        

        except ImportError:
            print(f"Error: Could not find the module named '{featureMapMutation}'.")
        return None


