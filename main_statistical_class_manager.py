import importlib

from classes.parameters import MyParameters

from classes.default_parameters import DefaultParameters


class MainStatisticalClassManager: 

    def getMainStatisticalClass():

        # print(f'getMainClass, DefaultParameters.featureMapType: {DefaultParameters.featureMapType }')

        mainClassMutation = f'main_statistical_class_m{MyParameters.testMutation}'

        module = ''

        try:
        # The standard and safest way to do dynamic imports in Python
            
            if MyParameters.testMutation in MyParameters.mainStatisticalClassMutationList:

                module = importlib.import_module(mainClassMutation)
                print(f'getMainStatisticalClass, module: {module}')

            else:

                module = importlib.import_module('main_statistical_class')

            return module.MainStatisticalClass
        
        except ImportError:
            print(f"Error: Could not find the module named '{mainClassMutation}'.")
        return None


