# Từ điển Dữ liệu: Giá Nhà (House Pricing)

Tài liệu này giải thích chi tiết các biến (cột) trong tập dữ liệu, được chia thành 14 nhóm chính.

---

## 1. Thông tin chung về khu đất

| Cột | Giải thích dễ hiểu | Ví dụ |
| :--- | :--- | :--- |
| **MSSubClass** | Mã phân loại loại công trình/nhà ở | 20, 60, 120 |
| **MSZoning** | Phân loại quy hoạch khu vực mà căn nhà nằm trong | RL = Residential Low Density |
| **LotFrontage** | Chiều dài mặt tiền của mảnh đất tiếp giáp đường | 80 feet |
| **LotArea** | Diện tích mảnh đất | 10,000 ft² |
| **Street** | Loại đường mà nhà tiếp giáp | Pave, Grvl |
| **Alley** | Có đường hẻm phía sau/bên cạnh và loại gì | Grvl, Pave, NA |
| **LotShape** | Hình dạng mảnh đất | Reg = đều, IR1 = hơi không đều |
| **LandContour** | Địa hình của khu đất | Lvl = bằng phẳng |
| **Utilities** | Các tiện ích công cộng có sẵn | điện, nước, gas... |
| **LotConfig** | Cách bố trí mảnh đất | Inside, Corner, CulDSac |
| **LandSlope** | Độ dốc của mảnh đất | Gtl = dốc nhẹ |

**Ví dụ:**
Một căn nhà có:
*   `LotFrontage = 80`
*   `LotArea = 12000`
*   `LotShape = Reg`
*   `LandContour = Lvl`

> **Có thể hiểu:** Mảnh đất có mặt tiền 80 feet, diện tích 12.000 ft², hình dạng tương đối đều và địa hình bằng phẳng.

---

## 2. Vị trí và khu vực

| Cột | Giải thích |
| :--- | :--- |
| **Neighborhood** | Khu dân cư nơi căn nhà nằm |
| **Condition1** | Nhà có gần đường chính, đường sắt... hay không |
| **Condition2** | Điều kiện/proximity thứ hai nếu có |
| **BldgType** | Loại hình nhà |
| **HouseStyle** | Kiểu thiết kế nhà |

*   **Neighborhood**: Đây là một cột rất quan trọng. Vị trí thường ảnh hưởng mạnh đến giá nhà.
    *   Ví dụ: `Neighborhood = CollgCr` (nghĩa là căn nhà nằm trong một khu dân cư cụ thể).
*   **Condition1 & Condition2**: 
    *   `Condition1 = Norm` → không có ảnh hưởng đặc biệt.
    *   `Condition1 = Artery` → gần đường lớn.
    *   Ví dụ kết hợp: `Condition1 = Artery` và `Condition2 = Feedr` (nghĩa là nhà vừa gần đường lớn vừa gần một loại đường khác).

---

## 3. Chất lượng và tình trạng căn nhà
*(Đây là nhóm rất quan trọng khi dự đoán giá)*

| Cột | Ý nghĩa |
| :--- | :--- |
| **OverallQual** | Chất lượng tổng thể vật liệu và hoàn thiện |
| **OverallCond** | Tình trạng tổng thể của căn nhà |
| **YearBuilt** | Năm xây dựng |
| **YearRemodAdd** | Năm sửa chữa/cải tạo gần nhất |

*   **OverallQual**: Thường có giá trị từ khoảng 1 → 10. Điểm quan trọng là nó đánh giá *chất lượng*, không phải tuổi nhà.
    *   `OverallQual = 9` → chất lượng rất cao.
    *   `OverallQual = 4` → chất lượng thấp hơn.
*   **OverallCond**: Đánh giá tình trạng hiện tại của căn nhà.
    *   Ví dụ: `OverallQual = 8` và `OverallCond = 5`
    *   > **Có thể hiểu:** Nhà được xây bằng vật liệu/chất lượng tốt nhưng tình trạng hiện tại ở mức trung bình.
*   **YearBuilt & YearRemodAdd**:
    *   `YearBuilt = 2005` → xây năm 2005.
    *   `YearBuilt = 1980` & `YearRemodAdd = 2010` → xây năm 1980 nhưng được cải tạo vào năm 2010.

---

## 4. Mái và ngoại thất

| Cột | Giải thích |
| :--- | :--- |
| **RoofStyle** | Kiểu mái |
| **RoofMatl** | Vật liệu mái |
| **Exterior1st** | Vật liệu ngoại thất chính |
| **Exterior2nd** | Vật liệu ngoại thất thứ hai |
| **MasVnrType** | Loại lớp ốp đá/gạch trang trí bên ngoài |
| **MasVnrArea** | Diện tích lớp ốp đó |
| **ExterQual** | Chất lượng vật liệu bên ngoài |
| **ExterCond** | Tình trạng hiện tại của vật liệu bên ngoài |

**Ví dụ:**
*   `RoofStyle = Gable`
*   `RoofMatl = CompShg`
*   `Exterior1st = VinylSd`
*   `ExterQual = Gd`
> **Có thể hiểu:** Nhà có mái kiểu Gable, vật liệu mái dạng composite shingles, ngoại thất vinyl và chất lượng ngoại thất tốt.

---

## 5. Nền móng và tầng hầm
*(Đây là nhóm rất dễ bị nhầm)*

| Cột | Giải thích |
| :--- | :--- |
| **Foundation** | Loại móng nhà |
| **BsmtQual** | Chất lượng/độ cao tầng hầm |
| **BsmtCond** | Tình trạng tầng hầm |
| **BsmtExposure** | Mức độ tiếp xúc với bên ngoài của tầng hầm |
| **BsmtFinType1** | Kiểu hoàn thiện khu vực tầng hầm loại 1 |
| **BsmtFinSF1** | Diện tích tầng hầm hoàn thiện loại 1 |
| **BsmtFinType2** | Kiểu hoàn thiện loại 2 |
| **BsmtFinSF2** | Diện tích hoàn thiện loại 2 |
| **BsmtUnfSF** | Diện tích tầng hầm chưa hoàn thiện |
| **TotalBsmtSF** | Tổng diện tích tầng hầm |

*   **BsmtQual** (Đánh giá chất lượng tầng hầm): `Ex` = Excellent, `Gd` = Good, `TA` = Typical, `Fa` = Fair, `Po` = Poor, `NA` = No Basement.
*   **BsmtExposure** (Mức độ tầng hầm có cửa sổ/lối tiếp xúc với bên ngoài): 
    *   `Gd` (tiếp xúc khá tốt), `Av` (trung bình), `Mn` (ít), `No` (không có).
*   **Diện tích (SF)**: `BsmtFinSF1` và `BsmtFinSF2` là diện tích đã hoàn thiện.
    *   Ví dụ: `BsmtFinSF1 = 500`, `BsmtFinSF2 = 200`, `BsmtUnfSF = 300`
    *   > `TotalBsmtSF = 500 + 200 + 300 = 1000`

---

## 6. Hệ thống trong nhà

| Cột | Ý nghĩa |
| :--- | :--- |
| **Heating** | Hệ thống sưởi |
| **HeatingQC** | Chất lượng/tình trạng hệ thống sưởi |
| **CentralAir** | Có điều hòa trung tâm không |
| **Electrical** | Hệ thống điện |

**Ví dụ về CentralAir:**
*   `CentralAir = Y` → có điều hòa trung tâm.
*   `CentralAir = N` → không có.

---

## 7. Diện tích và không gian sinh hoạt
*(Đây là nhóm rất quan trọng để dự đoán giá)*

| Cột | Giải thích |
| :--- | :--- |
| **1stFlrSF** | Diện tích tầng 1 |
| **2ndFlrSF** | Diện tích tầng 2 |
| **LowQualFinSF** | Diện tích hoàn thiện nhưng chất lượng thấp |
| **GrLivArea** | Tổng diện tích sinh hoạt phía trên mặt đất |

**Ví dụ:**
Nếu `1stFlrSF = 1000` và `2ndFlrSF = 500`, thì thường `GrLivArea ≈ 1500`.
> **Lưu ý:** Đây là một biến rất dễ hiểu: Nhà càng có nhiều diện tích sinh hoạt thì thường giá càng cao.

---

## 8. Phòng tắm và phòng ngủ

| Cột | Ý nghĩa |
| :--- | :--- |
| **BsmtFullBath** | Số phòng tắm đầy đủ ở tầng hầm |
| **BsmtHalfBath** | Số phòng tắm một phần ở tầng hầm |
| **FullBath** | Số phòng tắm đầy đủ phía trên mặt đất |
| **HalfBath** | Số phòng tắm một phần phía trên mặt đất |
| **Bedroom** | Số phòng ngủ |
| **Kitchen** | Số phòng bếp |
| **KitchenQual** | Chất lượng bếp |
| **TotRmsAbvGrd** | Tổng số phòng phía trên mặt đất, không tính phòng tắm |

**Full Bath vs Half Bath:**
*   **FullBath:** Thường có toilet + lavabo + bồn tắm/vòi sen.
*   **HalfBath:** Có toilet + lavabo, nhưng không có bồn tắm/vòi sen đầy đủ.
*   Ví dụ: `FullBath = 2`, `HalfBath = 1` → có 2 phòng tắm đầy đủ và 1 phòng tắm một phần.

---

## 9. Chức năng và lò sưởi/lò sưởi trang trí

| Cột | Ý nghĩa |
| :--- | :--- |
| **Functional** | Mức độ hoạt động/chức năng của căn nhà |
| **Fireplaces** | Số lượng lò sưởi |
| **FireplaceQu** | Chất lượng lò sưởi |

**Ví dụ:**
*   `Fireplaces = 2`, `FireplaceQu = Gd` → nhà có 2 lò sưởi, chất lượng ở mức tốt.

---

## 10. Garage

| Cột | Ý nghĩa |
| :--- | :--- |
| **GarageType** | Vị trí/loại garage |
| **GarageYrBlt** | Năm xây garage |
| **GarageFinish** | Mức độ hoàn thiện bên trong |
| **GarageCars** | Sức chứa garage, số xe |
| **GarageArea** | Diện tích garage |
| **GarageQual** | Chất lượng garage |
| **GarageCond** | Tình trạng garage |

**Ví dụ:**
*   `GarageCars = 2`, `GarageArea = 550` → garage chứa khoảng 2 xe, diện tích 550 ft².

> ⚠️ **Lưu ý rất quan trọng:** Một số nhà không có garage. Khi đó những cột liên quan có thể có giá trị `NaN` (ví dụ: `GarageType = NaN`, `GarageYrBlt = NaN`, `GarageFinish = NaN`). Đây không nhất thiết là "dữ liệu lỗi". Nó mang ý nghĩa: **Nhà không có garage**.

---

## 11. Đường xe vào nhà

| Cột | Giải thích |
| :--- | :--- |
| **PavedDrive** | Tình trạng lát đường xe vào nhà |

**Ví dụ:** Có thể hiểu đại khái qua các mã:
*   `Y`: đã lát hoàn toàn
*   `P`: lát một phần
*   `N`: chưa lát

---

## 12. Khu vực ngoài trời

| Cột | Ý nghĩa |
| :--- | :--- |
| **WoodDeckSF** | Diện tích sàn gỗ ngoài trời |
| **OpenPorchSF** | Diện tích hiên mở |
| **EnclosedPorch** | Diện tích hiên được bao kín |
| **3SsnPorch** | Hiên sử dụng trong 3 mùa |
| **ScreenPorch** | Hiên có lưới chắn |
| **PoolArea** | Diện tích hồ bơi |
| **PoolQC** | Chất lượng hồ bơi |
| **Fence** | Chất lượng hàng rào |

**Ví dụ:**
*   `WoodDeckSF = 200`, `OpenPorchSF = 100` → nhà có 200 ft² sàn gỗ và 100 ft² hiên mở.

---

## 13. Tiện ích đặc biệt

| Cột | Giải thích |
| :--- | :--- |
| **MiscFeature** | Tính năng đặc biệt không thuộc các nhóm trên |
| **MiscVal** | Giá trị tiền của tính năng đó |

**Ví dụ:** `MiscFeature` có thể chứa một loại công trình/phần bổ sung đặc biệt.
*   `MiscFeature = Shed`, `MiscVal = 500` → có một tiện ích phụ (nhà kho nhỏ) và giá trị được ghi nhận là 500 USD.

---

## 14. Thông tin giao dịch
*(Nhóm này rất quan trọng vì nó cho biết khi nào và bằng cách nào căn nhà được bán)*

| Cột | Ý nghĩa |
| :--- | :--- |
| **MoSold** | Tháng bán |
| **YrSold** | Năm bán |
| **SaleType** | Loại giao dịch |
| **SaleCondition** | Điều kiện giao dịch |