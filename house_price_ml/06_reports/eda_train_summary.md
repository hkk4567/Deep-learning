# EDA (chỉ trên train) - tóm tắt

Nguồn: `01_data/splits/split_v1.csv`, lọc `split=='train'` (1022 dòng). Log tham chiếu: LOG-0020, LOG-0021, FND-0003.

## Phân phối SalePrice
- Lệch phải mạnh: skew = 1.73 → log1p(SalePrice) skew = 0.15 (gần chuẩn) → xác nhận log-transform là đúng hướng.

## Missing (khớp với audit toàn bộ ở P1, không lệch phân bố theo split)
PoolQC 99.4%, MiscFeature 96.0%, Alley 93.4%, Fence 80.2%, MasVnrType 59.2%, FireplaceQu 47.1%, LotFrontage 18.4%, nhóm Garage*/Bsmt* 5.2%.

## Tương quan cao nhất với SalePrice
OverallQual (0.79), GrLivArea (0.69), GarageCars (0.64), GarageArea (0.62), TotalBsmtSF (0.59).

## Phát hiện quan trọng: 2 điểm ngoại lai đã biết (FND-0003, mức High)
Id=524 và Id=1299: GrLivArea rất lớn (4676, 5642 sqft), OverallQual=10, nhưng SalePrice rất thấp (184750, 160000) vì `SaleCondition='Partial'` (nhà bán khi chưa xây xong). Đây là lỗi/ngoại lai nổi tiếng của dataset Ames Housing, tác giả dataset khuyến nghị loại khỏi train. Id=1183 (SalePrice=745000) là điểm hợp lệ, giữ lại.

## Quyết định (DECISION, log LOG-0021)
- Loại Id=524, Id=1299 khỏi train khi fit mô hình (P4/P5).
- Impute nhóm cột "missing có ý nghĩa" bằng "None"/0, không dùng median/mode mặc định.

Xem hình: `02_notebooks/eda_train.png`.
