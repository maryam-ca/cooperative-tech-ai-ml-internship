# Week 4 - Day 20

# Model Comparison - Feature Engineering, Baseline & Advanced Machine Learning Models

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-blue)
![GitHub](https://img.shields.io/badge/GitHub-Version_Control-181717)
![VS Code](https://img.shields.io/badge/VS_Code-Editor-007ACC)

---

# Objective

The objective of Day 20 was to develop a complete machine learning workflow for the Bank Marketing Dataset. The project focused on preparing data through feature engineering, training baseline and advanced classification models, comparing their performance, and selecting the most suitable model for predicting whether a customer subscribes to a term deposit.

The project also emphasized maintaining a professional project structure by saving processed datasets, trained models, evaluation metrics, and visualizations for future model development and deployment.

---

# Folder Structure

```text
week-4/
└── day-20/
    ├── data/
    │   ├── raw/
    │   │   └── bank-full.csv
    │   │
    │   └── processed/
    │       ├── X_train.csv
    │       ├── X_test.csv
    │       ├── y_train.csv
    │       └── y_test.csv
    │
    ├── notebooks/
    │   ├── 01_feature_engineering.ipynb
    │   ├── 02_baseline_models.ipynb
    │   ├── 03_advanced_models_start.ipynb
    │   └── 04_model_comparison.ipynb
    │
    ├── outputs/
    │   ├── model_results/
    │   │   ├── baseline_metrics.csv
    │   │   ├── advanced_metrics.csv
    │   │   └── model_comparison.csv
    │   │
    │   └── visualizations/
    │       ├── baseline_comparison.png
    │       ├── advanced_comparison.png
    │       └── model_comparison.png
    │
    ├── models/
    │   ├── baseline_logreg.pkl
    │   ├── baseline_dt.pkl
    │   ├── baseline_rf.pkl
    │   ├── gradient_boosting.pkl
    │   ├── xgboost.pkl
    │   ├── svm.pkl
    │   ├── scaler.pkl
    │   ├── label_encoder.pkl
    │   └── feature_encoders.pkl
    │
    └── README.md
```

---

# Dataset Used

## Bank Marketing Dataset

The **Bank Marketing Dataset** from the **UCI Machine Learning Repository** was used for this project.

The dataset contains information collected during direct marketing campaigns conducted by a Portuguese banking institution. The objective is to predict whether a client will subscribe to a term deposit.

---

## Dataset Statistics

| Attribute | Value |
|-----------|------|
| Total Samples | 45,211 |
| Total Features | 17 |
| Target Variable | y (yes/no) |
| Problem Type | Binary Classification |

---

## Features Included

### Client Information

- Age
- Job
- Marital Status
- Education
- Default
- Housing Loan
- Personal Loan

### Campaign Information

- Contact Type
- Month
- Duration
- Campaign
- Pdays
- Previous
- Poutcome

### Target Variable

- y
  - Yes
  - No

---

# Machine Learning Workflow

## 1. Feature Engineering & Data Preprocessing

The first notebook focused on preparing the dataset before model training.

### Tasks Performed

- Imported required libraries
- Loaded dataset
- Explored dataset structure
- Checked missing values
- Removed duplicate records
- Identified numerical and categorical features
- Encoded categorical variables
- Encoded target labels
- Standardized numerical features
- Performed train-test split
- Saved processed datasets
- Saved preprocessing objects

### Files Generated

- X_train.csv
- X_test.csv
- y_train.csv
- y_test.csv
- scaler.pkl
- label_encoder.pkl
- feature_encoders.pkl

### Outcome

A clean and reusable machine learning dataset was prepared for model training.

---

## 2. Baseline Machine Learning Models

Baseline models were trained to establish benchmark performance.

### Models Implemented

- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier

### Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-Score

### Files Generated

- baseline_logreg.pkl
- baseline_dt.pkl
- baseline_rf.pkl
- baseline_metrics.csv

### Outcome

Baseline performance was established for comparison with more advanced machine learning algorithms.

---

## 3. Advanced Machine Learning Models

Advanced classification models were implemented to improve predictive performance.

### Models Implemented

- Gradient Boosting Classifier
- XGBoost Classifier
- Support Vector Machine (SVM)

### Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-Score

### Files Generated

- gradient_boosting.pkl
- xgboost.pkl
- svm.pkl
- advanced_metrics.csv

### Outcome

Advanced machine learning models demonstrated improved predictive capability and provided multiple approaches for solving the classification problem.

---

## 4. Model Comparison

All baseline and advanced models were evaluated using the same performance metrics.

### Comparison Metrics

- Accuracy
- Precision
- Recall
- F1-Score

### Visualizations Generated

- Baseline Model Comparison
- Advanced Model Comparison
- Overall Model Comparison

### Files Generated

- model_comparison.csv
- baseline_comparison.png
- advanced_comparison.png
- model_comparison.png

### Outcome

A comprehensive comparison was performed to identify the best-performing classification model.

---

# Machine Learning Concepts Practiced

## Feature Engineering

- Feature Identification
- Label Encoding
- Target Encoding
- Feature Scaling
- Train-Test Split

---

## Baseline Models

- Logistic Regression
- Decision Tree
- Random Forest

---

## Advanced Models

- Gradient Boosting
- XGBoost
- Support Vector Machine (SVM)

---

## Model Evaluation

- Accuracy
- Precision
- Recall
- F1-Score
- Classification Report
- Model Comparison

---

## Data Visualization

- Accuracy Comparison
- F1-Score Comparison
- Precision vs Recall
- Model Performance Charts

---

# Key Findings

- Proper feature engineering significantly improves machine learning performance.
- Feature scaling is essential for distance-based algorithms such as Support Vector Machines.
- Ensemble learning methods generally achieve better predictive performance than individual classifiers.
- Comparing multiple algorithms helps identify the most suitable model for the given dataset.
- Saving preprocessing objects and trained models ensures reproducibility and simplifies future deployment.
- Maintaining a well-organized project structure improves maintainability and collaboration.

---

# Learning Outcomes

By completing Day 20, I learned how to:

- Build a complete machine learning pipeline.
- Perform feature engineering and preprocessing.
- Encode categorical variables and target labels.
- Apply feature scaling using StandardScaler.
- Train baseline classification models.
- Train advanced machine learning models.
- Evaluate models using multiple performance metrics.
- Compare different machine learning algorithms.
- Save trained models for future prediction.
- Organize a professional machine learning project using GitHub.

---

# Technologies & Libraries Used

### Programming Language

- Python

### Data Processing

- Pandas
- NumPy

### Machine Learning

- Scikit-Learn
- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting
- XGBoost
- Support Vector Machine (SVM)

### Preprocessing

- StandardScaler
- LabelEncoder

### Model Persistence

- Joblib

### Visualization

- Matplotlib

### Development Tools

- Jupyter Notebook
- Git
- GitHub
- Visual Studio Code (VS Code)

---

# Project Summary

This project demonstrates a complete end-to-end machine learning workflow, beginning with data preprocessing and feature engineering, followed by baseline and advanced model development, evaluation, and performance comparison.

The generated datasets, trained models, evaluation metrics, and visualizations provide a reusable foundation for future experimentation, hyperparameter tuning, and deployment of machine learning models.