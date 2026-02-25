import importlib

from classes.parameters import MyParameters

from classes.default_parameters import DefaultParameters


class MainClassManager: 

    def getMainClass():

        # print(f'getMainClass, DefaultParameters.featureMapType: {DefaultParameters.featureMapType }')

        mainClassMutation = f'main_class_m{MyParameters.testMutation}'

        module = ''

        try:
        # The standard and safest way to do dynamic imports in Python
            
            if MyParameters.testMutation in MyParameters.mainClassMutationList:

                module = importlib.import_module(mainClassMutation)
                print(f'getMainClass, module: {module}')

            else:

                module = importlib.import_module('main_class')

            return module.MainClass
        
        except ImportError:
            print(f"Error: Could not find the module named '{mainClassMutation}'.")
        return None


