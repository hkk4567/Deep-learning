# Xấp xỉ hàm Gaussian 2D bằng MLP (PyTorch)

Bài tập lớn môn Học sâu — Huỳnh Kiện Khải (MSSV 3123411137). Nội dung lấy từ notebook `docs/BTL01_notebook_goc.ipynb`; code trong `src/` là code của notebook được tách thành module (giữ nguyên tên hàm/biến, cách viết, comment), chỉ đổi phần lưu/đọc file.
Hàm cần xấp xỉ: `y = 1/(2π√|C|) · exp(-½ (x-μ)ᵀ C⁻¹ (x-μ))`, μ = [0,0], C = [[0.3,-0.5],[-0.5,2]],
x1 ~ U(-2,2), x2 ~ U(-4,4).

## Cấu trúc thư mục
```
mlp_gaussian_approx/
├── requirements.txt, README.md
├── src/
│   ├── config.py           # hằng số: μ, C, seed, epochs, batch, lr, cấu hình A/B/C, đường dẫn tương đối
│   ├── data_gen.py         # sinh dữ liệu Gaussian, chia 10% test / 20% val / còn lại train, DataLoader
│   ├── model.py            # lớp MLP (Linear+ReLU, đầu ra Linear)
│   ├── train.py            # vòng huấn luyện, lưu checkpoint theo val MSE nhỏ nhất
│   ├── evaluate.py         # MSE / RMSE / MAE trên test bằng checkpoint tốt nhất
│   ├── run_experiments.py  # chạy base, A, B, C
│   ├── select_model.py     # chọn mô hình sai số nhỏ nhất trong A, B, C (theo val) và kiểm tra lại
│   ├── plots.py            # xuất hình + bảng giống notebook từ logs/ và results/
│   ├── diagram.py          # sơ đồ kiến trúc MLP (fig12)
│   ├── build_report.js     # dựng báo cáo Word từ results/ và figures/
│   └── build_slides.js     # dựng slide .pptx từ results/ và figures/
├── data/DataSet.csv        # 1000 mẫu của mô hình chuẩn (x1, x2, y_real)
├── logs/                   # history_<tag>.csv (epoch, train_mse, val_mse) + run_all.log
├── results/                # base/expA/expB/expC_results.csv, table_*.csv, selected_model.json
├── figures/                # fig01..fig14 (.png)
├── weights/                # best_<tag>.pt từng cấu hình; selected_model.pt = kiến trúc được chọn
└── docs/                   # báo cáo .docx/.pdf, slide .pptx/.pdf, notebook gốc, LOG.md
```

## Cài đặt và chạy lại từ đầu
```bash
pip install -r requirements.txt
python -m src.run_experiments --exp all    # base + A + B + C (~12 phút trên CPU)
python -m src.select_model                 # chọn mô hình tốt nhất trong A, B, C + kiểm tra
python -m src.plots                        # xuất hình/bảng
python -m src.diagram                      # sơ đồ kiến trúc của mô hình được chọn
node src/build_report.js                   # báo cáo .docx (cần: npm i docx)
node src/build_slides.js                   # slide .pptx (cần: npm i pptxgenjs)
```
Chạy riêng từng thí nghiệm: `--exp base | A | B | C`. Chạy thử nhanh: thêm `--epochs 20`. Chạy từ thư mục gốc dự án.

## Thiết lập (theo notebook)
Seed 42; Adam, lr = 0.002; ReLU; MSE loss; 1000 epoch; batch 32 (mô hình chuẩn dùng full-batch 720 mẫu).
- **Mô hình chuẩn:** 1000 mẫu riêng (`DataSet.csv`), 1 tầng ẩn × 3 neuron.
- **A:** 1 tầng ẩn × 3 neuron; n ∈ {278,…,2778} mẫu từ bộ 3000 mẫu → train 200…2000.
- **B:** 1000 mẫu; 1 tầng ẩn, B = 1…10 neuron.
- **C:** 1000 mẫu; C = 1…4 tầng ẩn, mỗi tầng 3 neuron.
- Checkpoint chọn theo val MSE nhỏ nhất; mô hình được chọn theo val MSE nhỏ nhất trong cả A, B, C (`src/select_model.py`, kèm kiểm tra tái lập và rò rỉ dữ liệu).
