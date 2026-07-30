# Week 4 - Day 17

## Advanced Machine Learning - Support Vector Machines & GridSearchCV

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange)
![SVM](https://img.shields.io/badge/SVM-Classification-green)
![GridSearchCV](https://img.shields.io/badge/GridSearchCV-Hyperparameter_Tuning-red)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-blue)
![GitHub](https://img.shields.io/badge/GitHub-Version_Control-181717)
![VS Code](https://img.shields.io/badge/VS_Code-Editor-007ACC)

---

## Objective

The purpose of Day 17 was to understand and implement **Support Vector Machines (SVM)** for classification problems and learn **Hyperparameter Tuning** using **GridSearchCV**. The task involved training Linear and RBF kernel SVM models, visualizing decision boundaries, tuning model parameters using cross-validation, comparing SVM with Random Forest, and evaluating model performance using multiple classification metrics.

---

## Folder Structure

```text
day-17/
│
├── notebook/
│   └── SVM_GridSearchCV_Notebook.ipynb
│
├── outputs/
│   ├── linear_svm_confusion_matrix.png
│   ├── rbf_svm_confusion_matrix.png
│   ├── decision_boundary_linear.png
│   ├── decision_boundary_rbf.png
│   ├── feature_importance.png
│   ├── model_comparison.csv
│   └── accuracy_comparison.png
│
├── requirements.txt
│
└── README.md
```

---

## Dataset Used

### Breast Cancer Wisconsin Dataset

The Breast Cancer Wisconsin Dataset was used to practice Support Vector Machine classification.

The dataset contains diagnostic measurements of breast tumors used to classify tumors as malignant or benign.

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
  * Malignant (0)
  * Benign (1)

The dataset was preprocessed and standardized before training Support Vector Machine models.

---

## Machine Learning Tasks Performed

### 1. Data Loading and Exploration

The dataset was loaded using Scikit-Learn and explored to understand its structure.

**Operations Performed**

* Loaded Breast Cancer Dataset
* Displayed dataset information
* Checked dataset dimensions
* Generated descriptive statistics
* Verified missing values
* Explored target distribution

**Insights**

* Successfully loaded the dataset.
* Confirmed there were no missing values.
* Understood feature distribution before preprocessing.

---

### 2. Data Preprocessing

The dataset was prepared before model training.

**Operations Performed**

* Selected input and target variables
* Split dataset into training and testing sets
* Applied StandardScaler for feature scaling

**Insights**

* Standardized all features.
* Created an 80:20 train-test split.
* Prepared the dataset for SVM training.

---

### 3. Linear Support Vector Machine

A Linear Kernel SVM model was implemented for binary classification.

**Model Used**

* SVC (Kernel = Linear)

**Evaluation Metrics**

* Accuracy
* Precision
* Recall
* F1-Score
* Training Time

**Insights**

* Successfully classified the dataset.
* Achieved high prediction accuracy.
* Generated confusion matrix and classification report.

---

### 4. RBF Support Vector Machine

A Radial Basis Function (RBF) Kernel SVM model was implemented.

**Model Used**

* SVC (Kernel = RBF)

**Evaluation Metrics**

* Accuracy
* Precision
* Recall
* F1-Score
* Training Time

**Insights**

* Learned complex non-linear decision boundaries.
* Improved classification performance.
* Demonstrated the effectiveness of kernel functions.

---

### 5. Decision Boundary Visualization

Decision boundaries were visualized using a synthetic dataset.

**Visualizations Generated**

* Linear Kernel Decision Boundary
* RBF Kernel Decision Boundary

**Insights**

* Observed the difference between linear and non-linear classification.
* Understood how kernels transform feature space.

---

### 6. Hyperparameter Tuning using GridSearchCV

GridSearchCV was applied to optimize SVM performance.

**Parameters Tuned**

* C
* Kernel
* Gamma

**Evaluation Method**

* 5-Fold Cross Validation

**Insights**

* Automatically selected the best hyperparameters.
* Improved model performance.
* Reduced manual experimentation.

---

### 7. Random Forest Comparison

Random Forest was trained for comparison with SVM.

**Model Used**

* RandomForestClassifier

**Evaluation Metrics**

* Accuracy
* Precision
* Recall
* F1-Score
* Training Time

**Insights**

* Compared tree-based learning with SVM.
* Evaluated differences in accuracy and computational cost.
* Generated Feature Importance scores.

---

### 8. Model Comparison

All models were evaluated using common classification metrics.

**Comparison Metrics**

* Accuracy
* Precision
* Recall
* F1-Score
* Training Time

**Insights**

* Compared Linear SVM, RBF SVM, Tuned SVM, and Random Forest.
* Identified the best-performing model.
* Saved comparison results in CSV format.

---

## Machine Learning Concepts Practiced

### Support Vector Machines

* Linear Kernel
* RBF Kernel
* Hyperplanes
* Support Vectors
* Maximum Margin Classification

### Hyperparameter Tuning

* GridSearchCV
* Cross Validation
* Parameter Optimization

### Model Evaluation

* Accuracy
* Precision
* Recall
* F1-Score
* Confusion Matrix
* Classification Report
* Training Time

### Data Preprocessing

* Train-Test Split
* StandardScaler
* Feature Scaling

### Data Visualization

* Decision Boundary
* Confusion Matrix
* Feature Importance
* Accuracy Comparison Charts

---

## Key Findings

* Support Vector Machines perform exceptionally well on binary classification tasks.
* Feature Scaling is essential for SVM performance.
* The RBF Kernel effectively handles non-linear decision boundaries.
* GridSearchCV automates hyperparameter tuning and improves model performance.
* Random Forest provides feature importance and strong classification accuracy.
* Comparing multiple models helps identify the most suitable algorithm for a classification problem.

---

## Learning Outcomes

By completing Day 17, I learned how to:

* Understand the working principle of Support Vector Machines.
* Differentiate between Linear and RBF kernels.
* Apply Feature Scaling using StandardScaler.
* Train and evaluate SVM models.
* Tune hyperparameters using GridSearchCV.
* Compare SVM with Random Forest.
* Visualize decision boundaries.
* Interpret confusion matrices and classification reports.
* Organize a Machine Learning project professionally using GitHub.

---

## Tools Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-Learn
* Support Vector Machine (SVC)
* GridSearchCV
* Random Forest
* Jupyter Notebook
* Git
* GitHub
* Visual Studio Code (VS Code)