# Quy trình chạy lại toàn bộ pipeline (P0 → P11)

Toàn bộ lệnh dưới đây chạy từ thư mục gốc `house_price_ml/`, theo đúng thứ tự, cho ra kết quả giống hệt (các bước tất định — seed=42 cố định, Ridge không có yếu tố ngẫu nhiên — nên tái lập chính xác, đã tự kiểm chứng ở P10).

## Bước 0 — Cài môi trường (nếu chưa làm)
```bash
setup_env.bat
```

## Bước 1 — Kiểm toán dữ liệu (P1)
```bash
python 03_src/scripts/p1_kiem_toan_du_lieu/audit_dataset.py --raw 00_raw --out 01_data/audit --label-col SalePrice
```
> **→** `01_data/audit/{manifest.csv, duplicates.csv, audit.json, data_report.md}`

## Bước 2 — Chia train/val/test (P3)
```bash
python 03_src/scripts/p3_chia_du_lieu/make_splits.py --table 00_raw/train.csv --out 01_data/splits --version v1 --id-col Id --label-col SalePrice --val 0.15 --test 0.15 --seed 42
```
> **→** `01_data/splits/{split_v1.csv, split_v1_summary.json}`

## Bước 3 — EDA thủ công ban đầu (chỉ trên tập train)
```bash
python 03_src/scripts/p4_kham_pha_du_lieu/eda_train.py
```
> **→** `02_notebooks/eda_train.png`

## Bước 4 — Lọc 71 đặc trưng đã chọn
```bash
python 03_src/scripts/p4_kham_pha_du_lieu/select_features.py
```
> **→** `01_data/splits/split_v1_selected_features.csv`

## Bước 5 — EDA chính thức trên 71 đặc trưng đã chọn
```bash
python 03_src/scripts/p4_kham_pha_du_lieu/explore_tabular.py --split-csv 01_data/splits/split_v1_selected_features.csv --out-dir 06_reports/eda --label-col SalePrice --label-type numeric --id-col Id --ordinal-cols ExterQual,ExterCond,BsmtQual,BsmtCond,BsmtExposure,BsmtFinType1,BsmtFinType2,HeatingQC,KitchenQual,Functional,GarageFinish,GarageQual,GarageCond,PavedDrive,LandSlope,LotShape,Utilities,FireplaceQu --valid-range LotFrontage:0:None MasVnrArea:0:None GarageYrBlt:1800:2026
```
> **→** `06_reports/eda/{eda_report.md, eda.json, eda_plots/*.png}`

## Bước 6 — EDA đối chiếu trên toàn bộ 79 cột gốc
```bash
python 03_src/scripts/p4_kham_pha_du_lieu/explore_tabular.py --split-csv 01_data/splits/split_v1.csv --out-dir 06_reports/eda_full --label-col SalePrice --label-type numeric --id-col Id --ordinal-cols ExterQual,ExterCond,BsmtQual,BsmtCond,BsmtExposure,BsmtFinType1,BsmtFinType2,HeatingQC,KitchenQual,Functional,GarageFinish,GarageQual,GarageCond,PavedDrive,LandSlope,LotShape,Utilities,PoolQC,FireplaceQu,Fence --valid-range LotFrontage:0:None MasVnrArea:0:None GarageYrBlt:1800:2026
```
> **→** `06_reports/eda_full/{eda_report.md, eda.json}` — phát hiện thêm `Fireplaces`, `FireplaceQu`, `WoodDeckSF`, `OpenPorchSF` (FND-0004), dẫn tới Bước 4 được chạy lại với 71 cột (đã gồm 4 cột này).

## Bước 7 — Vẽ 9 biểu đồ theo nhóm
```bash
python 03_src/scripts/p4_kham_pha_du_lieu/eda_group_plots.py
```
> **→** `06_reports/eda/eda_plots/by_group/N1...N9.png` (script tự tạo thư mục output)

## Bước 8 — Áp quy tắc nghiệp vụ cố định (P5)
```bash
python 03_src/scripts/p5_tien_xu_ly/encode_business_rules.py
```
> **→** `01_data/splits/split_v1_prepped.csv` (1458 dòng × 74 cột — đã loại 2 outlier Id=524,1299; ordinal-encode 18 cột; điền 0 cho MasVnrArea/GarageYrBlt)

## Bước 9 — Tiền xử lý chính thức (P5, fit trên train)
```bash
python 03_src/scripts/p5_tien_xu_ly/preprocess_tabular.py fit \
  --split-csv 01_data/splits/split_v1_prepped.csv --out-dir 01_data/processed \
  --label-col SalePrice --label-type numeric --id-col Id \
  --impute median --scaler standard --valid-range LotFrontage:0:None --dedup-train
```
> **→** `01_data/processed/{preprocessor.joblib, preprocess_meta.json, processed_train/val/test.csv}` — 1020/219/219 dòng, 205 đặc trưng

## Bước 10 — Kiểm chứng không rò rỉ dữ liệu
```bash
python 03_src/scripts/p5_tien_xu_ly/preprocess_tabular.py check --split-csv 01_data/splits/split_v1_prepped.csv --out-dir 01_data/processed
```
> **→ Kết quả mong đợi:** `KIỂM CHỨNG: PASSED (bộ tiền xử lý chỉ học từ train)`

## Bước 11 — Baseline: tầm thường + XGBoost mặc định (P6, EXP-0001/0002)
```bash
python 03_src/scripts/p6_baseline/baseline.py
```
> **→** `05_experiments/baseline_metrics.json` — RMSLE val: hằng số=0.4060, XGBoost=0.1267

## Bước 12 — Baseline: Linear Regression (P6, EXP-0003)
```bash
python 03_src/scripts/p6_baseline/linear_regression_baseline.py
```
> **→** `05_experiments/{linear_regression_metrics.json, linear_regression_coefficients.csv}` — RMSLE val=0.1143 (lưu ý: hệ số không ổn định, xem model_card.md)

## Bước 13 — Baseline: Ridge Regression — MÔ HÌNH CUỐI (P6, EXP-0004)
```bash
python 03_src/scripts/p6_baseline/ridge_baseline.py
```
> **→** `05_experiments/{ridge_metrics.json, ridge_coefficients.csv}` — RMSLE val=0.1155, alpha=30 (chọn bằng CV trên train)

## Bước 14 — Thí nghiệm: tinh chỉnh siêu tham số XGBoost (P8, EXP-0005)
```bash
python 03_src/scripts/p8_thi_nghiem/exp005_xgb_tuning.py
```
> **→** `05_experiments/exp005_xgb_tuning_metrics.json` — RMSLE val=0.1245 (cải thiện so với XGBoost mặc định nhưng vẫn kém Ridge)

## Bước 15 — Đánh giá cuối trên val (Bootstrap CI, chưa mở test)
```bash
python 03_src/scripts/p9_danh_gia_cuoi/final_eval.py
```
> **→** `05_experiments/exp0004_val_bootstrap.json` — RMSLE val bootstrap 95% CI=[0.089, 0.145]

## Bước 16 — Mở test, đánh giá cuối (P9, CHỈ CHẠY ĐÚNG 1 LẦN)
```bash
python 03_src/scripts/p9_danh_gia_cuoi/final_eval.py --open-test
```
> **→** `05_experiments/{exp0004_test_FINAL.json, exp0004_test_predictions.csv}` — **RMSLE test=0.1301**, MAE=$14,280, R²=0.943

## Bước 17 — Lưu checkpoint mô hình cuối (P10)
```bash
python 03_src/scripts/p10_dong_goi/save_final_model.py
```
> **→** `01_data/processed/{final_model_ridge.joblib, final_model_meta.json}`

## Bước 18 — Suy luận độc lập trên dữ liệu thô (P10)
```bash
python 03_src/scripts/p10_dong_goi/predict_from_raw.py --input 00_raw/train.csv --output /tmp/pred.csv --sample-ids 1,7,191,496,886
```
> **→** Dự đoán `SalePrice` cho các Id chỉ định, chạy độc lập hoàn toàn với pipeline train (dùng để kiểm chứng đầu-cuối ở cổng G8).

---

**Log đầy đủ mọi lệnh, kết quả, quyết định, phát hiện:** `07_logs/change_log.xlsx` (sheet `Change_Log`, `Findings`, `Experiments`).
**Báo cáo tổng hợp:** `06_reports/final_report.md`. **Model card:** `06_reports/model_card.md`.
