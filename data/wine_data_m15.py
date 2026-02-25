from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from pennylane import numpy as np

class WineData:

    def getData(self):

        print(f'in wine_data_m18')

        wine_data = load_wine()
        x = wine_data.data
        y = wine_data.target

        x = x[y != 1]
        y = y[y != 2]

        scaler = StandardScaler(with_mean=False)
        x_scaled = scaler.fit_transform(x)

        norm = np.linalg.norm(x_scaled, axis=1)
        x_normalized = x_scaled / norm[:, np.newaxis]

        return x,y, x_normalized
    
