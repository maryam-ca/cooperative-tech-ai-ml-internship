# ============================================================
# Week 4 - Day 16
# Random Forest | Gradient Boosting | XGBoost
# AI/ML Internship
# ============================================================

import os
import time
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier
)

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

warnings.filterwarnings("ignore")

# ============================================================
# Create Output Folder
# ============================================================

os.makedirs("outputs", exist_ok=True)

# ============================================================
# Load Dataset
# ============================================================

print("=" * 60)
print("Loading Dataset")
print("=" * 60)

df = pd.read_csv("data/breast_cancer.csv")

print(df.head())

# ============================================================
# Dataset Information
# ============================================================

print("\nDataset Shape")
print(df.shape)

print("\nDataset Info")
print(df.info())

print("\nMissing Values")
print(df.isnull().sum())

# ============================================================
# Remove unnecessary columns
# ============================================================

if "id" in df.columns:
    df.drop("id", axis=1, inplace=True)

if "Unnamed: 32" in df.columns:
    df.drop("Unnamed: 32", axis=1, inplace=True)

# ============================================================
# Encode Target
# ============================================================

df["diagnosis"] = df["diagnosis"].map({
    "M": 1,
    "B": 0
})

# ============================================================
# Features & Labels
# ============================================================

X = df.drop("diagnosis", axis=1)

y = df["diagnosis"]

# ============================================================
# Train Test Split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

# ============================================================
# Function for Evaluation
# ============================================================

results = []


def evaluate_model(model, name):

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    start = time.time()

    model.fit(X_train, y_train)

    end = time.time()

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(y_test, predictions)

    recall = recall_score(y_test, predictions)

    f1 = f1_score(y_test, predictions)

    training_time = end - start

    print("\nAccuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))
    print("Time     :", round(training_time, 4), "seconds")

    print("\nClassification Report\n")
    print(classification_report(y_test, predictions))

    cm = confusion_matrix(y_test, predictions)

    plt.figure(figsize=(5, 4))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues"
    )

    plt.title(name + " Confusion Matrix")

    plt.xlabel("Predicted")

    plt.ylabel("Actual")

    plt.show()

    results.append([
        name,
        accuracy,
        precision,
        recall,
        f1,
        training_time
    ])

    return model

# ============================================================
# Random Forest
# ============================================================

rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

rf = evaluate_model(
    rf,
    "Random Forest"
)

# ============================================================
# Gradient Boosting
# ============================================================

gb = GradientBoostingClassifier(
    random_state=42
)

gb = evaluate_model(
    gb,
    "Gradient Boosting"
)

# ============================================================
# XGBoost
# ============================================================

xgb = XGBClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=5,
    random_state=42,
    eval_metric="logloss"
)

xgb = evaluate_model(
    xgb,
    "XGBoost"
)

# ============================================================
# Comparison Table
# ============================================================

comparison = pd.DataFrame(
    results,
    columns=[
        "Model",
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "Training Time"
    ]
)

comparison.to_csv(
    "outputs/model_results.csv",
    index=False
)

print("\nModel Comparison\n")

print(comparison)

# ============================================================
# Feature Importance Function
# ============================================================

def plot_feature_importance(model, title, filename):

    importance = pd.DataFrame({

        "Feature": X.columns,

        "Importance": model.feature_importances_

    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    plt.figure(figsize=(10, 7))

    plt.barh(
        importance["Feature"],
        importance["Importance"]
    )

    plt.title(title)

    plt.gca().invert_yaxis()

    plt.tight_layout()

    plt.savefig("outputs/" + filename)

    plt.show()


# ============================================================
# Random Forest Importance
# ============================================================

plot_feature_importance(
    rf,
    "Random Forest Feature Importance",
    "rf_feature_importance.png"
)

# ============================================================
# Gradient Boosting Importance
# ============================================================

plot_feature_importance(
    gb,
    "Gradient Boosting Feature Importance",
    "gb_feature_importance.png"
)

# ============================================================
# XGBoost Importance
# ============================================================

plot_feature_importance(
    xgb,
    "XGBoost Feature Importance",
    "xgb_feature_importance.png"
)

print("\nOutputs saved successfully.")

print("Check outputs folder.")