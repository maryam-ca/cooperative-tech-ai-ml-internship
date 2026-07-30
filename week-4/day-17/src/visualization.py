"""
visualization.py
---------------------------------------
Visualization functions for Week 4 Day 17

Includes:
1. Decision Boundary
2. Confusion Matrix
3. Accuracy Comparison
4. Training Time Comparison
5. Feature Importance
6. GridSearchCV Results

Author: Maryam Fatima
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix


# ---------------------------------------------------
# Confusion Matrix
# ---------------------------------------------------

def plot_confusion_matrix(y_true, y_pred, title):

    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(6,5))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False
    )

    plt.title(title)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------
# Accuracy Comparison
# ---------------------------------------------------

def plot_accuracy(models, accuracies):

    plt.figure(figsize=(8,5))

    plt.bar(models, accuracies)

    plt.title("Model Accuracy Comparison")
    plt.ylabel("Accuracy")
    plt.xlabel("Models")

    plt.ylim(0,1)

    for i,v in enumerate(accuracies):
        plt.text(i,v+0.01,f"{v:.3f}",ha='center')

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------
# Training Time Comparison
# ---------------------------------------------------

def plot_training_time(models, times):

    plt.figure(figsize=(8,5))

    plt.bar(models,times)

    plt.title("Training Time Comparison")
    plt.xlabel("Models")
    plt.ylabel("Seconds")

    for i,v in enumerate(times):
        plt.text(i,v,f"{v:.3f}s",ha='center')

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------
# Feature Importance
# ---------------------------------------------------

def plot_feature_importance(feature_df, top=15):

    top_features = feature_df.head(top)

    plt.figure(figsize=(10,6))

    plt.barh(
        top_features["Feature"],
        top_features["Importance"]
    )

    plt.title("Top Feature Importance")

    plt.xlabel("Importance")

    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------
# Grid Search Scores
# ---------------------------------------------------

def plot_gridsearch_scores(grid):

    results = grid.cv_results_

    scores = results["mean_test_score"]

    plt.figure(figsize=(10,5))

    plt.plot(scores, marker="o")

    plt.title("GridSearchCV Mean Test Scores")

    plt.xlabel("Parameter Combination")

    plt.ylabel("Mean F1 Score")

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# ---------------------------------------------------
# Decision Boundary
# ---------------------------------------------------

def plot_decision_boundary(model, X, y, title):

    x_min = X[:,0].min()-1
    x_max = X[:,0].max()+1

    y_min = X[:,1].min()-1
    y_max = X[:,1].max()+1

    xx, yy = np.meshgrid(
        np.arange(x_min,x_max,0.02),
        np.arange(y_min,y_max,0.02)
    )

    Z = model.predict(
        np.c_[xx.ravel(),yy.ravel()]
    )

    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(8,6))

    plt.contourf(
        xx,
        yy,
        Z,
        alpha=0.3
    )

    plt.scatter(
        X[:,0],
        X[:,1],
        c=y,
        edgecolors="k"
    )

    plt.title(title)

    plt.xlabel("Feature 1")

    plt.ylabel("Feature 2")

    plt.tight_layout()

    plt.show()


# ---------------------------------------------------
# Compare Multiple Models
# ---------------------------------------------------

def comparison_chart(results):

    models = list(results.keys())

    accuracy = [
        results[m]["accuracy"]
        for m in models
    ]

    f1 = [
        results[m]["f1"]
        for m in models
    ]

    x = np.arange(len(models))

    width = 0.35

    plt.figure(figsize=(9,5))

    plt.bar(
        x-width/2,
        accuracy,
        width,
        label="Accuracy"
    )

    plt.bar(
        x+width/2,
        f1,
        width,
        label="F1 Score"
    )

    plt.xticks(x,models)

    plt.ylim(0,1)

    plt.legend()

    plt.title("Accuracy vs F1 Score")

    plt.tight_layout()

    plt.show()