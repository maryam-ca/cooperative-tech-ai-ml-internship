"""
svm_model.py
------------------------
Train and evaluate Support Vector Machine models.

Models Included:
1. Linear SVM
2. RBF SVM
3. GridSearchCV Hyperparameter Tuning

Author: Maryam Fatima
Week 4 - Day 17
"""

import time
import joblib

from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
from sklearn.model_selection import GridSearchCV


def evaluate_model(model, X_test, y_test):
    """
    Evaluate a trained model.
    """

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    cm = confusion_matrix(y_test, predictions)

    print("=" * 50)
    print("Model Evaluation")
    print("=" * 50)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    print("\nConfusion Matrix")
    print(cm)

    print("\nClassification Report")
    print(classification_report(y_test, predictions))

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": cm
    }


def train_linear_svm(X_train, y_train):
    """
    Train Linear Kernel SVM.
    """

    print("\nTraining Linear SVM...")

    start = time.time()

    model = SVC(
        kernel="linear",
        C=1.0,
        random_state=42
    )

    model.fit(X_train, y_train)

    training_time = time.time() - start

    print(f"Training Time: {training_time:.4f} sec")

    return model, training_time


def train_rbf_svm(X_train, y_train):
    """
    Train RBF Kernel SVM.
    """

    print("\nTraining RBF SVM...")

    start = time.time()

    model = SVC(
        kernel="rbf",
        C=1.0,
        gamma="scale",
        random_state=42
    )

    model.fit(X_train, y_train)

    training_time = time.time() - start

    print(f"Training Time: {training_time:.4f} sec")

    return model, training_time


def tune_svm_gridsearch(X_train, y_train):
    """
    Hyperparameter tuning using GridSearchCV.
    """

    print("\nRunning GridSearchCV...")

    parameter_grid = {
        "C": [0.1, 1, 10, 100],
        "kernel": ["linear", "rbf"],
        "gamma": ["scale", "auto"]
    }

    grid_search = GridSearchCV(
        estimator=SVC(),
        param_grid=parameter_grid,
        cv=5,
        scoring="f1",
        n_jobs=-1
    )

    start = time.time()

    grid_search.fit(X_train, y_train)

    training_time = time.time() - start

    print("\nBest Parameters")
    print(grid_search.best_params_)

    print("\nBest Cross Validation Score")
    print(grid_search.best_score_)

    print(f"\nTraining Time: {training_time:.2f} sec")

    return grid_search.best_estimator_, training_time


def save_model(model, filename):
    """
    Save trained model.
    """

    joblib.dump(model, filename)
    print(f"Model saved successfully -> {filename}")