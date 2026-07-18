# Employee Attrition Predictor

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458)
![NumPy](https://img.shields.io/badge/NumPy-Numerical_Computing-013243)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-Machine_Learning-F7931E)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-FF4B4B)
![GitHub](https://img.shields.io/badge/GitHub-Version_Control-181717)

---

# Employee Attrition Predictor

## Project Overview

This project predicts whether an employee is likely to leave the company using Machine Learning. It uses the IBM HR Analytics Employee Attrition dataset and provides an interactive Streamlit dashboard for data exploration, visualization, and real-time prediction.

---

## Project Structure

```text
employee-attrition-predictor/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── WA_Fn-UseC_-HR-Employee-Attrition.csv
│
├── models/
│   └── best_model.pkl
│
├── notebooks/
│   ├── 01_EDA_and_Cleaning.ipynb
│   ├── 02_Feature_Engineering.ipynb
│   └── 03_Model_Training.ipynb
│
└── src/
    ├── data_loader.py
    ├── preprocessor.py
    └── model_trainer.py
```

---

## Features

* Employee Attrition Prediction
* Interactive Streamlit Dashboard
* Data Exploration
* Exploratory Data Analysis (EDA)
* Feature Engineering
* Logistic Regression & Random Forest Models
* Model Performance Evaluation
* Real-time Prediction

---

## Dataset

**Dataset:** IBM HR Analytics Employee Attrition & Performance

**Records:** 1,470

**Target Variable:** Attrition (Yes / No)

---

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Matplotlib
* Seaborn
* Jupyter Notebook
* Git & GitHub

---

## Workflow

1. Load Dataset
2. Clean Data
3. Perform EDA
4. Feature Engineering
5. Encode & Scale Features
6. Train Machine Learning Models
7. Evaluate Performance
8. Save Best Model
9. Deploy using Streamlit

---

## Machine Learning Models

* Logistic Regression
* Random Forest Classifier

**Evaluation Metrics**

* Accuracy
* Precision
* Recall
* F1-Score
* ROC-AUC Score

---

## Running the Project

### Clone Repository

```bash
git clone https://github.com/Samra-ca/ctpl-aiml-internship/tree/main/week-3/project-1/employee-attrition-predictor.git
cd employee-attrition-predictor
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Train Model

```bash
python src/model_trainer.py
```

### Run Streamlit App

```bash
streamlit run app.py
```

---

## Project Highlights

* End-to-End Machine Learning Project
* Interactive Web Application
* Data Visualization
* Employee Attrition Prediction
* Model Comparison
* Clean and Modular Python Code

---

## Learning Outcomes

* Data Preprocessing
* Feature Engineering
* Machine Learning Model Training
* Model Evaluation
* Streamlit Deployment
* Git & GitHub Workflow

---

## Future Improvements

* Hyperparameter Tuning
* XGBoost Model
* Batch Predictions
* Cloud Deployment
* Improved Dashboard UI
