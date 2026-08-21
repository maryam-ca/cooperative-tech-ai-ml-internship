"""
Lumina Evaluation Utilities
Deterministic live evaluation, model comparison, feature attribution,
and retraining — all aligned with the deployed artifact set.
"""

from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import roc_curve, confusion_matrix

from src.ui_components import (
    MODELS_DIR,
    DATA_FILE,
    model_type_label,
    artifact_mtime,
    load_config,
    load_pipeline,
)

MODEL_METADATA = MODELS_DIR / "model_metadata.json"

_SMOKE_ROW = {
    "Age": 30,
    "Gender": "Male",
    "MaritalStatus": "Single",
    "Department": "Research & Development",
    "JobRole": "Research Scientist",
    "Education": 3,
    "MonthlyIncome": 5000,
    "YearsAtCompany": 5,
    "OverTime": "No",
    "TotalWorkingYears": 10,
    "YearsInCurrentRole": 3,
    "JobSatisfaction": 3,
    "WorkLifeBalance": 3,
    "DistanceFromHome": 10,
    "NumCompaniesWorked": 2,
}


def ensure_deployed():
    """Verify the deployed artifacts are coherent; regenerate them if not.

    Guards against stale/mismatched scaler/encoders/feature-column sets on disk.
    """
    key = artifact_mtime()
    if st.session_state.get("_deployed_key") != key:
        st.session_state.pop("_deployed_ok", None)
        st.session_state["_deployed_key"] = key
    if st.session_state.get("_deployed_ok", False):
        return load_pipeline(key)

    model, pre = load_pipeline(key)
    try:
        proba = model.predict_proba(pre.transform(pd.DataFrame([_SMOKE_ROW])))[0, 1]
        if not 0.0 <= float(proba) <= 1.0:
            raise ValueError("unexpected probability output")
        st.session_state["_deployed_ok"] = True
        return model, pre
    except Exception:
        with st.spinner("Regenerating deployed model artifacts…"):
            retrain_and_save(load_config())
        st.session_state["_deployed_ok"] = True
        model, pre = load_pipeline(artifact_mtime())
        return model, pre


def _deployed_metrics_key():
    return artifact_mtime()


@st.cache_data(show_spinner="Evaluating deployed model\u2026")
def compute_evaluation(_key):
    """Return live metrics for the deployed best_model.pkl on a fixed split."""
    from src.preprocessor import DataPreprocessor
    from src.model_trainer import ModelTrainer

    df = pd.read_csv(DATA_FILE)
    pre = DataPreprocessor()
    proc = pre.preprocess(df, training=True)
    X, y, features = pre.prepare_features(proc)
    X_train, X_test, y_train, y_test = pre.split_data(X, y)

    deployed = joblib.load(MODELS_DIR / "best_model.pkl")
    st_train = ModelTrainer()
    lr = st_train.train_logistic_regression(X_train, y_train)
    rf = st_train.train_random_forest(X_train, y_train)

    dep_res = st_train.evaluate_model(deployed, X_test, y_test, "Deployed")
    lr_res = st_train.evaluate_model(lr, X_test, y_test, "Logistic Regression")
    rf_res = st_train.evaluate_model(rf, X_test, y_test, "Random Forest")

    y_pred = deployed.predict(X_test)
    y_prob = deployed.predict_proba(X_test)[:, 1]
    cm = confusion_matrix(y_test, y_pred).tolist()
    fpr, tpr, _ = roc_curve(y_test, y_prob)

    importance = _importance_for(deployed, features)

    return {
        "deployed_type": model_type_label(deployed),
        "metrics": _scalar_metrics(dep_res),
        "comparison": {
            "Logistic Regression": _scalar_metrics(lr_res),
            "Random Forest": _scalar_metrics(rf_res),
        },
        "confusion_matrix": cm,
        "roc": {"fpr": fpr, "tpr": tpr, "auc": float(dep_res["roc_auc"])},
        "importance": importance,
        "features": list(features),
        "n_rows": int(X.shape[0]),
        "n_test": int(X_test.shape[0]),
        "n_pos_test": int(y_test.sum()),
    }


def _scalar_metrics(res: dict) -> dict:
    return {
        "accuracy": float(res["accuracy"]),
        "precision": float(res["precision"]),
        "recall": float(res["recall"]),
        "f1": float(res["f1_score"]),
        "roc_auc": float(res["roc_auc"]),
    }


def _importance_for(model, features):
    """Signed importance: coefs for linear models, importances for trees."""
    if hasattr(model, "coef_"):
        coefs = np.asarray(model.coef_[0], dtype=float)
        order = np.argsort(-np.abs(coefs))
        return [
            {"feature": features[i], "value": float(coefs[i])}
            for i in order
        ]
    if hasattr(model, "feature_importances_"):
        imp = np.asarray(model.feature_importances_, dtype=float)
        order = np.argsort(-imp)
        return [
            {"feature": features[i], "value": float(imp[i])}
            for i in order
        ]
    return [{"feature": f, "value": 0.0} for f in features]


def predict_row(input_dict: dict, model, pre) -> tuple:
    """Transform a single raw input row and predict. Returns (pred, proba, df_scaled)."""
    df = pd.DataFrame([input_dict])
    processed = pre.transform(df)
    pred = int(model.predict(processed)[0])
    proba = float(model.predict_proba(processed)[0, 1])
    return pred, proba, processed


def row_factor_breakdown(input_dict: dict, model, pre, top_n: int = 5):
    """Per-intervention factor breakdown for one prediction."""
    df = pd.DataFrame([input_dict])
    processed = pre.transform(df)
    feat_cols = list(pre.feature_columns)
    if hasattr(model, "coef_"):
        coefs = model.coef_[0]
        vals = np.abs(coefs) * (np.asarray(processed)[0] if hasattr(processed, "to_numpy") else np.asarray(processed)[0])
        order = np.argsort(-vals)
    else:
        imp = model.feature_importances_
        vals = imp
        order = np.argsort(-imp)
    out = []
    for i in order[:top_n]:
        out.append({"feature": feat_cols[i] if i < len(feat_cols) else str(i), "value": float(vals[i])})
    return out


def retrain_and_save(cfg: dict) -> dict:
    """Retrain with the configured algorithm, save artifacts + metadata."""
    from src.preprocessor import DataPreprocessor
    from src.model_trainer import ModelTrainer

    df = pd.read_csv(DATA_FILE)
    pre = DataPreprocessor()
    proc = pre.preprocess(df, training=True)
    X, y, features = pre.prepare_features(proc)
    X_train, X_test, y_train, y_test = pre.split_data(X, y)

    trainer = ModelTrainer()
    algorithm = cfg.get("algorithm", "Logistic Regression")
    if algorithm == "Random Forest":
        model = trainer.train_random_forest(
            X_train, y_train, n_estimators=int(cfg.get("n_estimators", 100))
        )
    else:
        model = trainer.train_logistic_regression(X_train, y_train)

    res = trainer.evaluate_model(model, X_test, y_test, algorithm)
    trainer.save_model(model, pre)

    metadata = {
        "model_type": model_type_label(model),
        "algorithm": algorithm,
        "features": list(features),
        "performance": _scalar_metrics(res),
        "trained_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    MODEL_METADATA.write_text(
        __import__("json").dumps(metadata, indent=2), encoding="utf-8"
    )
    return metadata


def load_metadata() -> dict:
    if MODEL_METADATA.exists():
        try:
            return __import__("json").loads(MODEL_METADATA.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def model_summary_df(metrics: dict) -> pd.DataFrame:
    rows = []
    for name, m in metrics.items():
        rows.append(
            {
                "Model": name,
                "Accuracy": m["accuracy"],
                "Precision": m["precision"],
                "Recall": m["recall"],
                "F1 Score": m["f1"],
                "ROC-AUC": m["roc_auc"],
            }
        )
    return pd.DataFrame(rows)