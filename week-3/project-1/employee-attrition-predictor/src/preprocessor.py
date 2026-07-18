"""
Data Preprocessor Module
Handles data cleaning, encoding, and scaling
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Class for preprocessing employee attrition data"""

    TARGET_COLUMN = 'Attrition'
    INPUT_COLUMNS = [
        'Age', 'Gender', 'MaritalStatus', 'Department', 'JobRole', 'Education',
        'MonthlyIncome', 'YearsAtCompany', 'OverTime', 'TotalWorkingYears',
        'YearsInCurrentRole', 'JobSatisfaction', 'WorkLifeBalance',
        'DistanceFromHome', 'NumCompaniesWorked'
    ]
    NUMERIC_COLUMNS = [
        'Age', 'Education', 'MonthlyIncome', 'YearsAtCompany', 'TotalWorkingYears',
        'YearsInCurrentRole', 'JobSatisfaction', 'WorkLifeBalance',
        'DistanceFromHome', 'NumCompaniesWorked', 'YearsAtCompanyRatio', 'OvertimeIncomeRatio'
    ]
    BINARY_COLUMNS = ['Gender', 'OverTime']
    MULTI_CATEGORY_COLUMNS = ['Department', 'JobRole', 'MaritalStatus', 'TenureGroup']

    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        self.target_column = self.TARGET_COLUMN

    def _retain_required_columns(self, df, training=True):
        required = self.INPUT_COLUMNS.copy()
        if training and self.TARGET_COLUMN in df.columns:
            required.append(self.TARGET_COLUMN)
        return df.loc[:, [col for col in required if col in df.columns]].copy()

    def clean_data(self, df, training=True):
        """
        Clean the dataset by handling missing values and duplicates

        Args:
            df (pd.DataFrame): Raw data
            training (bool): Whether the data is used for training

        Returns:
            pd.DataFrame: Cleaned data
        """
        logger.info("Starting data cleaning...")
        df_clean = df.copy()

        missing = df_clean.isnull().sum()
        if missing.sum() > 0:
            logger.info(f"Found missing values: {missing[missing > 0].to_dict()}")
            df_clean = df_clean.dropna()
            logger.info(f"Dropped rows with missing values. New shape: {df_clean.shape}")

        duplicates = df_clean.duplicated().sum()
        if duplicates > 0:
            logger.info(f"Found {duplicates} duplicate rows. Removing...")
            df_clean = df_clean.drop_duplicates()
            logger.info(f"Removed duplicates. New shape: {df_clean.shape}")

        df_clean = self._retain_required_columns(df_clean, training=training)
        df_clean = self._fix_data_types(df_clean)

        logger.info("Data cleaning complete!")
        return df_clean

    def _fix_data_types(self, df):
        """Fix data types for consistency"""
        df_copy = df.copy()

        categorical_cols = self.BINARY_COLUMNS + ['MaritalStatus', 'Department', 'JobRole', 'TenureGroup']
        if self.TARGET_COLUMN in df_copy.columns:
            categorical_cols.append(self.TARGET_COLUMN)

        for col in categorical_cols:
            if col in df_copy.columns:
                df_copy[col] = df_copy[col].astype('object')

        numeric_cols = self.NUMERIC_COLUMNS
        for col in numeric_cols:
            if col in df_copy.columns:
                df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')

        return df_copy

    def create_feature_engineering(self, df):
        """
        Create engineered features from collected inputs

        Args:
            df (pd.DataFrame): Data after basic cleaning

        Returns:
            pd.DataFrame: Data with engineered features
        """
        logger.info("Creating engineered features...")
        df_engineered = df.copy()

        if 'TotalWorkingYears' in df_engineered.columns and 'YearsAtCompany' in df_engineered.columns:
            df_engineered['YearsAtCompanyRatio'] = (
                df_engineered['YearsAtCompany'] / (df_engineered['TotalWorkingYears'] + 1)
            )
            logger.info("Created 'YearsAtCompanyRatio'")

        if 'OverTime' in df_engineered.columns and 'MonthlyIncome' in df_engineered.columns:
            overtime_numeric = df_engineered['OverTime'].map({'Yes': 1, 'No': 0})
            df_engineered['OvertimeIncomeRatio'] = (
                overtime_numeric * df_engineered['MonthlyIncome']
            )
            logger.info("Created 'OvertimeIncomeRatio'")

        if 'YearsAtCompany' in df_engineered.columns:
            df_engineered['TenureGroup'] = pd.cut(
                df_engineered['YearsAtCompany'],
                bins=[-1, 2, 5, 10, np.inf],
                labels=['New', 'Mid', 'Senior', 'Veteran']
            )
            logger.info("Created 'TenureGroup'")

        return df_engineered

    def encode_categorical(self, df, training=True):
        """
        Encode categorical variables

        Args:
            df (pd.DataFrame): Data with categorical columns
            training (bool): Whether the data is used for training

        Returns:
            pd.DataFrame: Encoded data
        """
        logger.info("Encoding categorical variables...")
        df_encoded = df.copy()

        if training and self.TARGET_COLUMN in df_encoded.columns:
            attrition_encoder = LabelEncoder()
            df_encoded[self.TARGET_COLUMN] = attrition_encoder.fit_transform(df_encoded[self.TARGET_COLUMN])
            self.label_encoders[self.TARGET_COLUMN] = attrition_encoder
            logger.info(f"Encoded {self.TARGET_COLUMN}")

        for col in self.BINARY_COLUMNS:
            if col in df_encoded.columns:
                if training:
                    le = LabelEncoder()
                    df_encoded[col] = le.fit_transform(df_encoded[col])
                    self.label_encoders[col] = le
                    logger.info(f"Encoded {col}")
                else:
                    le = self.label_encoders.get(col)
                    if le is None:
                        raise ValueError(f"Missing encoder for column: {col}")
                    df_encoded[col] = df_encoded[col].map(
                        lambda value: le.transform([value])[0] if value in le.classes_ else np.nan
                    )

        multi_cols = [col for col in self.MULTI_CATEGORY_COLUMNS if col in df_encoded.columns]
        df_encoded = pd.get_dummies(df_encoded, columns=multi_cols, drop_first=False)
        logger.info(f"One-hot encoded columns: {multi_cols}")

        remaining_cat = df_encoded.select_dtypes(include=['object']).columns
        if len(remaining_cat) > 0:
            for col in remaining_cat:
                if training:
                    le = LabelEncoder()
                    df_encoded[col] = le.fit_transform(df_encoded[col])
                    self.label_encoders[col] = le
                    logger.info(f"Encoded remaining categorical column: {col}")
                else:
                    le = self.label_encoders.get(col)
                    if le is None:
                        raise ValueError(f"Missing encoder for column: {col}")
                    df_encoded[col] = df_encoded[col].map(
                        lambda value: le.transform([value])[0] if value in le.classes_ else np.nan
                    )

        logger.info("Categorical encoding complete!")
        return df_encoded

    def scale_features(self, df, training=True):
        """
        Scale numerical features

        Args:
            df (pd.DataFrame): Data with features
            training (bool): Whether the data is used for training

        Returns:
            pd.DataFrame: Scaled data
        """
        logger.info("Scaling numerical features...")
        df_scaled = df.copy()

        numeric_cols = [col for col in self.NUMERIC_COLUMNS if col in df_scaled.columns]
        if len(numeric_cols) > 0:
            if training:
                df_scaled[numeric_cols] = self.scaler.fit_transform(df_scaled[numeric_cols])
            else:
                df_scaled[numeric_cols] = self.scaler.transform(df_scaled[numeric_cols])
            logger.info(f"Scaled {len(numeric_cols)} features")

        return df_scaled

    def preprocess(self, df, training=True):
        """
        Run the full preprocessing pipeline

        Args:
            df (pd.DataFrame): Raw data
            training (bool): Whether the data is used for training

        Returns:
            pd.DataFrame: Preprocessed data
        """
        df_processed = self.clean_data(df, training=training)
        df_processed = self.create_feature_engineering(df_processed)
        df_processed = self.encode_categorical(df_processed, training=training)
        df_processed = self.scale_features(df_processed, training=training)
        return df_processed

    def prepare_features(self, df, target_col='Attrition'):
        """
        Prepare features and target for modeling

        Args:
            df (pd.DataFrame): Clean and encoded data
            target_col (str): Target column name

        Returns:
            tuple: (X, y, feature_names)
        """
        logger.info("Preparing features and target...")

        self.feature_columns = [col for col in df.columns if col != target_col]
        self.target_column = target_col

        X = df[self.feature_columns]
        y = df[target_col]

        logger.info(f"Features shape: {X.shape}")
        logger.info(f"Target shape: {y.shape}")
        logger.info(f"Target distribution:\n{y.value_counts().to_dict()}")

        return X, y, self.feature_columns

    def split_data(self, X, y, test_size=0.2, random_state=42):
        """
        Split data into train and test sets

        Args:
            X: Feature matrix
            y: Target vector
            test_size (float): Test set proportion
            random_state (int): Random seed

        Returns:
            tuple: X_train, X_test, y_train, y_test
        """
        logger.info(f"Splitting data: {test_size*100}% test, random_state={random_state}")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        logger.info(f"Training set: {X_train.shape[0]} samples")
        logger.info(f"Test set: {X_test.shape[0]} samples")

        return X_train, X_test, y_train, y_test

    def transform(self, df):
        """
        Transform new input rows for prediction

        Args:
            df (pd.DataFrame): New raw observation(s)

        Returns:
            pd.DataFrame: Preprocessed feature matrix aligned to saved columns
        """
        df_processed = self.preprocess(df, training=False)
        df_processed = df_processed.reindex(columns=self.feature_columns, fill_value=0)
        return df_processed

if __name__ == "__main__":
    # Test the preprocessor
    from data_loader import DataLoader

    loader = DataLoader("../data/WA_Fn-UseC_-HR-Employee-Attrition.csv")
    df = loader.load_data()

    preprocessor = DataPreprocessor()
    df_processed = preprocessor.preprocess(df, training=True)
    X, y, features = preprocessor.prepare_features(df_processed)
    X_train, X_test, y_train, y_test = preprocessor.split_data(X, y)

    print(f"Training: {X_train.shape[0]}, Test: {X_test.shape[0]}")