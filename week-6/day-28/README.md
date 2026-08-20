# Day 28: CNN Architecture - CIFAR-10 Image Classification

Build and train a Convolutional Neural Network (CNN) from scratch using TensorFlow/Keras to classify images from the CIFAR-10 dataset. This project demonstrates the complete image classification pipeline, including data preprocessing, CNN architecture design, model training, evaluation, and visualization.

---

## Overview

This project covers the fundamentals of Convolutional Neural Networks (CNNs) for computer vision. The model learns visual features from images through convolutional layers and performs multi-class classification on the CIFAR-10 dataset.

---

## Learning Objectives

- Understand the core components of CNNs
- Build a CNN using TensorFlow/Keras
- Train a model with professional callbacks
- Evaluate model performance using multiple metrics
- Visualize training results and prediction errors
- Analyze class-wise performance

---

# Dataset

**Dataset:** CIFAR-10

| Property | Value |
|----------|-------|
| Classes | 10 |
| Training Images | 50,000 |
| Test Images | 10,000 |
| Image Size | 32 × 32 |
| Channels | RGB (3) |
| Classes | Airplane, Automobile, Bird, Cat, Deer, Dog, Frog, Horse, Ship, Truck |

---

# CNN Architecture

```
Input (32 × 32 × 3)

│

├── Conv2D (32, 3×3)
├── BatchNormalization
├── ReLU
├── MaxPooling2D

│

├── Conv2D (64, 3×3)
├── BatchNormalization
├── ReLU
├── MaxPooling2D

│

├── Conv2D (128, 3×3)
├── BatchNormalization
├── ReLU
├── MaxPooling2D

│

├── Flatten
├── Dense (256, ReLU)
├── Dropout (0.5)
├── Dense (10, Softmax)

│

Output
```

---

# Project Structure

```
day-28/
│
├── notebooks/
│   └── day_28_cnn_cifar10.ipynb
│
├── outputs/
│   ├── models/
│   │   └── best_cnn_model.keras
│   │
│   ├── plots/
│   │   ├── sample_images.png
│   │   ├── training_curves.png
│   │   ├── confusion_matrix.png
│   │   ├── misclassified_grid.png
│   │   └── per_class_accuracy.png
│   │
│   └── logs/
│       ├── model_summary.txt
│       ├── classification_report.txt
│       └── notebook_summary.txt
│
└── README.md
```

---

# Installation

Clone the repository and install the required packages.

```bash
pip install tensorflow
pip install matplotlib
pip install seaborn
pip install scikit-learn
pip install numpy
pip install opencv-python
pip install pillow
pip install jupyter
```

Or install everything from the requirements file.

```bash
pip install -r requirements.txt
```

---

# Training Configuration

| Parameter | Value |
|-----------|-------|
| Optimizer | Adam |
| Learning Rate | 0.001 |
| Loss Function | Categorical Crossentropy |
| Batch Size | 64 |
| Epochs | 30 |
| Validation Split | 20% |

---

# Callbacks Used

| Callback | Purpose |
|----------|---------|
| EarlyStopping | Stops training when validation loss no longer improves |
| ModelCheckpoint | Saves the best-performing model |
| ReduceLROnPlateau | Reduces learning rate when validation loss plateaus |

---

# Model Evaluation

The notebook evaluates the trained model using:

- Test Accuracy
- Classification Report
- Confusion Matrix
- Per-Class Accuracy
- Misclassified Images
- Training & Validation Curves

---

# Output Files

After execution, the following outputs are generated.

```
outputs/

├── models/
│   └── best_cnn_model.keras
│
├── plots/
│   ├── sample_images.png
│   ├── training_curves.png
│   ├── confusion_matrix.png
│   ├── misclassified_grid.png
│   └── per_class_accuracy.png
│
└── logs/
    ├── model_summary.txt
    ├── classification_report.txt
    └── notebook_summary.txt
```

---

# Results

Typical performance for this architecture:

| Metric | Expected Value |
|---------|----------------|
| Training Accuracy | 85–90% |
| Validation Accuracy | 75–80% |
| Test Accuracy | 78–82% |

Performance may vary depending on hardware, random initialization, and training conditions.

---

# Key Concepts

- Convolutional Neural Networks (CNN)
- Convolution Layers
- Feature Extraction
- Max Pooling
- Batch Normalization
- ReLU Activation
- Dropout Regularization
- Softmax Classification
- Multi-Class Image Classification

---

# Technologies Used

- Python
- TensorFlow / Keras
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- OpenCV
- Jupyter Notebook

---

# How to Run

Launch Jupyter Notebook.

```bash
jupyter notebook
```

Open:

```
notebooks/day_28_cnn_cifar10.ipynb
```

Run all cells sequentially.
