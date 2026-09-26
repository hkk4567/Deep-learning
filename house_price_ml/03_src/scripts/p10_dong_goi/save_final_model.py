"""
save_final_model.py - Luu checkpoint mo hinh cuoi (Ridge alpha=30) thanh joblib,
kem metadata (config, seed, hash du lieu) de dong goi (P10).

Chay: python 03_src/scripts/p10_dong_goi/save_final_model.py
"""
import json
import hashlib
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import Ridge

TRAIN_PATH = "01_data/processed/processed_train.csv"
OUT_MODEL = "01_data/processed/final_model_ridge.joblib"
OUT_META = "01_data/processed/final_model_meta.json"
ALPHA = 30.0
SEED = 42


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    df = pd.read_csv(TRAIN_PATH)
    drop_cols = [c for c in ["Id", "SalePrice", "split"] if c in df.columns]
    X_train = df.drop(columns=drop_cols)
    y_train = df["SalePrice"].values

    model = Ridge(alpha=ALPHA)
    model.fit(X_train, np.log1p(y_train))
    joblib.dump(model, OUT_MODEL)

    meta = {
        "model": "sklearn.linear_model.Ridge",
        "alpha": ALPHA,
        "seed": SEED,
        "target_transform": "log1p (predict phai np.expm1 lai)",
        "n_features_in": X_train.shape[1],
        "feature_names": list(X_train.columns),
        "train_rows": len(X_train),
        "train_data_sha256": sha256_file(TRAIN_PATH),
        "exp_id": "EXP-0004",
        "val_rmsle": 0.1155,
        "test_rmsle": 0.1301,
    }
    with open(OUT_META, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"Da luu {OUT_MODEL}")
    print(f"Da luu {OUT_META}")
    print(f"train_data_sha256 = {meta['train_data_sha256']}")


if __name__ == "__main__":
    main()
