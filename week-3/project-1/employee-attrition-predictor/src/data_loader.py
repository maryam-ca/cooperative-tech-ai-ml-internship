"""
Data Loader Module
Handles loading and initial data inspection
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Class for loading and initial data exploration"""
    
    def __init__(self, file_path):
        """
        Initialize DataLoader with file path
        
        Args:
            file_path (str): Path to the CSV file
        """
        self.file_path = Path(file_path)
        self.data = None
        self.info = {}
        
    def load_data(self):
        """
        Load data from CSV file
        
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            logger.info(f"Loading data from {self.file_path}")
            self.data = pd.read_csv(self.file_path)
            logger.info(f"Successfully loaded {len(self.data)} rows")
            return self.data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def get_data_info(self):
        """
        Get comprehensive information about the dataset
        
        Returns:
            dict: Dataset information
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        self.info = {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'duplicate_rows': self.data.duplicated().sum(),
            'memory_usage': self.data.memory_usage(deep=True).sum() / 1024**2,
            'numeric_columns': list(self.data.select_dtypes(include=['int64', 'float64']).columns),
            'categorical_columns': list(self.data.select_dtypes(include=['object']).columns),
            'target_distribution': self.data['Attrition'].value_counts().to_dict() if 'Attrition' in self.data.columns else None
        }
        
        return self.info
    
    def preview_data(self, n=5):
        """
        Preview first n rows of data
        
        Args:
            n (int): Number of rows to preview
            
        Returns:
            pd.DataFrame: First n rows
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        return self.data.head(n)
    
    def get_summary_stats(self):
        """
        Get summary statistics for numerical columns
        
        Returns:
            pd.DataFrame: Summary statistics
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        return self.data[numeric_cols].describe()

if __name__ == "__main__":
    # Test the DataLoader
    loader = DataLoader("../data/WA_Fn-UseC_-HR-Employee-Attrition.csv")
    df = loader.load_data()
    info = loader.get_data_info()
    print(f"Dataset shape: {info['shape']}")
    print(f"Target distribution: {info['target_distribution']}")