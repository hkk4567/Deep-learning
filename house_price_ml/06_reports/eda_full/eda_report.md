# Báo cáo khám phá dữ liệu (EDA) — chỉ trên train

- Số mẫu (train): **1022**; số thuộc tính (đã loại ID): **79**

## Thang đo từng thuộc tính

| Thuộc tính | Kiểu | Thang đo |
|---|---|---|
| MSSubClass | int64 | tỷ lệ (ratio) |
| MSZoning | str | định danh (nominal) |
| LotFrontage | float64 | tỷ lệ (ratio) |
| LotArea | int64 | tỷ lệ (ratio) |
| Street | str | định danh (nominal) |
| Alley | str | định danh (nominal) |
| LotShape | str | thứ bậc (ordinal) |
| LandContour | str | định danh (nominal) |
| Utilities | str | thứ bậc (ordinal) |
| LotConfig | str | định danh (nominal) |
| LandSlope | str | thứ bậc (ordinal) |
| Neighborhood | str | định danh (nominal) |
| Condition1 | str | định danh (nominal) |
| Condition2 | str | định danh (nominal) |
| BldgType | str | định danh (nominal) |
| HouseStyle | str | định danh (nominal) |
| OverallQual | int64 | tỷ lệ (ratio) |
| OverallCond | int64 | tỷ lệ (ratio) |
| YearBuilt | int64 | tỷ lệ (ratio) |
| YearRemodAdd | int64 | tỷ lệ (ratio) |
| RoofStyle | str | định danh (nominal) |
| RoofMatl | str | định danh (nominal) |
| Exterior1st | str | định danh (nominal) |
| Exterior2nd | str | định danh (nominal) |
| MasVnrType | str | định danh (nominal) |
| MasVnrArea | float64 | tỷ lệ (ratio) |
| ExterQual | str | thứ bậc (ordinal) |
| ExterCond | str | thứ bậc (ordinal) |
| Foundation | str | định danh (nominal) |
| BsmtQual | str | thứ bậc (ordinal) |
| BsmtCond | str | thứ bậc (ordinal) |
| BsmtExposure | str | thứ bậc (ordinal) |
| BsmtFinType1 | str | thứ bậc (ordinal) |
| BsmtFinSF1 | int64 | tỷ lệ (ratio) |
| BsmtFinType2 | str | thứ bậc (ordinal) |
| BsmtFinSF2 | int64 | tỷ lệ (ratio) |
| BsmtUnfSF | int64 | tỷ lệ (ratio) |
| TotalBsmtSF | int64 | tỷ lệ (ratio) |
| Heating | str | định danh (nominal) |
| HeatingQC | str | thứ bậc (ordinal) |
| CentralAir | str | định danh (nominal) |
| Electrical | str | định danh (nominal) |
| 1stFlrSF | int64 | tỷ lệ (ratio) |
| 2ndFlrSF | int64 | tỷ lệ (ratio) |
| LowQualFinSF | int64 | tỷ lệ (ratio) |
| GrLivArea | int64 | tỷ lệ (ratio) |
| BsmtFullBath | int64 | tỷ lệ (ratio) |
| BsmtHalfBath | int64 | tỷ lệ (ratio) |
| FullBath | int64 | tỷ lệ (ratio) |
| HalfBath | int64 | tỷ lệ (ratio) |
| BedroomAbvGr | int64 | tỷ lệ (ratio) |
| KitchenAbvGr | int64 | tỷ lệ (ratio) |
| KitchenQual | str | thứ bậc (ordinal) |
| TotRmsAbvGrd | int64 | tỷ lệ (ratio) |
| Functional | str | thứ bậc (ordinal) |
| Fireplaces | int64 | tỷ lệ (ratio) |
| FireplaceQu | str | thứ bậc (ordinal) |
| GarageType | str | định danh (nominal) |
| GarageYrBlt | float64 | tỷ lệ (ratio) |
| GarageFinish | str | thứ bậc (ordinal) |
| GarageCars | int64 | tỷ lệ (ratio) |
| GarageArea | int64 | tỷ lệ (ratio) |
| GarageQual | str | thứ bậc (ordinal) |
| GarageCond | str | thứ bậc (ordinal) |
| PavedDrive | str | thứ bậc (ordinal) |
| WoodDeckSF | int64 | tỷ lệ (ratio) |
| OpenPorchSF | int64 | tỷ lệ (ratio) |
| EnclosedPorch | int64 | tỷ lệ (ratio) |
| 3SsnPorch | int64 | tỷ lệ (ratio) |
| ScreenPorch | int64 | tỷ lệ (ratio) |
| PoolArea | int64 | tỷ lệ (ratio) |
| PoolQC | str | thứ bậc (ordinal) |
| Fence | str | thứ bậc (ordinal) |
| MiscFeature | str | định danh (nominal) |
| MiscVal | int64 | tỷ lệ (ratio) |
| MoSold | int64 | tỷ lệ (ratio) |
| YrSold | int64 | tỷ lệ (ratio) |
| SaleType | str | định danh (nominal) |
| SaleCondition | str | định danh (nominal) |

> **Lưu ý:** thang đo ở bảng trên suy đoán từ dữ liệu quan sát được (tỷ lệ nếu mọi giá trị ≥ 0); cột có giá trị ngoài miền hợp lệ (mục dưới) có thể bị suy đoán sai thang đo — dựa vào ý nghĩa nghiệp vụ, không chỉ bảng này.

## Biến mục tiêu: `SalePrice`

Phân bố: {'140000': 13, '190000': 11, '110000': 10, '135000': 10, '180000': 9, '115000': 9, '155000': 9, '160000': 8, '185000': 8, '130000': 8, '145000': 8, '143000': 7, '170000': 7, '176000': 7, '120000': 7, '125000': 7, '165000': 7, '250000': 7, '100000': 6, '174000': 6, '127000': 6, '235000': 6, '215000': 6, '139000': 6, '189000': 6, '144000': 6, '200000': 6, '178000': 6, '147000': 6, '129000': 6, '124000': 5, '158000': 5, '112000': 5, '128000': 5, '157000': 5, '230000': 5, '173000': 5, '187500': 5, '239000': 5, '175000': 5, '148000': 5, '127500': 5, '192000': 4, '129900': 4, '320000': 4, '162000': 4, '132000': 4, '108000': 4, '117000': 4, '214000': 4, '141000': 4, '220000': 4, '118000': 4, '180500': 4, '240000': 4, '184000': 4, '87000': 4, '149900': 4, '205000': 4, '181000': 4, '133000': 4, '275000': 4, '168000': 4, '113000': 4, '132500': 4, '109500': 4, '171000': 4, '225000': 3, '137000': 3, '90000': 3, '79000': 3, '191000': 3, '207500': 3, '98000': 3, '197000': 3, '177000': 3, '167500': 3, '154000': 3, '195000': 3, '119000': 3, '116000': 3, '179000': 3, '125500': 3, '136500': 3, '260000': 3, '148500': 3, '165500': 3, '142000': 3, '163000': 3, '280000': 3, '187000': 3, '85000': 3, '105000': 3, '131000': 3, '159500': 3, '93000': 3, '212000': 3, '80000': 3, '137500': 3, '129500': 3, '172500': 3, '118500': 3, '151000': 3, '119500': 3, '201000': 3, '88000': 3, '159000': 3, '290000': 3, '120500': 3, '106000': 3, '130500': 3, '149000': 3, '109900': 3, '106500': 2, '128500': 2, '175500': 2, '228000': 2, '84500': 2, '89500': 2, '219500': 2, '221000': 2, '79900': 2, '177500': 2, '136000': 2, '150000': 2, '60000': 2, '126000': 2, '153500': 2, '197500': 2, '350000': 2, '277000': 2, '142500': 2, '226000': 2, '107000': 2, '167000': 2, '213000': 2, '110500': 2, '176500': 2, '134000': 2, '234000': 2, '345000': 2, '164500': 2, '164000': 2, '95000': 2, '231500': 2, '157500': 2, '270000': 2, '385000': 2, '193000': 2, '192500': 2, '81000': 2, '138000': 2, '272000': 2, '203000': 2, '179900': 2, '188000': 2, '175900': 2, '83000': 2, '224000': 2, '153000': 2, '340000': 2, '204000': 2, '122000': 2, '193500': 2, '186500': 2, '97000': 2, '256000': 2, '91500': 2, '302000': 2, '242000': 2, '157900': 2, '325000': 2, '166000': 2, '104900': 2, '167900': 2, '96500': 2, '222000': 2, '161500': 2, '131500': 2, '152000': 2, '278000': 2, '210000': 2, '82500': 2, '168500': 2, '124500': 2, '55000': 2, '217000': 2, '91000': 2, '107500': 2, '199900': 2, '139400': 2, '196500': 2, '134900': 2, '268000': 2, '237000': 2, '123000': 2, '194500': 2, '119900': 2, '222500': 2, '211000': 1, '138887': 1, '313000': 1, '109000': 1, '202500': 1, '161750': 1, '99500': 1, '213490': 1, '108500': 1, '216000': 1, '111000': 1, '282922': 1, '394432': 1, '383970': 1, '386250': 1, '289000': 1, '149500': 1, '82000': 1, '437154': 1, '150500': 1, '252000': 1, '214500': 1, '287090': 1, '301500': 1, '219210': 1, '193879': 1, '153337': 1, '137450': 1, '251000': 1, '153900': 1, '117500': 1, '145500': 1, '245500': 1, '228500': 1, '274300': 1, '158500': 1, '274725': 1, '555000': 1, '271000': 1, '142125': 1, '233230': 1, '241000': 1, '84900': 1, '184750': 1, '176432': 1, '314813': 1, '158900': 1, '259500': 1, '61000': 1, '245000': 1, '241500': 1, '195400': 1, '103600': 1, '215200': 1, '172785': 1, '178400': 1, '182000': 1, '143500': 1, '214900': 1, '87500': 1, '139900': 1, '430000': 1, '230500': 1, '121000': 1, '141500': 1, '213250': 1, '171900': 1, '165150': 1, '370878': 1, '189950': 1, '179600': 1, '178740': 1, '183200': 1, '159895': 1, '239900': 1, '325300': 1, '438780': 1, '173733': 1, '172400': 1, '116500': 1, '229000': 1, '90350': 1, '333168': 1, '223500': 1, '228950': 1, '119750': 1, '208500': 1, '173900': 1, '204750': 1, '446261': 1, '305900': 1, '238000': 1, '148800': 1, '136900': 1, '194700': 1, '122900': 1, '372500': 1, '315000': 1, '164900': 1, '264561': 1, '146500': 1, '325624': 1, '216837': 1, '361919': 1, '89471': 1, '255500': 1, '133900': 1, '271900': 1, '316600': 1, '85400': 1, '143250': 1, '312500': 1, '105900': 1, '178900': 1, '116900': 1, '315750': 1, '311872': 1, '294000': 1, '85500': 1, '263000': 1, '378500': 1, '128900': 1, '149350': 1, '144900': 1, '262280': 1, '248000': 1, '236500': 1, '265000': 1, '256300': 1, '102000': 1, '164990': 1, '58500': 1, '165600': 1, '206000': 1, '342643': 1, '440000': 1, '208300': 1, '221500': 1, '183000': 1, '185500': 1, '213500': 1, '266500': 1, '98600': 1, '142953': 1, '84000': 1, '372402': 1, '121500': 1, '76000': 1, '139600': 1, '485000': 1, '167240': 1, '229456': 1, '186000': 1, '201800': 1, '37900': 1, '745000': 1, '205950': 1, '217500': 1, '92000': 1, '163500': 1, '285000': 1, '132250': 1, '134500': 1, '135900': 1, '394617': 1, '224900': 1, '197900': 1, '172000': 1, '101800': 1, '159434': 1, '359100': 1, '354000': 1, '216500': 1, '269500': 1, '239686': 1, '162900': 1, '254000': 1, '232000': 1, '226700': 1, '80500': 1, '262500': 1, '176485': 1, '200141': 1, '181500': 1, '146000': 1, '281213': 1, '339750': 1, '307000': 1, '94500': 1, '319000': 1, '266000': 1, '274000': 1, '223000': 1, '274900': 1, '192140': 1, '39300': 1, '185850': 1, '295000': 1, '395000': 1, '66500': 1, '97500': 1, '92900': 1, '212900': 1, '171500': 1, '164700': 1, '151400': 1, '267000': 1, '121600': 1, '106250': 1, '78000': 1, '89000': 1, '324000': 1, '257000': 1, '122500': 1, '310000': 1, '112500': 1, '76500': 1, '319900': 1, '62383': 1, '274970': 1, '381000': 1, '198900': 1, '165400': 1, '402000': 1, '395192': 1, '297000': 1, '377426': 1, '237500': 1, '94750': 1, '328000': 1, '233170': 1, '162500': 1, '118964': 1, '52000': 1, '123500': 1, '475000': 1, '72500': 1, '114504': 1, '377500': 1, '184100': 1, '156932': 1, '309000': 1, '198500': 1, '142600': 1, '102776': 1, '262000': 1, '83500': 1, '119200': 1, '207000': 1, '337000': 1, '336000': 1, '206300': 1, '73000': 1, '258000': 1, '582933': 1, '184900': 1, '163900': 1, '133700': 1, '196000': 1, '156000': 1, '277500': 1, '235128': 1, '98300': 1, '227000': 1, '236000': 1, '116050': 1, '208900': 1, '149300': 1, '185750': 1, '263435': 1, '126175': 1, '239799': 1, '86000': 1, '105500': 1, '202665': 1, '111250': 1, '538000': 1, '128200': 1, '392000': 1, '326000': 1, '126500': 1, '318000': 1, '169000': 1, '227680': 1, '244000': 1, '135960': 1, '101000': 1, '303477': 1, '146800': 1, '163990': 1, '143900': 1, '257500': 1, '465000': 1, '287000': 1, '252678': 1, '124900': 1, '103000': 1, '501837': 1, '147400': 1, '188700': 1, '306000': 1, '218000': 1, '335000': 1, '179540': 1, '169500': 1, '269790': 1, '299800': 1, '286000': 1, '139500': 1, '174500': 1, '392500': 1, '134450': 1, '139950': 1, '143750': 1, '179665': 1, '159950': 1, '194000': 1, '245350': 1, '149700': 1, '138800': 1, '380000': 1, '123600': 1, '136905': 1, '265979': 1, '161000': 1, '153575': 1, '318061': 1, '233000': 1}

## Thống kê mô tả (đã bỏ giá trị thiếu)

| Cột | N | Thiếu | Mean | Median | Mode | Q1 | Q3 | IQR |
|---|---|---|---|---|---|---|---|---|
| MSSubClass | 1022 | 0 | 57.4168 | 50.0 | 20 | 20.0 | 70.0 | 50.0 |
| LotFrontage | 834 | 188 | 69.8417 | 70.0 | 60.0 | 59.0 | 80.0 | 21.0 |
| LotArea | 1022 | 0 | 10451.864 | 9515.0 | 9600 | 7540.75 | 11635.5 | 4094.75 |
| OverallQual | 1022 | 0 | 6.09 | 6.0 | 6 | 5.0 | 7.0 | 2.0 |
| OverallCond | 1022 | 0 | 5.6047 | 5.0 | 5 | 5.0 | 6.0 | 1.0 |
| YearBuilt | 1022 | 0 | 1970.9736 | 1972.0 | 2005 | 1954.0 | 2000.75 | 46.75 |
| YearRemodAdd | 1022 | 0 | 1984.9227 | 1994.0 | 1950 | 1966.0 | 2004.0 | 38.0 |
| MasVnrArea | 1015 | 7 | 101.9123 | 0.0 | 0.0 | 0.0 | 165.5 | 165.5 |
| BsmtFinSF1 | 1022 | 0 | 442.7348 | 379.5 | 0 | 0.0 | 732.75 | 732.75 |
| BsmtFinSF2 | 1022 | 0 | 36.9423 | 0.0 | 0 | 0.0 | 0.0 | 0.0 |
| BsmtUnfSF | 1022 | 0 | 564.1781 | 477.5 | 0 | 216.25 | 797.75 | 581.5 |
| TotalBsmtSF | 1022 | 0 | 1043.8552 | 983.5 | 0 | 784.0 | 1268.0 | 484.0 |
| 1stFlrSF | 1022 | 0 | 1157.6781 | 1087.0 | 864 | 876.75 | 1375.75 | 499.0 |
| 2ndFlrSF | 1022 | 0 | 358.4061 | 0.0 | 0 | 0.0 | 728.0 | 728.0 |
| LowQualFinSF | 1022 | 0 | 5.9687 | 0.0 | 0 | 0.0 | 0.0 | 0.0 |
| GrLivArea | 1022 | 0 | 1522.0528 | 1461.5 | 864 | 1144.0 | 1786.75 | 642.75 |
| BsmtFullBath | 1022 | 0 | 0.4129 | 0.0 | 0 | 0.0 | 1.0 | 1.0 |
| BsmtHalfBath | 1022 | 0 | 0.0597 | 0.0 | 0 | 0.0 | 0.0 | 0.0 |
| FullBath | 1022 | 0 | 1.5705 | 2.0 | 2 | 1.0 | 2.0 | 1.0 |
| HalfBath | 1022 | 0 | 0.3875 | 0.0 | 0 | 0.0 | 1.0 | 1.0 |
| BedroomAbvGr | 1022 | 0 | 2.8796 | 3.0 | 3 | 2.0 | 3.0 | 1.0 |
| KitchenAbvGr | 1022 | 0 | 1.0411 | 1.0 | 1 | 1.0 | 1.0 | 0.0 |
| TotRmsAbvGrd | 1022 | 0 | 6.5401 | 6.0 | 6 | 5.0 | 7.0 | 2.0 |
| Fireplaces | 1022 | 0 | 0.6106 | 1.0 | 0 | 0.0 | 1.0 | 1.0 |
| GarageYrBlt | 969 | 53 | 1978.5748 | 1980.0 | 2005.0 | 1962.0 | 2002.0 | 40.0 |
| GarageCars | 1022 | 0 | 1.774 | 2.0 | 2 | 1.0 | 2.0 | 1.0 |
| GarageArea | 1022 | 0 | 473.2211 | 480.0 | 0 | 338.0 | 576.0 | 238.0 |
| WoodDeckSF | 1022 | 0 | 95.0528 | 0.0 | 0 | 0.0 | 168.0 | 168.0 |
| OpenPorchSF | 1022 | 0 | 47.2074 | 25.0 | 0 | 0.0 | 68.75 | 68.75 |
| EnclosedPorch | 1022 | 0 | 21.1057 | 0.0 | 0 | 0.0 | 0.0 | 0.0 |
| 3SsnPorch | 1022 | 0 | 4.5431 | 0.0 | 0 | 0.0 | 0.0 | 0.0 |
| ScreenPorch | 1022 | 0 | 17.1732 | 0.0 | 0 | 0.0 | 0.0 | 0.0 |
| PoolArea | 1022 | 0 | 3.3777 | 0.0 | 0 | 0.0 | 0.0 | 0.0 |
| MiscVal | 1022 | 0 | 40.8317 | 0.0 | 0 | 0.0 | 0.0 | 0.0 |
| MoSold | 1022 | 0 | 6.3523 | 6.0 | 6 | 5.0 | 8.0 | 3.0 |
| YrSold | 1022 | 0 | 2007.8239 | 2008.0 | 2009 | 2007.0 | 2009.0 | 2.0 |

## Ngoại lai (IQR, k=1.5)

| Cột | Biên dưới | Biên trên | Số ngoại lai | % |
|---|---|---|---|---|
| MSSubClass | -55.0 | 145.0 | 74 | 7.24% |
| LotFrontage | 27.5 | 111.5 | 58 | 6.95% |
| LotArea | 1398.625 | 17777.625 | 43 | 4.21% |
| OverallQual | 2.0 | 10.0 | 2 | 0.2% |
| OverallCond | 3.5 | 7.5 | 86 | 8.41% |
| YearBuilt | 1883.875 | 2070.875 | 5 | 0.49% |
| YearRemodAdd | 1909.0 | 2061.0 | 0 | 0.0% |
| MasVnrArea | -248.25 | 413.75 | 68 | 6.7% |
| BsmtFinSF1 | -1099.125 | 1831.875 | 4 | 0.39% |
| BsmtFinSF2 | 0.0 | 0.0 | 102 | 9.98% |
| BsmtUnfSF | -656.0 | 1670.0 | 21 | 2.05% |
| TotalBsmtSF | 58.0 | 1994.0 | 47 | 4.6% |
| 1stFlrSF | 128.25 | 2124.25 | 13 | 1.27% |
| 2ndFlrSF | -1092.0 | 1820.0 | 1 | 0.1% |
| LowQualFinSF | 0.0 | 0.0 | 18 | 1.76% |
| GrLivArea | 179.875 | 2750.875 | 22 | 2.15% |
| BsmtFullBath | -1.5 | 2.5 | 1 | 0.1% |
| BsmtHalfBath | 0.0 | 0.0 | 60 | 5.87% |
| FullBath | -0.5 | 3.5 | 0 | 0.0% |
| HalfBath | -1.5 | 2.5 | 0 | 0.0% |
| BedroomAbvGr | 0.5 | 4.5 | 25 | 2.45% |
| KitchenAbvGr | 1.0 | 1.0 | 42 | 4.11% |
| TotRmsAbvGrd | 2.0 | 10.0 | 24 | 2.35% |
| Fireplaces | -1.5 | 2.5 | 4 | 0.39% |
| GarageYrBlt | 1902.0 | 2062.0 | 1 | 0.1% |
| GarageCars | -0.5 | 3.5 | 3 | 0.29% |
| GarageArea | -19.0 | 933.0 | 13 | 1.27% |
| WoodDeckSF | -252.0 | 420.0 | 30 | 2.94% |
| OpenPorchSF | -103.125 | 171.875 | 58 | 5.68% |
| EnclosedPorch | 0.0 | 0.0 | 135 | 13.21% |
| 3SsnPorch | 0.0 | 0.0 | 21 | 2.05% |
| ScreenPorch | 0.0 | 0.0 | 93 | 9.1% |
| PoolArea | 0.0 | 0.0 | 6 | 0.59% |
| MiscVal | 0.0 | 0.0 | 39 | 3.82% |
| MoSold | 0.5 | 12.5 | 0 | 0.0% |
| YrSold | 2004.0 | 2012.0 | 0 | 0.0% |

## Giá trị ngoài miền hợp lệ

- `LotFrontage` (hợp lệ: [0.0, None]): 0 giá trị vi phạm — coi là thiếu (NaN) rồi điền theo P5, hoặc loại dòng nếu ảnh hưởng nhỏ
- `MasVnrArea` (hợp lệ: [0.0, None]): 0 giá trị vi phạm — coi là thiếu (NaN) rồi điền theo P5, hoặc loại dòng nếu ảnh hưởng nhỏ
- `GarageYrBlt` (hợp lệ: [1800.0, 2026.0]): 0 giá trị vi phạm — coi là thiếu (NaN) rồi điền theo P5, hoặc loại dòng nếu ảnh hưởng nhỏ

## Độ lệch phân phối (skewness)

- `MSSubClass`: 1.42 (lệch phải mạnh)
- `LotFrontage`: 2.629 (lệch phải mạnh)
- `LotArea`: 10.829 (lệch phải mạnh)
- `OverallQual`: 0.196 (gần đối xứng)
- `OverallCond`: 0.628 (gần đối xứng)
- `YearBuilt`: -0.623 (gần đối xứng)
- `YearRemodAdd`: -0.506 (gần đối xứng)
- `MasVnrArea`: 2.215 (lệch phải mạnh)
- `BsmtFinSF1`: 1.967 (lệch phải mạnh)
- `BsmtFinSF2`: 4.611 (lệch phải mạnh)
- `BsmtUnfSF`: 0.928 (gần đối xứng)
- `TotalBsmtSF`: 1.857 (lệch phải mạnh)
- `1stFlrSF`: 1.554 (lệch phải mạnh)
- `2ndFlrSF`: 0.778 (gần đối xứng)
- `LowQualFinSF`: 8.966 (lệch phải mạnh)
- `GrLivArea`: 1.507 (lệch phải mạnh)
- `BsmtFullBath`: 0.67 (gần đối xứng)
- `BsmtHalfBath`: 3.925 (lệch phải mạnh)
- `FullBath`: 0.07 (gần đối xứng)
- `HalfBath`: 0.581 (gần đối xứng)
- `BedroomAbvGr`: 0.267 (gần đối xứng)
- `KitchenAbvGr`: 4.898 (lệch phải mạnh)
- `TotRmsAbvGrd`: 0.717 (gần đối xứng)
- `Fireplaces`: 0.652 (gần đối xứng)
- `GarageYrBlt`: -0.67 (gần đối xứng)
- `GarageCars`: -0.377 (gần đối xứng)
- `GarageArea`: 0.139 (gần đối xứng)
- `WoodDeckSF`: 1.625 (lệch phải mạnh)
- `OpenPorchSF`: 2.301 (lệch phải mạnh)
- `EnclosedPorch`: 3.291 (lệch phải mạnh)
- `3SsnPorch`: 8.921 (lệch phải mạnh)
- `ScreenPorch`: 3.904 (lệch phải mạnh)
- `PoolArea`: 13.435 (lệch phải mạnh)
- `MiscVal`: 16.94 (lệch phải mạnh)
- `MoSold`: 0.216 (gần đối xứng)
- `YrSold`: 0.064 (gần đối xứng)

## Độ liên quan với biến mục tiêu (gợi ý chọn đặc trưng ở P5)

- `MSSubClass`: {'method': 'pearson_vs_label', 'value': -0.079}
- `LotFrontage`: {'method': 'pearson_vs_label', 'value': 0.342}
- `LotArea`: {'method': 'pearson_vs_label', 'value': 0.266}
- `OverallQual`: {'method': 'pearson_vs_label', 'value': 0.786}
- `OverallCond`: {'method': 'pearson_vs_label', 'value': -0.075}
- `YearBuilt`: {'method': 'pearson_vs_label', 'value': 0.515}
- `YearRemodAdd`: {'method': 'pearson_vs_label', 'value': 0.511}
- `MasVnrArea`: {'method': 'pearson_vs_label', 'value': 0.453}
- `BsmtFinSF1`: {'method': 'pearson_vs_label', 'value': 0.356}
- `BsmtFinSF2`: {'method': 'pearson_vs_label', 'value': -0.015}
- `BsmtUnfSF`: {'method': 'pearson_vs_label', 'value': 0.225}
- `TotalBsmtSF`: {'method': 'pearson_vs_label', 'value': 0.592}
- `1stFlrSF`: {'method': 'pearson_vs_label', 'value': 0.583}
- `2ndFlrSF`: {'method': 'pearson_vs_label', 'value': 0.314}
- `LowQualFinSF`: {'method': 'pearson_vs_label', 'value': -0.009}
- `GrLivArea`: {'method': 'pearson_vs_label', 'value': 0.689}
- `BsmtFullBath`: {'method': 'pearson_vs_label', 'value': 0.23}
- `BsmtHalfBath`: {'method': 'pearson_vs_label', 'value': -0.035}
- `FullBath`: {'method': 'pearson_vs_label', 'value': 0.562}
- `HalfBath`: {'method': 'pearson_vs_label', 'value': 0.278}
- `BedroomAbvGr`: {'method': 'pearson_vs_label', 'value': 0.158}
- `KitchenAbvGr`: {'method': 'pearson_vs_label', 'value': -0.135}
- `TotRmsAbvGrd`: {'method': 'pearson_vs_label', 'value': 0.524}
- `Fireplaces`: {'method': 'pearson_vs_label', 'value': 0.46}
- `GarageYrBlt`: {'method': 'pearson_vs_label', 'value': 0.484}
- `GarageCars`: {'method': 'pearson_vs_label', 'value': 0.642}
- `GarageArea`: {'method': 'pearson_vs_label', 'value': 0.618}
- `WoodDeckSF`: {'method': 'pearson_vs_label', 'value': 0.328}
- `OpenPorchSF`: {'method': 'pearson_vs_label', 'value': 0.315}
- `EnclosedPorch`: {'method': 'pearson_vs_label', 'value': -0.146}
- `3SsnPorch`: {'method': 'pearson_vs_label', 'value': 0.062}
- `ScreenPorch`: {'method': 'pearson_vs_label', 'value': 0.143}
- `PoolArea`: {'method': 'pearson_vs_label', 'value': 0.127}
- `MiscVal`: {'method': 'pearson_vs_label', 'value': -0.015}
- `MoSold`: {'method': 'pearson_vs_label', 'value': 0.07}
- `YrSold`: {'method': 'pearson_vs_label', 'value': -0.004}

## Biểu đồ

Xem thư mục `eda_plots/` (36 histogram+boxplot, 1 heatmap tương quan, 1 scatter cặp mạnh nhất)
