# Week 6 - Day 27

# Training Techniques - Dropout, Batch Normalization, Callbacks & Learning Rate Scheduling

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

The objective of Day 27 was to improve upon Day 26's baseline Artificial Neural Network by applying core deep learning training techniques. The project focused on regularization using Dropout, stabilizing training with Batch Normalization, and controlling the training process using Keras callbacks (EarlyStopping, ModelCheckpoint, ReduceLROnPlateau). The improved model was compared directly against the basic model from Day 26 to evaluate the real impact of these techniques.

The project also involved experimenting with different Dropout rates and learning rate scheduling strategies to build an intuition for how each hyperparameter affects overfitting and convergence.

---

# Folder Structure

```text
week-6/
└── day-27/
    ├── data/
    │   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
    │
    ├── notebooks/
    │   └── 01_training_techniques.ipynb
    │
    ├── outputs/
    │   ├── best_improved_model.keras
    │   └── figures/
    │       ├── basic_vs_improved_curves.png
    │       ├── dropout_rate_comparison.png
    │       └── lr_schedule_comparison.png
    │
    ├── requirements.txt
    └── README.md
```

---

# Dataset Used

## Telco Customer Churn Dataset

The **Telco Customer Churn Dataset** from **Kaggle** was reused from Day 26 for this project, allowing a direct, apples-to-apples comparison between the basic and improved ANN.

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

# Deep Learning Workflow

## 1. Baseline Reconstruction

Day 26's basic ANN was rebuilt on the same preprocessed data to serve as a fair comparison point.

### Tasks Performed

- Reloaded and re-preprocessed the dataset (same pipeline as Day 26)
- Rebuilt the basic 2-hidden-layer ANN
- Retrained it under identical conditions for comparison

### Outcome

A consistent baseline to isolate the effect of the new training techniques.

---

## 2. Improved Model with Regularization

An improved ANN was built by adding regularization and normalization layers.

### Techniques Applied

- Batch Normalization after each Dense layer
- Dropout (0.4) after each hidden layer
- EarlyStopping (monitor: val_loss, patience: 5, restore_best_weights: True)
- ModelCheckpoint (saves best-performing weights)
- ReduceLROnPlateau (halves learning rate on plateau)

### Files Generated

- best_improved_model.keras

### Outcome

A more stable, regularized model less prone to overfitting than the Day 26 baseline.

---

## 3. Basic vs Improved Comparison

The basic and improved models were evaluated side by side on validation and test data.

### Comparison Metrics

- Validation Accuracy / Validation Loss
- Test Accuracy / Test Loss

### Files Generated

- basic_vs_improved_curves.png

### Outcome

A direct, visual comparison quantifying the benefit of Dropout, Batch Normalization, and callbacks.

---

## 4. Dropout Rate Experiment

Three Dropout rates were tested to observe their effect on the train-validation gap.

### Rates Tested

- 0.2
- 0.4
- 0.6

### Comparison Metrics

- Train Accuracy vs Validation Accuracy
- Overfitting Gap (Train Accuracy − Validation Accuracy)

### Files Generated

- dropout_rate_comparison.png

### Outcome

An empirical view of how increasing Dropout reduces overfitting, and the point at which it becomes too aggressive and hurts learning.

---

## 5. Learning Rate Scheduling Comparison

Two learning rate strategies were compared under identical model architectures.

### Strategies Compared

- ExponentialDecay (fixed decay schedule)
- ReduceLROnPlateau (adaptive, triggered by validation loss)

### Files Generated

- lr_schedule_comparison.png

### Outcome

A comparison of proactive vs reactive learning rate scheduling and their effect on convergence speed and stability.

---

# Deep Learning Concepts Practiced

## Regularization

- Dropout
- Batch Normalization

---

## Training Control

- EarlyStopping
- ModelCheckpoint
- ReduceLROnPlateau
- Learning Rate Scheduling (ExponentialDecay)

---

## Model Evaluation

- Train vs Validation Accuracy/Loss Curves
- Overfitting Gap Analysis
- Basic vs Improved Model Comparison

---

## Data Visualization

- Basic vs Improved Training Curves
- Dropout Rate Comparison Charts
- Learning Rate Schedule Comparison Charts

---

# Key Findings

- Dropout reduces the gap between training and validation accuracy, directly addressing overfitting — but excessively high rates (e.g. 0.6) can slow down learning.
- Batch Normalization stabilizes and speeds up training by keeping layer activations in a consistent range.
- EarlyStopping combined with `restore_best_weights=True` prevents wasted training time and automatically keeps the best-performing weights, without manually reloading a checkpoint.
- ReduceLROnPlateau adapts to the model's actual training behavior, while ExponentialDecay follows a fixed schedule regardless of performance — the better choice depends on how predictable the training curve is.
- Regularization techniques generally trade a small amount of training accuracy for better generalization on unseen data.

---

# Learning Outcomes

By completing Day 27, I learned how to:

- Apply Dropout and Batch Normalization to reduce overfitting and stabilize training.
- Use Keras callbacks (EarlyStopping, ModelCheckpoint, ReduceLROnPlateau) to control the training process.
- Compare a regularized model against a baseline model on the same dataset.
- Experiment with different Dropout rates and interpret their effect on the train-validation gap.
- Compare fixed vs adaptive learning rate scheduling strategies.
- Organize and document a deep learning experiment for reproducibility on GitHub.

---

# Technologies & Libraries Used

### Programming Language

- Python

### Data Processing

- Pandas
- NumPy

### Deep Learning

- TensorFlow
- Keras (Sequential API, Dense, BatchNormalization, Dropout layers, Callbacks)

### Preprocessing

- StandardScaler
- One-Hot Encoding

### Visualization

- Matplotlib

### Development Tools

- Jupyter Notebook
- Git
- GitHub
- Visual Studio Code (VS Code)

---

# Project Summary

This project demonstrates how core training techniques — Dropout, Batch Normalization, and Keras callbacks — improve a baseline Artificial Neural Network's stability and generalization. By directly comparing the Day 26 baseline model against a regularized Day 27 model, and by experimenting with Dropout rates and learning rate schedules, this project builds practical intuition for tuning deep learning models beyond just architecture design.

The generated visualizations, saved model checkpoint, and comparison results provide a reusable foundation for the more advanced deep learning topics covered later in Week 6 (CNNs and Transfer Learning).