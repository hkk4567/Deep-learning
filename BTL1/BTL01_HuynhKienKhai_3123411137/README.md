# Xấp xỉ hàm Gaussian 2D bằng MLP (PyTorch)

Bài tập lớn môn Học sâu — Huỳnh Kiện Khải (MSSV 3123411137). Nội dung lấy từ notebook `docs/BTL01_notebook_goc.ipynb`; code trong `src/` là code của notebook được tách thành module (giữ nguyên tên hàm/biến, cách viết, comment), chỉ đổi phần lưu/đọc file.
Hàm cần xấp xỉ: `y = 1/(2π√|C|) · exp(-½ (x-μ)ᵀ C⁻¹ (x-μ))`, μ = [0,0], C = [[0.3,-0.5],[-0.5,2]],
x1 ~ U(-2,2), x2 ~ U(-4,4).

## Cấu trúc thư mục
```
mlp_gaussian_approx/
├── requirements.txt, README.md
├── src/
│   ├── config.py           # hằng số: μ, C, seed, epochs, batch, lr, cấu hình A/B/C (A: train 200…2000), SEEDS, đường dẫn tương đối
│   ├── data_gen.py         # sinh dữ liệu Gaussian, chia 10% test / 20% val / còn lại train, DataLoader
│   ├── model.py            # lớp MLP (Linear+ReLU, đầu ra Linear)
│   ├── train.py            # vòng huấn luyện, lưu checkpoint theo val MSE nhỏ nhất
│   ├── evaluate.py         # MSE / RMSE / MAE trên test bằng checkpoint tốt nhất
│   ├── run_experiments.py  # chạy base, A, B, C
│   ├── summarize_seeds.py  # tổng hợp mean ± std qua 3 seed, vẽ fig15–fig17
│   ├── select_model.py     # chọn mô hình sai số nhỏ nhất trong A, B, C (theo val) và kiểm tra lại
│   ├── plots.py            # xuất hình + bảng giống notebook từ logs/ và results/
│   ├── diagram.py          # sơ đồ kiến trúc MLP (fig12)
├── data/DataSet.csv        # 1000 mẫu của mô hình chuẩn (x1, x2, y_real)
├── logs/                   # log theo thí nghiệm và theo seed
│   ├── base_log/seed_<s>/  #   history_base.csv + run.log
│   ├── expA_log/seed_<s>/  #   history_A<n>.csv (epoch, train_mse, val_mse) + run.log
│   ├── expB_log/seed_<s>/, expC_log/seed_<s>/   (tương tự)
├── results/                # expA/B/C, base _results.csv (seed 42 = kết quả chính), table_*.csv, selected_model.json
│   ├── seeds/              #   <exp>_results_seed<s>.csv của từng seed
│   └── seeds_summary_*.csv, seeds_best_config.csv   # mean ± std qua 3 seed
├── figures/                # fig01..fig14 (seed 42) + fig15–fig17 (3 seed, mean ± std)
├── weights/                # trọng số theo thí nghiệm và theo seed
│   ├── base_weight/seed_<s>/best_base.pt
│   ├── expA_weight/seed_<s>/best_A<n>.pt, expB_weight/…/best_B<n>.pt, expC_weight/…/best_C<n>.pt
│   └── selected_model.pt   #   kiến trúc được chọn (từ seed chính 42)
└── docs/                   # báo cáo .docx/.pdf, slide .pptx/.pdf, notebook gốc
```

## Cài đặt và chạy lại từ đầu
```bash
pip install -r requirements.txt
python -m src.run_experiments --exp all    # base + A + B + C, lần lượt 3 seed 42/123/2024 (~12 phút/seed trên CPU)
python -m src.summarize_seeds              # bảng mean ± std qua 3 seed + fig15–fig17
python -m src.select_model                 # chọn mô hình tốt nhất trong A, B, C + kiểm tra
python -m src.plots                        # xuất hình/bảng
python -m src.diagram                      # sơ đồ kiến trúc của mô hình được chọn
```
Chạy riêng từng thí nghiệm: `--exp base | A | B | C`; chọn seed: `--seeds 42 123 2024` (mặc định là `SEEDS` trong `src/config.py`). Chạy thử nhanh: thêm `--epochs 20`. Chạy từ thư mục gốc dự án.

## Thiết lập 
Seed 42; Adam, lr = 0.002; ReLU; MSE loss; 1000 epoch; batch 32 (mô hình chuẩn dùng full-batch 720 mẫu).
- **Mô hình chuẩn:** 1000 mẫu riêng (`DataSet.csv`), 1 tầng ẩn × 3 neuron.
- **A:** 1 tầng ẩn × 3 neuron; train = 200…2000 mẫu lấy từ phần còn lại của bộ 3000 mẫu (mẫu thứ 1000 trở đi); val (180) và test (100) cố định, chia từ 1000 mẫu đầu giống B, C nên mọi điểm của A so sánh trực tiếp được (và so được với B, C).
- **B:** 1000 mẫu; 1 tầng ẩn, B = 1…10 neuron.
- **C:** 1000 mẫu; C = 1…4 tầng ẩn, mỗi tầng 3 neuron.
- Checkpoint chọn theo val MSE nhỏ nhất; mô hình được chọn theo val MSE nhỏ nhất trong cả A, B, C (`src/select_model.py`, kèm kiểm tra tái lập và rò rỉ dữ liệu).

## Thử nghiệm trên 3 seed
- Seed ∈ {42, 123, 2024} quyết định khởi tạo trọng số (`torch.manual_seed(seed)`) và thứ tự shuffle của DataLoader. Dữ liệu và cách chia train/val/test giữ cố định (seed 42) nên chỉ đo độ nhạy với khởi tạo/huấn luyện.
- Seed 42 là kết quả chính: ghi vào `results/*_results.csv`, dùng cho `plots.py`, `select_model.py` và báo cáo/slide (trùng kết quả trước khi thêm 3 seed).
- Tổng hợp: `results/seeds_summary_{base,A,B,C}.csv` (mean/std từng cấu hình), `results/seeds_best_config.csv` (cấu hình tốt nhất theo val ở từng seed), hình `fig15`–`fig17`.
