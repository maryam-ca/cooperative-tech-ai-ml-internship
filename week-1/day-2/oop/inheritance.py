"""
Machine Learning Dataset System
"""

class Dataset:
    """
    Parent class representing a dataset.
    """

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name

    def load_data(self):
        print(f"Loading dataset: {self.dataset_name}")


class MLDataset(Dataset):
    """
    Child class inheriting Dataset.
    """

    def clean_data(self):
        print("Removing missing values...")

    def train_model(self):
        print("Training Machine Learning Model...")


dataset = MLDataset("Student Performance Dataset")

dataset.load_data()
dataset.clean_data()
dataset.train_model()