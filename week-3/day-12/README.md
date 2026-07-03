# Week 3 - Day 12

# Supervised Machine Learning - Classification Algorithms

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?logo=scikitlearn)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-green)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-blueviolet)
![Jupyter Notebook](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

# AI/ML Internship

**Organization:** Cooperative Tech Private Limited

**Internship:** Artificial Intelligence & Machine Learning Internship

**Week:** 3

**Day:** 12

---

# Overview

Day 12 focuses on **Supervised Machine Learning Classification Algorithms**.

The objective of this task is to understand how different classification algorithms work, compare their performance, and evaluate them using standard machine learning metrics.

During this task, multiple classification models were implemented using the Iris Dataset and a custom Classification Dataset. The project also includes feature engineering, model evaluation, visualization, comparison, and model saving for future deployment.

---

# Learning Objectives

After completing this task, I was able to:

- Understand Classification Problems
- Differentiate between Regression and Classification
- Implement Logistic Regression
- Implement Decision Tree Classification
- Implement K-Nearest Neighbors (KNN)
- Compare Multiple Machine Learning Models
- Apply Feature Scaling
- Evaluate Models using Accuracy, Precision, Recall and F1-Score
- Generate Confusion Matrices
- Visualize Decision Trees
- Analyze Feature Importance
- Save Trained Models using Joblib

---

# Classification Algorithms Covered

## 1. Logistic Regression

Logistic Regression is one of the most widely used supervised learning algorithms for classification problems.

### Topics Covered

- Binary Classification
- Multi-Class Classification
- Probability Prediction
- Sigmoid Function
- Decision Boundary
- Classification Report
- Confusion Matrix

---

## 2. Decision Tree

Decision Tree is a rule-based supervised learning algorithm.

### Topics Covered

- Tree Structure
- Gini Index
- Information Gain
- Tree Depth
- Feature Importance
- Tree Visualization
- Model Evaluation

---

## 3. K-Nearest Neighbors (KNN)

KNN is a distance-based supervised learning algorithm.

### Topics Covered

- Euclidean Distance
- Feature Scaling
- Choosing Best K
- Accuracy vs K Graph
- Model Evaluation

---

## 4. Model Comparison

Different models were compared using standard evaluation metrics.

Models Compared

- Logistic Regression
- Decision Tree
- KNN

Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1 Score

---

## 5. Project 1 Model Training

A second dataset was used for Project 1 implementation.

Algorithms Used

- Logistic Regression
- Random Forest

Tasks Performed

- Data Loading
- Feature Engineering
- Feature Scaling
- Model Training
- Model Evaluation
- ROC Curve
- Feature Importance
- Model Saving

---

# Folder Structure

```text
day-12/

│

├── data/
│   ├── iris.csv
│   ├── classification_dataset.csv
│   └── README.md
│
├── images/
│   ├── species_distribution.png
│   ├── species_distribution_decision_tree.png
│   ├── correlation_heatmap.png
│   ├── confusion_matrix_logistic.png
│   ├── confusion_matrix_decision_tree.png
│   ├── confusion_matrix_knn.png
│   ├── confusion_matrix_random_forest.png
│   ├── decision_tree_visualization.png
│   ├── feature_importance.png
│   ├── knn_accuracy_vs_k.png
│   ├── model_comparison_accuracy.png
│   ├── model_metrics_heatmap.png
│   ├── roc_curve.png
│   └── random_forest_feature_importance.png
│
├── notebooks/
│   ├── 01_logistic_regression.ipynb
│   ├── 02_decision_tree.ipynb
│   ├── 03_knn_classifier.ipynb
│   ├── 04_model_comparison.ipynb
│   └── 05_project1_model_training.ipynb
│
├── models/
│   ├── model.pkl
│   └── scaler.pkl
│
├── outputs/
│   ├── comparison_results.csv
│   ├── model_comparison.csv
│   ├── model_metrics.csv
│   ├── predictions.csv
│   └── classification_report.txt
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Datasets Used

## Iris Dataset

The Iris Dataset is one of the most popular datasets for learning machine learning classification.

Features

- Sepal Length
- Sepal Width
- Petal Length
- Petal Width

Target

- Species

Classification Type

- Multi-Class Classification

---

## Classification Dataset

Features

- Age
- Income

Target

- Will Buy

Classification Type

- Binary Classification

---

# Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-Learn
- Joblib
- Jupyter Notebook

---

# Notebooks Included

## 01_logistic_regression.ipynb

Topics

- Logistic Regression
- Feature Scaling
- Prediction
- Confusion Matrix
- Classification Report

---

## 02_decision_tree.ipynb

Topics

- Decision Tree
- Tree Visualization
- Feature Importance
- Confusion Matrix
- Tree Depth
- Number of Leaves

---

## 03_knn_classifier.ipynb

Topics

- KNN Classification
- Best K Selection
- Accuracy vs K
- Confusion Matrix
- Classification Report

---

## 04_model_comparison.ipynb

Topics

- Compare Multiple Models
- Accuracy Comparison
- Precision
- Recall
- F1 Score
- Best Model Selection

---

## 05_project1_model_training.ipynb

Topics

- Project Dataset
- Logistic Regression
- Random Forest
- ROC Curve
- Feature Importance
- Save Model
- Save Scaler

---

# Generated Outputs

After executing all notebooks, the project automatically generates

## Images

- Species Distribution
- Correlation Heatmap
- Confusion Matrix
- Decision Tree Visualization
- Feature Importance
- ROC Curve
- Model Comparison Graph
- Accuracy vs K Graph

---

## Models

- model.pkl
- scaler.pkl

---

## CSV Files

- comparison_results.csv
- model_comparison.csv
- model_metrics.csv
- predictions.csv

---

## Reports

- classification_report.txt

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/cooperative-tech-ai-ml-internship.git
```

Move into the project

```bash
cd week-3/day-12
```

Install dependencies

```bash
pip install -r requirements.txt
```

Launch Jupyter Notebook

```bash
jupyter notebook
```

---

# Learning Outcomes

After completing this task, I gained practical experience in

- Supervised Machine Learning
- Classification Algorithms
- Logistic Regression
- Decision Tree
- KNN Classification
- Random Forest
- Feature Engineering
- Feature Scaling
- Confusion Matrix
- Precision, Recall and F1 Score
- ROC Curve
- Feature Importance
- Model Comparison
- Saving Trained Models
- Machine Learning Workflow

---

# Future Improvements

Possible enhancements include

- Hyperparameter Tuning using GridSearchCV
- Cross Validation
- RandomizedSearchCV
- XGBoost Classifier
- LightGBM
- CatBoost
- Streamlit Deployment
- Flask API Deployment

---

# Author

**Maryam Fatima**

BS Software Engineering

Artificial Intelligence & Machine Learning Intern

Cooperative Tech Private Limited

---

## Thank You

Thank you for exploring my Week 3 Day 12 internship work.

If you found this project useful, consider giving the repository a ⭐ on GitHub.