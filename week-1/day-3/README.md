#  Day 3: NumPy & Pandas Deep Dive

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![NumPy](https://img.shields.io/badge/NumPy-Array_Computing-013243?style=for-the-badge&logo=numpy)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter)
![VS Code](https://img.shields.io/badge/VS_Code-IDE-007ACC?style=for-the-badge&logo=visualstudiocode)
![Git](https://img.shields.io/badge/Git-Version_Control-F05032?style=for-the-badge&logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)

---

#  Introduction

Day 3 of the AI/ML Internship focused on learning **NumPy** and **Pandas**, two of the most important libraries used in Data Science and Machine Learning.

The objective of this task was to understand how numerical data is processed using NumPy arrays and how real-world datasets can be loaded, analyzed, cleaned, transformed, and merged using Pandas DataFrames.

For this task, the **Titanic Dataset** was used to perform practical data analysis and preprocessing operations.

---

#  Objectives

## By completing this task, I learned how to:

- Create NumPy arrays
- Perform statistical analysis on numerical data
- Reshape and slice arrays
- Apply broadcasting operations
- Load CSV files using Pandas
- Inspect datasets efficiently
- Handle missing values
- Remove duplicate records
- Convert data types
- Merge DataFrames
- Save processed datasets

---

#  Technologies & Tools Used

| Tool | Purpose |
|--------|----------|
| Python | Programming Language |
| NumPy | Numerical Computing |
| Pandas | Data Analysis |
| Jupyter Notebook | Interactive Coding |
| VS Code | Development Environment |
| Git | Version Control |
| GitHub | Project Hosting |

---

#  Project Structure

```text
day-3/
│
├── data/
│   ├── titanic.csv
│   └── cleaned_titanic.csv
│
├── notebook/
│   └── day3_numpy_pandas.ipynb
│
├── outputs/
│   ├── numpy_results.txt
│   ├── merged_dataset.csv
│   └── cleaning_report.txt
│
├── screenshots/
│   ├── dataframe_head.png
│   ├── missing_values.png
│   └── merged_output.png
│
└── README.md
```

---

#  Dataset Information

## Dataset Name

**Titanic Dataset**

## Dataset Description

The Titanic dataset contains passenger information from the Titanic ship disaster.

It includes details such as:

- Passenger ID
- Survival Status
- Passenger Class
- Passenger Name
- Gender
- Age
- Fare
- Cabin Information
- Embarkation Port

This dataset is widely used for practicing Data Science and Machine Learning concepts.

---

#  Task 1: NumPy Practice

## Array Creation

A NumPy array containing **20 random numbers between 1 and 100** was generated.

```python
arr = np.random.randint(1, 101, 20)
```

---

## Statistical Analysis

The following statistical operations were performed:

- Mean
- Median
- Standard Deviation
- Minimum Value
- Maximum Value

```python
np.mean(arr)
np.median(arr)
np.std(arr)
np.min(arr)
np.max(arr)
```

---

## Array Reshaping

The array was reshaped into a **4 × 5 matrix**.

```python
matrix = arr.reshape(4,5)
```

---

## Array Slicing

The first two rows of the matrix were extracted.

```python
matrix[:2]
```

---

## Broadcasting

Every value inside the matrix was multiplied by 2 using broadcasting.

```python
matrix * 2
```

---

#  Task 2: Data Loading & Inspection

## Loading Dataset

The Titanic dataset was loaded using Pandas.

```python
df = pd.read_csv("../data/titanic.csv")
```

---

## Dataset Inspection

The following functions were used:

### First 10 Records

```python
df.head(10)
```

### Dataset Shape

```python
df.shape
```

### Data Types

```python
df.dtypes
```

### Dataset Information

```python
df.info()
```

### Statistical Summary

```python
df.describe()
```

---

## Inspection Findings

- Dataset loaded successfully
- Multiple numerical and categorical columns were identified
- Missing values were present in several columns
- Statistical information was generated for analysis

---

#  Task 3: Data Cleaning

Data cleaning is one of the most important steps before building Machine Learning models.

---

## Missing Values Analysis

Missing values were identified using:

```python
df.isnull().sum()
```

### Columns Containing Missing Values

| Column | Status |
|----------|----------|
| Age | Missing Values Present |
| Cabin | Missing Values Present |
| Embarked | Missing Values Present |

---

## Handling Numerical Missing Values

Missing values in the **Age** column were replaced with the column mean.

```python
df["Age"] = df["Age"].fillna(df["Age"].mean())
```

---

## Handling Categorical Missing Values

Missing values in the **Embarked** column were replaced with "Unknown".

```python
df["Embarked"] = df["Embarked"].fillna("Unknown")
```

---

## Handling Cabin Values

Missing values in the **Cabin** column were replaced with "Not Available".

```python
df["Cabin"] = df["Cabin"].fillna("Not Available")
```

---

## Removing Duplicate Records

Duplicate rows were removed.

```python
df = df.drop_duplicates()
```

---

## Data Type Verification

```python
df.dtypes
```

The data types were verified after cleaning.

---

#  Task 4: Data Merging

## Creating a Supplementary DataFrame

A secondary DataFrame was created manually.

```python
class_df = pd.DataFrame({
    "Pclass":[1,2,3],
    "Class_Name":[
        "First Class",
        "Second Class",
        "Third Class"
    ]
})
```

---

## Merging DataFrames

The Titanic dataset was merged with the supplementary DataFrame.

```python
merged_df = pd.merge(
    df,
    class_df,
    on="Pclass",
    how="left"
)
```

---

## Merge Result

A new column named:

```text
Class_Name
```

was successfully added to the dataset.

---

#  Output Files Generated

The following files were generated during the task:

##  cleaned_titanic.csv

Contains the cleaned version of the dataset.

---

##  merged_dataset.csv

Contains the merged dataset after joining two DataFrames.

---

##  numpy_results.txt

Contains statistical results generated using NumPy.

---

##  cleaning_report.txt

Contains documentation of all cleaning operations performed.

---

#  Screenshots

The following screenshots were captured and stored in the screenshots folder.

## dataframe_head.png

Displays the first few rows of the dataset.

---

## missing_values.png

Displays the missing values present in each column.

---

## merged_output.png

Displays the final merged dataset.

---

#  Key Learnings

## Important Concepts Learned

- NumPy Array Operations
- Statistical Calculations
- Array Reshaping
- Array Slicing
- Broadcasting
- Data Loading using Pandas
- Data Cleaning Techniques
- Missing Value Handling
- Duplicate Removal
- Data Type Conversion
- DataFrame Merging

---

#  Outcomes

By completing this task, I gained practical experience in:

- Working with structured datasets
- Cleaning real-world data
- Performing statistical analysis
- Manipulating DataFrames
- Preparing datasets for future Machine Learning projects

---

#  Conclusion

Day 3 provided a strong foundation in data preprocessing and analysis using NumPy and Pandas.

The Titanic dataset was successfully loaded, inspected, cleaned, transformed, and merged while applying industry-standard data preparation techniques.

These skills are essential for future AI, Machine Learning, and Data Science projects and will be used throughout the internship.

---

#  Author

## Maryam Fatima

**AI/ML Intern**  
**Cooperative Tech Private Limited**

---
 If you found this repository helpful, don't forget to star it.