# Định nghĩa bài toán (P2)

Ngày chốt: 2026-09-22 (dòng log tham chiếu: LOG-0003, LOG-0004, LOG-0005)

## Bài toán
- **Loại**: Hồi quy (regression) trên dữ liệu bảng (tabular).
- **Đầu vào**: 79 đặc trưng mô tả một căn nhà (Ames Housing) — 36 numeric, 43 categorical (xem `01_data/audit/data_report.md`).
- **Đầu ra**: `SalePrice` (USD) — giá bán dự đoán của căn nhà.
- **Mục đích sử dụng**: đồ án học tập (không triển khai production).

## Metric
- **Metric chính**: RMSLE — RMSE tính trên `log1p(SalePrice)`. Đây là metric chuẩn của bài toán Kaggle House Prices, phù hợp vì `SalePrice` lệch phải mạnh (skew ≈ 1.88) và RMSLE phạt tương đối (theo %) thay vì tuyệt đối, hợp lý khi nhà rẻ và nhà đắt cùng tồn tại.
- **Metric phụ**: MAE ($, dễ diễn giải theo đơn vị tiền thật), R² (mức giải thích phương sai).
- **Tiêu chí thành công đo được**: mô hình cuối phải vượt baseline tầm thường (dự đoán bằng trung bình/trung vị train) một khoảng có ý nghĩa, và RMSLE trên test nằm trong khoảng cùng bậc với các lời giải công khai cho dataset này (tham khảo, không phải mục tiêu cứng vì đây là đồ án học tập).

## Mô hình
- **Không dùng Deep Learning** (quyết định tường minh của người dùng — LOG-0003). Theo đúng nguyên tắc #8 của skill (dữ liệu bảng nhỏ/vừa → gradient boosting thường thắng DL), pipeline dùng scikit-learn (Ridge, Lasso, RandomForest, GradientBoosting) và XGBoost làm ứng viên chính.

## Ràng buộc
- Phần cứng người dùng: CPU Intel i5-12400F, GPU RTX5060. Vì không dùng DL nên **không cần GPU** cho dự án này; toàn bộ pipeline chạy trên CPU, dự kiến dưới 5 phút.
- Không có ràng buộc độ trễ suy luận hay kích thước mô hình (không triển khai thực tế).

## Rủi ro và giả định
- Dataset có 19 cột missing, phần lớn là "missing có ý nghĩa" (nhà không có đặc điểm đó) — đã ghi FINDING FND-0001, sẽ xử lý ở bước tiền xử lý (P5), không dùng median/mode mặc định cho nhóm này.
- `SalePrice` là biến liên tục gần như toàn giá trị duy nhất → không thể stratify khi chia split; đã dùng chia ngẫu nhiên có seed cố định thay thế (FND-0002, Wontfix — chấp nhận được cho hồi quy).
- Dữ liệu chỉ có 1460 dòng (nhỏ) → nguy cơ overfit với mô hình phức tạp; sẽ dùng cross-validation ở bước baseline/thí nghiệm để kiểm soát.
- Không có thông tin về thời điểm bán nhà theo chuỗi thời gian thực (chỉ có `YrSold`/`MoSold` dạng cột), nên không chia theo thời gian.
