from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from pennylane import numpy as np

class WineData:

    def getData(self):

        wine_data = load_wine()
        x = wine_data.data
        y = wine_data.target
        
        # x = np.vstack([x, x[0]])
        # y = np.append(y, y[0])

        # print(f'len(x): {len(x)}')
        # print(f'len(y): {len(y)}')
        # print(f'x[-1]:{x[-1]}')
        # print(f'y[-1]:{y[-1]}')

        x = x[y != 2]
        y = y[y != 2]

        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x)

        norm = np.linalg.norm(x_scaled, axis=1)
        x_normalized = x_scaled / norm[:, np.newaxis]

        return x,y, x_normalized
    
