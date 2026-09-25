"""
select_features.py - Loc bang split_v1.csv chi con 71 dac trung da chon (P4)
Chay: python 03_src/scripts/select_features.py
Dau vao:  01_data/splits/split_v1.csv
Dau ra:   01_data/splits/split_v1_selected_features.csv

Danh sach 71 cot duoc chon theo 9 nhom y nghia nghiep vu (xem 06_reports/problem_definition.md
va cac dong log LOG-0034/LOG-0035 trong 07_logs/change_log.xlsx de biet ly do gium/loai tung cot).
"""
import pandas as pd

IN_PATH = "01_data/splits/split_v1.csv"
OUT_PATH = "01_data/splits/split_v1_selected_features.csv"

SELECTED_FEATURES = [
    # Nhom 1 - Khu dat
    "MSSubClass", "MSZoning", "LotFrontage", "LotArea", "Street", "Alley",
    "LotShape", "LandContour", "Utilities", "LotConfig", "LandSlope",
    # Nhom 2 - Vi tri
    "Neighborhood", "Condition1", "Condition2",
    # Nhom 3 - Chat luong/tinh trang nha (+ Fireplaces, FireplaceQu them lai theo FND-0004)
    "BldgType", "HouseStyle", "OverallQual", "OverallCond", "YearBuilt", "YearRemodAdd",
    "RoofStyle", "RoofMatl", "Exterior1st", "Exterior2nd", "MasVnrType", "MasVnrArea",
    "ExterQual", "ExterCond", "Foundation", "Fireplaces", "FireplaceQu",
    # Nhom 4 - Mong/tang ham
    "BsmtQual", "BsmtCond", "BsmtExposure", "BsmtFinType1", "BsmtFinSF1",
    "BsmtFinType2", "BsmtFinSF2", "BsmtUnfSF", "TotalBsmtSF", "BsmtFullBath", "BsmtHalfBath",
    # Nhom 5 - He thong trong nha
    "Heating", "HeatingQC", "CentralAir", "Electrical",
    # Nhom 6 - Dien tich/khong gian sinh hoat (+ WoodDeckSF, OpenPorchSF them lai theo FND-0004)
    "1stFlrSF", "2ndFlrSF", "LowQualFinSF", "GrLivArea", "FullBath", "HalfBath",
    "BedroomAbvGr", "KitchenAbvGr", "KitchenQual", "TotRmsAbvGrd", "Functional",
    "WoodDeckSF", "OpenPorchSF",
    # Nhom 7 - Garage
    "GarageType", "GarageYrBlt", "GarageFinish", "GarageCars", "GarageArea",
    "GarageQual", "GarageCond",
    # Nhom 8 - Duong xe vao
    "PavedDrive",
    # Nhom 9 - Thong tin giao dich
    "MoSold", "YrSold", "SaleType", "SaleCondition",
]

# Cac cot loai han (tin hieu qua yeu, xem FND-0004): Fence, MiscFeature, MiscVal,
# PoolArea, PoolQC, EnclosedPorch, 3SsnPorch, ScreenPorch


def main():
    df = pd.read_csv(IN_PATH)
    keep_cols = ["Id"] + SELECTED_FEATURES + ["SalePrice", "split"]
    missing = [c for c in keep_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Thieu cot trong du lieu goc: {missing}")
    out = df[keep_cols]
    out.to_csv(OUT_PATH, index=False)
    print(f"Da luu {OUT_PATH} | shape={out.shape} | so dac trung={len(SELECTED_FEATURES)}")


if __name__ == "__main__":
    main()
