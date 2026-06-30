#  Week 3 - Day 11

# Linear Regression & Polynomial Regression

> **Cooperative Tech Private Limited - AI/ML Internship Program**

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?style=for-the-badge&logo=scikitlearn)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?style=for-the-badge&logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-blue?style=for-the-badge)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-4C72B0?style=for-the-badge)

---

#  Project Overview

This project was completed as part of **Week 3 - Day 11** of the **AI/ML Internship Program** at **Cooperative Tech Private Limited**.

The objective of this practical is to understand the fundamentals of **Supervised Machine Learning** by implementing **Linear Regression** and **Polynomial Regression** using Scikit-Learn.

The notebook covers the complete machine learning workflow, including:

- Data Loading
- Exploratory Data Analysis (EDA)
- Feature Selection
- Data Preprocessing
- Feature Scaling
- Model Training
- Model Evaluation
- Data Visualization
- Model Comparison

---

#  Learning Objectives

After completing this practical, I was able to:

- Understand Supervised Machine Learning
- Understand Regression Problems
- Learn Linear Regression
- Learn Polynomial Regression
- Perform Exploratory Data Analysis (EDA)
- Prepare data for Machine Learning
- Train Regression Models
- Evaluate Regression Models
- Compare Multiple Regression Algorithms
- Visualize Prediction Results

---

#  Machine Learning Concepts Covered

## Supervised Learning

Supervised Learning is a type of Machine Learning where the model learns from labeled data.

The algorithm learns the relationship between input features and target values to make predictions on unseen data.

---

## Regression

Regression is used when the target variable is continuous.

Examples include:

- House Price Prediction
- Salary Prediction
- Stock Price Prediction
- Sales Forecasting
- Temperature Prediction

---

## Linear Regression

Linear Regression is the simplest regression algorithm.

It finds the best-fit straight line that minimizes prediction errors using the Ordinary Least Squares (OLS) method.

Equation:

y = mx + c

Where:

- y = Predicted Value
- x = Input Feature
- m = Slope
- c = Intercept

---

## Polynomial Regression

Polynomial Regression extends Linear Regression by adding polynomial features.

Instead of fitting only straight lines, it can model curved relationships between variables.

This makes it suitable for datasets where the relationship between input and output is nonlinear.

---

#  Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Scikit-Learn
- Jupyter Notebook

---

#  Project Structure

```text
week-3/
│
└── day-11/
    │
    ├── notebooks/
    │   └── 01_linear_polynomial_regression.ipynb
    │
    ├── data/
    │   └── california_housing.csv
    │
    ├── images/
    │   ├── correlation_heatmap.png
    │   ├── actual_vs_predicted.png
    │   ├── residual_plot.png
    │   └── polynomial_regression_plot.png
    │
    ├── outputs/
    │   ├── regression_metrics.csv
    │   └── model_comparison.csv
    │
    ├── README.md
    ├── requirements.txt
    └── .gitignore
```

---

#  Dataset Information

Dataset Used:

**California Housing Dataset**

Target Variable:

- Median House Price

Features:

- MedInc
- HouseAge
- AveRooms
- AveBedrms
- Population
- AveOccup
- Latitude
- Longitude

This dataset is available in Scikit-Learn and is widely used for regression tasks.

---

#  Machine Learning Workflow

The complete workflow followed in this notebook is:

### Step 1

Import Required Libraries

↓

### Step 2

Load Dataset

↓

### Step 3

Explore Dataset

↓

### Step 4

Perform Exploratory Data Analysis

↓

### Step 5

Check Missing Values

↓

### Step 6

Feature Selection

↓

### Step 7

Train-Test Split

↓

### Step 8

Feature Scaling

↓

### Step 9

Train Linear Regression Model

↓

### Step 10

Evaluate Model

↓

### Step 11

Visualize Predictions

↓

### Step 12

Train Polynomial Regression Model

↓

### Step 13

Compare Both Models

↓

### Step 14

Draw Final Conclusions

---

#  Evaluation Metrics

The following regression metrics were used to evaluate the models:

## Mean Absolute Error (MAE)

Measures the average absolute prediction error.

Lower values indicate better performance.

---

## Mean Squared Error (MSE)

Squares prediction errors before averaging.

Large errors receive higher penalties.

---

## Root Mean Squared Error (RMSE)

Square root of MSE.

Provides prediction error in the original units.

---

## R² Score

Measures how well the model explains the variance in the target variable.

Higher values indicate better performance.

---

#  Visualizations

The notebook includes several visualizations such as:

- Correlation Heatmap
- Feature Distribution Histograms
- Pair Plot
- Actual vs Predicted Scatter Plot
- Residual Plot
- Polynomial Regression Analysis

---

#  Results

The implemented models were evaluated using multiple regression metrics.

Both models successfully learned patterns from the dataset.

Polynomial Regression demonstrated improved performance on nonlinear relationships, while Linear Regression provided a strong baseline model.

---

#  Key Learnings

During this practical, I learned:

- Complete Regression Workflow
- Data Preprocessing
- Feature Scaling
- Model Training
- Model Prediction
- Model Evaluation
- Error Analysis
- Visualization Techniques
- Model Comparison
- Regression Concepts

---

#  Future Improvements

Possible future improvements include:

- Hyperparameter Tuning
- Cross Validation
- Feature Engineering
- Regularization Techniques
- Ridge Regression
- Lasso Regression
- ElasticNet Regression
- Random Forest Regression
- XGBoost Regression

---

#  Installation

Clone the repository:

```bash
git clone https://github.com/your-username/ctpl-aiml-internship.git
```

Move into the project directory:

```bash
cd week-3/day-11
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the notebook:

```bash
jupyter notebook
```

---

#  Requirements

- Python 3.12+
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Scikit-Learn
- Jupyter Notebook

---

#  Author

**Maryam Fatima**

AI/ML Intern

Cooperative Tech Private Limited

---

#  Acknowledgements

Special thanks to **Cooperative Tech Private Limited** for providing practical machine learning training through hands-on internship tasks.

This project helped strengthen my understanding of Regression algorithms, Machine Learning workflows, and real-world data analysis.