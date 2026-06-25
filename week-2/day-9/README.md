# 📊 Week 2 - Day 9
# Correlation Analysis & Hypothesis Testing with SciPy & Statsmodels

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green?style=for-the-badge)
![SciPy](https://img.shields.io/badge/SciPy-Statistics-orange?style=for-the-badge)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-purple?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Charts-red?style=for-the-badge)

---

# 📖 Project Overview

This project was completed as part of the **Cooperative Tech Private Limited AI/ML Internship Program - Week 2 Day 9**.

The objective of this task is to perform **Statistical Analysis** on the Marketing Campaign Dataset using Correlation Analysis and Hypothesis Testing techniques.

Statistical analysis plays an important role in Data Science because it helps identify meaningful relationships between variables and validates whether observed patterns are statistically significant or simply due to random chance.

This notebook focuses on:

- Correlation Analysis
- Correlation Heatmap
- T-Test Analysis
- Chi-Square Testing
- Feature Importance Ranking
- Statistical Interpretation

The findings from this analysis will be used during future Machine Learning model development.

---

# 🎯 Objectives

The main objectives of this project are:

✅ Understand relationships between variables

✅ Perform Correlation Analysis

✅ Visualize feature relationships using Heatmaps

✅ Apply Statistical Hypothesis Testing

✅ Conduct Independent T-Tests

✅ Conduct Chi-Square Tests

✅ Identify Important Features

✅ Prepare data insights for Machine Learning

---

# 📂 Dataset Information

## Dataset Name

**Marketing Campaign Dataset**

## Description

The Marketing Campaign Dataset contains customer demographic information, spending behavior, purchasing history, and campaign response information.

The dataset is used to analyze customer behavior and determine which factors influence customer responses to marketing campaigns.

---

## Target Variable

### Response

```text
0 = Customer did not respond

1 = Customer responded
```

The Response column is used as the target variable throughout this analysis.

---

# 🛠 Technologies Used

The following libraries and tools were used:

| Tool | Purpose |
|--------|---------|
| Python | Programming Language |
| Pandas | Data Manipulation |
| NumPy | Numerical Operations |
| Matplotlib | Data Visualization |
| Seaborn | Statistical Visualization |
| SciPy | Hypothesis Testing |
| Jupyter Notebook | Analysis Environment |
| Git & GitHub | Version Control |

---

# 📊 Task 1: Correlation Analysis

## What is Correlation?

Correlation measures the strength and direction of the relationship between two numerical variables.

The correlation coefficient ranges from:

| Value | Meaning |
|---------|---------|
| +1 | Perfect Positive Correlation |
| 0 | No Correlation |
| -1 | Perfect Negative Correlation |

---

## Activities Performed

### Numerical Feature Selection

Selected all numerical columns from the dataset.

### Correlation Matrix Generation

Computed pairwise correlation values between numerical variables.

### Correlation Heatmap

Created a visual heatmap to identify:

- Strong Positive Correlations
- Strong Negative Correlations
- Weak Relationships

### Target Correlation Analysis

Measured the correlation of all numerical features with the target variable.

---

## Key Learning

Correlation helps identify important features that may contribute significantly to Machine Learning model performance.

---

# 📈 Task 2: T-Test Analysis

## What is a T-Test?

A T-Test is used to compare the means of two groups and determine whether the difference is statistically significant.

---

## Null Hypothesis (H₀)

There is no significant difference between the means of the two groups.

---

## Alternative Hypothesis (H₁)

There is a significant difference between the means of the two groups.

---

## Decision Rule

```text
If p-value < 0.05

Reject Null Hypothesis
```

```text
If p-value >= 0.05

Fail to Reject Null Hypothesis
```

---

## Features Tested

The following numerical features were analyzed:

### Income

Compared customer income between:

- Responded Customers
- Non-Responded Customers

### MntWines

Compared wine spending behavior between customer groups.

### NumWebPurchases

Compared online purchasing behavior between customer groups.

---

## Outcome

T-Test results help determine whether customer behavior differs significantly between campaign responders and non-responders.

---

# 📊 Task 3: Chi-Square Test

## What is Chi-Square Test?

The Chi-Square Test is used to determine whether two categorical variables are related.

---

## Null Hypothesis (H₀)

The variables are independent.

---

## Alternative Hypothesis (H₁)

The variables are related.

---

## Features Tested

### Education vs Response

Examined whether education level influences campaign response.

### Marital Status vs Response

Examined whether marital status influences campaign response.

---

## Outcome

Chi-Square testing helps identify whether customer demographic characteristics influence marketing campaign effectiveness.

---

# 🏆 Task 4: Feature Importance Ranking

## Objective

To identify the most influential variables associated with customer responses.

---

## Ranking Method

Features were ranked based on:

- Correlation Strength
- Statistical Significance
- Business Relevance

---

## Benefits

Feature ranking helps:

- Improve Model Accuracy
- Reduce Noise
- Enhance Feature Selection
- Improve Model Interpretability

---

# 📁 Generated Outputs

The following visualizations and reports were generated during this analysis:

```text
outputs/
│
├── correlation_heatmap.png
├── top_correlated_features.png
├── ttest_results.png
├── chi_square_results.png
└── feature_importance.png
```

---

# 📷 Visualizations

## Correlation Heatmap

Displays relationships among numerical variables.

### Insights

- Strong Positive Relationships
- Strong Negative Relationships
- Multicollinearity Detection

---

## Top Correlated Features

Displays the strongest predictors of campaign response.

---

## T-Test Summary Table

Displays:

- T Statistics
- P Values
- Statistical Decisions

---

## Chi-Square Summary Table

Displays:

- Chi-Square Statistics
- P Values
- Relationship Significance

---

## Feature Importance Chart

Visual ranking of the most predictive features.

---

# 📚 Statistical Concepts Learned

Through this project, the following statistical concepts were explored:

### Correlation Analysis

Understanding variable relationships.

### Pearson Correlation

Measuring linear relationships between variables.

### Hypothesis Testing

Testing assumptions using statistical evidence.

### T-Test

Comparing means of two groups.

### Chi-Square Test

Analyzing relationships between categorical variables.

### Feature Selection

Identifying important predictors.

### Statistical Interpretation

Making data-driven conclusions from test results.

---

# 🚀 Project Workflow

```text
Load Dataset
      │
      ▼
Data Understanding
      │
      ▼
Correlation Analysis
      │
      ▼
Heatmap Visualization
      │
      ▼
T-Test Analysis
      │
      ▼
Chi-Square Testing
      │
      ▼
Feature Ranking
      │
      ▼
Statistical Conclusions
```

---

# 🎓 Learning Outcomes

After completing this project, I learned how to:

- Analyze relationships between variables
- Generate and interpret correlation matrices
- Build correlation heatmaps
- Apply hypothesis testing
- Interpret p-values correctly
- Conduct T-Tests
- Conduct Chi-Square Tests
- Rank features based on statistical evidence
- Draw meaningful business insights from data

---

# 🔮 Future Scope

The findings from this analysis will be used in upcoming Machine Learning tasks, including:

- Feature Selection
- Classification Models
- Customer Response Prediction
- Model Optimization
- Predictive Analytics

---

# ✅ Conclusion

This project successfully performed a complete statistical analysis of the Marketing Campaign Dataset.

Correlation Analysis identified relationships among numerical variables, while T-Tests and Chi-Square Tests validated whether observed patterns were statistically significant.

The results provided valuable insights into customer behavior and identified the most influential features associated with campaign response.

These findings create a strong foundation for future Machine Learning model development and predictive analytics projects.

---

# 👩‍💻 Author

**Maryam Fatima**

AI/ML Intern

Cooperative Tech Private Limited

Week 2 - Day 9

Correlation Analysis & Hypothesis Testing