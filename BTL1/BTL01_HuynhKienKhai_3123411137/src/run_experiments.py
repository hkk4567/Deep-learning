# Chạy thí nghiệm theo notebook: base (mô hình chuẩn), A (số mẫu), B (số perceptron), C (số hiden layer)
# python -m src.run_experiments --exp all
# python -m src.run_experiments --exp B --epochs 50      # chạy thử nhanh
# python -m src.run_experiments --exp all --seeds 42 123 2024   # 3 seed (mặc định = SEEDS trong config.py)
import argparse
import contextlib
import sys
import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from .config import device, RESULT_DIR, SEED_DIR, SEEDS, SEED_CHINH, weight_dir, log_dir, cau_hinh_data, cau_hinh_perceptron, cau_hinh_hiden_layer
from .data_gen import tao_data_chuan, chia_data_chuan, chuyen_tensor_chuan, data_split_and_to_tensor, data_A, tao_data_thi_nghiem
from .model import MLP
from .train import Train
from .evaluate import evaluate, to_float


# 1. Mô hình chuẩn: 1000 mẫu (DataSet.csv), 1 hiden layer, 3 perceptron, batch = toàn bộ train
def exp_base(seed = 42, epochs = 1000):
  tao_data_chuan()
  X_train, X_val, X_test, y_train, y_val, y_test = chia_data_chuan()
  X_train_tensor, y_train_tensor, X_val_tensor, y_val_tensor, X_test_tensor, y_test_tensor, train_loader = chuyen_tensor_chuan(X_train, X_val, X_test, y_train, y_val, y_test)

  # cấu hình model tiêu chuẩn
  torch.manual_seed(seed)
  model = MLP(hiden_sizes = [3]).to(device)
  criterion = nn.MSELoss()
  optimizer = torch.optim.Adam(model.parameters(), lr=0.002)

  file = weight_dir("base", seed) / "best_base.pt"
  output = Train(train_loader, X_val_tensor, y_val_tensor, model, optimizer, criterion, file, epochs)
  output.update(evaluate(model, file, X_test_tensor, y_test_tensor))
  output["hiden_sizes"] = [3]
  output["n_train"], output["n_val"], output["n_test"] = len(y_train_tensor), len(y_val_tensor), len(y_test_tensor)
  return output


# Thí nghiệm A: hiden layer = 1, perceptron = 3, n = số mẫu train (val và test cố định)
def exp_A(n, X_all, y_all, seed = 42, epochs = 1000):
  # khai báo tham số model
  torch.manual_seed(seed)
  model_expA = MLP().to(device)
  criterion_expA = nn.MSELoss()
  optimizer_expA = torch.optim.Adam(model_expA.parameters(), lr=0.002)

  # chuẩn bị và chia dữ liệu: n = số mẫu train; val và test cố định như B, C
  X_train_tensor, y_train_tensor, X_val_tensor, y_val_tensor, X_test_tensor, y_test_tensor, train_loader = data_A(X_all, y_all, n)

  # huấn luyện và đánh giá lưu vào output(map) dùng để vẽ
  file = weight_dir("A", seed) / f"best_A{len(y_train_tensor)}.pt" # tên file theo A = số mẫu train
  output = Train(train_loader, X_val_tensor, y_val_tensor, model_expA, optimizer_expA, criterion_expA, file, epochs)
  output.update(evaluate(model_expA, file, X_test_tensor, y_test_tensor))
  output["A"] = len(y_train_tensor)
  output["total_data"] = len(y_train_tensor) + len(y_val_tensor) + len(y_test_tensor)
  output["hiden_sizes"] = [3]
  output["n_train"], output["n_val"], output["n_test"] = len(y_train_tensor), len(y_val_tensor), len(y_test_tensor)
  return output


# Thí nghiệm B: 1000 mẫu, 1 hiden layer, thay đổi số perceptron
def exp_B(n, data_B, seed = 42, epochs = 1000):
  X_train_tensor_B, y_train_tensor_B, X_val_tensor_B, y_val_tensor_B, X_test_tensor_B, y_test_tensor_B, train_loader_B = data_B
  data_ = 1000
  # khai báo tham số model
  torch.manual_seed(seed)
  model_expB = MLP(hiden_sizes = [n]).to(device)
  criterion_expB = nn.MSELoss()
  optimizer_expB = torch.optim.Adam(model_expB.parameters(), lr=0.002)

  # huấn luyện và đánh giá lưu vào output(map) dùng để vẽ
  file = weight_dir("B", seed) / f"best_B{n}.pt"
  output = Train(train_loader_B, X_val_tensor_B, y_val_tensor_B, model_expB, optimizer_expB, criterion_expB, file, epochs)
  output.update(evaluate(model_expB, file, X_test_tensor_B, y_test_tensor_B))
  output["B"] = n
  output["total_data"] = data_
  output["hiden_sizes"] = [n]
  output["n_train"], output["n_val"], output["n_test"] = len(y_train_tensor_B), len(y_val_tensor_B), len(y_test_tensor_B)
  return output


# Thí nghiệm C: 1000 mẫu, mỗi hiden layer 3 perceptron, thay đổi số hiden layer
def exp_c(n, data_C, seed = 42, epochs = 1000):
  X_train_tensor_C, y_train_tensor_C, X_val_tensor_C, y_val_tensor_C, X_test_tensor_C, y_test_tensor_C, train_loader_C = data_C
  data_ = 1000
  # khai báo tham số model
  torch.manual_seed(seed)
  hiden_sizes = []
  for i in range(n):
    hiden_sizes.append(3)

  model_expC = MLP(hiden_sizes = hiden_sizes).to(device)
  criterion_expC = nn.MSELoss()
  optimizer_expC = torch.optim.Adam(model_expC.parameters(), lr=0.002)

  # huấn luyện và đánh giá lưu vào output(map) dùng để vẽ
  file = weight_dir("C", seed) / f"best_C{n}.pt"

  # đo thời gian
  start_time = time.perf_counter()

  output = Train(train_loader_C, X_val_tensor_C, y_val_tensor_C, model_expC, optimizer_expC, criterion_expC, file, epochs)

  train_time = time.perf_counter() - start_time

  output.update(evaluate(model_expC, file, X_test_tensor_C, y_test_tensor_C))
  output["C"] = n
  output["total_data"] = data_
  output["train_time_sec"] = train_time
  output["hiden_sizes"] = hiden_sizes
  output["n_train"], output["n_val"], output["n_test"] = len(y_train_tensor_C), len(y_val_tensor_C), len(y_test_tensor_C)
  return output


# lưu history (train/val MSE từng epoch) và bảng kết quả ra file để vẽ hình, chọn mô hình về sau
def luu_ket_qua(res, ten_cot, ten_file, exp, seed):
  rows = []
  for r in res:
    tag = f"{ten_cot}{r[ten_cot]}" if ten_cot else "base"
    train_history = [to_float(v) for v in r["history"]["train"]]
    val_history = [to_float(v) for v in r["history"]["val"]]
    pd.DataFrame({
        "epoch": range(1, len(train_history) + 1),
        "train_mse": train_history,
        "val_mse": val_history
    }).to_csv(log_dir(exp, seed) / f"history_{tag}.csv", index=False)

    best_idx = int(r["best_epoch"]) - 1
    row = {
        "tag": tag,
        "hidden_sizes": str(list(r["hiden_sizes"])),
        "n_train": r["n_train"],
        "n_val": r["n_val"],
        "n_test": r["n_test"],
        "best_epoch": int(r["best_epoch"]),
        "train_mse": train_history[best_idx],
        "val_mse": r["best_val_loss"],
        "test_mse": to_float(r["test_mse"]),
        "test_rmse": to_float(r["test_rmse"]),
        "test_mae": to_float(r["test_mae"]),
    }
    if "train_time_sec" in r:
      row["train_time_sec"] = r["train_time_sec"]
    if ten_cot:
      row[ten_cot] = r[ten_cot]
    row["seed"] = seed
    rows.append(row)
  df = pd.DataFrame(rows)
  df.to_csv(SEED_DIR / ten_file.replace(".csv", f"_seed{seed}.csv"), index=False)  # kết quả của từng seed
  if seed == SEED_CHINH:  # seed chính (42) cũng ghi vào results/ để plots.py, select_model.py dùng như cũ
    df.drop(columns="seed").to_csv(RESULT_DIR / ten_file, index=False)


# vừa in ra màn hình vừa ghi vào file log của thí nghiệm (logs/expX_log/seed_<s>/run.log)
class Tee:
  def __init__(self, *streams):
    self.streams = streams
  def write(self, text):
    for st in self.streams:
      st.write(text)
  def flush(self):
    for st in self.streams:
      st.flush()

@contextlib.contextmanager
def ghi_log(exp, seed):
  with open(log_dir(exp, seed) / "run.log", "w", encoding="utf-8") as f:
    with contextlib.redirect_stdout(Tee(sys.stdout, f)):
      print(f"===== Thí nghiệm {exp} | seed = {seed} =====")
      yield


def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--exp", default="all", choices=["base", "A", "B", "C", "all"])
  ap.add_argument("--epochs", type=int, default=1000)
  ap.add_argument("--seeds", type=int, nargs="+", default=SEEDS)
  a = ap.parse_args()
  wanted = ["base", "A", "B", "C"] if a.exp == "all" else [a.exp]

  for seed in a.seeds:
    if "base" in wanted:
      with ghi_log("base", seed):
        luu_ket_qua([exp_base(seed, a.epochs)], None, "base_results.csv", "base", seed)

    if wanted == ["base"]:
      continue
    X_all, y_all = tao_data_thi_nghiem()  # dữ liệu cố định (seed 42), chỉ seed của mô hình thay đổi

    if "A" in wanted:
      with ghi_log("A", seed):
        res = []
        for n in cau_hinh_data:
          res.append(exp_A(n, X_all, y_all, seed, a.epochs))
        luu_ket_qua(res, "A", "expA_results.csv", "A", seed)

    if "B" in wanted:
      with ghi_log("B", seed):
        data_ = 1000
        X_B = X_all[:data_]
        y_B = y_all[:data_]
        data_B = data_split_and_to_tensor(X_B, y_B)

        res_B = []
        for n in cau_hinh_perceptron:
          print("số perceptron cho mô hình: ",n)
          res_B.append(exp_B(n, data_B, seed, a.epochs))
        luu_ket_qua(res_B, "B", "expB_results.csv", "B", seed)

    if "C" in wanted:
      with ghi_log("C", seed):
        data_ = 1000
        X_C = X_all[:data_]
        y_C = y_all[:data_]
        data_C = data_split_and_to_tensor(X_C, y_C)

        res_C = []
        for n in cau_hinh_hiden_layer:
          print("số hiden_layer cho mô hình: ",n)
          res_C.append(exp_c(n, data_C, seed, a.epochs))
        luu_ket_qua(res_C, "C", "expC_results.csv", "C", seed)


if __name__ == "__main__":
  main()
