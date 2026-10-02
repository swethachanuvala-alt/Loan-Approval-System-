"""
Pure machine-learning helpers (no Streamlit imports here, so that
`train_model.py` can reuse them from the command line).

The pipeline mirrors the notebook GGST_7.ipynb:
    train/test split (80/20, stratified, random_state=42)
      -> StandardScaler (fit on train only)
      -> SMOTE on the scaled training data
      -> tuned Logistic Regression (C=0.1, solver='newton-cg', max_iter=2000)
"""
from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "loan_prediction_dataset.csv"
MODEL_PATH = ROOT / "model" / "logistic_regression_model.pkl"
SCALER_PATH = ROOT / "model" / "scaler.pkl"

FEATURES = ["age", "income", "credit_score", "dependents", "home_owner"]
TARGET = "loan_approved"
NICE_NAMES = {
    "age": "Age",
    "income": "Income",
    "credit_score": "Credit score",
    "dependents": "Dependents",
    "home_owner": "Home ownership",
}
BEST_PARAMS = dict(C=0.1, solver="newton-cg", max_iter=2000, random_state=42)


# --------------------------------------------------------------------------- data
def load_dataset(path: Path = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def split_data(df: pd.DataFrame):
    X, y = df[FEATURES], df[TARGET]
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


# --------------------------------------------------------------------------- training
def _simple_smote(X, y, k: int = 5, seed: int = 42):
    """Tiny SMOTE look-alike, used only when `imbalanced-learn` isn't installed."""
    X, y = np.asarray(X), np.asarray(y)
    classes, counts = np.unique(y, return_counts=True)
    minority = classes[np.argmin(counts)]
    n_new = counts.max() - counts.min()
    X_min = X[y == minority]
    k = min(k, len(X_min) - 1)
    nn = NearestNeighbors(n_neighbors=k + 1).fit(X_min)
    neigh = nn.kneighbors(X_min, return_distance=False)[:, 1:]
    rng = np.random.default_rng(seed)
    base = rng.integers(0, len(X_min), n_new)
    pick = neigh[base, rng.integers(0, k, n_new)]
    gap = rng.random((n_new, 1))
    synth = X_min[base] + gap * (X_min[pick] - X_min[base])
    return np.vstack([X, synth]), np.concatenate([y, np.full(n_new, minority)])


def fit_pipeline(df: pd.DataFrame):
    """Re-create the notebook pipeline and return (scaler, model)."""
    X_train, _, y_train, _ = split_data(df)
    scaler = StandardScaler().fit(X_train)
    X_scaled = scaler.transform(X_train)
    try:
        from imblearn.over_sampling import SMOTE

        X_res, y_res = SMOTE(random_state=42).fit_resample(X_scaled, y_train)
    except ImportError:
        X_res, y_res = _simple_smote(X_scaled, y_train)
    model = LogisticRegression(**BEST_PARAMS).fit(X_res, y_res)
    return scaler, model


def save_artifacts(scaler, model) -> None:
    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(model, MODEL_PATH)


def load_or_train(df: pd.DataFrame | None = None):
    """
    Load the saved scaler + model. If the .pkl files are missing, or were saved
    with an incompatible scikit-learn version, quietly re-train from the CSV.
    Returns (scaler, model, source) where source is 'saved' or 'retrained'.
    """
    df = load_dataset() if df is None else df
    try:
        scaler = joblib.load(SCALER_PATH)
        model = joblib.load(MODEL_PATH)
        probe = pd.DataFrame([df[FEATURES].iloc[0]])
        model.predict_proba(scaler.transform(probe))  # sanity check
        return scaler, model, "saved"
    except Exception:
        scaler, model = fit_pipeline(df)
        return scaler, model, "retrained"


# --------------------------------------------------------------------------- inference
def predict_one(scaler, model, applicant: dict):
    """Return (approval probability, per-feature contribution to the log-odds, intercept)."""
    row = pd.DataFrame([applicant])[FEATURES]
    scaled = scaler.transform(row)
    prob = float(model.predict_proba(scaled)[0, 1])
    contrib = dict(zip(FEATURES, (model.coef_[0] * scaled[0]).tolist()))
    return prob, contrib, float(model.intercept_[0])


def predict_many(scaler, model, frame: pd.DataFrame) -> np.ndarray:
    return model.predict_proba(scaler.transform(frame[FEATURES]))[:, 1]


# --------------------------------------------------------------------------- evaluation
def evaluate(scaler, model, df: pd.DataFrame) -> dict:
    """Score the model on the same 20 % hold-out split used in the notebook."""
    _, X_test, _, y_test = split_data(df)
    prob = predict_many(scaler, model, X_test)
    pred = (prob >= 0.5).astype(int)
    fpr, tpr, _ = roc_curve(y_test, prob)
    return {
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred),
        "recall": recall_score(y_test, pred),
        "f1": f1_score(y_test, pred),
        "roc_auc": roc_auc_score(y_test, prob),
        "cm": confusion_matrix(y_test, pred),
        "fpr": fpr,
        "tpr": tpr,
        "n_test": len(y_test),
    }


def coefficient_table(model) -> pd.DataFrame:
    t = pd.DataFrame({"feature": FEATURES, "coef": model.coef_[0]})
    t["label"] = t["feature"].map(NICE_NAMES)
    t["abs"] = t["coef"].abs()
    return t.sort_values("abs", ascending=False).reset_index(drop=True)
