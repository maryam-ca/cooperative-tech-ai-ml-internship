# Week 6 - Day 26

# ANN Fundamentals - Architecture, Forward Propagation, Backpropagation & Activation Functions

![Python](https://img.shields.io/badge/Python-3.12-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Deep_Learning-FF6F00)
![Keras](https://img.shields.io/badge/Keras-Neural_Networks-D00000)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-blue)
![GitHub](https://img.shields.io/badge/GitHub-Version_Control-181717)
![VS Code](https://img.shields.io/badge/VS_Code-Editor-007ACC)

---

# Objective

The objective of Day 26 was to understand and implement Artificial Neural Networks (ANNs) from the ground up using the Telco Customer Churn dataset. The project focused on learning how neurons, layers, forward propagation, and backpropagation work, visualizing activation functions, building and training a Keras ANN, comparing different network architectures, and benchmarking the ANN against classical machine learning models trained on the same data.

The project also emphasized maintaining a professional project structure by saving processed outputs, training visualizations, and a written explanation of the core deep learning concepts covered.

---

# Folder Structure

```text
week-6/
└── day-26/
    ├── data/
    │   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
    │
    ├── notebooks/
    │   └── 01_ann_fundamentals.ipynb
    │
    ├── outputs/
    │   └── figures/
    │       ├── activation_functions.png
    │       ├── basic_ann_curves.png
    │       └── architecture_comparison.png
    │
    ├── requirements.txt
    └── README.md
```

---

# Dataset Used

## Telco Customer Churn Dataset

The **Telco Customer Churn Dataset** from **Kaggle** was used for this project.

The dataset contains customer account information from a telecommunications company. The objective is to predict whether a customer will churn (leave the company) based on their account and service usage details.

**Source:** https://www.kaggle.com/datasets/blastchar/telco-customer-churn

---

## Dataset Statistics

| Attribute | Value |
|-----------|------|
| Total Samples | 7,043 |
| Total Features | 20 (after dropping customerID) |
| Target Variable | Churn (Yes/No) |
| Problem Type | Binary Classification |

---

## Features Included

### Customer Information

- Gender
- Senior Citizen
- Partner
- Dependents
- Tenure

### Account & Service Information

- Contract
- Payment Method
- Monthly Charges
- Total Charges
- Internet Service
- Phone Service
- Online Security, Backup, Tech Support, Streaming TV/Movies

### Target Variable

- Churn
  - Yes
  - No

---

# Deep Learning Workflow

## 1. Data Cleaning & Preprocessing

The first part of the notebook focused on preparing the dataset before model training.

### Tasks Performed

- Imported required libraries
- Loaded dataset
- Explored dataset structure
- Converted `TotalCharges` from text to numeric and handled missing values
- Dropped non-predictive `customerID` column
- One-hot encoded categorical features
- One-hot encoded the target variable using `to_categorical`
- Performed train-test split
- Scaled numerical features using `StandardScaler`

### Outcome

A clean, fully numeric, properly scaled dataset ready for neural network training.

---

## 2. Activation Function Visualization

Activation functions were plotted and explained before building the network.

### Functions Covered

- ReLU (Rectified Linear Unit)
- Sigmoid
- Softmax

### Files Generated

- activation_functions.png

### Outcome

A clear visual and conceptual understanding of why non-linear activation functions are necessary in neural networks.

---

## 3. ANN Architecture & Training

A simple Artificial Neural Network was built using the Keras Sequential API.

### Model Implemented

- Input Layer → Dense(64, ReLU) → Dense(32, ReLU) → Dense(2, Softmax)
- Optimizer: Adam
- Loss: Categorical Crossentropy

### Evaluation Metrics

- Training Accuracy / Validation Accuracy
- Training Loss / Validation Loss
- Test Accuracy

### Files Generated

- basic_ann_curves.png

### Outcome

A working baseline ANN with training/validation curves used to diagnose overfitting and underfitting.

---

## 4. Architecture Comparison

Three ANN configurations were trained and compared on the same dataset.

### Architectures Implemented

- Small: [16, 8]
- Medium: [64, 32]
- Large: [256, 128, 64]

### Comparison Metrics

- Validation Accuracy
- Validation Loss

### Files Generated

- architecture_comparison.png

### Outcome

A comparative analysis showing whether increasing network size consistently improves performance, or leads to overfitting on a small tabular dataset.

---

## 5. Comparison to Classical Machine Learning

The ANN's test performance was benchmarked against classical ML models trained on the same train/test split.

### Models Compared

- Logistic Regression
- Random Forest Classifier
- Simple ANN

### Outcome

A fair, side-by-side comparison identifying whether deep learning offers an advantage over classical models on this tabular dataset.

---

# Deep Learning Concepts Practiced

## ANN Fundamentals

- Neurons, Weights & Biases
- Forward Propagation
- Loss Functions
- Backpropagation & Gradient Descent

---

## Activation Functions

- ReLU
- Sigmoid
- Softmax

---

## Model Building & Training

- Keras Sequential API
- Model Compilation (optimizer, loss, metrics)
- model.fit() & Validation Split
- Architecture Comparison

---

## Model Evaluation

- Training vs Validation Accuracy/Loss Curves
- Test Set Evaluation
- Comparison with Classical ML Models

---

## Data Visualization

- Activation Function Plots
- Accuracy & Loss Curves
- Architecture Comparison Charts

---

# Key Findings

- Neural networks require careful feature scaling since they are highly sensitive to input magnitude.
- Non-linear activation functions like ReLU are essential — without them, stacking layers is mathematically equivalent to a single linear transformation.
- A bigger network does not always mean better performance; larger architectures can overfit small tabular datasets faster than they improve validation accuracy.
- On tabular data of moderate size, classical ML models can match or outperform a simple ANN — neural networks tend to show their advantage on larger or unstructured data (images, text).
- Understanding forward propagation and backpropagation conceptually is essential for troubleshooting and tuning deep learning models, even though frameworks like TensorFlow handle the underlying calculus automatically.

---

# Learning Outcomes

By completing Day 26, I learned how to:

- Explain how an ANN makes predictions using forward propagation.
- Explain how an ANN learns using backpropagation and gradient descent.
- Visualize and describe the role of ReLU, Sigmoid, and Softmax activation functions.
- Build, compile, and train a neural network using Keras.
- Compare different neural network architectures and interpret training/validation curves.
- Evaluate a neural network on a held-out test set.
- Benchmark deep learning performance against classical machine learning models.
- Organize a professional deep learning project using GitHub.

---

# Technologies & Libraries Used

### Programming Language

- Python

### Data Processing

- Pandas
- NumPy

### Deep Learning

- TensorFlow
- Keras (Sequential API, Dense layers)

### Machine Learning

- Scikit-Learn
- Logistic Regression
- Random Forest

### Preprocessing

- StandardScaler
- One-Hot Encoding

### Visualization

- Matplotlib
- Seaborn

### Development Tools

- Jupyter Notebook
- Git
- GitHub
- Visual Studio Code (VS Code)

---

# Project Summary

This project demonstrates the fundamentals of deep learning, beginning with data preprocessing for neural networks, followed by activation function visualization, ANN architecture design, training, architecture comparison, and evaluation against classical machine learning benchmarks.

The generated visualizations, trained model, and written conceptual explanation provide a reusable foundation for the more advanced deep learning topics covered later in Week 6 (training techniques, CNNs, and Transfer Learning).