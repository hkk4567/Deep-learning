#!/bin/bash
# Chạy lại toàn bộ thử nghiệm trên 3 seed (song song theo seed), rồi tổng hợp/chọn mô hình/vẽ hình.
# Dùng:  bash run_all_seeds.sh      (chạy từ thư mục gốc dự án; ~25-30 phút trên 2 CPU)
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python -m src.run_experiments --exp base            # mô hình chuẩn: tuần tự vì cùng ghi data/DataSet.csv
for s in 42 123 2024; do
  ( for e in A B C; do python -m src.run_experiments --exp $e --seeds $s; done ) &
done
wait
python -m src.summarize_seeds > logs/summarize_seeds.log
python -m src.select_model > logs/select_model.log
python -m src.plots > logs/plots.log
python -m src.diagram
