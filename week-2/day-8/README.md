# Week 2 - Day 8
# Feature Engineering: Encoding, Scaling & Feature Transformation

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-Feature%20Engineering-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

#  Introduction

Feature Engineering is one of the most important steps in the Machine Learning pipeline. Raw datasets often contain categorical values, unscaled numerical features, and information that is not directly useful for predictive models.

The purpose of Feature Engineering is to transform raw data into meaningful features that improve model performance and help machine learning algorithms learn patterns more effectively.

In this task, the Marketing Campaign dataset was used to perform:

- Categorical Encoding
- Feature Creation
- Feature Scaling
- Feature Documentation

---

#  Objectives

The main objectives of this task were:

- Identify categorical features
- Convert categorical data into numerical format
- Create meaningful new features
- Scale numerical data using StandardScaler
- Prepare data for future Machine Learning models
- Document all final features

---

#  Dataset

### Dataset Used

**Marketing Campaign Dataset**

File:

```text
marketing_campaign.csv
```

### Dataset Description

The dataset contains customer information including:

- Demographics
- Income
- Education Level
- Marital Status
- Spending Habits
- Product Purchases
- Campaign Responses

The dataset is commonly used for customer behavior analysis and predictive modeling.

---

#  Step 1: Data Loading

The dataset was loaded using Pandas.

```python
import pandas as pd

df = pd.read_csv("marketing_campaign.csv", sep="\t")
```

### Dataset Shape

```python
print(df.shape)
```

### Preview Dataset

```python
df.head()
```

This helps understand the structure of the dataset before starting feature engineering.

---

#  Step 2: Identify Categorical Columns

Machine Learning models cannot directly process text values.

Therefore, categorical columns must be converted into numerical form.

### Detecting Categorical Features

```python
df.select_dtypes(include='object').columns
```

### Categorical Columns Found

```text
Education
Marital_Status
```

---

#  Step 3: Categorical Encoding

## What is Encoding?

Encoding is the process of converting categorical values into numbers.

### Example

Before Encoding:

| Education |
|------------|
| Graduation |
| PhD |
| Master |

After Encoding:

| Education_PhD | Education_Master |
|--------------|------------------|
| 0 | 0 |
| 1 | 0 |
| 0 | 1 |

---

## One-Hot Encoding

One-Hot Encoding was applied using:

```python
pd.get_dummies()
```

### Implementation

```python
df_encoded = pd.get_dummies(
    df,
    columns=['Education', 'Marital_Status'],
    drop_first=True
)
```

### Why drop_first=True?

This avoids the Dummy Variable Trap and reduces multicollinearity.

---

#  Before and After Encoding

### Original Dataset Shape

```python
print(df.shape)
```

### Encoded Dataset Shape

```python
print(df_encoded.shape)
```

The increase in columns confirms successful encoding.

---

#  Step 4: Feature Creation

Creating new features helps models learn better relationships from data.

A minimum of three new features were created.

---

## Feature 1: Total Spending

### Purpose

Calculate total customer spending across all product categories.

### Formula

```python
df_encoded['Total_Spending'] = (
    df_encoded['MntWines']
    + df_encoded['MntFruits']
    + df_encoded['MntMeatProducts']
    + df_encoded['MntFishProducts']
    + df_encoded['MntSweetProducts']
    + df_encoded['MntGoldProds']
)
```

### Business Value

This feature represents the overall purchasing power of a customer.

---

## Feature 2: Total Children

### Purpose

Determine total dependents in a household.

### Formula

```python
df_encoded['Total_Children'] = (
    df_encoded['Kidhome']
    + df_encoded['Teenhome']
)
```

### Business Value

Customers with more children may have different spending patterns.

---

## Feature 3: Age

### Purpose

Convert birth year into actual age.

### Formula

```python
current_year = 2025

df_encoded['Age'] = current_year - df_encoded['Year_Birth']
```

### Business Value

Age is often a strong predictor of purchasing behavior.

---

## Feature 4: Income Per Person

### Purpose

Measure available income per household member.

### Formula

```python
df_encoded['Income_Per_Person'] = (
    df_encoded['Income']
    /
    (df_encoded['Total_Children'] + 1)
)
```

### Business Value

Provides a more realistic measure of purchasing capacity.

---

#  Feature Visualization

Visualizing engineered features helps understand their distribution.

---

## Total Spending Distribution

```python
sns.histplot(
    df_encoded['Total_Spending'],
    kde=True
)
```

### Output

```text
outputs/total_spending_distribution.png
```

### Observation

Most customers have low-to-medium spending while a smaller group spends significantly more.

---

## Age Distribution

```python
sns.histplot(
    df_encoded['Age'],
    kde=True
)
```

### Output

```text
outputs/age_distribution.png
```

### Observation

The customer base mainly consists of middle-aged individuals.

---

#  Step 5: Data Scaling

## Why Scaling?

Different features have different ranges.

Example:

```text
Age → 18 to 80

Income → 10,000 to 100,000
```

Large-value features can dominate machine learning algorithms.

Scaling solves this problem.

---

# Train-Test Split

Before scaling, the dataset was split.

```python
from sklearn.model_selection import train_test_split

X = df_encoded.drop('Response', axis=1)
y = df_encoded['Response']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)
```

---

# StandardScaler

StandardScaler standardizes data using:

```text
Mean = 0
Standard Deviation = 1
```

### Implementation

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)
```

---

# Verification

```python
import numpy as np

print(np.mean(X_train_scaled[:,0]))
print(np.std(X_train_scaled[:,0]))
```

### Expected Result

```text
Mean ≈ 0

Standard Deviation ≈ 1
```

This confirms scaling was applied correctly.

---

#  Step 6: Final Feature Summary

A feature summary table was created.

### Columns Included

| Feature | Data Type | Type |
|----------|-----------|--------|
| Income | Numeric | Original |
| Age | Numeric | Engineered |
| Total_Spending | Numeric | Engineered |
| Total_Children | Numeric | Engineered |
| Income_Per_Person | Numeric | Engineered |

---

## Generate Summary Table

```python
feature_summary = pd.DataFrame({
    "Feature": df_encoded.columns,
    "Data Type": df_encoded.dtypes.astype(str)
})
```

---

## Save Summary

```python
feature_summary.to_csv(
    "outputs/feature_summary.csv",
    index=False
)
```

---

#  Generated Outputs

The following outputs were generated during this task:

```text
outputs/
│
├── total_spending_distribution.png
├── age_distribution.png
├── before_scaling.png
├── feature_summary.csv
```

---

#  Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-Learn
- Jupyter Notebook
- Git
- GitHub

---

#  Key Learnings

During this task, the following concepts were learned:

- Difference between categorical and numerical data
- One-Hot Encoding
- Feature Creation Techniques
- Data Scaling
- Train-Test Split
- StandardScaler
- Feature Documentation
- Data Preparation for Machine Learning

---

#  Conclusion

This Feature Engineering task successfully transformed the raw Marketing Campaign dataset into a machine-learning-ready format.

Categorical variables were encoded, meaningful new features were created, numerical features were scaled, and all features were documented. These preprocessing steps improve data quality and prepare the dataset for future Machine Learning model development in upcoming internship tasks.

The resulting dataset is now cleaner, more informative, and suitable for predictive analytics and model training.