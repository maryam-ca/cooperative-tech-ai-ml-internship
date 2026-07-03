#  Week 3 - Day 13 | Model Evaluation

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Jupyter Notebook](https://img.shields.io/badge/Jupyter-Notebook-orange?style=for-the-badge&logo=jupyter)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?style=for-the-badge&logo=scikitlearn)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?style=for-the-badge&logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-4C72B0?style=for-the-badge)
![Joblib](https://img.shields.io/badge/Joblib-Model%20Saving-success?style=for-the-badge)
![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)

---

##  Overview

This repository contains the complete implementation of **Week 3 - Day 13** of the AI/ML Internship Program at Cooperative Tech Private Limited.

The primary objective of Day 13 is to understand how Machine Learning models are evaluated using professional evaluation metrics instead of relying only on accuracy.

During this task, a Logistic Regression model is trained on the Iris dataset and evaluated using various performance metrics such as Accuracy, Precision, Recall, F1 Score, Confusion Matrix, ROC Curve, ROC-AUC Score, and Cross Validation.

The trained model and scaler are also saved using Joblib for future deployment in a Streamlit application.

---

#  Learning Objectives

After completing this task, you will be able to:

- Understand why Accuracy alone is not enough.
- Interpret Confusion Matrix.
- Calculate Precision, Recall and F1 Score.
- Generate Classification Report.
- Plot ROC Curve.
- Calculate ROC-AUC Score.
- Perform 5-Fold Cross Validation.
- Save Machine Learning models using Joblib.
- Prepare models for deployment.

---

#  Machine Learning Concepts Covered

##  Logistic Regression

Logistic Regression is a supervised machine learning algorithm used for classification problems.

Unlike Linear Regression, it predicts probabilities instead of continuous values.

It is commonly used for:

- Email Spam Detection
- Customer Churn Prediction
- Disease Prediction
- Fraud Detection
- Sentiment Analysis

---

##  Confusion Matrix

A Confusion Matrix is one of the most important evaluation techniques for classification models.

It shows how many predictions are correct and how many are incorrect.

It consists of:

- True Positive (TP)
- True Negative (TN)
- False Positive (FP)
- False Negative (FN)

Using these four values, many evaluation metrics can be calculated.

---

##  Classification Report

Classification Report provides:

- Precision
- Recall
- F1 Score
- Support

for every class in the dataset.

It helps us understand the model performance in greater detail.

---

##  Precision

Precision measures how many predicted positive samples are actually positive.

### Formula

```text
Precision = TP / (TP + FP)
```

Higher Precision means fewer false positives.

---

##  Recall

Recall measures how many actual positive samples are correctly identified.

### Formula

```text
Recall = TP / (TP + FN)
```

Higher Recall means fewer false negatives.

---

##  F1 Score

F1 Score is the harmonic mean of Precision and Recall.

### Formula

```text
F1 = 2 × (Precision × Recall)
      -------------------------
       Precision + Recall
```

F1 Score becomes important when datasets are imbalanced.

---

##  ROC Curve

ROC stands for

Receiver Operating Characteristic Curve.

It shows how well the classifier separates different classes.

The graph plots

- True Positive Rate
- False Positive Rate

at different threshold values.

---

##  ROC-AUC Score

ROC-AUC measures the overall quality of the classifier.

Score Range

| Score | Performance |
|--------|------------|
| 1.0 | Perfect Model |
| 0.9 | Excellent |
| 0.8 | Very Good |
| 0.7 | Good |
| 0.6 | Fair |
| 0.5 | Random Guess |

---

##  Cross Validation

Cross Validation is used to test the stability of a machine learning model.

Instead of training only once, the dataset is divided into multiple folds.

The model is trained several times.

Finally, the average performance is calculated.

Benefits include:

- Better performance estimation
- Reduced overfitting
- More reliable results

---

#  Folder Structure

```text
day-13/
│
├── data/
│   ├── iris.csv
│   └── README.md
│
├── images/
│   ├── confusion_matrix.png
│   ├── roc_curve.png
│   ├── evaluation_summary.png
│
├── models/
│   ├── logistic_model.pkl
│   └── scaler.pkl
│
├── notebooks/
│   └── day13_model_evaluation.ipynb
│
├── outputs/
│   ├── classification_report.txt
│   ├── evaluation_metrics.csv
│   └── cross_validation_results.csv
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

#  Dataset Used

Dataset Name

**Iris Dataset**

Source

Scikit-Learn Built-in Dataset

Number of Samples

150

Number of Features

4

Target Classes

- Setosa
- Versicolor
- Virginica

---

#  Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-Learn
- Joblib
- Jupyter Notebook

---

#  Required Libraries

```bash
pip install pandas numpy matplotlib seaborn scikit-learn joblib notebook
```

---

#  Project Workflow

The following workflow was followed throughout the notebook.

### Step 1

Import Libraries

↓

### Step 2

Load Dataset

↓

### Step 3

Explore Dataset

↓

### Step 4

Train Test Split

↓

### Step 5

Feature Scaling

↓

### Step 6

Train Logistic Regression Model

↓

### Step 7

Make Predictions

↓

### Step 8

Calculate Accuracy

↓

### Step 9

Generate Confusion Matrix

↓

### Step 10

Generate Classification Report

↓

### Step 11

Calculate Precision

↓

### Step 12

Calculate Recall

↓

### Step 13

Calculate F1 Score

↓

### Step 14

Generate ROC Curve

↓

### Step 15

Calculate ROC-AUC Score

↓

### Step 16

Perform 5-Fold Cross Validation

↓

### Step 17

Save Model using Joblib

---

#  Evaluation Metrics

The notebook calculates:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix
- ROC Curve
- ROC-AUC Score
- Cross Validation Mean
- Cross Validation Standard Deviation

---

#  Output Files

The project generates the following files.

### Models

- logistic_model.pkl
- scaler.pkl

### Images

- Confusion Matrix
- ROC Curve

### Reports

- Classification Report
- Evaluation Metrics
- Cross Validation Results

---

#  Saving Model

The trained model is saved using Joblib.

```python
joblib.dump(model, "logistic_model.pkl")
joblib.dump(scaler, "scaler.pkl")
```

These files can later be loaded inside a Streamlit application without retraining the model.

---

#  Results

Successfully completed:

- Logistic Regression Training
- Model Prediction
- Confusion Matrix
- Classification Report
- Precision
- Recall
- F1 Score
- ROC Curve
- ROC-AUC
- Cross Validation
- Model Saving
- Scaler Saving

---

#  Skills Learned

During this task the following skills were developed.

- Data Preprocessing
- Feature Scaling
- Classification
- Model Evaluation
- Performance Metrics
- Cross Validation
- Model Serialization
- Machine Learning Workflow

---

#  Internship Outcome

By completing Day 13, a complete understanding of professional Machine Learning model evaluation techniques was achieved.

This task also prepares the trained model for deployment in Streamlit, which will be completed during the upcoming internship days.

---

#  Author

**Maryam Fatima**

BS Software Engineering

AI/ML Intern

Cooperative Tech Private Limited

---

#  Acknowledgements

Special thanks to

**Cooperative Tech Private Limited**

for providing practical Machine Learning training through real-world internship tasks.

---

#  License

This project is created for educational and internship purposes only.