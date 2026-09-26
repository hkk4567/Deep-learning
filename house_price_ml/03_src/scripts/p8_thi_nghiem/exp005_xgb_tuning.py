"""
exp005_xgb_tuning.py - P8, thi nghiem EXP-0005
Gia thuyet: XGBoost mac dinh (EXP-0002, RMSLE=0.1267) chua toi uu sieu tham so;
tim sieu tham so tot hon bang RandomizedSearchCV (5-fold, CHI tren train) co the cai thien.

Chay: python 03_src/scripts/p8_thi_nghiem/exp005_xgb_tuning.py
"""
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV, KFold
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

TRAIN_PATH = "01_data/processed/processed_train.csv"
VAL_PATH = "01_data/processed/processed_val.csv"
OUT_METRICS = "05_experiments/exp005_xgb_tuning_metrics.json"


def rmsle(y_true, y_pred):
    return np.sqrt(mean_squared_error(np.log1p(y_true), np.log1p(np.clip(y_pred, 1e-6, None))))


def load_xy(path):
    df = pd.read_csv(path)
    drop_cols = [c for c in ["Id", "SalePrice", "split"] if c in df.columns]
    return df.drop(columns=drop_cols), df["SalePrice"].values


def main():
    X_train, y_train = load_xy(TRAIN_PATH)
    X_val, y_val = load_xy(VAL_PATH)

    param_dist = {
        "n_estimators": [300, 500, 800, 1200],
        "max_depth": [2, 3, 4, 5, 6],
        "learning_rate": [0.01, 0.02, 0.03, 0.05, 0.08],
        "subsample": [0.6, 0.7, 0.8, 0.9, 1.0],
        "colsample_bytree": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        "reg_alpha": [0, 0.01, 0.1, 0.5, 1],
        "reg_lambda": [0.5, 1, 1.5, 2, 3],
        "min_child_weight": [1, 2, 3, 5],
    }
    base = XGBRegressor(random_state=42, n_jobs=-1)
    search = RandomizedSearchCV(
        base, param_distributions=param_dist, n_iter=60,
        scoring="neg_root_mean_squared_error",
        cv=KFold(5, shuffle=True, random_state=42),
        random_state=42, n_jobs=-1, verbose=0,
    )
    search.fit(X_train, np.log1p(y_train))
    print("Sieu tham so tot nhat (CV tren train):", search.best_params_)
    print("CV RMSE(log) tot nhat:", -search.best_score_)

    best_model = search.best_estimator_
    pred = np.expm1(best_model.predict(X_val))
    metrics = {
        "best_params": search.best_params_,
        "cv_rmse_log_train": float(-search.best_score_),
        "val_rmsle": rmsle(y_val, pred),
        "val_mae": mean_absolute_error(y_val, pred),
        "val_r2": r2_score(y_val, pred),
    }
    print("Val:", metrics["val_rmsle"], metrics["val_mae"], metrics["val_r2"])

    with open(OUT_METRICS, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print(f"Da luu {OUT_METRICS}")


if __name__ == "__main__":
    main()
