# house_price_ml

Nguoi thuc hien: Huynh Kien Khai
Du an ML (khong Deep Learning) du doan SalePrice tu dataset bang (Ames Housing). Cau truc:

| Thu muc | Noi dung |
|---|---|
| 00_raw | Dataset goc, chi doc, khong sua |
| 01_data | audit/ (manifest, bao cao du lieu), splits/ (file chia), processed/ |
| 02_notebooks | EDA, phan tich loi |
| 03_src | Ma nguon (data, models, train, evaluate, predict) |
| 04_configs | YAML cho tung thi nghiem |
| 05_experiments | Ket qua tung thi nghiem (config, metrics.csv, checkpoint) |
| 06_reports | data_report, experiment_summary, final_report, model_card |
| 07_logs | change_log.xlsx (Change_Log, Findings, File_Registry, Experiments, Summary) |
| 08_backups | Ban sao truoc moi lan sua file |

Tai lap: xem `06_reports/final_report.md` muc "Cach chay lai".

## Cấu trúc 03_src/scripts/ (sắp xếp theo bước)

```
03_src/scripts/
├── chung/                    # Dùng xuyên suốt mọi bước
│   └── log_change.py
├── p0_khoi_tao/
│   └── scaffold_project.py
├── p1_kiem_toan_du_lieu/
│   └── audit_dataset.py
├── p3_chia_du_lieu/
│   └── make_splits.py
├── p4_kham_pha_du_lieu/
│   ├── eda_train.py          # EDA thủ công ban đầu
│   ├── select_features.py    # Lọc 71 đặc trưng đã chọn
│   ├── explore_tabular.py    # EDA chính thức (script chuẩn của skill)
│   └── eda_group_plots.py    # Vẽ biểu đồ theo 9 nhóm
└── p5_tien_xu_ly/
    ├── encode_business_rules.py  # Quy tắc cố định: ordinal encode, fill 0, loại outlier
    └── preprocess_tabular.py     # Tiền xử lý chính thức (fit/check), script chuẩn của skill
```
