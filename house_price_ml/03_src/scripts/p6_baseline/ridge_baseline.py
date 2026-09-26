"""
ridge_baseline.py - Ridge Regression (co regularization L2) de doc he so on dinh hon
so voi Linear Regression thuong (EXP-0003).

Chay: python 03_src/scripts/p6_baseline/ridge_baseline.py
"""
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

TRAIN_PATH = "01_data/processed/processed_train.csv"
VAL_PATH = "01_data/processed/processed_val.csv"
OUT_METRICS = "05_experiments/ridge_metrics.json"
OUT_COEFS = "05_experiments/ridge_coefficients.csv"

ALPHAS = [0.1, 0.3, 1, 3, 10, 30, 100, 300, 1000]


def rmsle(y_true, y_pred):
    return np.sqrt(mean_squared_error(np.log1p(y_true), np.log1p(np.clip(y_pred, 1e-6, None))))


def load_xy(path):
    df = pd.read_csv(path)
    drop_cols = [c for c in ["Id", "SalePrice", "split"] if c in df.columns]
    X = df.drop(columns=drop_cols)
    y = df["SalePrice"].values
    return X, y


def main():
    X_train, y_train = load_xy(TRAIN_PATH)
    X_val, y_val = load_xy(VAL_PATH)
    print(f"Train: {X_train.shape}, Val: {X_val.shape}")

    # RidgeCV tu chon alpha tot nhat bang cross-validation NOI BO tren train
    # (khong dung val de chon alpha, tranh ro ri)
    model = RidgeCV(alphas=ALPHAS, cv=5)
    model.fit(X_train, np.log1p(y_train))
    print(f"Alpha toi uu (chon bang CV tren train): {model.alpha_}")

    pred_log = model.predict(X_val)
    pred = np.expm1(pred_log)
    metrics = {
        "alpha": float(model.alpha_),
        "rmsle": rmsle(y_val, pred),
        "mae": mean_absolute_error(y_val, pred),
        "r2": r2_score(y_val, pred),
    }
    print("Ridge:", metrics)

    coefs = pd.Series(model.coef_, index=X_train.columns)
    coefs["__intercept__"] = model.intercept_
    coefs = coefs.sort_values(key=abs, ascending=False)
    coefs.to_csv(OUT_COEFS, header=["coef_on_log1p_SalePrice"])

    with open(OUT_METRICS, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print(f"\nDa luu {OUT_METRICS} va {OUT_COEFS}")
    print("\nTop 15 he so lon nhat (theo tri tuyet doi):")
    print(coefs.head(15).to_string())


if __name__ == "__main__":
    main()
