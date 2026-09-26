"""
encode_business_rules.py - Ap quy tac nghiep vu CO DINH (khong hoc tu du lieu),
nen ap dong nhat cho ca train/val/test, TRUOC khi dua vao preprocess_tabular.py.

Gom 3 viec:
  1. Map cac cot ordinal (danh muc CO thu bac) sang so nguyen theo dung thu tu.
     Cot co the "khong co dac diem" (NaN nghia la NA that su) duoc gan hang 0.
  2. Dien 0 cho MasVnrArea, GarageYrBlt khi thieu (thieu = khong co dac diem do,
     xem FND-0001). Luu y: GarageYrBlt=0 la gia tri "sentinel" (nam ngoai mien
     nam thuc), phu hop cho mo hinh cay; neu dung mo hinh tuyen tinh/khoang cach
     can xem lai (vd dung YearBuilt thay the).
  3. Loai 2 dong ngoai lai da chot o FND-0003 (Id=524, Id=1299) - chi anh huong
     train vi ca 2 deu roi vao train o split_v1.

Chay: python 03_src/scripts/encode_business_rules.py
Vao:  01_data/splits/split_v1_selected_features.csv
Ra:   01_data/splits/split_v1_prepped.csv
"""
import pandas as pd
import numpy as np

IN_PATH = "01_data/splits/split_v1_selected_features.csv"
OUT_PATH = "01_data/splits/split_v1_prepped.csv"

OUTLIER_IDS = [524, 1299]  # FND-0003: SaleCondition=Partial, GrLivArea>4000, gia bat thuong thap

# Cot ordinal CO muc "NA = khong co dac diem" -> NA xep hang 0
ORDINAL_WITH_NA = {
    "BsmtQual":     ["NA", "Po", "Fa", "TA", "Gd", "Ex"],
    "BsmtCond":     ["NA", "Po", "Fa", "TA", "Gd", "Ex"],
    "BsmtExposure": ["NA", "No", "Mn", "Av", "Gd"],
    "BsmtFinType1": ["NA", "Unf", "LwQ", "Rec", "BLQ", "ALQ", "GLQ"],
    "BsmtFinType2": ["NA", "Unf", "LwQ", "Rec", "BLQ", "ALQ", "GLQ"],
    "FireplaceQu":  ["NA", "Po", "Fa", "TA", "Gd", "Ex"],
    "GarageFinish": ["NA", "Unf", "RFn", "Fin"],
    "GarageQual":   ["NA", "Po", "Fa", "TA", "Gd", "Ex"],
    "GarageCond":   ["NA", "Po", "Fa", "TA", "Gd", "Ex"],
}

# Cot ordinal LUON co gia tri (khong co truong hop NA)
ORDINAL_NO_NA = {
    "ExterQual":  ["Po", "Fa", "TA", "Gd", "Ex"],
    "ExterCond":  ["Po", "Fa", "TA", "Gd", "Ex"],
    "HeatingQC":  ["Po", "Fa", "TA", "Gd", "Ex"],
    "KitchenQual": ["Po", "Fa", "TA", "Gd", "Ex"],
    "Functional": ["Sal", "Sev", "Maj2", "Maj1", "Mod", "Min2", "Min1", "Typ"],
    "PavedDrive": ["N", "P", "Y"],
    "LotShape":   ["IR3", "IR2", "IR1", "Reg"],
    "LandSlope":  ["Sev", "Mod", "Gtl"],
    "Utilities":  ["NoSeWa", "AllPub"],
}


def map_ordinal(series, order):
    mapping = {level: rank for rank, level in enumerate(order)}
    s = series.fillna("NA")
    unknown = set(s.unique()) - set(mapping)
    if unknown:
        raise ValueError(f"{series.name}: gia tri khong co trong bang anh xa: {unknown}")
    return s.map(mapping).astype(int)


def main():
    df = pd.read_csv(IN_PATH)

    before = len(df)
    df = df[~df["Id"].isin(OUTLIER_IDS)].reset_index(drop=True)
    print(f"Da loai {before - len(df)} dong ngoai lai (Id={OUTLIER_IDS}) - FND-0003")

    df["MasVnrArea"] = df["MasVnrArea"].fillna(0)
    df["GarageYrBlt"] = df["GarageYrBlt"].fillna(0)
    print("Da dien 0 cho MasVnrArea, GarageYrBlt khi thieu (missing co y nghia)")

    for col, order in ORDINAL_WITH_NA.items():
        df[col] = map_ordinal(df[col], order)
    for col, order in ORDINAL_NO_NA.items():
        df[col] = map_ordinal(df[col], order)
    print(f"Da ma hoa ordinal {len(ORDINAL_WITH_NA) + len(ORDINAL_NO_NA)} cot")

    df.to_csv(OUT_PATH, index=False)
    print(f"Da luu {OUT_PATH} | shape={df.shape}")


if __name__ == "__main__":
    main()
