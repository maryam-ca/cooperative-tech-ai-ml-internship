"""
randomforest_model.py
----------------------------------------
Train and evaluate Random Forest Classifier.

Includes:
1. Random Forest Training
2. GridSearchCV Hyperparameter Tuning
3. Feature Importance
4. Evaluation Metrics
5. Save Model

Author: Maryam Fatima
Week 4 - Day 17
"""

import time
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


def train_random_forest(X_train, y_train):
    """
    Train Random Forest Classifier.
    """

    print("\nTraining Random Forest...")

    start_time = time.time()

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )

    model.fit(X_train, y_train)

    training_time = time.time() - start_time

    print(f"Training Time : {training_time:.4f} seconds")

    return model, training_time


def evaluate_random_forest(model, X_test, y_test):
    """
    Evaluate Random Forest model.
    """

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    cm = confusion_matrix(y_test, predictions)

    print("\n==============================")
    print("Random Forest Evaluation")
    print("==============================")

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


def tune_random_forest(X_train, y_train):
    """
    Hyperparameter tuning using GridSearchCV.
    """

    print("\nRunning GridSearchCV for Random Forest...")

    parameter_grid = {
        "n_estimators": [100, 200, 300],
        "max_depth": [5, 10, 15, None]
    }

    grid = GridSearchCV(
        estimator=RandomForestClassifier(random_state=42),
        param_grid=parameter_grid,
        cv=5,
        scoring="f1",
        n_jobs=-1
    )

    start_time = time.time()

    grid.fit(X_train, y_train)

    training_time = time.time() - start_time

    print("\nBest Parameters")
    print(grid.best_params_)

    print(f"Best CV Score : {grid.best_score_:.4f}")
    print(f"Training Time : {training_time:.4f} sec")

    return grid.best_estimator_, training_time


def feature_importance(model, feature_names):
    """
    Display Feature Importance.
    """

    importance = pd.DataFrame({
        "Feature": feature_names,
        "Importance": model.feature_importances_
    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    print("\nTop Important Features\n")
    print(importance)

    return importance


def save_random_forest(model, filename):
    """
    Save trained Random Forest model.
    """

    joblib.dump(model, filename)

    print(f"\nModel saved successfully as {filename}")