const pptxgen = require("pptxgenjs");

const TEAL = "0E5C4A";
const GOLD = "E6A700";
const CREAM = "FBF7EE";
const DARK = "1F2A1F";
const GRAY = "6B6B6B";

function newDeck() {
  const p = new pptxgen();
  p.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
  return p;
}
const pres = newDeck();

function bgSlide(title) {
  const s = pres.addSlide();
  s.background = { color: CREAM };
  s.addShape("rect", { x: 0, y: 0, w: 13.33, h: 0.9, fill: { color: TEAL } });
  s.addText(title, { x: 0.5, y: 0.12, w: 12.3, h: 0.65, fontFace: "Calibri", fontSize: 26, bold: true, color: "FFFFFF", isTextBox: true, valign: "middle" });
  s.addShape("ellipse", { x: 12.7, y: 0.15, w: 0.35, h: 0.35, fill: { color: GOLD } });
  return s;
}
function pageNum(s, n) {
  s.addText(String(n), { x: 12.85, y: 7.15, w: 0.4, h: 0.3, fontSize: 10, color: GRAY, align: "right", isTextBox: true });
}

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
    x: 0.7, y: 3.5, w: 11.5, h: 0.6, fontFace: "Calibri", fontSize: 20, color: "CDE7C4", isTextBox: true,
  });
  s.addShape("line", { x: 0.72, y: 4.35, w: 1.4, h: 0, line: { color: GOLD, width: 3 } });
  s.addText("Huỳnh Kiện Khải", { x: 0.7, y: 5.0, w: 8, h: 0.4, fontSize: 18, bold: true, color: "FFFFFF", isTextBox: true });
  s.addText("Khoa Công nghệ Thông tin — Trường Đại học Sài Gòn", { x: 0.7, y: 5.4, w: 8, h: 0.4, fontSize: 14, color: "CDE7C4", isTextBox: true });
}

// ---- Slide 2: Agenda ----
{
  const s = bgSlide("Nội dung trình bày");
  const items = [
    "1. Giới thiệu bài toán", "2. Dữ liệu & Kiểm toán", "3. Khám phá dữ liệu (EDA)",
    "4. Lựa chọn đặc trưng", "5. Tiền xử lý dữ liệu", "6. Mô hình & Thí nghiệm",
    "7. Kết quả cuối trên tập kiểm tra", "8. Phân tích lỗi & Hạn chế", "9. Kết luận",
  ];
  items.forEach((t, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.6 + col * 4.1, y = 1.4 + row * 1.7;
    s.addShape("roundRect", { x, y, w: 3.7, h: 1.35, rectRadius: 0.1, fill: { color: "FFFFFF" }, line: { color: "E0E0D8", width: 1 } });
    s.addShape("ellipse", { x: x + 0.2, y: y + 0.2, w: 0.5, h: 0.5, fill: { color: TEAL } });
    s.addText(String(i + 1), { x: x + 0.2, y: y + 0.2, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: "FFFFFF", isTextBox: true });
    s.addText(t.replace(/^\d+\.\s*/, ""), { x: x + 0.85, y: y + 0.15, w: 2.7, h: 1.05, fontSize: 14, bold: true, color: DARK, valign: "middle", isTextBox: true, margin: 0 });
  });
  pageNum(s, 2);
}

// ---- Slide 3: Gioi thieu ----
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
  pageNum(s, 3);
}

// ---- Slide 4: Du lieu ----
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
    [{ text: "Cột", options: { bold: true, fill: { color: "CDE7C4" } } }, { text: "% thiếu", options: { bold: true, fill: { color: "CDE7C4" } } }, { text: "Ý nghĩa", options: { bold: true, fill: { color: "CDE7C4" } } }],
    ["PoolQC", "99.4%", "Không có hồ bơi"],
    ["MiscFeature", "96.0%", "Không có tiện ích đặc biệt"],
    ["Alley", "93.4%", "Không có lối hẻm"],
    ["MasVnrType", "59.2%", "Không ốp mặt tiền"],
  ], { x: 6.8, y: 1.8, w: 5.9, fontSize: 12.5, border: { type: "solid", color: "E0E0D8", pt: 1 }, rowH: 0.4 });
  s.addShape("roundRect", { x: 6.8, y: 4.3, w: 5.9, h: 1.4, rectRadius: 0.08, fill: { color: "FFF3CD" }, line: { color: GOLD, width: 1 } });
  s.addText("Phần lớn missing mang tính \"ngữ nghĩa\" (nhà không có đặc điểm đó), không phải lỗi nhập liệu — quyết định: điền giá trị 0/\"None\", không dùng median/mode mặc định.", {
    x: 7.0, y: 4.4, w: 5.5, h: 1.2, fontSize: 13, color: DARK, isTextBox: true, valign: "middle",
  });
  pageNum(s, 4);
}

// ---- Slide 5: EDA ----
{
  const s = bgSlide("3. Khám phá dữ liệu (chỉ trên train)");
  s.addImage({ path: "poster_assets/n3.png", x: 0.5, y: 1.15, w: 7.3, h: 5.6 });
  s.addText([
    { text: "Phát hiện chính\n\n", options: { bold: true, fontSize: 17, color: TEAL } },
    { text: "• SalePrice lệch phải (skew=1.73) → log1p còn 0.15\n\n", options: { fontSize: 14 } },
    { text: "• Top tương quan: OverallQual (0.79), GrLivArea (0.69), GarageCars (0.64)\n\n", options: { fontSize: 14 } },
    { text: "• ExterQual, FireplaceQu: bậc thang tăng rõ theo chất lượng\n\n", options: { fontSize: 14 } },
    { text: "• Phát hiện 2 ngoại lai đã biết của dataset (GrLivArea lớn, giá thấp bất thường, Partial sale)", options: { fontSize: 14 } },
  ], { x: 8.1, y: 1.3, w: 4.7, h: 5, color: DARK, isTextBox: true, lineSpacingMultiple: 1.2 });
  pageNum(s, 5);
}

// ---- Slide 6: Lua chon dac trung ----
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
  pageNum(s, 6);
}

// ---- Slide 7: Tien xu ly ----
{
  const s = bgSlide("5. Tiền xử lý dữ liệu");
  s.addTable([
    [{ text: "Bước", options: { bold: true, fill: { color: TEAL }, color: "FFFFFF" } }, { text: "Xử lý", options: { bold: true, fill: { color: TEAL }, color: "FFFFFF" } }],
    ["18 cột chất lượng", "Ordinal encode: Po<Fa<TA<Gd<Ex..."],
    ["MasVnrArea, GarageYrBlt", "Điền 0 khi thiếu (không tồn tại)"],
    ["LotFrontage", "Median-impute — học từ train"],
    ["22 cột danh định", "One-Hot Encoding"],
    ["49 cột số", "StandardScaler — học từ train"],
  ], { x: 0.6, y: 1.25, w: 7.1, fontSize: 14, border: { type: "solid", color: "E0E0D8", pt: 1 }, rowH: 0.48 });
  s.addShape("roundRect", { x: 8.0, y: 1.25, w: 4.7, h: 2.1, rectRadius: 0.1, fill: { color: "E8F5E9" }, line: { color: TEAL, width: 1.5 } });
  s.addText([
    { text: "Kiểm chứng không rò rỉ\n", options: { bold: true, fontSize: 15, color: TEAL } },
    { text: "PASSED\n", options: { bold: true, fontSize: 28, color: "1B5E20" } },
    { text: "Toàn bộ tham số (impute, scale, one-hot) chỉ học từ train", options: { fontSize: 12.5, color: DARK } },
  ], { x: 8.2, y: 1.4, w: 4.3, h: 1.9, align: "center", isTextBox: true });
  s.addShape("roundRect", { x: 8.0, y: 3.6, w: 4.7, h: 1.6, rectRadius: 0.1, fill: { color: "FFFFFF" }, line: { color: "E0E0D8", width: 1 } });
  s.addText([
    { text: "205\n", options: { bold: true, fontSize: 32, color: TEAL } },
    { text: "đặc trưng sau mã hóa\n(49 số + 156 one-hot)", options: { fontSize: 13, color: GRAY } },
  ], { x: 8.0, y: 3.7, w: 4.7, h: 1.4, align: "center", isTextBox: true });
  pageNum(s, 7);
}

// ---- Slide 8: Mo hinh & thi nghiem ----
{
  const s = bgSlide("6. Mô hình & Thí nghiệm");
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
  s.addText("Linear Regression: hệ số bị chi phối bởi mức hạng mục hiếm (phương sai cao). Ridge (regularization): hệ số ổn định, OverallQual/GrLivArea lên top đầu — khớp EDA.", {
    x: 7.3, y: 5.4, w: 5.5, h: 1.5, fontSize: 12.5, color: DARK, isTextBox: true, lineSpacingMultiple: 1.2,
  });
  pageNum(s, 8);
}

// ---- Slide 9: Ket qua cuoi ----
{
  const s = bgSlide("7. Kết quả cuối trên tập kiểm tra");
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
  pageNum(s, 9);
}

// ---- Slide 10: Phan tich loi ----
{
  const s = bgSlide("8. Phân tích lỗi & Hạn chế");
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
  pageNum(s, 10);
}

// ---- Slide 11: Ket luan ----
{
  const s = bgSlide("9. Kết luận");
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
  pageNum(s, 11);
}

pres.writeFile({ fileName: "Slide_HouseSalePrice.pptx" }).then(() => console.log("done"));
