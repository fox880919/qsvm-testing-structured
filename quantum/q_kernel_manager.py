import importlib



class QKernelManager: 
    def getqKernel(self):
        
        from classes.parameters import MyParameters

        qKernelMutation = f'quantum.q_kernel_m{MyParameters.testMutation}'

        module = ''

        try:
        # The standard and safest way to do dynamic imports in Python
            
            if MyParameters.testMutation in MyParameters.qKernelMutationList:

                module = importlib.import_module(qKernelMutation)
                print(f'getqKernel, module: {module}')

            else:

                module = importlib.import_module('quantum.q_kernel')

            return module.QKernel
        
        except ImportError:
            print(f"Error: Could not find the module named '{qKernelMutation}'.")
        return None


