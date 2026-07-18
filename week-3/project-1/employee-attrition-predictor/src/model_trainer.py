"""
Model Trainer Module
Handles model training, evaluation, and comparison
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                           f1_score, roc_auc_score, confusion_matrix, 
                           classification_report)
import pickle
import joblib
import logging
from pathlib import Path
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    """Class for training and evaluating ML models"""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_model_name = None
        
    def train_logistic_regression(self, X_train, y_train, max_iter=1000):
        """
        Train Logistic Regression model
        
        Args:
            X_train: Training features
            y_train: Training target
            max_iter (int): Maximum iterations
            
        Returns:
            LogisticRegression: Trained model
        """
        logger.info("Training Logistic Regression...")
        start_time = time.time()
        
        model = LogisticRegression(
            max_iter=max_iter,
            class_weight='balanced',
            random_state=self.random_state
        )
        
        model.fit(X_train, y_train)
        
        training_time = time.time() - start_time
        logger.info(f"Logistic Regression trained in {training_time:.2f} seconds")
        
        self.models['Logistic Regression'] = model
        return model
    
    def train_random_forest(self, X_train, y_train, n_estimators=100):
        """
        Train Random Forest model
        
        Args:
            X_train: Training features
            y_train: Training target
            n_estimators (int): Number of trees
            
        Returns:
            RandomForestClassifier: Trained model
        """
        logger.info("Training Random Forest...")
        start_time = time.time()
        
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            class_weight='balanced',
            random_state=self.random_state
        )
        
        model.fit(X_train, y_train)
        
        training_time = time.time() - start_time
        logger.info(f"Random Forest trained in {training_time:.2f} seconds")
        
        self.models['Random Forest'] = model
        return model
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """
        Evaluate model performance
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test target
            model_name (str): Name of the model
            
        Returns:
            dict: Evaluation metrics
        """
        logger.info(f"Evaluating {model_name}...")
        
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        logger.info(f"{model_name} - Accuracy: {metrics['accuracy']:.3f}")
        logger.info(f"{model_name} - ROC-AUC: {metrics['roc_auc']:.3f}")
        
        self.results[model_name] = metrics
        return metrics
    
    def train_and_evaluate_all(self, X_train, X_test, y_train, y_test):
        """
        Train all models and evaluate them
        
        Args:
            X_train: Training features
            X_test: Test features
            y_train: Training target
            y_test: Test target
            
        Returns:
            dict: All results
        """
        # Train Logistic Regression
        lr_model = self.train_logistic_regression(X_train, y_train)
        lr_metrics = self.evaluate_model(lr_model, X_test, y_test, 'Logistic Regression')
        
        # Train Random Forest
        rf_model = self.train_random_forest(X_train, y_train)
        rf_metrics = self.evaluate_model(rf_model, X_test, y_test, 'Random Forest')
        
        # Compare models
        self._select_best_model()
        
        return self.results
    
    def _select_best_model(self):
        """
        Select the best model, preserving Logistic Regression as the default choice.
        """
        if not self.results:
            raise ValueError("No models evaluated yet. Run train_and_evaluate_all() first.")

        if 'Logistic Regression' in self.results:
            self.best_model = self.models['Logistic Regression']
            self.best_model_name = 'Logistic Regression'
            logger.info("Selected default model: Logistic Regression")
            return self.best_model_name

        # Fallback to weighted score if Logistic Regression is not available
        best_score = -1
        for model_name, metrics in self.results.items():
            score = 0.7 * metrics['roc_auc'] + 0.3 * metrics['f1_score']
            if score > best_score:
                best_score = score
                self.best_model = self.models[model_name]
                self.best_model_name = model_name

        logger.info(f"Best model: {self.best_model_name} with score {best_score:.3f}")
        return self.best_model_name
    
    def save_model(self, model, preprocessor, filename='best_model.pkl'):
        model_path = Path(__file__).parent.parent / "models"
        model_path.mkdir(exist_ok=True)

        # Save Model
        joblib.dump(model, model_path / filename)

        # Save Scaler
        joblib.dump(preprocessor.scaler, model_path / "scaler.pkl")

        # Save Label Encoders
        joblib.dump(preprocessor.label_encoders, model_path / "label_encoders.pkl")

        # Save Feature Columns
        joblib.dump(preprocessor.feature_columns, model_path / "feature_columns.pkl")

        logger.info("All files saved successfully.")
    def load_model(self, filename='best_model.pkl'):
        """
        Load a saved model from disk
        
        Args:
            filename (str): Model filename
            
        Returns:
            object: Loaded model
        """
        model_path = Path(__file__).parent.parent / 'models' / filename
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")
        return model
    
    def get_feature_importance(self, model, feature_names, top_n=10):
        """
        Get feature importance for tree-based models
        
        Args:
            model: Trained model (must have feature_importances_)
            feature_names: List of feature names
            top_n (int): Number of top features to return
            
        Returns:
            pd.DataFrame: Feature importance dataframe
        """
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
            
            feature_importance = pd.DataFrame({
                'Feature': feature_names,
                'Importance': importance
            }).sort_values('Importance', ascending=False)
            
            return feature_importance.head(top_n)
        else:
            logger.warning("Model does not have feature_importances_ attribute")
            return None
    
    def create_results_summary(self):
        """
        Create a summary of all model results
        
        Returns:
            pd.DataFrame: Results summary
        """
        if not self.results:
            raise ValueError("No results available. Run train_and_evaluate_all() first.")
        
        summary_data = []
        metrics_to_include = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
        
        for model_name, metrics in self.results.items():
            row = {'Model': model_name}
            for metric in metrics_to_include:
                row[metric.capitalize()] = f"{metrics[metric]:.3f}"
            summary_data.append(row)
        
        return pd.DataFrame(summary_data)

if __name__ == "__main__":
    from data_loader import DataLoader
    from preprocessor import DataPreprocessor
    from pathlib import Path

    data_path = Path(__file__).resolve().parent.parent / "data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
    loader = DataLoader(data_path)
    df = loader.load_data()

    preprocessor = DataPreprocessor()
    df_processed = preprocessor.preprocess(df, training=True)
    X, y, features = preprocessor.prepare_features(df_processed)
    X_train, X_test, y_train, y_test = preprocessor.split_data(X, y)

    trainer = ModelTrainer()
    trainer.train_and_evaluate_all(X_train, X_test, y_train, y_test)
    trainer.save_model(trainer.best_model, preprocessor)

    print(f"Saved best model: {trainer.best_model_name} to {Path(__file__).resolve().parent.parent / 'models' / 'best_model.pkl'}")
    print("\nModel Comparison:")
    print(trainer.create_results_summary())

    if trainer.best_model_name == 'Random Forest':
        importance = trainer.get_feature_importance(trainer.best_model, features, top_n=10)
        print("\nTop 10 Important Features:")
        print(importance)