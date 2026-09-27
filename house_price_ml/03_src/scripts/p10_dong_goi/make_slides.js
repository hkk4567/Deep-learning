const pptxgen = require("pptxgenjs");

const TEAL = "0E5C4A";
const GOLD = "E6A700";
const CREAM = "FBF7EE";
const DARK = "1F2A1F";
const GRAY = "6B6B6B";
const LIGHTTEAL = "CDE7C4";
const RED = "C0392B";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";

function bgSlide(title) {
  const s = pres.addSlide();
  s.background = { color: CREAM };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.9, fill: { color: TEAL } });
  s.addText(title, { x: 0.5, y: 0.12, w: 12.3, h: 0.65, fontFace: "Calibri", fontSize: 24, bold: true, color: "FFFFFF", isTextBox: true, valign: "middle" });
  s.addShape("ellipse", { x: 12.7, y: 0.15, w: 0.35, h: 0.35, fill: { color: GOLD } });
  return s;
}
function pageNum(s, n) {
  s.addText(String(n), { x: 12.85, y: 7.15, w: 0.4, h: 0.3, fontSize: 10, color: GRAY, align: "right", isTextBox: true });
}
function arrowBetween(s, x1, y, x2) {
  s.addShape("rightArrow", { x: x1, y: y - 0.12, w: x2 - x1, h: 0.24, fill: { color: GOLD }, line: { type: "none" } });
}

let n = 1;

// ---- Slide 1: Title ----
{
  const s = pres.addSlide();
  s.background = { color: TEAL };
  s.addShape("rect", { x: 0, y: 4.6, w: 13.33, h: 2.9, fill: { color: "0A4A3B" } });
  for (let i = 0; i < 6; i++) {
    s.addShape("ellipse", { x: 10.8 + (i % 3) * 0.85, y: 0.6 + Math.floor(i / 3) * 0.85, w: 0.18, h: 0.18, fill: { color: GOLD }, line: { type: "none" } });
  }
  s.addText("Dự đoán Giá Nhà bằng Mô hình Học Máy", {
    x: 0.7, y: 2.3, w: 11.5, h: 1.3, fontFace: "Calibri", fontSize: 40, bold: true, color: "FFFFFF", isTextBox: true,
  });
  s.addText("So sánh Ridge Regression và XGBoost trên bộ dữ liệu Ames Housing", {
    x: 0.7, y: 3.5, w: 11.5, h: 0.6, fontFace: "Calibri", fontSize: 20, color: LIGHTTEAL, isTextBox: true,
  });
  s.addShape("line", { x: 0.72, y: 4.35, w: 1.4, h: 0, line: { color: GOLD, width: 3 } });
  s.addText("Huỳnh Kiện Khải", { x: 0.7, y: 5.0, w: 8, h: 0.4, fontSize: 18, bold: true, color: "FFFFFF", isTextBox: true });
  s.addText("Khoa Công nghệ Thông tin — Trường Đại học Sài Gòn", { x: 0.7, y: 5.4, w: 8, h: 0.4, fontSize: 14, color: LIGHTTEAL, isTextBox: true });
}

// ---- Slide 2: Agenda ----
{
  const s = bgSlide("Nội dung trình bày");
  const items = [
    "Quy trình tổng thể", "1. Giới thiệu bài toán", "2. Dữ liệu & Kiểm toán", "3. Khám phá dữ liệu (EDA)", "4. Lựa chọn đặc trưng",
    "5. Tiền xử lý dữ liệu", "6. Mô hình hoạt động ra sao?", "7. Thí nghiệm & So sánh", "8. Kết quả cuối (Test)", "9. Phân tích lỗi & Kết luận",
  ];
  items.forEach((t, i) => {
    const col = i % 5, row = Math.floor(i / 5);
    const x = 0.45 + col * 2.5, y = 1.5 + row * 2.3;
    s.addShape("roundRect", { x, y, w: 2.3, h: 2.0, rectRadius: 0.1, fill: { color: "FFFFFF" }, line: { color: "E0E0D8", width: 1 } });
    s.addShape("ellipse", { x: x + 0.85, y: y + 0.25, w: 0.6, h: 0.6, fill: { color: TEAL } });
    s.addText(String(i), { x: x + 0.85, y: y + 0.25, w: 0.6, h: 0.6, align: "center", valign: "middle", fontSize: 18, bold: true, color: "FFFFFF", isTextBox: true });
    s.addText(t.replace(/^\d+\.\s*/, ""), { x: x + 0.15, y: y + 1.0, w: 2.0, h: 0.9, align: "center", fontSize: 12.5, bold: true, color: DARK, valign: "top", isTextBox: true, margin: 0 });
  });
  pageNum(s, 2);
}

// ---- Slide 3: Quy trinh tong the (PIPELINE DIAGRAM) ----
{
  const s = bgSlide("Quy trình tổng thể (Pipeline)");
  const steps = [
    ["📋", "Kiểm toán", "Missing, trùng lặp"],
    ["🔍", "EDA", "Chỉ trên train"],
    ["🧩", "Chọn đặc trưng", "79 → 71 cột"],
    ["⚙️", "Tiền xử lý", "Encode, impute, scale"],
    ["🤖", "Huấn luyện", "5 cấu hình mô hình"],
    ["✅", "Đánh giá", "Test — mở 1 lần"],
  ];
  const boxW = 1.85, gap = 0.28, startX = 0.4, y = 2.4;
  steps.forEach((st, i) => {
    const x = startX + i * (boxW + gap);
    s.addShape("roundRect", { x, y, w: boxW, h: 1.9, rectRadius: 0.1, fill: { color: i === steps.length - 1 ? "E8F5E9" : "FFFFFF" }, line: { color: TEAL, width: 1.5 } });
    s.addText(st[0], { x, y: y + 0.12, w: boxW, h: 0.55, align: "center", fontSize: 26, isTextBox: true });
    s.addText(st[1], { x: x + 0.08, y: y + 0.68, w: boxW - 0.16, h: 0.5, align: "center", fontSize: 13, bold: true, color: TEAL, isTextBox: true });
    s.addText(st[2], { x: x + 0.08, y: y + 1.18, w: boxW - 0.16, h: 0.65, align: "center", fontSize: 10.5, color: GRAY, isTextBox: true });
    if (i < steps.length - 1) arrowBetween(s, x + boxW, y + 0.95, x + boxW + gap);
  });
  s.addText("Mỗi bước đều được ghi log (Change_Log, Findings, Experiments) trong change_log.xlsx — không rò rỉ thông tin giữa train/val/test qua bất kỳ bước nào.", {
    x: 0.8, y: 4.8, w: 11.7, h: 0.8, align: "center", fontSize: 14, italic: true, color: DARK, isTextBox: true,
  });
  pageNum(s, 3);
}

// ---- Slide 4: Gioi thieu ----
{
  const s = bgSlide("1. Giới thiệu bài toán");
  s.addText([
    { text: "Bài toán: ", options: { bold: true, color: TEAL } },
    { text: "Dự đoán giá bán nhà (SalePrice) từ đặc điểm căn nhà — hồi quy trên dữ liệu bảng.\n\n", options: {} },
    { text: "Vì sao quan trọng: ", options: { bold: true, color: TEAL } },
    { text: "Định giá bất động sản ảnh hưởng người mua, người bán, tổ chức tín dụng.\n\n", options: {} },
    { text: "Bộ dữ liệu: ", options: { bold: true, color: TEAL } },
    { text: "Ames Housing (Kaggle House Prices) — 1460 căn nhà, 79 đặc trưng, Ames, Iowa (2006–2010).\n\n", options: {} },
    { text: "Mục tiêu nghiên cứu:", options: { bold: true, color: TEAL } },
  ], { x: 0.6, y: 1.2, w: 7.3, h: 4.5, fontSize: 16, color: DARK, isTextBox: true, lineSpacingMultiple: 1.3 });
  const goals = [
    "Quy trình tiền xử lý không rò rỉ thông tin (train/val/test)",
    "So sánh Ridge Regression (tuyến tính) vs XGBoost (cây tăng cường)",
    "Phân tích lỗi để hiểu giới hạn thực tiễn của mô hình",
  ];
  goals.forEach((g, i) => {
    s.addShape("roundRect", { x: 0.8, y: 4.75 + i * 0.55, w: 0.3, h: 0.3, rectRadius: 0.15, fill: { color: GOLD } });
    s.addText(g, { x: 1.25, y: 4.68 + i * 0.55, w: 6.5, h: 0.45, fontSize: 13.5, color: DARK, isTextBox: true, valign: "middle" });
  });
  s.addImage({ path: "poster_assets/heatmap.png", x: 8.3, y: 1.3, w: 4.4, h: 4.4 });
  pageNum(s, 4);
}

// ---- Slide 5: Du lieu ----
{
  const s = bgSlide("2. Dữ liệu & Kiểm toán");
  s.addTable([
    [{ text: "Đặc điểm", options: { bold: true, fill: { color: TEAL }, color: "FFFFFF" } }, { text: "Giá trị", options: { bold: true, fill: { color: TEAL }, color: "FFFFFF" } }],
    ["Số dòng gốc", "1460"],
    ["Số đặc trưng gốc", "79 (36 số, 43 hạng mục)"],
    ["Dòng trùng lặp", "0"],
    ["Cột có missing", "19"],
    ["Ngoại lai đã loại", "2 (Id=524, 1299 — Partial sale)"],
    ["Chia train/val/test", "1020 / 219 / 219 (seed=42)"],
  ], { x: 0.6, y: 1.3, w: 5.8, fontSize: 14, border: { type: "solid", color: "E0E0D8", pt: 1 }, autoPage: false, rowH: 0.5 });
  s.addText("Missing đáng chú ý (% dòng thiếu)", { x: 6.8, y: 1.3, w: 5.9, h: 0.4, fontSize: 15, bold: true, color: TEAL, isTextBox: true });
  s.addTable([
    [{ text: "Cột", options: { bold: true, fill: { color: LIGHTTEAL } } }, { text: "% thiếu", options: { bold: true, fill: { color: LIGHTTEAL } } }, { text: "Ý nghĩa", options: { bold: true, fill: { color: LIGHTTEAL } } }],
    ["PoolQC", "99.4%", "Không có hồ bơi"],
    ["MiscFeature", "96.0%", "Không có tiện ích đặc biệt"],
    ["Alley", "93.4%", "Không có lối hẻm"],
    ["MasVnrType", "59.2%", "Không ốp mặt tiền"],
  ], { x: 6.8, y: 1.8, w: 5.9, fontSize: 12.5, border: { type: "solid", color: "E0E0D8", pt: 1 }, rowH: 0.4 });
  s.addShape("roundRect", { x: 6.8, y: 4.3, w: 5.9, h: 1.4, rectRadius: 0.08, fill: { color: "FFF3CD" }, line: { color: GOLD, width: 1 } });
  s.addText("Phần lớn missing mang tính \"ngữ nghĩa\" (nhà không có đặc điểm đó), không phải lỗi nhập liệu — quyết định: điền giá trị 0/\"None\", không dùng median/mode mặc định.", {
    x: 7.0, y: 4.4, w: 5.5, h: 1.2, fontSize: 13, color: DARK, isTextBox: true, valign: "middle",
  });
  pageNum(s, 5);
}

// ---- Slide 6: EDA ----
{
  const s = bgSlide("3. Khám phá dữ liệu (chỉ trên train)");
  s.addImage({ path: "poster_assets/fig_outliers.png", x: 0.5, y: 1.15, w: 6.6, h: 4.73 });
  s.addText([
    { text: "Phát hiện chính\n\n", options: { bold: true, fontSize: 17, color: TEAL } },
    { text: "• SalePrice lệch phải (skew=1.73) → log1p còn 0.15\n\n", options: { fontSize: 14 } },
    { text: "• Top tương quan: OverallQual (0.79), GrLivArea (0.69), GarageCars (0.64)\n\n", options: { fontSize: 14 } },
    { text: "• ExterQual, FireplaceQu: bậc thang tăng rõ theo chất lượng\n\n", options: { fontSize: 14 } },
    { text: "• Phát hiện 2 ngoại lai đã biết của dataset (đã loại khỏi train)", options: { fontSize: 14 } },
  ], { x: 7.4, y: 1.5, w: 5.4, h: 5, color: DARK, isTextBox: true, lineSpacingMultiple: 1.2 });
  pageNum(s, 6);
}

// ---- Slide 7: Lua chon dac trung ----
{
  const s = bgSlide("4. Lựa chọn đặc trưng");
  s.addText("79 đặc trưng gốc → 71 đặc trưng chọn lọc theo 9 nhóm nghiệp vụ", { x: 0.6, y: 1.15, w: 12, h: 0.5, fontSize: 17, bold: true, color: TEAL, isTextBox: true });
  const groups = ["Khu đất (11)", "Vị trí (3)", "Chất lượng nhà (17)", "Móng/Tầng hầm (11)", "Hệ thống (4)", "Diện tích sinh hoạt (13)", "Garage (7)", "Đường vào (1)", "Giao dịch (4)"];
  groups.forEach((g, i) => {
    const col = i % 5, row = Math.floor(i / 5);
    const x = 0.6 + col * 2.48, y = 1.85 + row * 0.85;
    s.addShape("roundRect", { x, y, w: 2.3, h: 0.65, rectRadius: 0.08, fill: { color: "FFFFFF" }, line: { color: TEAL, width: 1 } });
    s.addText(g, { x, y, w: 2.3, h: 0.65, align: "center", valign: "middle", fontSize: 12, bold: true, color: DARK, isTextBox: true });
  });
  s.addShape("roundRect", { x: 0.6, y: 3.9, w: 12.1, h: 2.7, rectRadius: 0.08, fill: { color: "FFF3CD" }, line: { color: GOLD, width: 1 } });
  s.addText([
    { text: "Đối chiếu ngược với EDA toàn bộ 79 cột\n\n", options: { bold: true, fontSize: 16, color: "8A6D00" } },
    { text: "8 cột loại đúng (tín hiệu yếu): PoolArea, PoolQC, Fence, MiscFeature, MiscVal, EnclosedPorch, 3SsnPorch, ScreenPorch\n\n", options: { fontSize: 14 } },
    { text: "4 cột bổ sung lại (tín hiệu bị bỏ sót): Fireplaces (corr=0.46), FireplaceQu (η²=0.30), WoodDeckSF (corr=0.33), OpenPorchSF (corr=0.32)\n", options: { fontSize: 14, bold: true, color: "1B5E20" } },
  ], { x: 0.9, y: 4.05, w: 11.5, h: 2.4, isTextBox: true, lineSpacingMultiple: 1.15 });
  pageNum(s, 7);
}

// ---- Slide 8: Tien xu ly (1/2) - Quy tac nghiep vu ----
{
  const s = bgSlide("5. Tiền xử lý dữ liệu (1/2) — Quy tắc cố định");
  s.addText("Bước 1: áp dụng đồng nhất cho train/val/test (không học từ dữ liệu)", { x: 0.6, y: 1.1, w: 12, h: 0.4, fontSize: 14, italic: true, color: GRAY, isTextBox: true });
  s.addText("Ví dụ mã hóa Ordinal — ExterQual (chất lượng ngoại thất)", { x: 0.6, y: 1.6, w: 6, h: 0.4, fontSize: 14, bold: true, color: TEAL, isTextBox: true });
  const levels = [["Po", "0"], ["Fa", "1"], ["TA", "2"], ["Gd", "3"], ["Ex", "4"]];
  levels.forEach((lv, i) => {
    const x = 0.7 + i * 1.15;
    s.addShape("roundRect", { x, y: 2.1, w: 0.95, h: 0.75, rectRadius: 0.08, fill: { color: i === 0 ? "FFE0E0" : (i === 4 ? "E8F5E9" : "FFFFFF") }, line: { color: TEAL, width: 1 } });
    s.addText(lv[0], { x, y: 2.15, w: 0.95, h: 0.35, align: "center", fontSize: 13, bold: true, color: DARK, isTextBox: true });
    s.addText("→ " + lv[1], { x, y: 2.5, w: 0.95, h: 0.3, align: "center", fontSize: 11, color: GRAY, isTextBox: true });
    if (i < 4) arrowBetween(s, x + 0.95, 2.47, x + 1.15);
  });
  s.addText("Giữ đúng thứ tự chất lượng — one-hot sẽ làm mất thông tin \"Ex tốt hơn Gd\"", { x: 0.7, y: 3.05, w: 6, h: 0.4, fontSize: 12, italic: true, color: GRAY, isTextBox: true });

  s.addText("Điền giá trị 0 cho \"thiếu có ý nghĩa\"", { x: 0.6, y: 3.7, w: 6, h: 0.4, fontSize: 14, bold: true, color: TEAL, isTextBox: true });
  s.addTable([
    [{ text: "Cột", options: { bold: true, fill: { color: LIGHTTEAL } } }, { text: "Khi thiếu →", options: { bold: true, fill: { color: LIGHTTEAL } } }],
    ["MasVnrArea", "0 (không ốp mặt tiền)"],
    ["GarageYrBlt", "0 (không có garage)"],
  ], { x: 0.6, y: 4.15, w: 6.0, fontSize: 13, border: { type: "solid", color: "E0E0D8", pt: 1 }, rowH: 0.45 });

  s.addShape("roundRect", { x: 7.3, y: 1.6, w: 5.4, h: 5.0, rectRadius: 0.1, fill: { color: "FFFFFF" }, line: { color: TEAL, width: 1.5 } });
  s.addText("18 cột Ordinal được mã hóa:", { x: 7.55, y: 1.75, w: 5, h: 0.4, fontSize: 14, bold: true, color: TEAL, isTextBox: true });
  s.addText("ExterQual, ExterCond, BsmtQual, BsmtCond, BsmtExposure, BsmtFinType1/2, HeatingQC, KitchenQual, Functional, GarageFinish, GarageQual, GarageCond, PavedDrive, LandSlope, LotShape, Utilities, FireplaceQu", {
    x: 7.55, y: 2.2, w: 5.0, h: 2.0, fontSize: 12, color: DARK, isTextBox: true, lineSpacingMultiple: 1.25,
  });
  s.addShape("line", { x: 7.55, y: 4.35, w: 4.9, h: 0, line: { color: "E0E0D8", width: 1 } });
  s.addText("+ Loại 2 dòng ngoại lai (Id=524, 1299) khỏi train trước khi fit mô hình", { x: 7.55, y: 4.5, w: 4.9, h: 0.9, fontSize: 13, bold: true, color: RED, isTextBox: true, valign: "middle" });
  pageNum(s, 8);
}

// ---- Slide 9: Tien xu ly (2/2) - Hoc tu train ----
{
  const s = bgSlide("5. Tiền xử lý dữ liệu (2/2) — Học từ train");
  const steps2 = [
    ["LotFrontage", "Median-impute\n(học từ train)"],
    ["22 cột danh định", "One-Hot\nEncoding"],
    ["49 cột số", "StandardScaler\n(học từ train)"],
  ];
  steps2.forEach((st, i) => {
    const x = 0.6 + i * 4.1;
    s.addShape("roundRect", { x, y: 1.4, w: 3.7, h: 1.5, rectRadius: 0.1, fill: { color: "FFFFFF" }, line: { color: TEAL, width: 1.5 } });
    s.addText(st[0], { x, y: 1.5, w: 3.7, h: 0.5, align: "center", fontSize: 15, bold: true, color: TEAL, isTextBox: true });
    s.addText(st[1], { x, y: 2.0, w: 3.7, h: 0.8, align: "center", fontSize: 13, color: DARK, isTextBox: true });
    if (i < 2) arrowBetween(s, x + 3.7, 2.15, x + 4.1);
  });
  s.addShape("downArrow", { x: 6.0, y: 3.0, w: 0.3, h: 0.4, fill: { color: GOLD } });
  s.addShape("roundRect", { x: 3.5, y: 3.5, w: 6.3, h: 1.2, rectRadius: 0.1, fill: { color: "E8F5E9" }, line: { color: TEAL, width: 1.5 } });
  s.addText("205 đặc trưng sau mã hóa (49 số + 156 one-hot)", { x: 3.5, y: 3.65, w: 6.3, h: 0.5, align: "center", fontSize: 16, bold: true, color: TEAL, isTextBox: true });
  s.addText("→ dùng cho toàn bộ 5 cấu hình mô hình ở phần sau", { x: 3.5, y: 4.15, w: 6.3, h: 0.4, align: "center", fontSize: 12, italic: true, color: GRAY, isTextBox: true });

  s.addShape("roundRect", { x: 3.9, y: 5.0, w: 5.5, h: 1.4, rectRadius: 0.1, fill: { color: TEAL } });
  s.addText("✔ KIỂM CHỨNG: PASSED", { x: 3.9, y: 5.15, w: 5.5, h: 0.5, align: "center", fontSize: 18, bold: true, color: "FFFFFF", isTextBox: true });
  s.addText("Toàn bộ tham số impute/scale/one-hot chỉ học từ train — không rò rỉ", { x: 4.1, y: 5.65, w: 5.1, h: 0.65, align: "center", fontSize: 12, color: LIGHTTEAL, isTextBox: true });
  pageNum(s, 9);
}

// ---- Slide 10: Minh hoa Ridge ----
{
  const s = bgSlide("6. Mô hình hoạt động ra sao? — Ridge Regression");
  s.addText("Ý tưởng: phạt các hệ số lớn để tránh mô hình \"tự tin thái quá\" vào vài đặc trưng hiếm", {
    x: 0.6, y: 1.1, w: 12, h: 0.5, fontSize: 14, italic: true, color: GRAY, isTextBox: true,
  });
  // Left: Linear regression - large coefficients
  s.addShape("roundRect", { x: 0.6, y: 1.75, w: 5.8, h: 4.6, rectRadius: 0.1, fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 } });
  s.addText("Linear Regression (không phạt)", { x: 0.6, y: 1.9, w: 5.8, h: 0.4, align: "center", fontSize: 14, bold: true, color: RED, isTextBox: true });
  const badFeats = [["OverallQual", 0.35], ["Condition2=RRAe", 0.9], ["Exterior1st=BrkComm", 0.85], ["GrLivArea", 0.4]];
  badFeats.forEach((f, i) => {
    const y = 2.5 + i * 0.85;
    s.addText(f[0], { x: 0.9, y, w: 2.0, h: 0.4, fontSize: 11.5, color: DARK, isTextBox: true, valign: "middle" });
    s.addShape("rect", { x: 3.0, y: y + 0.08, w: f[1] * 2.8, h: 0.28, fill: { color: RED } });
  });
  s.addText("→ Hệ số bị \"giật\" bởi mức hạng mục chỉ có vài mẫu (phương sai cao)", { x: 0.9, y: 5.7, w: 5.2, h: 0.55, fontSize: 11.5, italic: true, color: GRAY, isTextBox: true });

  // Right: Ridge - shrunk coefficients
  s.addShape("roundRect", { x: 6.9, y: 1.75, w: 5.8, h: 4.6, rectRadius: 0.1, fill: { color: "FFFFFF" }, line: { color: "1B5E20", width: 1.5 } });
  s.addText("Ridge Regression (có phạt L2, α=30)", { x: 6.9, y: 1.9, w: 5.8, h: 0.4, align: "center", fontSize: 14, bold: true, color: "1B5E20", isTextBox: true });
  const goodFeats = [["OverallQual", 0.7], ["GrLivArea", 0.68], ["Neighborhood=Crawfor", 0.5], ["Condition2=RRAe", 0.05]];
  goodFeats.forEach((f, i) => {
    const y = 2.5 + i * 0.85;
    s.addText(f[0], { x: 7.2, y, w: 2.1, h: 0.4, fontSize: 11.5, color: DARK, isTextBox: true, valign: "middle" });
    s.addShape("rect", { x: 9.4, y: y + 0.08, w: f[1] * 2.5, h: 0.28, fill: { color: "1B5E20" } });
  });
  s.addText("→ Hệ số ổn định, khớp với hiểu biết miền (OverallQual/GrLivArea mạnh nhất)", { x: 7.2, y: 5.7, w: 5.2, h: 0.55, fontSize: 11.5, italic: true, color: GRAY, isTextBox: true });
  pageNum(s, 10);
}

// ---- Slide 11: Minh hoa XGBoost ----
{
  const s = bgSlide("6. Mô hình hoạt động ra sao? — XGBoost");
  s.addText("Ý tưởng: xây nhiều cây quyết định NHỎ tuần tự, mỗi cây sửa lỗi của các cây trước", {
    x: 0.6, y: 1.1, w: 12, h: 0.5, fontSize: 14, italic: true, color: GRAY, isTextBox: true,
  });
  const trees = ["Cây 1", "Cây 2", "Cây 3", "...", "Cây N"];
  const boxW = 1.9, gap = 0.55, startX = 0.7, y = 2.3;
  trees.forEach((t, i) => {
    const x = startX + i * (boxW + gap);
    s.addShape("roundRect", { x, y, w: boxW, h: 1.3, rectRadius: 0.1, fill: { color: "FFFFFF" }, line: { color: TEAL, width: 1.5 } });
    s.addText("🌳", { x, y: y + 0.05, w: boxW, h: 0.6, align: "center", fontSize: 24, isTextBox: true });
    s.addText(t, { x, y: y + 0.75, w: boxW, h: 0.45, align: "center", fontSize: 13, bold: true, color: TEAL, isTextBox: true });
    if (i < trees.length - 1) {
      arrowBetween(s, x + boxW, y + 0.65, x + boxW + gap);
      s.addText("sai số\ncòn lại", { x: x + boxW, y: y - 0.55, w: gap, h: 0.55, align: "center", fontSize: 9, color: GRAY, isTextBox: true });
    }
  });
  s.addShape("downArrow", { x: 6.2, y: 3.75, w: 0.3, h: 0.4, fill: { color: GOLD } });
  s.addShape("roundRect", { x: 3.9, y: 4.3, w: 5.5, h: 1.0, rectRadius: 0.1, fill: { color: "E8F5E9" }, line: { color: TEAL, width: 1.5 } });
  s.addText("Dự đoán cuối = Σ (dự đoán từng cây)", { x: 3.9, y: 4.3, w: 5.5, h: 1.0, align: "center", valign: "middle", fontSize: 16, bold: true, color: TEAL, isTextBox: true });
  s.addText("Siêu tham số quan trọng: số cây (n_estimators), độ sâu cây (max_depth), tốc độ học (learning_rate) — đã tinh chỉnh bằng RandomizedSearchCV (60 vòng, 5-fold CV trên train).", {
    x: 1.0, y: 5.6, w: 11.3, h: 1.0, align: "center", fontSize: 13, color: DARK, isTextBox: true, lineSpacingMultiple: 1.2,
  });
  pageNum(s, 11);
}

// ---- Slide 12: Mo hinh & thi nghiem (so sanh) ----
{
  const s = bgSlide("7. Thí nghiệm & So sánh mô hình");
  s.addImage({ path: "poster_assets/rmsle_compare.png", x: 0.5, y: 1.15, w: 6.5, h: 5.6 });
  s.addTable([
    [{ text: "Model", options: { bold: true, fill: { color: TEAL }, color: "FFFFFF" } }, { text: "RMSLE", options: { bold: true, fill: { color: TEAL }, color: "FFFFFF" } }],
    ["Hằng số (trung bình)", "0.4060"],
    ["XGBoost (mặc định)", "0.1267"],
    ["Linear Regression", "0.1143"],
    [{ text: "Ridge (α=30) — chọn", options: { bold: true } }, { text: "0.1155", options: { bold: true } }],
    ["XGBoost (đã tune)", "0.1245"],
  ], { x: 7.3, y: 1.4, w: 5.5, fontSize: 15, border: { type: "solid", color: "E0E0D8", pt: 1 }, rowH: 0.55 });
  s.addText("Vì sao chọn Ridge thay vì Linear Regression (RMSLE nhỉnh hơn)?", { x: 7.3, y: 4.9, w: 5.5, h: 0.5, fontSize: 14, bold: true, color: TEAL, isTextBox: true });
  s.addText("Linear Regression: hệ số bị chi phối bởi mức hạng mục hiếm (xem slide trước). Ridge: hệ số ổn định, khớp EDA — đánh đổi nhỏ về RMSLE lấy độ tin cậy.", {
    x: 7.3, y: 5.4, w: 5.5, h: 1.5, fontSize: 12.5, color: DARK, isTextBox: true, lineSpacingMultiple: 1.2,
  });
  pageNum(s, 12);
}

// ---- Slide 13: Ket qua cuoi ----
{
  const s = bgSlide("8. Kết quả cuối trên tập kiểm tra");
  s.addText("Test mở đúng 1 lần (219 mẫu, chưa từng dùng để chỉnh mô hình)", { x: 0.6, y: 1.1, w: 12, h: 0.4, fontSize: 14, italic: true, color: GRAY, isTextBox: true });
  const stats = [["0.1301", "RMSLE"], ["$14,280", "MAE"], ["0.943", "R²"]];
  stats.forEach((st, i) => {
    const x = 0.6 + i * 2.5;
    s.addShape("roundRect", { x, y: 1.6, w: 2.3, h: 1.5, rectRadius: 0.1, fill: { color: "FFFFFF" }, line: { color: TEAL, width: 1.5 } });
    s.addText(st[0], { x, y: 1.65, w: 2.3, h: 0.85, align: "center", fontSize: 30, bold: true, color: TEAL, isTextBox: true });
    s.addText(st[1], { x, y: 2.45, w: 2.3, h: 0.5, align: "center", fontSize: 13, color: GRAY, isTextBox: true });
  });
  s.addText("95% CI (bootstrap 1000 lần): [0.099, 0.159] — chồng lấp với val → không overfit nghiêm trọng", {
    x: 0.6, y: 3.25, w: 7, h: 1.3, fontSize: 13.5, color: DARK, isTextBox: true, lineSpacingMultiple: 1.2,
  });
  s.addText("So với tiêu chí thành công đã đề ra: RMSLE giảm từ 0.406 → 0.130 (giảm 68% so với baseline tầm thường).", {
    x: 0.6, y: 4.5, w: 7, h: 1.2, fontSize: 13.5, bold: true, color: "1B5E20", isTextBox: true, lineSpacingMultiple: 1.2,
  });
  s.addImage({ path: "poster_assets/test_scatter.png", x: 7.9, y: 1.5, w: 5.0, h: 5.0 });
  pageNum(s, 13);
}

// ---- Slide 14: Phan tich loi ----
{
  const s = bgSlide("9. Phân tích lỗi & Hạn chế");
  s.addShape("roundRect", { x: 0.6, y: 1.3, w: 12.1, h: 1.7, rectRadius: 0.1, fill: { color: "FFF3CD" }, line: { color: GOLD, width: 1 } });
  s.addText([
    { text: "6/10 ", options: { bold: true, fontSize: 26, color: "8A6D00" } },
    { text: "dự đoán sai nhiều nhất trên val đều có SaleCondition ≠ Normal (Abnorml/Partial)\n", options: { fontSize: 15, color: DARK } },
    { text: "Ca cực đoan: nhà $34,900 (rẻ nhất dataset, bán gấp) — dự đoán lệch 131%", options: { fontSize: 13.5, italic: true, color: GRAY } },
  ], { x: 0.9, y: 1.4, w: 11.5, h: 1.5, isTextBox: true, valign: "middle" });
  const limits = [
    ["Test chỉ 219 mẫu", "Khoảng tin cậy bootstrap còn khá rộng"],
    ["Bảng ánh xạ ordinal cố định", "Giá trị mới ngoài bảng sẽ gây lỗi thay vì âm thầm sai"],
    ["Chỉ 1 thành phố, 1 giai đoạn", "Ames, Iowa 2006–2010 — không đại diện thị trường khác"],
  ];
  limits.forEach((l, i) => {
    const y = 3.3 + i * 1.1;
    s.addShape("ellipse", { x: 0.6, y, w: 0.35, h: 0.35, fill: { color: TEAL } });
    s.addText("!", { x: 0.6, y, w: 0.35, h: 0.35, align: "center", valign: "middle", fontSize: 16, bold: true, color: "FFFFFF", isTextBox: true });
    s.addText(l[0], { x: 1.15, y: y - 0.05, w: 3.3, h: 0.5, fontSize: 14, bold: true, color: TEAL, isTextBox: true });
    s.addText(l[1], { x: 4.6, y: y - 0.05, w: 8.0, h: 0.5, fontSize: 13, color: DARK, isTextBox: true, valign: "middle" });
  });
  pageNum(s, 14);
}

// ---- Slide 15: Ket luan ----
{
  const s = bgSlide("Kết luận");
  s.addText([
    { text: "✔ ", options: { color: "1B5E20", bold: true, fontSize: 16 } },
    { text: "Xây dựng thành công pipeline dự đoán giá nhà với kiểm soát rò rỉ nghiêm ngặt qua toàn bộ vòng đời dữ liệu\n\n", options: { fontSize: 15.5, color: DARK } },
    { text: "✔ ", options: { color: "1B5E20", bold: true, fontSize: 16 } },
    { text: "Ridge Regression vượt trội XGBoost (kể cả đã tune) trên dữ liệu bảng quy mô nhỏ — hệ số ổn định, diễn giải được\n\n", options: { fontSize: 15.5, color: DARK } },
    { text: "✔ ", options: { color: "1B5E20", bold: true, fontSize: 16 } },
    { text: "RMSLE test = 0.1301, giảm 68% so với baseline\n\n", options: { fontSize: 15.5, color: DARK } },
    { text: "→ Hướng phát triển: ", options: { bold: true, fontSize: 15.5, color: TEAL } },
    { text: "đặc trưng tương tác với SaleCondition, stacking Ridge+XGBoost, nested cross-validation", options: { fontSize: 15.5, color: DARK } },
  ], { x: 0.7, y: 1.4, w: 11.9, h: 4.3, isTextBox: true, lineSpacingMultiple: 1.3 });
  s.addShape("line", { x: 0.7, y: 6.0, w: 11.9, h: 0, line: { color: "E0E0D8", width: 1 } });
  s.addText("Cảm ơn đã theo dõi — Huỳnh Kiện Khải", { x: 0.7, y: 6.2, w: 11.9, h: 0.5, fontSize: 16, italic: true, color: GRAY, align: "center", isTextBox: true });
  pageNum(s, 15);
}

pres.writeFile({ fileName: "Slide_HouseSalePrice.pptx" }).then(() => console.log("done"));
