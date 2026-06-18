#  Week 1 - Day 4
# Data Visualization using Matplotlib, Seaborn & Plotly

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-green?style=for-the-badge&logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange?style=for-the-badge)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical_Graphs-purple?style=for-the-badge)
![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-red?style=for-the-badge)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter)

---

#  Project Overview

This project was completed as part of the **AI/ML Internship Program – Week 1 Day 4**.

The purpose of this task was to learn and apply **Data Visualization techniques** using Python libraries including **Matplotlib, Seaborn, and Plotly**. Data visualization is an important step in Data Science because it helps transform raw data into meaningful graphical representations that reveal patterns, trends, relationships, and insights.

For this task, the **Titanic Dataset** from Kaggle was used. Multiple visualizations were created to understand passenger demographics, survival trends, fare distributions, correlations, and relationships between variables.

---

#  Objectives

The main objectives of this task were:

- Understand the importance of Data Visualization.
- Learn how to create professional charts using Python.
- Explore passenger information from the Titanic Dataset.
- Analyze relationships between different variables.
- Identify trends, distributions, and outliers.
- Create both static and interactive visualizations.
- Interpret charts and extract meaningful insights.

---

#  Technologies & Libraries Used

| Technology | Purpose |
|------------|----------|
| Python | Programming Language |
| Pandas | Data Loading & Analysis |
| NumPy | Numerical Computation |
| Matplotlib | Static Visualizations |
| Seaborn | Statistical Visualizations |
| Plotly | Interactive Visualizations |
| Jupyter Notebook | Development Environment |
| Git & GitHub | Version Control |

---

#  Dataset Information

## Dataset Name

**Titanic Dataset**

## Source

Kaggle Titanic Dataset

## Dataset Description

The Titanic dataset contains information about passengers aboard the RMS Titanic, including:

- Passenger ID
- Passenger Class
- Name
- Gender
- Age
- Ticket Information
- Fare
- Cabin Information
- Port of Embarkation
- Survival Status

The dataset is widely used for Machine Learning and Data Analysis practice.

---

#  Dataset Overview

Before creating visualizations, the dataset was explored and inspected.

### Initial Checks Performed

- Dataset Shape
- Column Names
- Data Types
- Missing Values
- Statistical Summary

### Dataset Dimensions

```python
Rows: 891
Columns: 12
```

---

#  Visualization Tasks Completed

A total of **8 visualizations** were created using different libraries.

---

#  Chart 1 – Histogram

## Age Distribution of Passengers

### Purpose

To understand the distribution of passenger ages.

### Library Used

Matplotlib

### Insights

- Most passengers were between 20 and 40 years old.
- Very few passengers were above 70 years old.
- The age distribution is slightly right-skewed.

---

#  Chart 2 – Bar Chart

## Survival Count by Passenger Class

### Purpose

To compare survival counts among passenger classes.

### Library Used

Matplotlib

### Insights

- First-class passengers had the highest survival count.
- Third-class passengers had the lowest survival count.
- Passenger class significantly influenced survival rates.

---

#  Chart 3 – Boxplot

## Fare Distribution by Passenger Class

### Purpose

To identify fare distributions and outliers.

### Library Used

Seaborn

### Insights

- Several fare outliers were detected.
- First-class passengers generally paid higher fares.
- Fare distributions differ significantly across classes.

---

#  Chart 4 – Correlation Heatmap

## Relationship Between Numerical Variables

### Purpose

To identify correlations among numerical features.

### Library Used

Seaborn

### Insights

- Strong relationships exist between certain variables.
- Some variables show weak or no correlation.
- Correlation analysis helps understand feature importance.

---

#  Chart 5 – Scatter Plot with Regression Line

## Age vs Fare

### Purpose

To analyze the relationship between passenger age and fare.

### Library Used

Seaborn

### Insights

- A weak positive relationship exists.
- Older passengers occasionally paid higher fares.
- No strong linear relationship was observed.

---

#  Chart 6 – Violin Plot

## Fare Distribution Across Passenger Classes

### Purpose

To compare fare distributions among classes.

### Library Used

Seaborn

### Insights

- First-class fares are significantly higher.
- Fare distributions vary across passenger classes.
- Passenger class strongly affects fare amount.

---

#  Chart 7 – Interactive Bar Chart

## Survival Count by Passenger Class

### Purpose

To create an interactive version of the bar chart.

### Library Used

Plotly Express

### Insights

- Hover functionality allows detailed analysis.
- Interactive charts improve data exploration.
- Users can easily inspect values.

---

#  Chart 8 – Interactive Scatter Plot

## Age vs Fare by Gender

### Purpose

To analyze fare patterns across genders.

### Library Used

Plotly Express

### Insights

- Different fare distributions exist among genders.
- Passenger class and gender influence fare patterns.
- Interactive visualization improves understanding.

---

#  Project Structure

```text
day-4/
│
├── dataset/
│   ├── Titanic-Dataset.csv
│   └── cleaned_titanic.csv
│
├── notebook/
│   └── day4_visualization.ipynb
│
├── output/
│   ├── chart1_histogram.png
│   ├── chart2_bar_chart.png
│   ├── chart3_boxplot.png
│   ├── chart4_heatmap.png
│   ├── chart5_scatterplot.png
│   ├── chart6_violinplot.png
│
└── README.md
```

---

#  Key Findings

After completing the visual analysis, the following insights were identified:

###  Age Distribution

Most passengers belonged to the 20–40 age group.

###  Passenger Class Impact

Passenger class played an important role in survival rates.

###  Fare Differences

First-class passengers generally paid much higher fares.

###  Outliers

Several extreme fare values were detected.

###  Correlations

Some numerical variables showed meaningful relationships.

###  Interactive Analysis

Plotly charts provided a more detailed and user-friendly exploration experience.

---

#  Skills Learned

Through this task, the following skills were developed:

- Data Visualization Fundamentals
- Matplotlib Plotting
- Seaborn Statistical Charts
- Plotly Interactive Visualizations
- Correlation Analysis
- Distribution Analysis
- Outlier Detection
- Data Interpretation
- Exploratory Data Analysis (EDA)

---

#  Conclusion

This project provided practical experience in visualizing and interpreting real-world data using Python. Various chart types were created to understand passenger demographics, fare distributions, survival trends, and variable relationships within the Titanic dataset.

The task strengthened understanding of data visualization techniques and demonstrated how graphical representations can transform raw data into meaningful insights that support better decision-making.

---

#  Author

**Maryam Fatima**

AI/ML Internship Program

Week 1 – Day 4

Data Visualization using Matplotlib, Seaborn & Plotly

---