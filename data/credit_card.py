import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split # Import train_test_split
from pennylane import numpy as np

from classes.parameters import MyParameters

class KaggleCreditCardData:
    """
    Loads and preprocesses a stratified sample of the Kaggle Credit Card Fraud dataset.
    """
    def getData(self):
        """
        Loads a percentage of the data from "./datasets/creditcard.csv" using stratification.

        Args:
            data_fraction (float): The fraction of the dataset to load (e.g., 0.1 for 10%).
                                   Defaults to 1.0 (100% of the data).

        Returns:
            A tuple containing:
            - The original sampled features as a numpy array.
            - The sampled labels as a numpy array.
            - The processed (scaled and normalized) sampled features as a numpy array.
        """
        
        data_fraction = 1.0

        if MyParameters.usePercentageOfData:
            data_fraction = MyParameters.PercentageOfData


        file_path = "./datasets/creditcard.csv"
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            return None, None, None

        if not (0 < data_fraction <= 1.0):
            raise ValueError("data_fraction must be between 0 and 1.")

        # Separate features and target from the full dataset
        X_full = df.drop('Class', axis=1).values
        y_full = df['Class'].values

        # If we want the full dataset, no need to split
        if data_fraction == 1.0:
            X_sample, y_sample = X_full, y_full
        else:
            # Use train_test_split to create a stratified sample
            # We only care about the "train" part, which is our sample. The "_" discards the rest.
            X_sample, _, y_sample, _ = train_test_split(
                X_full,
                y_full,
                train_size=data_fraction,
                stratify=y_full,  # This is the crucial part for stratification!
                random_state=42    # for reproducible results
            )

        # --- Preprocessing Steps (on the sample) ---

        # 1. Scale the sampled features
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(X_sample)

        # 2. Normalize the vectors
        norm = np.linalg.norm(x_scaled, axis=1)
        x_normalized = x_scaled / (norm[:, np.newaxis] + 1e-9)

        return X_sample, y_sample, x_normalized

# --- How to Use ---
if __name__ == '__main__':
    # Load just 10% of the data
    sample_percentage = 0.1
    print(f"Attempting to load {sample_percentage:.0%} of the credit card data... 📉")

    data_loader = KaggleCreditCardData()
    X_original, y_labels, X_processed = data_loader.getData(data_fraction=sample_percentage)

    if X_original is not None:
        print("\nDataset sample loaded successfully! ✅")
        print(f"Shape of the processed features: {X_processed.shape}")
        print(f"Shape of the labels: {y_labels.shape}")

        print("\nChecking the fraud distribution in the sample:")
        unique, counts = np.unique(y_labels, return_counts=True)
        fraud_percentage = (counts[1] / len(y_labels)) * 100
        print(dict(zip(unique, counts)))
        print(f"Fraud cases make up {fraud_percentage:.4f}% of the sample.")