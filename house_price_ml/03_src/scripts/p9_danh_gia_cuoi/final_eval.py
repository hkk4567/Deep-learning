"""
final_eval.py - P9 Danh gia cuoi (cong G7)
Mo hinh cuoi: Ridge(alpha=30), fit tren train, 205 dac trung sau P5.

Chay: python 03_src/scripts/p9_danh_gia_cuoi/final_eval.py [--open-test]
Mac dinh KHONG mo test (chi tinh bootstrap CI tren val).
Truyen --open-test de chay danh gia tren test (CHI CHAY 1 LAN).
"""
import argparse
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

TRAIN_PATH = "01_data/processed/processed_train.csv"
VAL_PATH = "01_data/processed/processed_val.csv"
TEST_PATH = "01_data/processed/processed_test.csv"
ALPHA = 30.0
SEED = 42
N_BOOTSTRAP = 1000


def rmsle_arr(y_true, y_pred):
    return np.sqrt((np.log1p(y_true) - np.log1p(np.clip(y_pred, 1e-6, None))) ** 2)


def load_xy(path):
    df = pd.read_csv(path)
    drop_cols = [c for c in ["Id", "SalePrice", "split"] if c in df.columns]
    return df.drop(columns=drop_cols), df["SalePrice"].values, df.get("Id")


def bootstrap_ci(y_true, y_pred, n=N_BOOTSTRAP, seed=SEED):
    rng = np.random.RandomState(seed)
    n_samples = len(y_true)
    stats = []
    errs = rmsle_arr(y_true, y_pred)
    for _ in range(n):
        idx = rng.randint(0, n_samples, n_samples)
        stats.append(np.sqrt(np.mean(errs.values[idx] ** 2)) if hasattr(errs, "values") else np.sqrt(np.mean(np.array(errs)[idx] ** 2)))
    stats = np.array(stats)
    return float(np.mean(stats)), float(np.percentile(stats, 2.5)), float(np.percentile(stats, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--open-test", action="store_true")
    args = ap.parse_args()

    X_train, y_train, _ = load_xy(TRAIN_PATH)
    X_val, y_val, _ = load_xy(VAL_PATH)

    model = Ridge(alpha=ALPHA)
    model.fit(X_train, np.log1p(y_train))

    pred_val = np.expm1(model.predict(X_val))
    rmsle_val = float(np.sqrt(mean_squared_error(np.log1p(y_val), np.log1p(pred_val))))
    mean_ci, lo_ci, hi_ci = bootstrap_ci(pd.Series(y_val), pred_val)
    val_report = {
        "rmsle_point": rmsle_val,
        "rmsle_bootstrap_mean": mean_ci,
        "rmsle_bootstrap_95ci": [lo_ci, hi_ci],
        "mae": float(mean_absolute_error(y_val, pred_val)),
        "r2": float(r2_score(y_val, pred_val)),
    }
    print("VAL (bootstrap 1000 lan):", json.dumps(val_report, indent=2))
    with open("05_experiments/exp0004_val_bootstrap.json", "w", encoding="utf-8") as f:
        json.dump(val_report, f, indent=2, ensure_ascii=False)

    if not args.open_test:
        print("\n[Chua mo test - chay lai voi --open-test khi da san sang danh gia cuoi]")
        return

    X_test, y_test, id_test = load_xy(TEST_PATH)
    pred_test = np.expm1(model.predict(X_test))
    rmsle_test = float(np.sqrt(mean_squared_error(np.log1p(y_test), np.log1p(pred_test))))
    mean_ci_t, lo_ci_t, hi_ci_t = bootstrap_ci(pd.Series(y_test), pred_test)
    test_report = {
        "rmsle_point": rmsle_test,
        "rmsle_bootstrap_mean": mean_ci_t,
        "rmsle_bootstrap_95ci": [lo_ci_t, hi_ci_t],
        "mae": float(mean_absolute_error(y_test, pred_test)),
        "r2": float(r2_score(y_test, pred_test)),
        "n_test": len(y_test),
    }
    print("\n*** TEST (chay dung 1 lan) ***:", json.dumps(test_report, indent=2))
    with open("05_experiments/exp0004_test_FINAL.json", "w", encoding="utf-8") as f:
        json.dump(test_report, f, indent=2, ensure_ascii=False)

    # Luu chi tiet du doan test de phan tich (khong dung de chinh mo hinh)
    detail = pd.DataFrame({"Id": id_test, "y_true": y_test, "y_pred": pred_test})
    detail["abs_error"] = (detail["y_true"] - detail["y_pred"]).abs()
    detail.to_csv("05_experiments/exp0004_test_predictions.csv", index=False)
    print("Da luu 05_experiments/exp0004_test_FINAL.json va exp0004_test_predictions.csv")


if __name__ == "__main__":
    main()
