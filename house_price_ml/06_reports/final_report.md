# Báo cáo cuối — Dự đoán giá nhà (Ames Housing, ML không DL)

## 1. Tóm tắt
Bài toán hồi quy dự đoán `SalePrice` từ 79 đặc trưng nhà (Ames Housing, Kaggle House Prices), thu hẹp còn 71 đặc trưng được chọn có căn cứ EDA. Mô hình cuối: **Ridge Regression (alpha=30)** trên 205 cột sau one-hot/ordinal encode. Kết quả **test (mở đúng 1 lần): RMSLE = 0.1301** (MAE ≈ $14,280, R² = 0.943), vượt xa baseline tầm thường (RMSLE 0.406) và tốt hơn XGBoost đã tune (0.1245). Giới hạn chính: dự đoán kém hơn rõ rệt với nhà bán trong điều kiện bất thường (`SaleCondition` ≠ Normal).

## 2. Dữ liệu
- Nguồn: `train.csv` (Kaggle House Prices/Ames Housing), người dùng tải lên. 1460 dòng, 81 cột gốc.
- Làm sạch: loại 2 dòng ngoại lai đã biết của dataset (`Id=524, Id=1299` — nhà `SaleCondition=Partial`, diện tích cực lớn nhưng giá bất thường thấp; xem FND-0003), còn 1458 dòng dùng cho split.
- Chia: `make_splits.py`, ngẫu nhiên (không stratify được vì nhãn liên tục), seed=42, tỉ lệ 70/15/15 → train 1020 (sau loại outlier)/val 219/test 219 dòng. File: `01_data/splits/split_v1.csv`.
- Dataset fingerprint (SHA256, từ `01_data/audit/audit.json`): `74d13bc3f7...` (xem file đầy đủ).
- Không có cấu trúc nhóm ngầm (mỗi dòng là 1 giao dịch nhà độc lập).

## 3. Đặc trưng và EDA (chỉ trên train)
71 đặc trưng được người dùng chọn lọc theo 9 nhóm nghiệp vụ, đối chiếu bằng EDA toàn bộ 79 cột (`06_reports/eda_full/`) và bổ sung 4 cột có tín hiệu bị bỏ sót (`Fireplaces`, `FireplaceQu`, `WoodDeckSF`, `OpenPorchSF` — FND-0004). Phát hiện chính: `SalePrice` lệch phải (skew 1.73 → log1p còn 0.15); top tương quan `OverallQual` (0.79), `GrLivArea` (0.69); 19 cột missing phần lớn "missing có ý nghĩa" (FND-0001); 3 cụm cộng tuyến rõ (GrLivArea/FullBath/TotRmsAbvGrd, GarageCars/GarageArea, TotalBsmtSF/BsmtUnfSF/BsmtFinSF1).

## 4. Tiền xử lý (P5)
- Quy tắc cố định (`encode_business_rules.py`): Ordinal encode 18 cột chất lượng (Po<Fa<TA<Gd<Ex...); điền 0 cho `MasVnrArea`/`GarageYrBlt` khi thiếu; loại 2 outlier.
- Học từ train (`preprocess_tabular.py fit`): median-impute `LotFrontage`; one-hot 22 cột nominal; chuẩn hóa (StandardScaler) toàn bộ 49 cột số. Kiểm chứng **PASSED** — không rò rỉ.

## 5. Baseline và các thí nghiệm

| Exp_ID | Model | RMSLE (val) | Ghi chú |
|---|---|---|---|
| EXP-0001 | Hằng số = trung bình train | 0.4060 | Sàn dưới cùng |
| EXP-0002 | XGBoost mặc định | 0.1267 | Baseline cổ điển |
| EXP-0003 | Linear Regression (không regularization) | 0.1143 | Hệ số không ổn định (bị mức hạng mục hiếm chi phối) |
| EXP-0004 | **Ridge (alpha=30, chọn bằng CV trên train)** | **0.1155** | **Mô hình cuối — hệ số ổn định, khớp EDA** |
| EXP-0005 | XGBoost đã tune (RandomizedSearchCV) | 0.1245 | Cải thiện so với EXP-0002 nhưng vẫn kém Ridge |

Kết luận vòng thí nghiệm: với 205 đặc trưng đã one-hot/ordinal kỹ trên tập dữ liệu nhỏ (1020 dòng), quan hệ với `log(SalePrice)` chủ yếu tuyến tính — mô hình tuyến tính có regularization thắng thế so với gradient boosting.

## 6. Mô hình cuối và kết quả
- **Mô hình**: `sklearn.linear_model.Ridge(alpha=30)`, fit trên `log1p(SalePrice)`, 205 đặc trưng, seed=42 (không có yếu tố ngẫu nhiên khác vì Ridge tất định).
- **Val**: RMSLE = 0.1155 (bootstrap 1000 lần: mean=0.1148, 95% CI=[0.089, 0.145]).
- **Test (mở đúng 1 lần)**: **RMSLE = 0.1301** (bootstrap mean=0.1274, 95% CI=[0.099, 0.159]), MAE = $14,280, R² = 0.943, n=219.
- So với tiêu chí thành công đã chốt ở `problem_definition.md` ("vượt baseline tầm thường một khoảng có ý nghĩa"): **ĐẠT** — RMSLE giảm từ 0.406 xuống 0.130 (giảm ~68%).
- Test kém hơn val (0.1301 vs 0.1155) nhưng nằm trong khoảng CI chồng lấp nhau → không có dấu hiệu overfit nghiêm trọng lên val qua các thí nghiệm.

## 7. Phân tích lỗi (trên val)
6/10 dự đoán sai nhiều nhất đều có `SaleCondition` khác "Normal" (Abnorml/Partial). Case cực đoan: `Id=496` ($34,900 — rẻ nhất dataset, bán gấp/khó khăn tài chính, 720 sqft) bị lệch 131%. → FND-0006 (Medium, Open): mô hình chưa nắm bắt tốt các giao dịch bất thường (giá bị ảnh hưởng bởi hoàn cảnh bán, không chỉ đặc điểm vật lý căn nhà).

## 8. Hạn chế và rủi ro
- Test chỉ 219 mẫu — khoảng tin cậy bootstrap khá rộng ([0.099, 0.159]), kết quả điểm đơn lẻ có thể dao động.
- Yếu với giao dịch `SaleCondition` bất thường (xem mục 7).
- Dữ liệu chỉ từ Ames, Iowa (2006-2010) — không đảm bảo tổng quát cho thị trường/thời điểm khác.
- Chưa thử stacking Ridge+XGBoost hay feature engineering sâu hơn (interaction terms) — dừng vòng thí nghiệm sau EXP-0005 theo yêu cầu người dùng.
- Test đã mở **đúng 1 lần**, chưa từng dùng để chỉnh mô hình.

## 9. Cách chạy lại
Xem đầy đủ trong `06_reports/quy_trinh_chay_lai.md` (Bước 0–10) và `requirements.txt` (phiên bản thư viện đã ghim). Bước cuối (P9):
```bash
python 03_src/scripts/p9_danh_gia_cuoi/final_eval.py --open-test
```

## 10. Nhật ký
`07_logs/change_log.xlsx`: 66 dòng Change_Log, 6 Findings (3 Done, 1 Wontfix, ~2 Open), 5 Experiments (EXP-0001 → EXP-0005). Finding còn Open: **FND-0006** (phân tích lỗi SaleCondition, mục 7). Không có DECISION nào ở trạng thái Needs-confirmation.

## 11. Việc đã chạy thật vs chưa chạy
| Việc | Trạng thái |
|---|---|
| Audit, split, EDA (train), tiền xử lý | ✔ Chạy thật, kiểm chứng PASSED |
| Baseline tầm thường + cổ điển (XGBoost, Linear, Ridge) | ✔ Chạy thật trên val |
| Tuning XGBoost (EXP-0005) | ✔ Chạy thật (RandomizedSearchCV, 60 iter) |
| Đánh giá cuối trên test | ✔ Chạy thật, đúng 1 lần |
| Stacking / feature engineering sâu hơn | ✘ Chưa làm (dừng theo quyết định người dùng) |
| Đóng gói script suy luận độc lập, model_card.md (P10) | ✘ Chưa làm — bước tiếp theo nếu cần |
