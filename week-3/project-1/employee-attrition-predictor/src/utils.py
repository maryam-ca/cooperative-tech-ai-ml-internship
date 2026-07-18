"""
Utility Functions Module
Helper functions for the application
"""

import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Utils:
    """Utility class for common operations"""
    
    @staticmethod
    def load_data(file_path):
        """
        Load data with caching for Streamlit
        
        Args:
            file_path (str): Path to data file
            
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    @staticmethod
    def prepare_feature_importance(model, feature_names, top_n=10):
        """
        Prepare feature importance for visualization
        
        Args:
            model: Trained model
            feature_names: List of feature names
            top_n (int): Number of top features
            
        Returns:
            pd.DataFrame: Feature importance dataframe
        """
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
            
            # Create dataframe
            df_importance = pd.DataFrame({
                'Feature': feature_names,
                'Importance': importance
            }).sort_values('Importance', ascending=False)
            
            return df_importance.head(top_n)
        else:
            logger.warning("Model does not have feature_importances_")
            return None
    
    @staticmethod
    def plot_confusion_matrix(cm, classes=['No', 'Yes']):
        """
        Plot confusion matrix
        
        Args:
            cm: Confusion matrix
            classes: Class labels
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=classes, yticklabels=classes, ax=ax)
        ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
        ax.set_xlabel('Predicted', fontsize=12)
        ax.set_ylabel('Actual', fontsize=12)
        return fig
    
    @staticmethod
    def plot_roc_curve(fpr, tpr, roc_auc):
        """
        Plot ROC curve
        
        Args:
            fpr: False positive rates
            tpr: True positive rates
            roc_auc: ROC-AUC score
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(fpr, tpr, color='darkorange', lw=2, 
               label=f'ROC curve (AUC = {roc_auc:.3f})')
        ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate', fontsize=12)
        ax.set_ylabel('True Positive Rate', fontsize=12)
        ax.set_title('Receiver Operating Characteristic (ROC) Curve', 
                    fontsize=14, fontweight='bold')
        ax.legend(loc="lower right")
        ax.grid(True, alpha=0.3)
        return fig
    
    @staticmethod
    def display_metrics(metrics, title="Model Metrics"):
        """
        Display metrics in a clean format
        
        Args:
            metrics: Dictionary of metrics
            title: Title for the metrics display
        """
        st.markdown(f"### {title}")
        
        cols = st.columns(len(metrics))
        for idx, (metric_name, value) in enumerate(metrics.items()):
            with cols[idx]:
                st.metric(
                    metric_name.replace('_', ' ').title(),
                    f"{value:.3f}"
                )

def load_data(file_path):
    """Convenience function to load data"""
    return Utils.load_data(file_path)

def prepare_features_for_prediction(input_data, preprocessor):
    """
    Prepare single prediction input data
    
    Args:
        input_data (dict): User input data
        preprocessor: DataPreprocessor instance
        
    Returns:
        np.array: Processed features
    """
    # Convert input to DataFrame
    df_input = pd.DataFrame([input_data])
    
    # Clean data
    df_input = preprocessor.clean_data(df_input)
    
    # Apply feature engineering
    df_input = preprocessor.create_feature_engineering(df_input)
    
    # Encode categorical
    df_input = preprocessor.encode_categorical(df_input)
    
    # Scale features
    df_input = preprocessor.scale_features(df_input)
    
    # Get feature columns
    feature_cols = preprocessor.feature_columns
    
    # Ensure all features are present
    missing_cols = [col for col in feature_cols if col not in df_input.columns]
    for col in missing_cols:
        df_input[col] = 0
    
    # Select and order features
    X_input = df_input[feature_cols]
    
    return X_input.values

def display_prediction_result(prediction, probability, threshold=0.5):
    """
    Display prediction result with styling
    
    Args:
        prediction (int): 0 or 1
        probability (float): Prediction probability
        threshold (float): Classification threshold
    """
    if prediction == 1:
        st.error(f"""
        ### ⚠️ High Attrition Risk
        **Probability:** {probability[1]:.2%}
        This employee has a high probability of leaving.
        """)
    else:
        st.success(f"""
        ### ✅ Low Attrition Risk  
        **Probability:** {probability[0]:.2%}
        This employee is likely to stay.
        """)

if __name__ == "__main__":
    # Test utility functions
    print("Utils module loaded successfully")