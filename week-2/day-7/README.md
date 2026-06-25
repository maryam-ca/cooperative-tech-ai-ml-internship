# Week 2 - Day 7
# Full EDA Pipeline: Missing Values, Outliers & Feature Distributions

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green?style=for-the-badge&logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-orange?style=for-the-badge&logo=numpy)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-purple?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Charts-red?style=for-the-badge)
![SciPy](https://img.shields.io/badge/SciPy-Statistics-yellow?style=for-the-badge)
![EDA](https://img.shields.io/badge/EDA-Exploratory%20Data%20Analysis-success?style=for-the-badge)

---

#  Overview

Day 7 focused on performing a **complete Exploratory Data Analysis (EDA)** on the **Customer Personality Analysis Dataset**.

Unlike basic data exploration, this task involved a professional EDA workflow designed to identify:

- Missing Values
- Outliers
- Feature Distributions
- Skewness
- Data Quality Issues
- Target Variable Characteristics

EDA is one of the most important steps in the Data Science lifecycle because it helps us understand the dataset before Feature Engineering and Machine Learning model development.

---

#  Objectives

The main objectives of this task were:

- Analyze missing values and their patterns.
- Detect outliers using statistical techniques.
- Visualize feature distributions.
- Measure skewness in numerical features.
- Apply data transformations where required.
- Analyze the target variable distribution.
- Generate meaningful insights from the dataset.

---

#  Dataset Information

## Dataset Name

**Customer Personality Analysis Dataset**

## Description

The dataset contains customer demographic information, spending habits, and campaign response records.

The objective is to understand customer behavior and identify important patterns that can support future predictive analytics tasks.

---

#  Technologies & Libraries Used

## Python Libraries

### Pandas

Used for:

- Data Loading
- Data Cleaning
- Missing Value Analysis
- Data Manipulation

### NumPy

Used for:

- Numerical Operations
- Log Transformations
- Statistical Calculations

### Matplotlib

Used for:

- Data Visualization
- Histogram Creation
- Distribution Analysis

### Seaborn

Used for:

- Statistical Visualization
- KDE Plots
- Boxplots
- Countplots

### Missingno

Used for:

- Missing Value Pattern Visualization

### SciPy

Used for:

- Statistical Analysis
- Outlier Detection Support

---

#  Project Structure

```text
week-2/
└── day-7/
    ├── marketing_campaign.csv
    ├── day7_advanced_eda.ipynb
    ├── outputs/
    │   ├── missing_values_matrix.png
    │   ├── income_boxplot.png
    │   ├── all_boxplots.png
    │   ├── income_distribution.png
    │   ├── income_log_transform.png
    │   ├── age_distribution.png
    │   └── response_distribution.png
    └── README.md
```

---

#  Task 1: Missing Value Analysis

## Purpose

Missing values can negatively affect machine learning models and statistical analysis.

This task was performed to:

- Identify missing values.
- Calculate missing value percentages.
- Understand missing value patterns.

## Analysis Performed

- Counted missing values for every column.
- Calculated missing value percentages.
- Visualized missing data using Missingno Matrix.

## Findings

- The **Income** column contained missing values.
- Missing values represented only a small percentage of the dataset.
- Median imputation was identified as a suitable strategy.

---

#  Task 2: Missing Value Visualization

## Technique Used

### Missingno Matrix

The Missingno Matrix was used to visualize missing data patterns.

### Output

```text
missing_values_matrix.png
```

## Insights

- Missing values were limited to a few records.
- No strong missing value pattern was observed.
- Missing values appeared mostly random.

---

#  Task 3: Outlier Detection

## Purpose

Outliers are observations that significantly differ from the majority of data.

Outliers may represent:

- Data Entry Errors
- Measurement Errors
- Genuine Rare Cases

## Method Used

### Interquartile Range (IQR)

Formula:

```text
IQR = Q3 - Q1

Lower Bound = Q1 - 1.5 × IQR

Upper Bound = Q3 + 1.5 × IQR
```

Values outside these bounds were classified as outliers.

---

#  Boxplot Analysis

## Visualizations Created

### Income Boxplot

```text
income_boxplot.png
```

### All Numerical Features Boxplot

```text
all_boxplots.png
```

## Findings

Outliers were detected in:

- Income
- MntWines
- MntMeatProducts
- MntGoldProds

These values may represent high-value customers rather than errors.

Therefore, removing them immediately would not be appropriate.

---

#  Task 4: Distribution Analysis

## Purpose

Distribution analysis helps determine:

- Data Shape
- Spread
- Normality
- Skewness

## Visualizations Created

### Income Distribution

```text
income_distribution.png
```

### Age Distribution

```text
age_distribution.png
```

## Findings

- Income showed a right-skewed distribution.
- Age distribution appeared relatively balanced.
- Spending variables showed long tails.

---

#  Task 5: Skewness Analysis

## Purpose

Skewness measures distribution asymmetry.

### Interpretation

| Skewness Value | Meaning |
|---------------|----------|
| 0 | Symmetrical Distribution |
| Positive | Right Skewed |
| Negative | Left Skewed |

## Findings

The Income feature showed positive skewness.

This indicates that a small number of customers have significantly higher income compared to the majority.

---

#  Task 6: Log Transformation

## Purpose

Log Transformation reduces skewness and improves distribution symmetry.

## Method Used

```python
np.log1p()
```

## Visualization

```text
income_log_transform.png
```

## Findings

### Before Transformation

- Highly Right Skewed

### After Transformation

- More Balanced Distribution
- Improved Normality

---

#  Task 7: Target Variable Analysis

## Target Variable

```text
Response
```

### Meaning

| Value | Description |
|---------|-------------|
| 0 | Customer Did Not Accept Campaign |
| 1 | Customer Accepted Campaign |

---

## Visualization

```text
response_distribution.png
```

## Findings

- Majority of customers belonged to Response = 0.
- Minority belonged to Response = 1.
- Class imbalance exists in the dataset.

This imbalance should be considered during machine learning model training.

---

#  Key Insights

### Insight 1

Income contains missing values but only in a small number of records.

### Insight 2

Several spending-related features contain significant outliers.

### Insight 3

Income distribution is positively skewed.

### Insight 4

Log transformation improves Income distribution.

### Insight 5

The dataset contains class imbalance in the target variable.

### Insight 6

High-spending customers contribute to extreme values in multiple features.

---

#  Learning Outcomes

Through this task, the following concepts were learned:

- Professional Exploratory Data Analysis Workflow
- Missing Value Analysis
- Missing Value Visualization
- Outlier Detection using IQR
- Boxplot Interpretation
- Distribution Analysis
- Skewness Measurement
- Log Transformation
- Target Variable Analysis
- Data Quality Assessment

---

#  Future Work

The findings from this EDA will be used in upcoming tasks:

- Feature Engineering
- Data Preprocessing
- Feature Selection
- Machine Learning Model Development
- Predictive Analytics

---

#  Conclusion

A complete Exploratory Data Analysis (EDA) was successfully performed on the Customer Personality Analysis Dataset.

The analysis identified missing values, outliers, skewed features, and class imbalance within the dataset. These insights provide a strong foundation for future Feature Engineering and Machine Learning tasks.

The results demonstrate the importance of EDA in understanding data quality, uncovering hidden patterns, and preparing data for predictive modeling.