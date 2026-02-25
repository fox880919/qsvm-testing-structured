import importlib

from classes.parameters import MyParameters



class WineDataManager: 

    # def __init__(self):
   
    def getWineData():

        # print(f"getWineData has been accessed!")

        # print(f' in getWineData, :{MyParameters.testMutation}')
        wineDataMutation = f'data.wine_data_m{MyParameters.testMutation}'

        module = ''

        try:
        # The standard and safest way to do dynamic imports in Python
            
            if MyParameters.testMutation in MyParameters.dataMutationList:
                
                # print(f'WineDataManager getWineData, {MyParameters.testMutation} is in {MyParameters.dataMutationList}')
                module = importlib.import_module(wineDataMutation)
                print(f'getWineData, module: {module}')

            else:

                # print(f'WineDataManager getWineData, {MyParameters.testMutation} is not in {MyParameters.dataMutationList}')


                module = importlib.import_module('data.wine_data')

            return module.WineData
        
        except ImportError:
            print(f"Error: Could not find the module named '{wineDataMutation}'.")
        return None


