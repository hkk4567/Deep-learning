# Quy trình thực hiện EDA và Chuẩn bị dữ liệu

Dưới đây là các bước chạy pipeline từ việc thiết lập môi trường, kiểm toán dữ liệu cho đến khi tạo ra các báo cáo EDA chi tiết.

## Bước 0 — Cài môi trường (nếu chưa làm)
Chạy tệp batch sau để thiết lập môi trường:
```bash
setup_env.bat
```

## Bước 1 — Kiểm toán dữ liệu (P1)
```bash
python 03_src/scripts/audit_dataset.py --raw 00_raw --out 01_data/audit --label-col SalePrice
```

## Bước 2 — Chia train/val/test (P3)
```bash
python 03_src/scripts/make_splits.py --table 00_raw/train.csv --out 01_data/splits --version v1 --id-col Id --label-col SalePrice --val 0.15 --test 0.15 --seed 42
```

## Bước 3 — EDA thủ công ban đầu (chỉ trên tập train)
```bash
python 03_src/scripts/eda_train.py
```
> **→ Kết quả đầu ra:** `02_notebooks/eda_train.png`

## Bước 4 — Lọc 71 đặc trưng đã chọn
```bash
python 03_src/scripts/select_features.py
```
> **→ Kết quả đầu ra:** `01_data/splits/split_v1_selected_features.csv`

## Bước 5 — EDA chính thức trên 71 đặc trưng đã chọn
```bash
python 03_src/scripts/explore_tabular.py --split-csv 01_data/splits/split_v1_selected_features.csv --out-dir 06_reports/eda --label-col SalePrice --label-type numeric --id-col Id --ordinal-cols ExterQual,ExterCond,BsmtQual,BsmtCond,BsmtExposure,BsmtFinType1,BsmtFinType2,HeatingQC,KitchenQual,Functional,GarageFinish,GarageQual,GarageCond,PavedDrive,LandSlope,LotShape,Utilities,FireplaceQu --valid-range LotFrontage:0:None MasVnrArea:0:None GarageYrBlt:1800:2026
```

## Bước 6 — EDA đối chiếu trên toàn bộ 79 cột gốc
```bash
python 03_src/scripts/explore_tabular.py --split-csv 01_data/splits/split_v1.csv --out-dir 06_reports/eda_full --label-col SalePrice --label-type numeric --id-col Id --ordinal-cols ExterQual,ExterCond,BsmtQual,BsmtCond,BsmtExposure,BsmtFinType1,BsmtFinType2,HeatingQC,KitchenQual,Functional,GarageFinish,GarageQual,GarageCond,PavedDrive,LandSlope,LotShape,Utilities,PoolQC,FireplaceQu,Fence --valid-range LotFrontage:0:None MasVnrArea:0:None GarageYrBlt:1800:2026
```

## Bước 7 — Vẽ 9 biểu đồ theo nhóm
```bash
python 03_src/scripts/eda_group_plots.py (tạo thư mục by_group trước)
```
> **→ Kết quả đầu ra:** Các tệp ảnh `06_reports/eda/eda_plots/by_group/N1...N9.png`