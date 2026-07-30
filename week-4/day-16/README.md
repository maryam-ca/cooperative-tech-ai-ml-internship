# Week 4 - Day 16

## Advanced Machine Learning - Ensemble Methods

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange)
![XGBoost](https://img.shields.io/badge/XGBoost-Ensemble_Model-green)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-blue)
![GitHub](https://img.shields.io/badge/GitHub-Version_Control-181717)
![VS Code](https://img.shields.io/badge/VS_Code-Editor-007ACC)

---

## Objective

The purpose of Day 16 was to learn and implement Ensemble Machine Learning algorithms using a real-world classification dataset. The task involved training and comparing Random Forest, Gradient Boosting, and XGBoost models, evaluating their performance using multiple metrics, measuring training time, and analyzing Feature Importance to identify the most influential features.

---

## Folder Structure

```text
day-16/
│
├── data/
│   └── breast_cancer.csv
│
├── notebook/
│   └── Ensemble_Notebook.ipynb
│
├── outputs/
│   ├── rf_feature_importance.png
│   ├── gb_feature_importance.png
│   ├── xgb_feature_importance.png
│   └── model_results.csv
│
├── ensemble_models.py
│
├── requirements.txt
│
└── README.md
```

---

## Dataset Used

### Breast Cancer Wisconsin Dataset

The Breast Cancer Wisconsin Dataset was used to practice Ensemble Machine Learning algorithms for binary classification.

The dataset contains diagnostic measurements of breast tumors.

### Features Include

* Radius
* Texture
* Perimeter
* Area
* Smoothness
* Compactness
* Concavity
* Symmetry
* Fractal Dimension

### Target Variable

* Diagnosis
  * Malignant (M)
  * Benign (B)

The dataset was preprocessed and used to train three ensemble learning models for performance comparison.

---

## Machine Learning Tasks Performed

### 1. Data Loading and Exploration

The dataset was loaded using Pandas and explored to understand its structure and quality.

**Operations Performed**

* Loaded CSV dataset
* Displayed dataset information
* Checked dataset dimensions
* Generated descriptive statistics
* Identified missing values

**Insights**

* Successfully loaded the dataset.
* Confirmed that the dataset contained no missing values.
* Explored all available features before preprocessing.

---

### 2. Data Preprocessing

The dataset was prepared for Machine Learning model training.

**Operations Performed**

* Removed unnecessary columns
* Encoded target variable
* Selected input and output variables
* Split dataset into training and testing sets

**Insights**

* Prepared clean data for model development.
* Created an 80:20 train-test split for evaluation.

---

### 3. Random Forest Classification

Random Forest was implemented as the first Ensemble Learning model.

**Model Used**

* RandomForestClassifier

**Evaluation Metrics**

* Accuracy
* Precision
* Recall
* F1-Score
* Training Time

**Insights**

* Achieved high classification accuracy.
* Generated Feature Importance scores for all input features.
* Demonstrated the effectiveness of the Bagging technique.

---

### 4. Gradient Boosting Classification

Gradient Boosting was implemented as the second Ensemble Learning model.

**Model Used**

* GradientBoostingClassifier

**Evaluation Metrics**

* Accuracy
* Precision
* Recall
* F1-Score
* Training Time

**Insights**

* Improved predictive performance by learning from previous errors.
* Produced Feature Importance rankings.
* Demonstrated the Boosting approach.

---

### 5. XGBoost Classification

XGBoost was implemented as an optimized Gradient Boosting algorithm.

**Model Used**

* XGBClassifier

**Evaluation Metrics**

* Accuracy
* Precision
* Recall
* F1-Score
* Training Time

**Insights**

* Achieved excellent predictive performance.
* Reduced overfitting using built-in regularization.
* Generated Feature Importance analysis.

---

### 6. Model Comparison

All three models were evaluated and compared using common performance metrics.

**Comparison Metrics**

* Accuracy
* Precision
* Recall
* F1-Score
* Training Time

**Insights**

* Compared overall model performance.
* Identified the best-performing Ensemble Learning algorithm.
* Saved comparison results in CSV format.

---

### 7. Feature Importance Analysis

Feature Importance was analyzed for all three models.

**Visualizations Generated**

* Random Forest Feature Importance
* Gradient Boosting Feature Importance
* XGBoost Feature Importance

**Insights**

* Identified the most influential features.
* Improved model interpretability.
* Compared feature rankings across different ensemble models.

---

## Machine Learning Concepts Practiced

### Ensemble Learning

* Random Forest
* Gradient Boosting
* XGBoost

### Model Evaluation

* Accuracy
* Precision
* Recall
* F1-Score
* Training Time

### Feature Engineering

* Feature Importance

### Data Preprocessing

* Data Cleaning
* Label Encoding
* Train-Test Split

### Data Visualization

* Feature Importance Charts
* Confusion Matrix

---

## Key Findings

* Ensemble Learning significantly improves prediction accuracy.
* Random Forest provides stable and reliable performance.
* Gradient Boosting learns sequentially and improves model predictions.
* XGBoost combines boosting with regularization to achieve high performance.
* Feature Importance helps identify the variables that contribute most to classification.
* Comparing multiple models helps select the best algorithm for a classification problem.

---

## Learning Outcomes

By completing Day 16, I learned how to:

* Understand the concept of Ensemble Learning.
* Implement Random Forest, Gradient Boosting, and XGBoost models.
* Compare multiple machine learning algorithms.
* Evaluate classification models using different performance metrics.
* Analyze Feature Importance.
* Measure model training time.
* Generate visualizations for model interpretation.
* Organize a Machine Learning project professionally using GitHub.

---

## Tools Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-Learn
* XGBoost
* Jupyter Notebook
* Git
* GitHub
* Visual Studio Code (VS Code)