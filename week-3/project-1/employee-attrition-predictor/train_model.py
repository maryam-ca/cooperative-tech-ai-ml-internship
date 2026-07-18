"""Train the attrition prediction model."""
import sys
sys.path.insert(0, r"C:\Users\Maryam\OneDrive\ドキュメント\GitHub\cooperative-tech-ai-ml-internship\week-3\project-1\employee-attrition-predictor")

import pandas as pd
from pathlib import Path
from src.preprocessor import DataPreprocessor
from src.model_trainer import ModelTrainer

data_path = Path(r"C:\Users\Maryam\OneDrive\ドキュメント\GitHub\cooperative-tech-ai-ml-internship\week-3\project-1\employee-attrition-predictor\data\WA_Fn-UseC_-HR-Employee-Attrition.csv")
df = pd.read_csv(data_path)
print(f"Loaded {len(df)} rows")

preprocessor = DataPreprocessor()
df_processed = preprocessor.preprocess(df, training=True)
X, y, features = preprocessor.prepare_features(df_processed)
X_train, X_test, y_train, y_test = preprocessor.split_data(X, y)

trainer = ModelTrainer()
trainer.train_and_evaluate_all(X_train, X_test, y_train, y_test)
trainer.save_model(trainer.best_model, preprocessor)

print(f"\nSaved best model: {trainer.best_model_name}")
print("\nModel Comparison:")
print(trainer.create_results_summary())
