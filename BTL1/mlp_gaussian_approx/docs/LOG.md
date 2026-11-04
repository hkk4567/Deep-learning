# LOG file sinh ra (làm lại theo notebook, 2026-10-25)

| Ngày | Giai đoạn | File | Đường dẫn | Nội dung | Script sinh ra |
|---|---|---|---|---|---|
| 2026-10-25 | Dữ liệu | DataSet.csv | data/ | 1000 mẫu của mô hình chuẩn (seed 42) | src/run_experiments.py (gọi src/data_gen.py) |
| 2026-10-25 | Huấn luyện | history_<tag>.csv | logs/ | train/val MSE từng epoch của mỗi cấu hình | src/run_experiments.py → src/train.py |
| 2026-10-25 | Huấn luyện | best_<tag>.pt | weights/ | checkpoint val MSE nhỏ nhất của từng cấu hình | src/run_experiments.py |
| 2026-10-25 | Chọn mô hình | selected_model.pt, selected_model.json, selection_check.json, table_selection.csv | weights/, results/ | mô hình sai số nhỏ nhất trong A, B, C (C3 = [3,3,3]) và kết quả kiểm tra | src/select_model.py |
| 2026-10-25 | Kết quả | base/expA/expB/expC_results.csv, selected_model.json | results/ | số liệu từng cấu hình | src/run_experiments.py |
| 2026-10-25 | Kết quả | table_*.csv | results/ | bảng như notebook (A, B, C) và kiến trúc được chọn | src/plots.py |
| 2026-10-25 | Hình | fig01…fig11, fig13, fig14 (.png) | figures/ | dữ liệu, A/B/C, learning curve, minh họa mô hình chuẩn và mô hình được chọn | src/plots.py |
| 2026-10-25 | Hình | fig12_mlp_architecture.png | figures/ | sơ đồ kiến trúc mô hình được chọn (2-3-3-3-1, kích thước lớp, 37 tham số) | src/diagram.py |
| 2026-10-25 | Log chạy | run_all.log | logs/ | stdout của `python -m src.run_experiments --exp all` | lệnh chạy |
| 2026-10-25 | Báo cáo | BaoCao_BTL01_HuynhKienKhai_3123411137.docx / .pdf | docs/ | báo cáo 14 trang (14 hình, 5 bảng) | src/build_report.js (+ soffice ra PDF) |
| 2026-10-25 | Slide | Slide_BTL01_HuynhKienKhai_3123411137.pptx / .pdf | docs/ | 13 slide, biểu đồ A/B/C là chart gốc của PowerPoint | src/build_slides.js (+ soffice ra PDF) |
| — | Tham khảo | BTL01_notebook_goc.ipynb | docs/ | notebook gốc (không sửa) | — |

## Ghi chú
- Nội dung bám notebook. Đã bỏ các phần mình tự thêm ở bản trước: thí nghiệm A với val/test cố định, hình "mức phẳng" của A, bảng so sánh cùng số tham số, bảng thống kê mô tả, cột số tham số.
- Quyết định của chủ dự án: A dùng cách chia của notebook; lr = 0.002 theo code; batch size giữ nguyên.
- Khác biệt so với notebook buộc phải có để tái lập: bộ 1000 mẫu của mô hình chuẩn (notebook không đặt seed khi sinh) nay dùng seed 42, nên số liệu mô hình chuẩn khác bản notebook; số liệu A, B, C trùng notebook (một ô A=1600 lệch nhỏ).
- Phần đề yêu cầu nhưng notebook chưa có: sơ đồ kiến trúc (fig12), chọn kiến trúc theo val MSE (selected_model.pt) và hình minh họa cho kiến trúc được chọn (fig13, fig14).
- 2026-10-25 (theo yêu cầu): chọn mô hình có sai số nhỏ nhất trong cả A, B, C bằng src/select_model.py (bước chọn này không còn nằm trong run_experiments.py). Kết quả: A→A1800 (val 9.15e-4), B→B9 (8.30e-5), C→C3 (1.22e-5); chọn C3, cũng là mô hình có test MSE nhỏ nhất. Kiểm tra lại đạt cả 8 mục (tái lập val/test, train-val-test không giao nhau, số tham số 37, dự đoán hữu hạn).
- Sơ đồ kiến trúc vẽ lại theo mô hình được chọn.
- Thứ tự chạy: run_experiments → select_model → plots → diagram → build_report/build_slides.

## 2026-10-28 — Viết lại src/ theo đúng code notebook
- Viết lại config, data_gen, model, train, evaluate, run_experiments, plots, select_model: copy hàm từ notebook (Gaussian_2D, gen_data_set, MLP(hiden_sizes), Train, evaluate, data_split_and_to_tensor, exp_A, exp_B, exp_c, các đoạn vẽ hình/bảng), thụt 2 space, comment tiếng Việt như notebook. diagram.py giữ nguyên.
- Chỉ đổi: (1) lưu checkpoint vào weights/best_<tag>.pt thay cho best_*.pth; (2) tên file A theo số mẫu train (best_A200.pt…) như bản trước; (3) thêm .to(device) cho batch trong Train; (4) thêm lưu history/results ra logs/, results/ để plots.py và select_model.py dùng lại; (5) plt.show() → lưu hình vào figures/; (6) thêm `import torch` trong train.py, weights_only=True khi nạp checkpoint; (7) DataSet.csv lưu float64 như notebook (giá trị float32 không đổi); (8) tham số --epochs cho chạy thử nhanh.
- Chạy lại toàn bộ `python -m src.run_experiments --exp all` → select_model → plots → diagram: base/A/B/C và mô hình được chọn (C3) trùng 100% bản trước (sai khác tối đa 0.0 ở best_epoch, train/val/test MSE, RMSE, MAE; table_*.csv cùng cột và số). Thời gian huấn luyện (C) đo lại nên khác.
- Script sinh file: logs/history_*.csv, results/*_results.csv, weights/best_*.pt ← src/run_experiments.py; table_*.csv, fig01–fig11, fig13–fig14 ← src/plots.py; selected_model.*, selection_check.json, table_selection.csv ← src/select_model.py; fig12 ← src/diagram.py; log chạy ← logs/run_all.log, select_model.log, plots.log.

## 2026-10-28 — Làm lại báo cáo (bước 2)
- Dựng lại BaoCao_BTL01_HuynhKienKhai_3123411137.docx / .pdf (15 trang, 14 hình, 5 bảng) bằng src/build_report.js (+ soffice ra PDF); số liệu và hình đọc trực tiếp từ results/ và figures/ của lần chạy mới.
- Nội dung, cấu trúc mục giữ như bản trước (bám notebook). Khác bản trước: các đoạn mã ở mục 3.4 là code notebook (hiden_sizes, Train, evaluate), hình vẽ lại bằng code notebook, thời gian huấn luyện C là số đo của lần chạy mới (16.76 / 18.14 / 20.97 / 25.12 s), các số còn lại không đổi.
- Lệnh: `node src/build_report.js` (cần `npm i docx`) rồi `soffice --headless --convert-to pdf --outdir docs docs/BaoCao_BTL01_HuynhKienKhai_3123411137.docx`.

## 2026-10-28 — Làm lại slide (bước 3)
- Dựng lại Slide_BTL01_HuynhKienKhai_3123411137.pptx / .pdf (13 slide, 3 biểu đồ A/B/C là chart gốc của PowerPoint, có ghi chú người nói) bằng src/build_slides.js (+ soffice ra PDF). Số liệu và hình đọc từ results/ và figures/ của lần chạy mới; mã ở slide 5 là code Train của notebook.
- Bố cục và nội dung bám bản slide trước; số liệu giống bản trước, riêng thời gian huấn luyện C là số đo của lần chạy mới.
- Lệnh: `node src/build_slides.js` (cần `npm i pptxgenjs`; nếu có file apply_theme.js của skill pptx thì đặt đường dẫn vào biến APPLY_THEME để ghi màu theme) rồi `soffice --headless --convert-to pdf --outdir docs docs/Slide_BTL01_HuynhKienKhai_3123411137.pptx`.

## 2026-11-04 — Tìm learning rate, bước 1: LR range test
- Mục tiêu: khoanh vùng lr cho Adam trên mô hình chuẩn (base: hiden_sizes=[3], 720 train/180 val, full-batch → 1 step = 1 epoch). Lý do chọn base: là mốc chung của A/B/C nên dùng 1 lr cho cả ba thì so sánh công bằng; C3 sẽ kiểm chứng lại ở bước sau.
- Thêm src/lr_range_test.py: lr tăng theo hàm mũ 1e-5 → 1 trong 400 step, 3 seed (42, 43, 44), ghi train/val loss mỗi step; tìm 3 điểm đặc trưng trên loss đã làm mượt (dốc nhất, loss thấp nhất, điểm phân kỳ).
- Kết quả: lr dốc nhất (seed 42/43/44) = 2.55e-3 / 2.02e-3 / 3.71e-3; loss không phân kỳ đến lr=1 (Adam, MLP nhỏ); val loss giảm mạnh trong khoảng ~3e-3 → 3e-2 rồi đi ngang quanh 2.5e-3 – 3e-3.
- Script sinh file: figures/fig15_lr_range_test.png, results/lr_range_test.json, logs/lr_range_test_history.csv ← src/lr_range_test.py.
- Lệnh: `python -m src.lr_range_test` (thêm `--steps 50 --seeds 42` để chạy thử nhanh). Cần torch (đã có trong requirements.txt).
