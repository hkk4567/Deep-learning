# Quy trình thực hiện EDA và Chuẩn bị dữ liệu

Dưới đây là các bước chạy pipeline từ việc thiết lập môi trường, kiểm toán dữ liệu cho đến khi tiền xử lý xong dữ liệu, sẵn sàng cho bước Baseline (P6).

> **Lưu ý đường dẫn:** các script trong `03_src/scripts/` đã được sắp xếp lại vào thư mục con theo từng bước (xem `README.md`). Toàn bộ lệnh dưới đây đã cập nhật đúng đường dẫn mới.

## Bước 0 — Cài môi trường (nếu chưa làm)
```bash
setup_env.bat
```

## Bước 1 — Kiểm toán dữ liệu (P1)
```bash
python 03_src/scripts/p1_kiem_toan_du_lieu/audit_dataset.py --raw 00_raw --out 01_data/audit --label-col SalePrice
```

## Bước 2 — Chia train/val/test (P3)
```bash
python 03_src/scripts/p3_chia_du_lieu/make_splits.py --table 00_raw/train.csv --out 01_data/splits --version v1 --id-col Id --label-col SalePrice --val 0.15 --test 0.15 --seed 42
```

## Bước 3 — EDA thủ công ban đầu (chỉ trên tập train)
```bash
python 03_src/scripts/p4_kham_pha_du_lieu/eda_train.py
```
> **→ Kết quả đầu ra:** `02_notebooks/eda_train.png`

## Bước 4 — Lọc 71 đặc trưng đã chọn
```bash
python 03_src/scripts/p4_kham_pha_du_lieu/select_features.py
```
> **→ Kết quả đầu ra:** `01_data/splits/split_v1_selected_features.csv`

## Bước 5 — EDA chính thức trên 71 đặc trưng đã chọn
```bash
python 03_src/scripts/p4_kham_pha_du_lieu/explore_tabular.py --split-csv 01_data/splits/split_v1_selected_features.csv --out-dir 06_reports/eda --label-col SalePrice --label-type numeric --id-col Id --ordinal-cols ExterQual,ExterCond,BsmtQual,BsmtCond,BsmtExposure,BsmtFinType1,BsmtFinType2,HeatingQC,KitchenQual,Functional,GarageFinish,GarageQual,GarageCond,PavedDrive,LandSlope,LotShape,Utilities,FireplaceQu --valid-range LotFrontage:0:None MasVnrArea:0:None GarageYrBlt:1800:2026
```
> **→ Kết quả đầu ra:** `06_reports/eda/eda_report.md`, `06_reports/eda/eda.json`, `06_reports/eda/eda_plots/*.png`

## Bước 6 — EDA đối chiếu trên toàn bộ 79 cột gốc
```bash
python 03_src/scripts/p4_kham_pha_du_lieu/explore_tabular.py --split-csv 01_data/splits/split_v1.csv --out-dir 06_reports/eda_full --label-col SalePrice --label-type numeric --id-col Id --ordinal-cols ExterQual,ExterCond,BsmtQual,BsmtCond,BsmtExposure,BsmtFinType1,BsmtFinType2,HeatingQC,KitchenQual,Functional,GarageFinish,GarageQual,GarageCond,PavedDrive,LandSlope,LotShape,Utilities,PoolQC,FireplaceQu,Fence --valid-range LotFrontage:0:None MasVnrArea:0:None GarageYrBlt:1800:2026
```
> **→ Kết quả đầu ra:** `06_reports/eda_full/eda_report.md`, `06_reports/eda_full/eda.json` — dùng để đối chiếu, phát hiện thêm `Fireplaces`, `FireplaceQu`, `WoodDeckSF`, `OpenPorchSF` (xem FND-0004).

## Bước 7 — Vẽ 9 biểu đồ theo nhóm
```bash
python 03_src/scripts/p4_kham_pha_du_lieu/eda_group_plots.py
```
> **→ Kết quả đầu ra:** `06_reports/eda/eda_plots/by_group/N1...N9.png` (script tự tạo thư mục output, không cần `mkdir` tay).

## Bước 8 — Áp quy tắc nghiệp vụ cố định (P5)
Mã hóa Ordinal cho 18 cột chất lượng/thứ bậc, điền `0` cho `MasVnrArea`/`GarageYrBlt` khi thiếu (missing có ý nghĩa, FND-0001), loại 2 dòng ngoại lai `Id=524, Id=1299` (FND-0003):
```bash
python 03_src/scripts/p5_tien_xu_ly/encode_business_rules.py
```
> **→ Kết quả đầu ra:** `01_data/splits/split_v1_prepped.csv` (1458 dòng × 74 cột)

## Bước 9 — Tiền xử lý chính thức (P5, fit trên train)
```bash
python 03_src/scripts/p5_tien_xu_ly/preprocess_tabular.py fit \
  --split-csv 01_data/splits/split_v1_prepped.csv --out-dir 01_data/processed \
  --label-col SalePrice --label-type numeric --id-col Id \
  --impute median --scaler standard --valid-range LotFrontage:0:None --dedup-train
```
> **→ Kết quả đầu ra:** `01_data/processed/{preprocessor.joblib, preprocess_meta.json, processed_train.csv, processed_val.csv, processed_test.csv}` — 1020 train / 219 val / 219 test dòng, 205 đặc trưng (49 số + 22 hạng mục one-hot).

## Bước 10 — Kiểm chứng không rò rỉ dữ liệu
```bash
python 03_src/scripts/p5_tien_xu_ly/preprocess_tabular.py check --split-csv 01_data/splits/split_v1_prepped.csv --out-dir 01_data/processed
```
> **→ Kết quả mong đợi:** `KIỂM CHỨNG: PASSED (bộ tiền xử lý chỉ học từ train)`
