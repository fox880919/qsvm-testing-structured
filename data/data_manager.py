
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from pennylane import numpy as np

from .load_digits import DigitsData
from .credit_card import KaggleCreditCardData
from .mnist import MNISTData

# from .wine_data import WineData

from .wine_data_manager import WineDataManager

class DataManager:

  
    
    def getData(self, number = 0):

        wineDataManagerClass = WineDataManager.getWineData()
        WineData = wineDataManagerClass

        options = {
        0 : WineData,
        1: DigitsData, 
        2: KaggleCreditCardData,
        3: MNISTData
      }

        # myData = WineData()

        # myData = DataManager.options[number]()
        data_class = options.get(number, WineData)
        myData = data_class()

        x,y, x_normalized = myData.getData()

        # print(f'DataManager getData, len(x): {len(x)}')

        return  x,y, x_normalized
    
