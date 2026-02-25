from sklearn.datasets import fetch_openml
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from pennylane import numpy as np

from classes.parameters import MyParameters

class MNISTData:
    """
    Loads and preprocesses a stratified sample of the full MNIST dataset.
    """
    def getData(self):
        """
        Loads a percentage of the MNIST dataset using stratification.

        Args:
            data_fraction (float): The fraction of the dataset to load (e.g., 0.1 for 10%).
                                   Defaults to 1.0 (100% of the data).

        Returns:
            A tuple containing:
            - The original sampled features (pixel values) as a numpy array.
            - The sampled labels (digits 0-9) as a numpy array.
            - The processed (scaled and normalized) sampled features as a numpy array.
        """

        data_fraction = 1.0

        if MyParameters.usePercentageOfData:
            data_fraction = MyParameters.PercentageOfData

        if not (0 < data_fraction <= 1.0):
            raise ValueError("data_fraction must be between 0 and 1.")

        # Load the full MNIST dataset from OpenML.
        # as_frame=False returns the data as NumPy arrays directly.
        print("Loading full MNIST dataset... (This may take a moment on the first run)")
        mnist_data = fetch_openml('mnist_784', version=1, as_frame=False, parser='auto')
        print("Dataset loaded.")

        X_full = mnist_data.data
        # The labels are loaded as strings, so we convert them to integers
        y_full = mnist_data.target.astype(int)

        # If we want the full dataset, no need to split
        if data_fraction == 1.0:
            X_sample, y_sample = X_full, y_full
        else:
            # Create a stratified sample of the desired size
            X_sample, _, y_sample, _ = train_test_split(
                X_full,
                y_full,
                train_size=data_fraction,
                stratify=y_full,  # Ensures each digit is proportionally represented
                random_state=42   # For reproducible results
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
    # Load just 5% of the data (3,500 images) due to the large size of MNIST
    sample_percentage = 0.05
    print(f"Attempting to load {sample_percentage:.0%} of the MNIST dataset... ✍️")

    data_loader = MNISTData()
    X_original, y_labels, X_processed = data_loader.getData(data_fraction=sample_percentage)

    if X_original is not None:
        print("\nDataset sample loaded successfully! ✅")
        print(f"Shape of the processed features: {X_processed.shape}")
        print(f"Shape of the labels: {y_labels.shape}")

        print("\nChecking the digit distribution in the sample:")
        unique, counts = np.unique(y_labels, return_counts=True)
        distribution = dict(zip(unique, counts))
        print(distribution)