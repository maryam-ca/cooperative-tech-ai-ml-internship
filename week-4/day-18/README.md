# Week 4 - Day 18

## Advanced Machine Learning - Regularization (Ridge, Lasso & ElasticNet)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange)
![Ridge](https://img.shields.io/badge/Ridge-L2_Regularization-blue)
![Lasso](https://img.shields.io/badge/Lasso-L1_Regularization-green)
![ElasticNet](https://img.shields.io/badge/ElasticNet-Regularization-red)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-blue)
![GitHub](https://img.shields.io/badge/GitHub-Version_Control-181717)
![VS Code](https://img.shields.io/badge/VS_Code-Editor-007ACC)

---

# Objective

The objective of Day 18 was to understand the importance of **Regularization** in Machine Learning and how it helps reduce overfitting. The task involved implementing **Linear Regression, Ridge Regression, Lasso Regression, and ElasticNet**, visualizing regularization paths, tuning hyperparameters using **GridSearchCV**, applying **Logistic Regression with L1 and L2 Regularization**, and comparing different regression models.

---

# Folder Structure

```text
day-18/
│
├── dataset/
│   └── housing.csv
│
├── images/
│   ├── overfitting_vs_underfitting.png
│   ├── ridge_regularization_path.png
│   └── lasso_regularization_path.png
│
├── outputs/
│   ├── model_comparison.csv
│   ├── model_coefficients.csv
│   ├── ridge_coefficients.csv
│   ├── lasso_coefficients.csv
│   ├── elasticnet_coefficients.csv
│   ├── week3_week4_comparison.csv
│   ├── algorithm_cheat_sheet.csv
│   └── best_parameters.txt
│
├── Regularization_Notebook.ipynb
├── requirements.txt
└── README.md
```

---

# Dataset Used

## California Housing Dataset

The California Housing Dataset was used to practice different Regularization techniques on a regression problem.

The dataset contains housing information collected from different districts of California.

The objective is to predict the **Median House Value** using various housing-related features.

### Features Include

- Longitude
- Latitude
- Housing Median Age
- Total Rooms
- Total Bedrooms
- Population
- Households
- Median Income
- Ocean Proximity

### Target Variable

- Median House Value

Before training the models, missing values were handled, categorical features were encoded using One-Hot Encoding, and numerical features were standardized.

---

# Machine Learning Tasks Performed

## 1. Data Loading and Exploration

The California Housing dataset was loaded and explored to understand its structure.

### Operations Performed

- Loaded the dataset
- Displayed dataset information
- Checked dataset dimensions
- Generated descriptive statistics
- Identified missing values
- Explored feature distributions

### Insights

- Successfully loaded the dataset.
- Identified missing values in the **total_bedrooms** column.
- Understood the overall structure of the dataset before preprocessing.

---

## 2. Data Preprocessing

The dataset was prepared before model training.

### Operations Performed

- Handled missing values using the median
- Applied One-Hot Encoding on categorical features
- Selected input and target variables
- Performed Train-Test Split
- Applied StandardScaler

### Insights

- Missing values were successfully handled.
- Categorical data was converted into numerical format.
- Features were standardized for regularization algorithms.

---

## 3. Linear Regression

Linear Regression was implemented as the baseline regression model.

### Model Used

- LinearRegression

### Evaluation Metrics

- R² Score
- RMSE

### Insights

- Established a baseline for comparison.
- Measured regression performance before applying regularization.

---

## 4. Ridge Regression

Ridge Regression was implemented using L2 Regularization.

### Model Used

- Ridge Regression

### Evaluation Metrics

- R² Score
- RMSE

### Insights

- Reduced large coefficient values.
- Improved model stability.
- Reduced overfitting.

---

## 5. Lasso Regression

Lasso Regression was implemented using L1 Regularization.

### Model Used

- Lasso Regression

### Evaluation Metrics

- R² Score
- RMSE

### Insights

- Automatically removed less important features.
- Performed feature selection.
- Produced a simpler regression model.

---

## 6. ElasticNet Regression

ElasticNet combined both L1 and L2 Regularization techniques.

### Model Used

- ElasticNet

### Evaluation Metrics

- R² Score
- RMSE

### Insights

- Balanced Ridge and Lasso penalties.
- Improved generalization.
- Worked well with correlated features.

---

## 7. Regularization Path Visualization

The effect of different alpha values was visualized using Regularization Path plots.

### Visualizations Generated

- Ridge Regularization Path
- Lasso Regularization Path
- Overfitting vs Underfitting Graph

### Insights

- Ridge gradually shrinks coefficients.
- Lasso sets some coefficients exactly to zero.
- Stronger regularization reduces model complexity.

---

## 8. Hyperparameter Tuning using GridSearchCV

GridSearchCV was used to determine the optimal alpha value for Ridge and Lasso Regression.

### Parameters Tuned

- Alpha

### Evaluation Method

- 5-Fold Cross Validation

### Insights

- Automatically selected the optimal alpha.
- Improved regression performance.
- Reduced manual parameter tuning.

---

## 9. Logistic Regression with Regularization

Regularization was also applied to a classification problem using Logistic Regression.

### Models Used

- Logistic Regression (No Regularization)
- Logistic Regression (L1)
- Logistic Regression (L2)

### Evaluation Metrics

- Accuracy

### Insights

- Compared different regularization penalties.
- Observed the effect of L1 and L2 Regularization on classification performance.

---

## 10. Model Comparison

All regression models were evaluated using common regression metrics.

### Comparison Metrics

- R² Score
- RMSE

### Models Compared

- Linear Regression
- Ridge Regression
- Lasso Regression
- ElasticNet

### Insights

- Compared the effect of different regularization techniques.
- Identified the most suitable regression model.
- Saved comparison results in CSV format.

---

# Machine Learning Concepts Practiced

## Regularization

- Ridge Regression (L2)
- Lasso Regression (L1)
- ElasticNet

## Regression

- Linear Regression
- Model Evaluation

## Hyperparameter Tuning

- GridSearchCV
- Cross Validation

## Classification

- Logistic Regression
- L1 Regularization
- L2 Regularization

## Data Preprocessing

- Missing Value Handling
- One-Hot Encoding
- Train-Test Split
- StandardScaler

## Data Visualization

- Overfitting vs Underfitting
- Ridge Regularization Path
- Lasso Regularization Path

---

# Key Findings

- Regularization effectively reduces overfitting.
- Ridge Regression shrinks coefficients while keeping all features.
- Lasso Regression performs automatic feature selection.
- ElasticNet combines the strengths of Ridge and Lasso.
- Feature Scaling is essential before applying Regularization techniques.
- GridSearchCV helps identify the optimal regularization parameter automatically.
- Comparing multiple regression models provides better insight into model performance.

---

# Learning Outcomes

By completing Day 18, I learned how to:

- Understand Overfitting and Underfitting.
- Apply Ridge Regression.
- Apply Lasso Regression.
- Apply ElasticNet Regression.
- Perform Feature Scaling using StandardScaler.
- Tune model parameters using GridSearchCV.
- Visualize Regularization Paths.
- Compare multiple regression models.
- Apply Regularization in Logistic Regression.
- Organize a Machine Learning project professionally using GitHub.

---

# Tools Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-Learn
- Linear Regression
- Ridge Regression
- Lasso Regression
- ElasticNet
- Logistic Regression
- GridSearchCV
- StandardScaler
- Jupyter Notebook
- Git
- GitHub
- Visual Studio Code (VS Code)