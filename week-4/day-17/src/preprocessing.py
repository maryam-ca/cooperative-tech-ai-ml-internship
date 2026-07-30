"""
preprocessing.py
----------------
This module loads the dataset, performs preprocessing,
splits the data into training/testing sets, and scales features.
"""

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(test_size=0.2, random_state=42):
    """
    Load Breast Cancer Dataset.

    Returns:
        X_train_scaled
        X_test_scaled
        y_train
        y_test
        feature_names
    """

    # Load dataset
    data = load_breast_cancer()

    X = data.data
    y = data.target
    feature_names = data.feature_names

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    # Feature Scaling
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return (
        X_train_scaled,
        X_test_scaled,
        y_train,
        y_test,
        feature_names
    )