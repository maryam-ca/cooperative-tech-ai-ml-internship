"""
utils.py
--------------------------------------------
Utility functions for Week 4 - Day 17

Includes:
1. Save Model
2. Load Model
3. Save Metrics
4. Save Best Parameters
5. Display Results Table

Author: Maryam Fatima
"""

import os
import joblib
import pandas as pd


# ===================================================
# Create Folder
# ===================================================

def create_directory(folder_name):
    """
    Create directory if it does not exist.
    """

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"{folder_name} folder created.")
    else:
        print(f"{folder_name} already exists.")


# ===================================================
# Save Model
# ===================================================

def save_model(model, filename):
    """
    Save trained ML model.
    """

    joblib.dump(model, filename)

    print(f"\nModel saved successfully!")
    print(f"Location : {filename}")


# ===================================================
# Load Model
# ===================================================

def load_model(filename):
    """
    Load saved ML model.
    """

    model = joblib.load(filename)

    print(f"\nModel loaded successfully!")
    print(f"Location : {filename}")

    return model


# ===================================================
# Save Metrics
# ===================================================

def save_metrics(results, filename):
    """
    Save evaluation metrics into CSV.
    """

    df = pd.DataFrame(results)

    df.to_csv(filename, index=False)

    print(f"\nMetrics saved to {filename}")


# ===================================================
# Save Best Parameters
# ===================================================

def save_best_parameters(parameters, filename):
    """
    Save GridSearchCV best parameters.
    """

    with open(filename, "w") as file:

        file.write("Best Parameters\n")
        file.write("=======================\n\n")

        for key, value in parameters.items():
            file.write(f"{key} : {value}\n")

    print(f"\nBest Parameters saved to {filename}")


# ===================================================
# Results Table
# ===================================================

def results_table(model_names,
                  accuracy,
                  precision,
                  recall,
                  f1,
                  training_time):
    """
    Create performance comparison table.
    """

    df = pd.DataFrame({

        "Model": model_names,

        "Accuracy": accuracy,

        "Precision": precision,

        "Recall": recall,

        "F1 Score": f1,

        "Training Time (sec)": training_time

    })

    return df


# ===================================================
# Print Results
# ===================================================

def print_results(df):
    """
    Print results neatly.
    """

    print("\n")
    print("="*70)

    print("MODEL COMPARISON")

    print("="*70)

    print(df)

    print("="*70)


# ===================================================
# Save Results Table
# ===================================================

def export_results(df, filename):
    """
    Export results table.
    """

    df.to_csv(filename, index=False)

    print(f"\nResults exported to {filename}")


# ===================================================
# Project Banner
# ===================================================

def banner():

    print("="*70)
    print("        WEEK 4 - DAY 17")
    print(" Support Vector Machine & GridSearchCV ")
    print("="*70)