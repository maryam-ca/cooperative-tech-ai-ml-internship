# Week 4 - Day 19

## Project 2 Kickoff - Advanced Machine Learning Project

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-blue)
![GitHub](https://img.shields.io/badge/GitHub-Version_Control-181717)
![VS Code](https://img.shields.io/badge/VS_Code-Editor-007ACC)

---

# Objective

The objective of Day 19 was to officially kick off Project 2 by selecting a suitable dataset, planning the project workflow, performing initial data exploration, preparing the dataset for machine learning, and building a baseline classification model. The task also focused on organizing the project professionally using GitHub and establishing a reusable preprocessing pipeline for future advanced machine learning models.

---

# Folder Structure

```text
day-19/
│
├── dataset/
│   └── bank-full.csv
│
├── notebook/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   └── 03_baseline_model.ipynb
│
├── outputs/
│   ├── eda_plots/
│   │   ├── target_distribution.png
│   │   ├── numerical_features.png
│   │   ├── numerical_boxplots.png
│   │   ├── categorical_features.png
│   │   ├── correlation_heatmap.png
│   │   ├── scaling_comparison.png
│   │   └── smote_comparison.png
│   │
│   └── model_results/
│       ├── baseline_performance.png
│       ├── feature_importance.png
│       ├── baseline_metrics.csv
│       └── feature_importance.csv
│
├── models/
│   ├── baseline_model.pkl
│   ├── scaler.pkl
│   └── label_encoders.pkl
│
├── reports/
│   ├── Day19_Project_Plan.md
│   ├── Day19_EDA_Summary.txt
│   └── Day19_Baseline_Summary.txt
│
├── requirements.txt
│
└── README.md
```

---

# Dataset Used

## Bank Marketing Dataset

The **Bank Marketing Dataset** from the UCI Machine Learning Repository was selected for this project.

The dataset contains information collected from direct marketing campaigns conducted by a Portuguese banking institution. The objective is to predict whether a client will subscribe to a term deposit.

### Dataset Statistics

| Attribute | Value |
|-----------|------|
| Samples | 45,211 |
| Features | 17 |
| Target | y (yes/no) |
| Problem Type | Binary Classification |

### Features Include

**Client Information**

- Age
- Job
- Marital Status
- Education
- Default
- Housing Loan
- Personal Loan

**Campaign Information**

- Contact Type
- Month
- Duration
- Campaign
- Pdays
- Previous
- Poutcome

**Target Variable**

- **y**
    - Yes
    - No

---

# Machine Learning Tasks Performed

## 1. Project Planning

The project scope and workflow were planned before implementation.

### Activities Performed

- Selected the project dataset
- Defined project objectives
- Planned preprocessing workflow
- Identified expected outputs
- Prepared folder structure

### Insights

- Created a structured workflow.
- Planned the complete machine learning pipeline.
- Organized the project professionally.

---

## 2. Data Loading & Exploration

The dataset was loaded and explored to understand its structure.

### Operations Performed

- Loaded dataset
- Displayed dataset information
- Checked dimensions
- Generated descriptive statistics
- Checked missing values
- Explored target distribution

### Insights

- Successfully loaded the dataset.
- Understood feature types.
- Verified data quality before preprocessing.

---

## 3. Data Visualization

Exploratory Data Analysis (EDA) was performed to better understand the dataset.

### Visualizations Generated

- Target Distribution
- Numerical Feature Histograms
- Numerical Boxplots
- Categorical Feature Distribution
- Correlation Heatmap

### Insights

- Identified feature distributions.
- Observed class imbalance.
- Detected relationships between variables.

---

## 4. Data Preprocessing

The dataset was prepared before training machine learning models.

### Operations Performed

- Feature Selection
- Target Selection
- One-Hot Encoding
- StandardScaler
- Train-Test Split
- SMOTE for class balancing

### Outputs Generated

- X_train.csv
- X_test.csv
- y_train.csv
- y_test.csv

### Insights

- Converted categorical features into numerical values.
- Standardized numerical variables.
- Balanced the dataset using SMOTE.

---

## 5. Baseline Model

A baseline Logistic Regression model was trained to establish initial performance.

### Model Used

- Logistic Regression

### Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

### Insights

- Established baseline performance.
- Identified opportunities for improvement using advanced models.

---

## 6. Model Evaluation

The baseline model was evaluated using multiple classification metrics.

### Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

### Outputs Generated

- Baseline Performance Graph
- Feature Importance
- Performance CSV

### Insights

- Evaluated classification performance.
- Generated benchmark results for future comparison.

---

# Machine Learning Concepts Practiced

## Data Preprocessing

- One-Hot Encoding
- StandardScaler
- SMOTE
- Train-Test Split

## Classification

- Logistic Regression
- Binary Classification
- Model Evaluation

## Data Visualization

- Target Distribution
- Feature Distribution
- Correlation Heatmap
- Feature Importance

## Model Evaluation

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

---

# Key Findings

- The dataset contains an imbalanced target variable.
- SMOTE helps balance minority class samples.
- Feature Scaling improves model performance.
- Logistic Regression provides a strong baseline model.
- A well-organized preprocessing pipeline simplifies future model development.
- Proper project organization improves reproducibility and maintainability.

---

# Learning Outcomes

By completing Day 19, I learned how to:

- Plan an end-to-end machine learning project.
- Explore and understand a real-world dataset.
- Perform exploratory data analysis.
- Handle categorical features using One-Hot Encoding.
- Balance imbalanced datasets using SMOTE.
- Apply Feature Scaling using StandardScaler.
- Train and evaluate a baseline Logistic Regression model.
- Organize a professional machine learning project using GitHub.
- Prepare datasets for advanced machine learning models.

---

# Tools Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-Learn
- Logistic Regression
- StandardScaler
- OneHotEncoder
- SMOTE
- Jupyter Notebook
- Git
- GitHub
- Visual Studio Code (VS Code)