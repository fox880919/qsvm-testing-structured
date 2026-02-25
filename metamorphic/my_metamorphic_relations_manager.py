import importlib

from classes.parameters import MyParameters


class QKernelManager: 
    def getqKernel(self):
        
        metamorphicMutation = f'metamorphic.my_metamorphic_relations_m{MyParameters.testMutation}'

        module = ''

        try:
        # The standard and safest way to do dynamic imports in Python
            
            if MyParameters.testMutation in MyParameters.metamorphicMutationList:

                module = importlib.import_module(metamorphicMutation)
                print(f'metamorphicMutation, module: {module}')

            else:

                module = importlib.import_module('metamorphic.my_metamorphic_relations')

            return module.MyMetamorphicRelations
        
        except ImportError:
            print(f"Error: Could not find the module named '{metamorphicMutation}'.")
        return None


