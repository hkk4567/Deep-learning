"""
baseline.py - P6 Baseline (cong G3)
  1) Baseline tam thuong: du doan hang so = trung binh SalePrice cua train
  2) Baseline co dien: XGBoost tren dac trung da tien xu ly (P5)

Metric chinh: RMSLE = RMSE(log1p(y_true), log1p(y_pred)), theo problem_definition.md
Chi danh gia tren VAL (test con khoa, chi mo o P9 danh gia cuoi).

Chay: python 03_src/scripts/p6_baseline/baseline.py
"""
import json
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

TRAIN_PATH = "01_data/processed/processed_train.csv"
VAL_PATH = "01_data/processed/processed_val.csv"
OUT_PATH = "05_experiments/baseline_metrics.json"


def rmsle(y_true, y_pred):
    return np.sqrt(mean_squared_error(np.log1p(y_true), np.log1p(np.clip(y_pred, 0, None))))


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

    # --- Baseline 1: tam thuong (hang so = trung binh train) ---
    const_pred = np.full_like(y_val, fill_value=y_train.mean(), dtype=float)
    m1 = {
        "rmsle": rmsle(y_val, const_pred),
        "mae": mean_absolute_error(y_val, const_pred),
        "r2": r2_score(y_val, const_pred),
    }
    print("Baseline 1 (hang so = trung binh train):", m1)

    # --- Baseline 2: co dien (XGBoost, hoc tren log1p(SalePrice)) ---
    model = XGBRegressor(
        n_estimators=500, learning_rate=0.05, max_depth=4,
        subsample=0.8, colsample_bytree=0.8, random_state=42, n_jobs=-1,
    )
    model.fit(X_train, np.log1p(y_train))
    pred_log = model.predict(X_val)
    pred = np.expm1(pred_log)
    m2 = {
        "rmsle": rmsle(y_val, pred),
        "mae": mean_absolute_error(y_val, pred),
        "r2": r2_score(y_val, pred),
    }
    print("Baseline 2 (XGBoost co dien):", m2)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump({"baseline_1_constant_mean": m1, "baseline_2_xgboost": m2}, f, indent=2, ensure_ascii=False)
    print(f"Da luu {OUT_PATH}")


if __name__ == "__main__":
    main()
