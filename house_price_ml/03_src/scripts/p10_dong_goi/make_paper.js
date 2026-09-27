const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
} = require("docx");

const FONT = "Times New Roman";

function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 300, after: 150 },
    children: [new TextRun({ text, bold: true, size: 28, font: FONT })] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, bold: true, size: 24, font: FONT })] });
}
function p(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.JUSTIFIED,
    spacing: { after: 160, line: 300 },
    children: [new TextRun({ text, font: FONT, size: 22, italics: opts.italics || false, bold: opts.bold || false })],
  });
}
function cell(text, opts = {}) {
  return new TableCell({
    width: { size: opts.width || 2000, type: WidthType.DXA },
    shading: opts.header ? { type: ShadingType.CLEAR, fill: "D9E2F3" } : undefined,
    children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, font: FONT, size: 20, bold: !!opts.header })] })],
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

const doc = new Document({
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 } } }, // A4
    children: [
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
        children: [new TextRun({ text: "Dự đoán Giá Nhà bằng Mô hình Học Máy: So sánh Hồi quy Tuyến tính có Regularization và Gradient Boosting trên Bộ dữ liệu Ames Housing",
          bold: true, size: 30, font: FONT })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
        children: [new TextRun({ text: "Huỳnh Kiện Khải", size: 24, font: FONT })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
        children: [new TextRun({ text: "Khoa Công nghệ Thông tin, Trường Đại học Sài Gòn", italics: true, size: 20, font: FONT })] }),

      h2("Tóm tắt"),
      p("Định giá bất động sản chính xác là bài toán quan trọng trong lĩnh vực tài chính và quy hoạch đô thị. Nghiên cứu này xây dựng và so sánh các mô hình học máy nhằm dự đoán giá bán nhà (SalePrice) trên bộ dữ liệu công khai Ames Housing (Kaggle House Prices), gồm 1460 quan sát và 79 đặc trưng mô tả đặc điểm nhà ở. Từ 79 đặc trưng gốc, 71 đặc trưng được chọn lọc có căn cứ dựa trên phân tích khám phá dữ liệu (EDA) chỉ thực hiện trên tập huấn luyện, tránh rò rỉ thông tin sang tập kiểm định và tập kiểm tra. Quy trình tiền xử lý gồm mã hóa thứ bậc (ordinal encoding) cho các đặc trưng chất lượng, mã hóa one-hot cho đặc trưng danh định, và xử lý giá trị thiếu theo ngữ nghĩa (thiếu có ý nghĩa hay thiếu thực sự). Năm mô hình được so sánh: dự đoán hằng số, Linear Regression, Ridge Regression, XGBoost mặc định và XGBoost đã tinh chỉnh siêu tham số. Kết quả cho thấy Ridge Regression (alpha=30) đạt hiệu suất tốt nhất và ổn định nhất, với RMSLE trên tập kiểm tra (chỉ mở một lần) là 0.1301, MAE 14.280 USD, và hệ số xác định R2 = 0.943, vượt xa baseline tầm thường (RMSLE 0.406). Phân tích lỗi cho thấy mô hình gặp khó khăn với các giao dịch có điều kiện bán bất thường (SaleCondition khác Normal).", { italics: true }),
      p("Từ khóa: dự đoán giá nhà, hồi quy, Ridge Regression, XGBoost, Ames Housing, học máy.", { italics: true }),

      h1("1. Giới thiệu"),
      p("Định giá bất động sản là bài toán có ý nghĩa thực tiễn lớn, ảnh hưởng trực tiếp đến quyết định của người mua, người bán, tổ chức tín dụng và nhà hoạch định chính sách đô thị. Giá nhà chịu tác động của nhiều nhóm yếu tố đan xen: đặc điểm vật lý (diện tích, chất lượng xây dựng), vị trí (khu vực dân cư), và bối cảnh giao dịch (thời điểm, điều kiện bán). Việc định lượng đóng góp của từng nhóm yếu tố này là một bài toán hồi quy phức tạp, phù hợp để áp dụng các phương pháp học máy hiện đại."),
      p("Bộ dữ liệu Ames Housing (De Cock, 2011), được sử dụng rộng rãi trong cuộc thi Kaggle House Prices, cung cấp 79 đặc trưng chi tiết cho 1460 căn nhà tại thành phố Ames, bang Iowa, Hoa Kỳ, giai đoạn 2006-2010. So với bộ dữ liệu Boston Housing kinh điển, Ames Housing có số lượng đặc trưng lớn hơn nhiều và bao gồm cả biến định lượng lẫn định tính, đòi hỏi quy trình tiền xử lý và lựa chọn đặc trưng cẩn trọng."),
      p("Nghiên cứu này hướng đến ba mục tiêu: (1) xây dựng quy trình tiền xử lý dữ liệu có kiểm soát rò rỉ thông tin nghiêm ngặt (chia dữ liệu trước, học tham số tiền xử lý chỉ trên tập huấn luyện); (2) so sánh hiệu suất giữa mô hình tuyến tính có regularization (Ridge) và mô hình cây tăng cường (XGBoost) trên dữ liệu bảng quy mô nhỏ; (3) phân tích các trường hợp mô hình dự đoán sai để xác định giới hạn thực tiễn của mô hình."),

      h1("2. Đối tượng và phương pháp"),
      h2("2.1. Tập dữ liệu"),
      p("Bộ dữ liệu train.csv (Kaggle House Prices - Ames Housing) gồm 1460 dòng, 79 đặc trưng và biến mục tiêu liên tục SalePrice (giá bán, USD). Đặc trưng gồm 36 cột số và 43 cột hạng mục, mô tả 9 nhóm thông tin: khu đất, vị trí, chất lượng/tình trạng nhà, nền móng/tầng hầm, hệ thống trong nhà, diện tích sinh hoạt, garage, đường xe vào, và thông tin giao dịch."),
      p("Kiểm toán dữ liệu ban đầu phát hiện 19 cột có giá trị thiếu, không có dòng trùng lặp. Phần lớn giá trị thiếu mang tính ngữ nghĩa (ví dụ PoolQC thiếu ở 99,5% số dòng vì nhà không có hồ bơi), không phải lỗi nhập liệu. Phân tích khám phá dữ liệu (EDA), thực hiện độc quyền trên tập huấn luyện theo nguyên tắc tránh rò rỉ, phát hiện 2 quan sát ngoại lai đã được ghi nhận trong tài liệu gốc của bộ dữ liệu: hai căn nhà có diện tích sinh hoạt trên 4000 sqft, chất lượng tổng thể tối đa (OverallQual=10), nhưng giá bán bất thường thấp do điều kiện bán là “Partial” (nhà bán khi chưa hoàn thiện xây dựng). Hai quan sát này được loại khỏi tập huấn luyện."),
      p("Dữ liệu được chia ngẫu nhiên (seed=42) theo tỉ lệ 70/15/15 thành tập huấn luyện (1020 dòng sau khi loại ngoại lai), tập kiểm định (219 dòng) và tập kiểm tra (219 dòng). Do biến mục tiêu là liên tục với hầu hết giá trị duy nhất, việc chia theo tầng (stratified) không khả thi; chia ngẫu nhiên có seed cố định được sử dụng thay thế."),

      h2("2.2. Lựa chọn đặc trưng"),
      p("Từ 79 đặc trưng gốc, 71 đặc trưng được chọn lọc dựa trên ý nghĩa nghiệp vụ (khu đất, vị trí, chất lượng nhà, móng/tầng hầm, hệ thống, diện tích, garage, đường vào, giao dịch), loại bỏ 8 đặc trưng có tín hiệu thống kê yếu với biến mục tiêu (tương quan Pearson hoặc hệ số eta-squared gần 0): PoolArea, PoolQC, Fence, MiscFeature, MiscVal, EnclosedPorch, 3SsnPorch, ScreenPorch. Đối chiếu ngược với phân tích trên toàn bộ 79 cột xác nhận 4 đặc trưng ban đầu bị loại (Fireplaces, FireplaceQu, WoodDeckSF, OpenPorchSF) thực chất có tín hiệu đáng kể (hệ số tương quan/eta-squared từ 0,3 đến 0,46) và được bổ sung trở lại, đưa tổng số đặc trưng cuối cùng lên 71."),

      h2("2.3. Mô hình đề xuất"),
      p("Năm cấu hình được so sánh theo nguyên tắc thay đổi một yếu tố mỗi lần, đánh giá bằng RMSLE (Root Mean Squared Logarithmic Error) trên tập kiểm định:"),
      p("(1) Baseline tầm thường: dự đoán hằng số bằng trung bình SalePrice của tập huấn luyện. (2) XGBoost với siêu tham số mặc định. (3) Linear Regression (bình phương tối thiểu thông thường, không regularization). (4) Ridge Regression, hệ số alpha được chọn bằng 5-fold cross-validation nội bộ trên tập huấn luyện. (5) XGBoost với siêu tham số được tinh chỉnh bằng RandomizedSearchCV (60 vòng thử, 5-fold cross-validation trên tập huấn luyện)."),
      p("Biến mục tiêu được biến đổi log1p trước khi huấn luyện (SalePrice có độ lệch phân phối skew=1,88; sau biến đổi còn 0,15), giúp ổn định phương sai và phù hợp với metric RMSLE."),

      h2("2.4. Chi tiết triển khai"),
      p("Tiền xử lý gồm hai giai đoạn. Giai đoạn thứ nhất áp dụng quy tắc nghiệp vụ cố định, không phụ thuộc dữ liệu: mã hóa thứ bậc (ordinal) cho 18 đặc trưng chất lượng theo đúng thang đo gốc (ví dụ Po<Fa<TA<Gd<Ex), với mức “không có đặc điểm” được gán hạng thấp nhất; điền giá trị 0 cho hai đặc trưng số có giá trị thiếu mang ý nghĩa “không tồn tại” (MasVnrArea, GarageYrBlt). Giai đoạn thứ hai học tham số từ tập huấn luyện: điền giá trị thiếu còn lại (LotFrontage) bằng trung vị, mã hóa one-hot cho 22 đặc trưng danh định, và chuẩn hóa (StandardScaler) toàn bộ đặc trưng số. Bộ tiền xử lý được kiểm chứng không rò rỉ thông tin bằng kiểm tra tự động, xác nhận toàn bộ tham số học được đều xuất phát từ tập huấn luyện. Sau mã hóa, không gian đặc trưng có 205 chiều (49 số, 156 one-hot). Toàn bộ mô hình và pipeline được cài đặt bằng scikit-learn 1.8.0 và XGBoost 3.4.1 (Python 3.12)."),

      h1("3. Thí nghiệm và kết quả"),
      h2("3.1. So sánh các mô hình trên tập kiểm định"),
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
      p(""),
      p("Linear Regression không regularization đạt RMSLE thấp nhất trên tập kiểm định (0,1143), tuy nhiên phân tích hệ số hồi quy cho thấy 15 hệ số có trị tuyệt đối lớn nhất đều thuộc về các cột one-hot của mức hạng mục hiếm (ví dụ Condition2=RRAe, Exterior1st=BrkComm, mỗi mức chỉ vài quan sát) — dấu hiệu phương sai ước lượng cao do cỡ mẫu nhỏ, không phản ánh tầm quan trọng thực sự của đặc trưng. Ridge Regression (regularization L2, alpha chọn bằng cross-validation trên tập huấn luyện) cho bảng hệ số ổn định hơn nhiều, với OverallQual và GrLivArea — hai đặc trưng có tương quan mạnh nhất với giá nhà theo EDA — đứng đầu bảng hệ số, phù hợp với hiểu biết miền. Vì lý do này, Ridge được chọn làm mô hình cuối cùng thay vì Linear Regression, dù RMSLE trên tập kiểm định chênh lệch không đáng kể."),
      p("XGBoost, kể cả sau khi tinh chỉnh siêu tham số bằng tìm kiếm ngẫu nhiên có kiểm định chéo, không vượt qua được các mô hình tuyến tính có regularization. Kết quả này gợi ý rằng, sau khi đặc trưng đã được mã hóa kỹ (ordinal cho thứ bậc, one-hot cho danh định), quan hệ giữa đặc trưng và log(SalePrice) chủ yếu mang tính tuyến tính, và trên tập dữ liệu có quy mô nhỏ (1020 quan sát huấn luyện), mô hình tuyến tính có regularization tổng quát hóa tốt hơn mô hình cây phi tuyến."),

      h2("3.2. Đánh giá cuối cùng trên tập kiểm tra"),
      p("Mô hình cuối cùng (Ridge, alpha=30) được đánh giá đúng một lần trên tập kiểm tra (219 quan sát, chưa từng được sử dụng cho bất kỳ quyết định nào trước đó). Khoảng tin cậy được ước lượng bằng bootstrap (1000 lần lấy mẫu lại)."),
      table(
        ["Tập", "RMSLE", "95% CI (bootstrap)", "MAE (USD)", "R2"],
        [
          ["Kiểm định", "0,1155", "[0,089 ; 0,145]", "13.197", "0,950"],
          ["Kiểm tra", "0,1301", "[0,099 ; 0,159]", "14.280", "0,943"],
        ],
        [1600, 1400, 2400, 1800, 1400],
      ),
      p(""),
      p("RMSLE trên tập kiểm tra (0,1301) cao hơn tập kiểm định (0,1155) nhưng nằm trong khoảng tin cậy chồng lấp nhau, cho thấy không có dấu hiệu rõ ràng của việc mô hình được chọn quá khớp (overfit) với tập kiểm định qua nhiều vòng thí nghiệm. Kết quả vượt xa tiêu chí thành công đã đề ra (vượt baseline tầm thường một cách có ý nghĩa): RMSLE giảm từ 0,406 xuống 0,130, tương đương giảm 68%."),

      h2("3.3. Phân tích lỗi"),
      p("Phân tích các quan sát có sai số tuyệt đối lớn nhất trên tập kiểm định (không sử dụng tập kiểm tra để tránh làm nhiễm thông tin) cho thấy 6 trong 10 trường hợp sai số lớn nhất đều có SaleCondition khác “Normal” (Abnorml — bán trong hoàn cảnh tài chính khó khăn, hoặc Partial — nhà mới xây bán trực tiếp). Trường hợp cực đoan nhất là một căn nhà giá 34.900 USD (thấp nhất toàn bộ dữ liệu, điều kiện bán Abnorml, diện tích chỉ 720 sqft), bị mô hình dự đoán lệch 131%. Phát hiện này cho thấy giá bán trong các giao dịch bất thường chịu ảnh hưởng mạnh của hoàn cảnh bán (không được mô tả đầy đủ qua đặc trưng vật lý căn nhà), là giới hạn cố hữu của mô hình hiện tại."),

      h1("4. Kết luận"),
      p("Nghiên cứu đã xây dựng thành công quy trình dự đoán giá nhà trên bộ dữ liệu Ames Housing với kiểm soát rò rỉ thông tin nghiêm ngặt qua toàn bộ vòng đời dữ liệu — từ kiểm toán, chia dữ liệu, khám phá dữ liệu (chỉ trên train), đến tiền xử lý (học tham số chỉ từ train, kiểm chứng tự động). Kết quả thực nghiệm cho thấy Ridge Regression, dù là mô hình tuyến tính đơn giản, vượt trội hơn XGBoost (kể cả sau khi tinh chỉnh siêu tham số) trên bộ dữ liệu bảng quy mô nhỏ này, đồng thời cho bảng hệ số hồi quy ổn định và có thể diễn giải được — một ưu điểm quan trọng ngoài độ chính xác thuần túy. Mô hình cuối đạt RMSLE 0,1301 trên tập kiểm tra, giảm 68% so với baseline tầm thường."),
      p("Hạn chế chính của nghiên cứu là hiệu suất kém hơn đáng kể đối với các giao dịch có điều kiện bán bất thường, và cỡ mẫu tập kiểm tra (219) khiến khoảng tin cậy còn tương đối rộng. Hướng phát triển tiếp theo bao gồm: xây dựng đặc trưng tương tác giữa SaleCondition và các đặc trưng chính, thử nghiệm mô hình stacking kết hợp Ridge và XGBoost, và mở rộng đánh giá bằng k-fold cross-validation lồng nhau (nested CV) để ước lượng phương sai của quy trình chọn mô hình chặt chẽ hơn."),

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
