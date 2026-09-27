const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, ImageRun,
} = require("docx");
const fs = require("fs");

const FONT = "Times New Roman";
const BLACK = "000000";
const ASSETS = "poster_assets/";

function h1(text) {
  return new Paragraph({ spacing: { before: 320, after: 150 }, keepNext: true,
    children: [new TextRun({ text, bold: true, size: 28, font: FONT, color: BLACK })] });
}
function h2(text) {
  return new Paragraph({ spacing: { before: 220, after: 110 }, keepNext: true,
    children: [new TextRun({ text, bold: true, size: 24, font: FONT, color: BLACK })] });
}
function p(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.JUSTIFIED,
    spacing: { after: 160, line: 300 },
    children: [new TextRun({ text, font: FONT, size: 22, italics: opts.italics || false, bold: opts.bold || false, color: BLACK })],
  });
}
function cell(text, opts = {}) {
  return new TableCell({
    width: { size: opts.width || 2000, type: WidthType.DXA },
    shading: opts.header ? { type: ShadingType.CLEAR, fill: "E5E5E5" } : undefined,
    children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, font: FONT, size: 20, bold: !!opts.header, color: BLACK })] })],
  });
}
function table(headerRow, rows, widths) {
  return new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({ children: headerRow.map((t, i) => cell(t, { header: true, width: widths[i] })) }),
      ...rows.map((r) => new TableRow({ children: r.map((t, i) => cell(t, { width: widths[i] })) })),
    ],
  });
}
function figure(file, widthIn, ratio, caption) {
  const buf = fs.readFileSync(ASSETS + file);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200, after: 60 },
      children: [new ImageRun({ data: buf, transformation: { width: widthIn * 96, height: (widthIn / ratio) * 96 }, type: "png" })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 220 },
      children: [new TextRun({ text: caption, italics: true, size: 19, font: FONT, color: BLACK })] }),
  ];
}

const doc = new Document({
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 } } },
    children: [
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
        children: [new TextRun({ text: "Dự đoán Giá Nhà bằng Mô hình Học Máy: So sánh Hồi quy Tuyến tính có Regularization và Gradient Boosting trên Bộ dữ liệu Ames Housing",
          bold: true, size: 30, font: FONT, color: BLACK })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
        children: [new TextRun({ text: "Huỳnh Kiện Khải", size: 24, font: FONT, color: BLACK })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
        children: [new TextRun({ text: "Khoa Công nghệ Thông tin, Trường Đại học Sài Gòn", italics: true, size: 20, font: FONT, color: BLACK })] }),

      h2("Tóm tắt"),
      p("Định giá bất động sản chính xác là bài toán quan trọng trong lĩnh vực tài chính, tín dụng và quy hoạch đô thị. Nghiên cứu này xây dựng và so sánh có hệ thống năm cấu hình mô hình học máy nhằm dự đoán giá bán nhà (SalePrice) trên bộ dữ liệu công khai Ames Housing (Kaggle House Prices), gồm 1460 quan sát và 79 đặc trưng mô tả đặc điểm nhà ở tại thành phố Ames, Iowa. Từ 79 đặc trưng gốc, 71 đặc trưng được chọn lọc có căn cứ định lượng dựa trên phân tích khám phá dữ liệu (EDA) thực hiện độc quyền trên tập huấn luyện, nhằm tránh rò rỉ thông tin sang tập kiểm định và tập kiểm tra. Quy trình tiền xử lý gồm mã hóa thứ bậc (ordinal encoding) cho các đặc trưng chất lượng theo đúng thang đo gốc, mã hóa one-hot cho đặc trưng danh định, và xử lý giá trị thiếu phân biệt theo ngữ nghĩa (thiếu có ý nghĩa — không tồn tại đặc điểm — hay thiếu thực sự do đo đạc). Năm mô hình được so sánh theo nguyên tắc thay đổi một yếu tố mỗi lần: dự đoán hằng số, Linear Regression, Ridge Regression, XGBoost mặc định và XGBoost đã tinh chỉnh siêu tham số bằng tìm kiếm ngẫu nhiên có kiểm định chéo. Kết quả cho thấy Ridge Regression (alpha=30, chọn bằng cross-validation nội bộ trên train) đạt hiệu suất tốt nhất và ổn định nhất trong số các mô hình có thể diễn giải được, với RMSLE trên tập kiểm tra (chỉ mở đúng một lần, sau khi đã chốt cấu hình) là 0,1301, sai số tuyệt đối trung bình (MAE) 14.280 USD, và hệ số xác định R2 = 0,943 — vượt xa baseline tầm thường (RMSLE 0,406), tương đương mức giảm 68%. Phân tích lỗi chi tiết cho thấy mô hình gặp khó khăn có hệ thống với các giao dịch có điều kiện bán bất thường (SaleCondition khác Normal), gợi ý hướng cải thiện cho các nghiên cứu tiếp theo.", { italics: true }),
      p("Từ khóa: dự đoán giá nhà, hồi quy, Ridge Regression, XGBoost, Ames Housing, học máy, kỹ thuật đặc trưng.", { italics: true }),

      h1("1. Giới thiệu"),
      p("Định giá bất động sản là bài toán có ý nghĩa thực tiễn lớn, ảnh hưởng trực tiếp đến quyết định của người mua, người bán, tổ chức tín dụng và nhà hoạch định chính sách đô thị. Giá nhà chịu tác động của nhiều nhóm yếu tố đan xen: đặc điểm vật lý (diện tích, chất lượng xây dựng, số phòng), vị trí (khu vực dân cư, mức độ tiện lợi), và bối cảnh giao dịch (thời điểm bán, điều kiện bán). Việc định lượng đóng góp của từng nhóm yếu tố này, đồng thời xây dựng một mô hình dự đoán có độ chính xác cao và có thể diễn giải được, là một bài toán hồi quy phức tạp, phù hợp để áp dụng các phương pháp học máy hiện đại."),
      p("Bộ dữ liệu Ames Housing (De Cock, 2011), được sử dụng rộng rãi trong cuộc thi Kaggle House Prices: Advanced Regression Techniques, cung cấp 79 đặc trưng chi tiết cho 1460 căn nhà tại thành phố Ames, bang Iowa, Hoa Kỳ, giao dịch trong giai đoạn 2006-2010. So với bộ dữ liệu Boston Housing kinh điển (chỉ 13 đặc trưng, 506 quan sát), Ames Housing có số lượng đặc trưng lớn hơn nhiều lần và bao gồm cả biến định lượng lẫn định tính đa dạng (từ chất lượng vật liệu, kiểu mái nhà đến điều kiện giao dịch), đòi hỏi quy trình tiền xử lý và lựa chọn đặc trưng cẩn trọng hơn đáng kể."),
      p("Nghiên cứu này hướng đến bốn mục tiêu cụ thể: (1) xây dựng quy trình tiền xử lý dữ liệu có kiểm soát rò rỉ thông tin nghiêm ngặt — chia dữ liệu trước khi phân tích, học tham số tiền xử lý (giá trị impute, thang đo chuẩn hóa, danh mục one-hot) chỉ trên tập huấn luyện, và kiểm chứng tự động; (2) xây dựng quy trình lựa chọn đặc trưng có căn cứ định lượng, đối chiếu hai chiều để tránh bỏ sót đặc trưng quan trọng; (3) so sánh có hệ thống hiệu suất giữa mô hình tuyến tính có regularization (Ridge) và mô hình cây tăng cường gradient (XGBoost) trên dữ liệu bảng quy mô nhỏ; (4) phân tích các trường hợp mô hình dự đoán sai nhiều nhất để xác định giới hạn thực tiễn và đề xuất hướng cải thiện."),

      h2("1.1. Công trình liên quan"),
      p("Bài toán dự đoán giá nhà trên bộ dữ liệu Ames Housing đã được nghiên cứu rộng rãi kể từ khi De Cock (2011) công bố như một lựa chọn thay thế cho bộ Boston Housing trong giảng dạy thống kê hồi quy. Các cách tiếp cận phổ biến trên nền tảng Kaggle thường sử dụng tổ hợp (ensemble) của nhiều mô hình gradient boosting (XGBoost, LightGBM, CatBoost) kết hợp kỹ thuật tạo đặc trưng sâu (feature engineering) như tổng diện tích, tuổi nhà tại thời điểm bán, và mã hóa mục tiêu (target encoding) cho biến hạng mục có cardinality cao. Hoerl và Kennard (1970) đề xuất Ridge Regression như một phương pháp ổn định ước lượng hồi quy khi các biến độc lập có tương quan cao (đa cộng tuyến) — vấn đề phổ biến trong dữ liệu nhà ở, nơi diện tích các tầng, số phòng tắm và diện tích tầng hầm thường tương quan chặt với nhau. Chen và Guestrin (2016) giới thiệu XGBoost như một thuật toán gradient boosting hiệu quả về mặt tính toán, đã trở thành lựa chọn mặc định cho nhiều bài toán học máy trên dữ liệu bảng. Khác với phần lớn các nghiên cứu tập trung tối đa hóa độ chính xác dự đoán bằng ensemble phức tạp, nghiên cứu này ưu tiên một quy trình có kiểm soát chặt chẽ rò rỉ thông tin và khả năng diễn giải mô hình, phù hợp với mục tiêu học thuật của một đồ án cá nhân."),

      h1("2. Đối tượng và phương pháp"),
      h2("2.1. Tập dữ liệu"),
      p("Bộ dữ liệu train.csv (Kaggle House Prices - Ames Housing) gồm 1460 dòng, 79 đặc trưng và biến mục tiêu liên tục SalePrice (giá bán, USD). Đặc trưng gồm 36 cột số và 43 cột hạng mục, mô tả 9 nhóm thông tin như trình bày ở Bảng 1."),
      table(
        ["Nhóm", "Số đặc trưng", "Ví dụ"],
        [
          ["Thông tin khu đất", "11", "LotArea, LotShape, Utilities"],
          ["Vị trí và khu vực", "3", "Neighborhood, Condition1/2"],
          ["Chất lượng và tình trạng nhà", "17", "OverallQual, YearBuilt, ExterQual"],
          ["Nền móng và tầng hầm", "11", "BsmtQual, TotalBsmtSF"],
          ["Hệ thống trong nhà", "4", "CentralAir, HeatingQC"],
          ["Diện tích và không gian sinh hoạt", "13", "GrLivArea, FullBath, KitchenQual"],
          ["Garage", "7", "GarageCars, GarageArea"],
          ["Đường xe vào nhà", "1", "PavedDrive"],
          ["Thông tin giao dịch", "4", "SaleType, SaleCondition"],
        ],
        [3600, 1800, 3200],
      ),
      p("Bảng 1: Chín nhóm đặc trưng nghiệp vụ và số lượng đặc trưng tương ứng (trước khi lựa chọn đặc trưng ở mục 2.2).", { italics: true, align: AlignmentType.CENTER }),
      p("Kiểm toán dữ liệu ban đầu (thống kê mô tả, kiểm tra trùng lặp, kiểm tra giá trị thiếu) phát hiện 19 cột có giá trị thiếu, không có dòng trùng lặp. Bảng 2 liệt kê các cột có tỉ lệ thiếu cao nhất."),
      table(
        ["Cột", "% thiếu", "Diễn giải"],
        [
          ["PoolQC", "99,5%", "Không có hồ bơi"],
          ["MiscFeature", "96,0%", "Không có tiện ích đặc biệt"],
          ["Alley", "93,8%", "Không có lối hẻm tiếp cận"],
          ["Fence", "80,8%", "Không có hàng rào"],
          ["MasVnrType", "59,7%", "Không ốp đá/gạch mặt tiền"],
          ["FireplaceQu", "47,1%", "Không có lò sưởi"],
          ["LotFrontage", "18,4%", "Không đo được / không ghi nhận"],
        ],
        [2600, 1400, 4600],
      ),
      p("Bảng 2: Các cột có tỉ lệ giá trị thiếu cao nhất. Ngoại trừ LotFrontage, các cột còn lại mang tính \"thiếu có ý nghĩa\" (đặc điểm không tồn tại), được xác nhận bằng đối chiếu chéo với cột hạng mục liên quan (ví dụ MasVnrArea=0 khi MasVnrType thiếu).", { italics: true, align: AlignmentType.CENTER }),
      p("Phân tích khám phá dữ liệu (EDA), thực hiện độc quyền trên tập huấn luyện theo nguyên tắc tránh rò rỉ thông tin, phát hiện 2 quan sát ngoại lai đã được ghi nhận trong tài liệu gốc của bộ dữ liệu (Hình 2): hai căn nhà có diện tích sinh hoạt trên 4000 sqft, chất lượng tổng thể tối đa (OverallQual=10), nhưng giá bán bất thường thấp (184.750 USD và 160.000 USD) do điều kiện bán là \"Partial\" (nhà bán khi chưa hoàn thiện xây dựng). Một quan sát thứ ba có diện tích tương tự nhưng giá bán 745.000 USD (cao nhất toàn bộ dữ liệu) được xác định là hợp lệ, không phải ngoại lai, và được giữ lại. Hai quan sát ngoại lai được loại khỏi tập huấn luyện trước khi huấn luyện mô hình."),
      ...figure("fig_outliers.png", 5.0, 1.395, "Hình 2: Quan hệ giữa diện tích sinh hoạt (GrLivArea) và giá bán (SalePrice) trên tập huấn luyện, với 2 quan sát ngoại lai được đánh dấu."),
      p("Dữ liệu được chia ngẫu nhiên (seed=42) theo tỉ lệ 70/15/15 thành tập huấn luyện (1020 dòng sau khi loại ngoại lai), tập kiểm định (219 dòng) và tập kiểm tra (219 dòng). Do biến mục tiêu là liên tục với hầu hết giá trị duy nhất (chỉ 2 giao dịch có cùng giá bán trong toàn bộ dữ liệu), việc chia theo tầng (stratified sampling) theo đúng nghĩa cổ điển không khả thi; chia ngẫu nhiên có seed cố định được sử dụng thay thế để đảm bảo khả năng tái lập."),

      h2("2.2. Lựa chọn đặc trưng"),
      p("Từ 79 đặc trưng gốc, 71 đặc trưng được chọn lọc ban đầu dựa trên ý nghĩa nghiệp vụ theo 9 nhóm ở Bảng 1, loại bỏ 12 đặc trưng thuộc nhóm \"tiện ích phụ\" (hồ bơi, hàng rào, tiện ích khác, hiên phụ) được cho là ít liên quan trực tiếp đến giá trị cốt lõi của căn nhà. Để kiểm chứng quyết định định tính này, một vòng phân tích đối chiếu được thực hiện: chạy lại phân tích tương quan/eta-squared trên toàn bộ 79 đặc trưng gốc và so sánh với tập 71 đặc trưng đã chọn. Kết quả đối chiếu (Bảng 3) xác nhận 8 trong 12 đặc trưng bị loại thực sự có tín hiệu thống kê yếu (hệ số tương quan Pearson hoặc eta-squared gần 0), nhưng phát hiện 4 đặc trưng (Fireplaces, FireplaceQu, WoodDeckSF, OpenPorchSF) có tín hiệu đáng kể bị bỏ sót, được bổ sung trở lại, đưa tổng số đặc trưng cuối cùng lên 71."),
      table(
        ["Đặc trưng", "Chỉ số liên quan", "Quyết định"],
        [
          ["Fireplaces", "corr = 0,46", "Bổ sung lại"],
          ["FireplaceQu", "eta2 = 0,30", "Bổ sung lại"],
          ["WoodDeckSF", "corr = 0,33", "Bổ sung lại"],
          ["OpenPorchSF", "corr = 0,32", "Bổ sung lại"],
          ["EnclosedPorch", "corr = -0,15", "Loại (đúng)"],
          ["PoolArea / PoolQC", "corr = 0,13 / eta2 = 0,01", "Loại (đúng)"],
          ["Fence / MiscFeature", "eta2 = 0,04 / 0,01", "Loại (đúng)"],
        ],
        [2800, 2600, 2200],
      ),
      p("Bảng 3: Đối chiếu tín hiệu thống kê của các đặc trưng thuộc nhóm bị loại ban đầu (tính trên tập huấn luyện, biến mục tiêu log1p(SalePrice)).", { italics: true, align: AlignmentType.CENTER }),

      h2("2.3. Mô hình đề xuất"),
      p("Năm cấu hình được so sánh theo nguyên tắc thay đổi một yếu tố mỗi lần, đánh giá bằng RMSLE (Root Mean Squared Logarithmic Error) trên tập kiểm định:"),
      p("(1) Baseline tầm thường: dự đoán hằng số bằng trung bình SalePrice của tập huấn luyện — cận dưới tham chiếu bắt buộc phải vượt qua. (2) XGBoost với siêu tham số mặc định (n_estimators=500, learning_rate=0,05, max_depth=4). (3) Linear Regression (bình phương tối thiểu thông thường, không regularization). (4) Ridge Regression, hệ số alpha được chọn bằng 5-fold cross-validation nội bộ trên tập huấn luyện, quét lưới alpha thuộc {0,1; 0,3; 1; 3; 10; 30; 100; 300; 1000}. (5) XGBoost với siêu tham số được tinh chỉnh bằng RandomizedSearchCV (60 vòng thử, 5-fold cross-validation trên tập huấn luyện), tìm kiếm trên không gian: n_estimators từ 300 đến 1200, max_depth từ 2 đến 6, learning_rate từ 0,01 đến 0,08, cùng với subsample, colsample_bytree, reg_alpha, reg_lambda, min_child_weight."),
      p("Biến mục tiêu được biến đổi log1p (log(1+x)) trước khi huấn luyện — SalePrice có độ lệch phân phối skew=1,88, sau biến đổi còn 0,15 — giúp ổn định phương sai phần dư và phù hợp trực tiếp với định nghĩa của metric RMSLE, vốn được định nghĩa là căn bậc hai trung bình bình phương sai lệch giữa log(1+giá thực tế) và log(1+giá dự đoán). Việc tối ưu hóa sai số bình phương trên thang log tương đương tối ưu hóa RMSLE trên thang gốc, nên các mô hình hồi quy tuyến tính/cây được huấn luyện trực tiếp trên log1p(SalePrice) mà không cần hàm mất mát tùy chỉnh."),

      h2("2.4. Chi tiết triển khai"),
      p("Tiền xử lý gồm hai giai đoạn tách biệt rõ ràng để đảm bảo không rò rỉ thông tin. Giai đoạn thứ nhất áp dụng quy tắc nghiệp vụ cố định, không phụ thuộc dữ liệu (áp dụng đồng nhất cho cả ba tập): mã hóa thứ bậc (ordinal) cho 18 đặc trưng chất lượng theo đúng thang đo gốc trong tài liệu mô tả dữ liệu (ví dụ ExterQual: Po<Fa<TA<Gd<Ex), với mức \"không có đặc điểm\" (NA) được gán hạng thấp nhất (0); điền giá trị 0 cho hai đặc trưng số có giá trị thiếu mang ý nghĩa \"không tồn tại\" (MasVnrArea, GarageYrBlt); loại 2 quan sát ngoại lai đã xác định ở mục 2.1. Giai đoạn thứ hai học tham số từ tập huấn luyện: điền giá trị thiếu còn lại (LotFrontage, thiếu thực sự chứ không mang ý nghĩa) bằng trung vị của tập huấn luyện; mã hóa one-hot cho 22 đặc trưng danh định còn lại, xử lý mức hạng mục chưa từng xuất hiện ở tập huấn luyện (xuất hiện ở val/test) bằng vector 0; và chuẩn hóa (StandardScaler, trừ trung bình chia độ lệch chuẩn của train) toàn bộ 49 đặc trưng số."),
      p("Bộ tiền xử lý được kiểm chứng không rò rỉ thông tin bằng một quy trình kiểm tra tự động, xác nhận toàn bộ tham số học được (giá trị trung vị, trung bình/độ lệch chuẩn, danh mục one-hot) đều xuất phát duy nhất từ tập huấn luyện, không chịu ảnh hưởng của tập kiểm định/kiểm tra. Sau mã hóa, không gian đặc trưng có 205 chiều (49 số đã chuẩn hóa, 156 nhị phân one-hot). Toàn bộ mô hình và pipeline được cài đặt bằng scikit-learn 1.8.0 và XGBoost 3.4.1 trên Python 3.12, chạy hoàn toàn trên CPU (không yêu cầu GPU)."),

      h1("3. Thí nghiệm và kết quả"),
      h2("3.1. So sánh các mô hình trên tập kiểm định"),
      ...figure("heatmap.png", 4.3, 1.0, "Hình 1: Ma trận tương quan giữa các đặc trưng số (tính trên tập huấn luyện), thể hiện 3 cụm cộng tuyến rõ rệt."),
      table(
        ["Mô hình", "RMSLE (val)", "Ghi chú"],
        [
          ["Hằng số = trung bình train", "0,4060", "Sàn dưới cùng"],
          ["XGBoost (mặc định)", "0,1267", "Baseline cổ điển"],
          ["Linear Regression", "0,1143", "Hệ số không ổn định do mức hạng mục hiếm"],
          ["Ridge (alpha=30)", "0,1155", "Mô hình cuối — hệ số ổn định"],
          ["XGBoost (đã tinh chỉnh)", "0,1245", "Cải thiện so với mặc định, vẫn kém Ridge"],
        ],
        [3200, 1600, 3800],
      ),
      p("Bảng 4: So sánh RMSLE của 5 cấu hình trên tập kiểm định (219 quan sát).", { italics: true, align: AlignmentType.CENTER }),
      ...figure("rmsle_compare.png", 4.6, 1.375, "Hình 3: Biểu đồ so sánh RMSLE giữa 5 cấu hình mô hình trên tập kiểm định."),
      p("Linear Regression không regularization đạt RMSLE thấp nhất trên tập kiểm định (0,1143), tuy nhiên phân tích hệ số hồi quy cho thấy 15 hệ số có trị tuyệt đối lớn nhất đều thuộc về các cột one-hot của mức hạng mục hiếm (ví dụ Condition2=RRAe, Exterior1st=BrkComm, mỗi mức chỉ vài quan sát trong toàn bộ tập huấn luyện) — dấu hiệu kinh điển của phương sai ước lượng cao do cỡ mẫu nhỏ trên từng mức, không phản ánh tầm quan trọng thực sự của đặc trưng đối với giá nhà."),
      p("Ridge Regression (regularization L2, alpha chọn bằng cross-validation trên tập huấn luyện) cho bảng hệ số ổn định hơn rõ rệt (Hình 5). OverallQual và GrLivArea — hai đặc trưng có tương quan mạnh nhất với giá nhà theo EDA (mục 2.1) — đứng đầu bảng hệ số, phù hợp với hiểu biết miền và với kết quả phân tích tương quan độc lập ở Bảng 3. Vì lý do này, Ridge được chọn làm mô hình cuối cùng thay vì Linear Regression, dù RMSLE trên tập kiểm định chênh lệch không đáng kể (0,1155 so với 0,1143) — sự đánh đổi nhỏ về độ chính xác điểm được bù lại bằng độ tin cậy và khả năng diễn giải của mô hình, một tiêu chí quan trọng không kém độ chính xác thuần túy trong ứng dụng thực tế."),
      ...figure("fig_ridge_coefs.png", 5.2, 1.354, "Hình 5: Top 12 hệ số hồi quy Ridge có trị tuyệt đối lớn nhất (thang log1p(SalePrice))."),
      p("XGBoost, kể cả sau khi tinh chỉnh siêu tham số bằng tìm kiếm ngẫu nhiên có kiểm định chéo (siêu tham số tốt nhất: max_depth=2, n_estimators=1200, learning_rate=0,03, subsample=0,7), không vượt qua được các mô hình tuyến tính có regularization. Kết quả này gợi ý rằng, sau khi đặc trưng đã được mã hóa kỹ (ordinal cho thứ bậc, one-hot cho danh định), quan hệ giữa đặc trưng và log(SalePrice) chủ yếu mang tính tuyến tính, và trên tập dữ liệu có quy mô nhỏ (1020 quan sát huấn luyện), mô hình tuyến tính có regularization tổng quát hóa tốt hơn mô hình cây phi tuyến — vốn thường cần nhiều dữ liệu hơn để phát huy ưu thế trước các mô hình tuyến tính đơn giản."),

      h2("3.2. Đánh giá cuối cùng trên tập kiểm tra"),
      p("Mô hình cuối cùng (Ridge, alpha=30) được đánh giá đúng một lần trên tập kiểm tra (219 quan sát, chưa từng được sử dụng cho bất kỳ quyết định thiết kế hay lựa chọn mô hình nào trước đó). Khoảng tin cậy được ước lượng bằng bootstrap (Efron & Tibshirani, 1994), lấy mẫu lại có hoàn lại 1000 lần từ tập kiểm định/kiểm tra tương ứng."),
      table(
        ["Tập", "RMSLE", "95% CI (bootstrap)", "MAE (USD)", "R2"],
        [
          ["Kiểm định", "0,1155", "[0,089 ; 0,145]", "13.197", "0,950"],
          ["Kiểm tra", "0,1301", "[0,099 ; 0,159]", "14.280", "0,943"],
        ],
        [1600, 1400, 2400, 1800, 1400],
      ),
      p("Bảng 5: Kết quả đánh giá cuối cùng của mô hình Ridge trên tập kiểm định và tập kiểm tra.", { italics: true, align: AlignmentType.CENTER }),
      ...figure("test_scatter.png", 4.6, 1.222, "Hình 4: Giá dự đoán so với giá thực tế trên tập kiểm tra (đường đứt nét đỏ biểu diễn dự đoán hoàn hảo)."),
      p("RMSLE trên tập kiểm tra (0,1301) cao hơn tập kiểm định (0,1155) nhưng nằm trong khoảng tin cậy chồng lấp nhau, cho thấy không có dấu hiệu rõ ràng của việc mô hình được chọn quá khớp (overfit) với tập kiểm định qua nhiều vòng thí nghiệm so sánh. Hình 4 cho thấy các điểm dự đoán bám sát đường chéo lý tưởng ở khoảng giá phổ biến (dưới 300.000 USD), với độ phân tán tăng nhẹ ở phân khúc giá cao — phù hợp với đặc điểm cỡ mẫu thưa hơn ở phân khúc này. Kết quả vượt xa tiêu chí thành công đã đề ra trong giai đoạn định nghĩa bài toán (vượt baseline tầm thường một cách có ý nghĩa): RMSLE giảm từ 0,406 xuống 0,130, tương đương giảm 68%."),

      h2("3.3. Phân tích lỗi"),
      p("Phân tích các quan sát có sai số tuyệt đối lớn nhất trên tập kiểm định (không sử dụng tập kiểm tra để tránh làm nhiễm thông tin cho các quyết định tiếp theo) cho thấy 6 trong 10 trường hợp sai số lớn nhất đều có SaleCondition khác \"Normal\" (Abnorml — bán trong hoàn cảnh tài chính khó khăn, hoặc Partial — nhà mới xây bán trực tiếp từ chủ đầu tư). Trường hợp cực đoan nhất là một căn nhà giá 34.900 USD (thấp nhất toàn bộ dữ liệu, điều kiện bán Abnorml, diện tích chỉ 720 sqft, chất lượng tổng thể thấp), bị mô hình dự đoán lệch 131% so với giá thực. Phát hiện này cho thấy giá bán trong các giao dịch bất thường chịu ảnh hưởng mạnh của hoàn cảnh bán (áp lực tài chính, quan hệ giữa người mua-bán) — thông tin không được mô tả đầy đủ qua các đặc trưng vật lý của căn nhà — là giới hạn cố hữu của mô hình hiện tại, không thể khắc phục chỉ bằng điều chỉnh siêu tham số hay đổi thuật toán."),

      h1("4. Kết luận"),
      p("Nghiên cứu đã xây dựng thành công quy trình dự đoán giá nhà trên bộ dữ liệu Ames Housing với kiểm soát rò rỉ thông tin nghiêm ngặt qua toàn bộ vòng đời dữ liệu — từ kiểm toán, chia dữ liệu, khám phá dữ liệu (chỉ trên train), lựa chọn đặc trưng có đối chiếu hai chiều, đến tiền xử lý (học tham số chỉ từ train, kiểm chứng tự động bằng quy trình kiểm tra độc lập). Kết quả thực nghiệm cho thấy Ridge Regression, dù là mô hình tuyến tính đơn giản hơn nhiều so với XGBoost, vượt trội hơn XGBoost (kể cả sau khi tinh chỉnh siêu tham số kỹ lưỡng bằng tìm kiếm ngẫu nhiên 60 vòng) trên bộ dữ liệu bảng quy mô nhỏ này, đồng thời cho bảng hệ số hồi quy ổn định và có thể diễn giải được — một ưu điểm thực tiễn quan trọng ngoài độ chính xác thuần túy, đặc biệt có giá trị trong bối cảnh cần giải thích quyết định định giá cho các bên liên quan. Mô hình cuối đạt RMSLE 0,1301 trên tập kiểm tra (mở đúng một lần), giảm 68% so với baseline tầm thường, với khoảng tin cậy bootstrap [0,099; 0,159]."),
      p("Hạn chế chính của nghiên cứu là hiệu suất kém hơn đáng kể đối với các giao dịch có điều kiện bán bất thường (mục 3.3), và cỡ mẫu tập kiểm tra (219 quan sát) khiến khoảng tin cậy bootstrap còn tương đối rộng, hạn chế độ chắc chắn khi so sánh sai lệch nhỏ giữa các mô hình. Ngoài ra, quy trình dừng lại sau 5 cấu hình so sánh theo quyết định phạm vi của đồ án, chưa khai thác các kỹ thuật tổ hợp mô hình (ensemble/stacking) vốn thường mang lại cải thiện thêm trên các benchmark tương tự. Hướng phát triển tiếp theo bao gồm: xây dựng đặc trưng tương tác giữa SaleCondition và các đặc trưng chính (diện tích, chất lượng) để mô hình hóa rõ ràng hơn ảnh hưởng của hoàn cảnh bán; thử nghiệm mô hình stacking kết hợp Ridge và XGBoost nhằm tận dụng đồng thời tính tuyến tính chủ đạo và khả năng bắt quan hệ phi tuyến cục bộ; và mở rộng đánh giá bằng k-fold cross-validation lồng nhau (nested cross-validation) để ước lượng phương sai của toàn bộ quy trình chọn mô hình một cách chặt chẽ hơn thay vì dựa trên một lần chia train/val/test duy nhất."),

      h2("Tài liệu tham khảo"),
      p("1) De Cock, D. (2011). \"Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project.\" Journal of Statistics Education, 19(3).", { align: AlignmentType.LEFT }),
      p("2) Pedregosa, F., et al. (2011). \"Scikit-learn: Machine learning in Python.\" Journal of Machine Learning Research, 12, 2825-2830.", { align: AlignmentType.LEFT }),
      p("3) Chen, T., & Guestrin, C. (2016). \"XGBoost: A Scalable Tree Boosting System.\" Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785-794.", { align: AlignmentType.LEFT }),
      p("4) Hoerl, A. E., & Kennard, R. W. (1970). \"Ridge Regression: Biased Estimation for Nonorthogonal Problems.\" Technometrics, 12(1), 55-67.", { align: AlignmentType.LEFT }),
      p("5) Efron, B., & Tibshirani, R. J. (1994). \"An Introduction to the Bootstrap.\" Chapman and Hall/CRC.", { align: AlignmentType.LEFT }),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => require("fs").writeFileSync("Paper_HouseSalePrice.docx", buf));
