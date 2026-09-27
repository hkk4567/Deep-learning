# Model Card — House Price Ridge Regression

## Mục đích sử dụng
Dự đoán `SalePrice` (giá bán, USD) của nhà ở tại Ames, Iowa dựa trên 71 đặc trưng mô tả căn nhà. Xây dựng cho mục đích **đồ án học tập**, không dùng cho quyết định tài chính/định giá thực tế.

**Ngoài phạm vi:** không dùng để định giá nhà ngoài khu vực Ames, Iowa; không dùng cho giao dịch thời điểm ngoài 2006–2010; không phù hợp cho nhà có `SaleCondition` bất thường (xem hạn chế).

## Dữ liệu huấn luyện
- Ames Housing / Kaggle House Prices, 1460 dòng gốc, còn 1458 sau loại 2 ngoại lai đã biết (FND-0003).
- Chia 70/15/15 (train 1020 / val 219 / test 219), ngẫu nhiên seed=42, không stratify được (nhãn liên tục).
- Thiên lệch tiềm ẩn: chỉ 1 thành phố (Ames), 1 giai đoạn thời gian (2006–2010), không đại diện thị trường hiện tại hay khu vực khác.

## Đặc trưng đầu vào và tiền xử lý bắt buộc
71 đặc trưng thô (xem `03_src/scripts/p4_kham_pha_du_lieu/select_features.py`) →
1. `encode_business_rules.py`: ordinal-encode 18 cột chất lượng, điền 0 cho `MasVnrArea`/`GarageYrBlt` khi thiếu.
2. `preprocessor.joblib` (`01_data/processed/`): median-impute `LotFrontage`, one-hot 22 cột nominal, chuẩn hóa 49 cột số.
3. `final_model_ridge.joblib`: dự đoán trên `log1p(SalePrice)` → lấy `expm1()` để ra giá thật.

Script suy luận đầy đủ, độc lập: `03_src/scripts/p10_dong_goi/predict_from_raw.py` — nhận CSV thô (schema như `00_raw/train.csv`), tự chạy đủ 3 bước trên.

## Metric và kết quả
| Tập | RMSLE | MAE | R² |
|---|---|---|---|
| Val | 0.1155 (bootstrap 95% CI: [0.089, 0.145]) | $13,197 | 0.950 |
| **Test (mở đúng 1 lần)** | **0.1301** (95% CI: [0.099, 0.159]) | $14,280 | 0.943 |

## Hạn chế đã biết
- **Yếu với giao dịch bất thường**: `SaleCondition` = Abnorml (bán gấp/khó khăn tài chính) hoặc Partial (nhà mới xây) — sai số cao hơn hẳn mức trung bình (FND-0006, còn Open). Ví dụ cực đoan: nhà giá $34,900 (rẻ nhất dataset, bán gấp) bị lệch 131%.
- Test chỉ 219 mẫu → khoảng tin cậy bootstrap khá rộng, kết quả điểm có thể dao động khi áp dụng dữ liệu mới.
- 18 cột ordinal dùng bảng ánh xạ cố định (`ORDINAL_WITH_NA`/`ORDINAL_NO_NA` trong `encode_business_rules.py`) — nếu dữ liệu mới có mức giá trị ngoài bảng này, script sẽ báo lỗi thay vì âm thầm sai.
- Vài mức hạng mục hiếm (`RoofMatl=Roll`, `Exterior1st=Stone/Stone`, `Electrical=Mix`) không xuất hiện ở train → tự động mã hóa thành vector 0, có thể giảm độ chính xác cho các nhà hiếm gặp này.

## Rủi ro và cách giảm thiểu
- **Rủi ro**: áp dụng ngoài phạm vi (nhà ở nơi khác, thời điểm khác) → dự đoán không đáng tin cậy. **Giảm thiểu**: chỉ dùng trong phạm vi Ames/2006-2010 hoặc huấn luyện lại với dữ liệu mới.
- **Rủi ro**: dựa vào dự đoán cho nhà có hoàn cảnh bán bất thường → sai số cao. **Giảm thiểu**: gắn cờ cảnh báo khi `SaleCondition != Normal`, xem xét thủ công.

## Phiên bản, ngày, người chịu trách nhiệm
- Ngày chốt: 2026-09-26 (theo log `07_logs/change_log.xlsx`, EXP-0004).
- Mô hình: `sklearn.linear_model.Ridge(alpha=30)`, scikit-learn 1.8.0 (xem `requirements.txt`).
- Thực hiện: Claude (AI), theo yêu cầu của Huỳnh Kiện Khải.
- Dataset fingerprint: SHA256 train đã xử lý = `cc5da2c468bf...` (xem `01_data/processed/final_model_meta.json`).
