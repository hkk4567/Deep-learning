"""
predict_from_raw.py - Script suy luan doc lap: nhan dau vao la CSV THO
(dung schema goc nhu 00_raw/train.csv, KHONG can cot SalePrice), chay qua
dung pipeline (loc 71 dac trung -> quy tac nghiep vu -> preprocessor.joblib
-> final_model_ridge.joblib) va tra ve gia du doan.

Day la kiem chung dau-cuoi doc lap voi luc train/danh gia (khong dung lai
cac file processed_*.csv co san).

Chay: python 03_src/scripts/p10_dong_goi/predict_from_raw.py --input <file.csv> --output <file.csv>
Vi du: python 03_src/scripts/p10_dong_goi/predict_from_raw.py --input 00_raw/train.csv --output /tmp/pred.csv --sample-ids 1,2,3
"""
import argparse
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import joblib
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = PROJECT_ROOT / "03_src" / "scripts"
FEATURE_DIR = SCRIPT_DIR / "p4_kham_pha_du_lieu"
PREPROCESS_DIR = SCRIPT_DIR / "p5_tien_xu_ly"

for extra_path in [str(SCRIPT_DIR), str(FEATURE_DIR), str(PREPROCESS_DIR)]:
    if extra_path not in sys.path:
        sys.path.insert(0, extra_path)

warnings.filterwarnings("ignore", message="X does not have valid feature names")

from select_features import SELECTED_FEATURES  # type: ignore[import-not-found]
from encode_business_rules import ORDINAL_WITH_NA, ORDINAL_NO_NA, map_ordinal  # type: ignore[import-not-found]

PREPROCESSOR_PATH = "01_data/processed/preprocessor.joblib"
MODEL_PATH = "01_data/processed/final_model_ridge.joblib"


def transform_raw(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Lap lai dung cac buoc da ap dung luc train, TRU loai outlier
    (chi hop ly khi lam sach tap train, khong ap cho mau suy luan moi)."""
    df = df_raw[[c for c in SELECTED_FEATURES if c in df_raw.columns]].copy()

    df["MasVnrArea"] = df["MasVnrArea"].fillna(0)
    df["GarageYrBlt"] = df["GarageYrBlt"].fillna(0)

    for col, order in ORDINAL_WITH_NA.items():
        df[col] = map_ordinal(df[col], order)
    for col, order in ORDINAL_NO_NA.items():
        df[col] = map_ordinal(df[col], order)
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="CSV tho, schema nhu 00_raw/train.csv")
    ap.add_argument("--output", required=True)
    ap.add_argument("--sample-ids", help="Vd '1,2,3' - chi du doan cac Id nay (de test nhanh)")
    args = ap.parse_args()

    df_raw = pd.read_csv(args.input)
    if args.sample_ids:
        ids = [int(x) for x in args.sample_ids.split(",")]
        df_raw = df_raw[df_raw["Id"].isin(ids)].reset_index(drop=True)

    X = transform_raw(df_raw)

    preprocessor = joblib.load(PREPROCESSOR_PATH)
    X_processed = preprocessor.transform(X)

    model = joblib.load(MODEL_PATH)
    pred_log = model.predict(X_processed)
    pred = np.expm1(pred_log)

    out = pd.DataFrame({"Id": df_raw["Id"].values, "SalePrice_predicted": pred})
    if "SalePrice" in df_raw.columns:
        out["SalePrice_actual"] = df_raw["SalePrice"].values
    out.to_csv(args.output, index=False)
    print(out.to_string(index=False))
    print(f"\nDa luu {args.output}")


if __name__ == "__main__":
    main()
