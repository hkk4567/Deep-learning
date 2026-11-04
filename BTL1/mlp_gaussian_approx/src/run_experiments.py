# Chạy thí nghiệm theo notebook: base (mô hình chuẩn), A (số mẫu), B (số perceptron), C (số hiden layer)
# python -m src.run_experiments --exp all
# python -m src.run_experiments --exp B --epochs 50      # chạy thử nhanh
import argparse
import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from .config import device, LOG_DIR, WEIGHT_DIR, RESULT_DIR, cau_hinh_data, cau_hinh_perceptron, cau_hinh_hiden_layer
from .data_gen import tao_data_chuan, chia_data_chuan, chuyen_tensor_chuan, data_split_and_to_tensor, tao_data_thi_nghiem
from .model import MLP
from .train import Train
from .evaluate import evaluate, to_float


# 1. Mô hình chuẩn: 1000 mẫu (DataSet.csv), 1 hiden layer, 3 perceptron, batch = toàn bộ train
def exp_base(epochs = 1000):
  tao_data_chuan()
  X_train, X_val, X_test, y_train, y_val, y_test = chia_data_chuan()
  X_train_tensor, y_train_tensor, X_val_tensor, y_val_tensor, X_test_tensor, y_test_tensor, train_loader = chuyen_tensor_chuan(X_train, X_val, X_test, y_train, y_val, y_test)

  # cấu hình model tiêu chuẩn
  torch.manual_seed(42)
  model = MLP(hiden_sizes = [3]).to(device)
  criterion = nn.MSELoss()
  optimizer = torch.optim.Adam(model.parameters(), lr=0.002)

  file = WEIGHT_DIR / "best_base.pt"
  output = Train(train_loader, X_val_tensor, y_val_tensor, model, optimizer, criterion, file, epochs)
  output.update(evaluate(model, file, X_test_tensor, y_test_tensor))
  output["hiden_sizes"] = [3]
  output["n_train"], output["n_val"], output["n_test"] = len(y_train_tensor), len(y_val_tensor), len(y_test_tensor)
  return output


# Thí nghiệm A: hiden layer = 1, perceptron = 3
def exp_A(n, X_all, y_all, epochs = 1000):
  # khai báo tham số model
  torch.manual_seed(42)
  model_expA = MLP().to(device)
  criterion_expA = nn.MSELoss()
  optimizer_expA = torch.optim.Adam(model_expA.parameters(), lr=0.002)

  # chuẩn bị dữ liệu
  X = X_all[:n]
  y = y_all[:n]
  # chia dữ liệu
  X_train_tensor, y_train_tensor, X_val_tensor, y_val_tensor, X_test_tensor, y_test_tensor, train_loader = data_split_and_to_tensor(X, y)

  # huấn luyện và đánh giá lưu vào output(map) dùng để vẽ
  file = WEIGHT_DIR / f"best_A{len(y_train_tensor)}.pt" # tên file theo A = số mẫu train
  output = Train(train_loader, X_val_tensor, y_val_tensor, model_expA, optimizer_expA, criterion_expA, file, epochs)
  output.update(evaluate(model_expA, file, X_test_tensor, y_test_tensor))
  output["A"] = len(y_train_tensor)
  output["total_data"] = n
  output["hiden_sizes"] = [3]
  output["n_train"], output["n_val"], output["n_test"] = len(y_train_tensor), len(y_val_tensor), len(y_test_tensor)
  return output


# Thí nghiệm B: 1000 mẫu, 1 hiden layer, thay đổi số perceptron
def exp_B(n, data_B, epochs = 1000):
  X_train_tensor_B, y_train_tensor_B, X_val_tensor_B, y_val_tensor_B, X_test_tensor_B, y_test_tensor_B, train_loader_B = data_B
  data_ = 1000
  # khai báo tham số model
  torch.manual_seed(42)
  model_expB = MLP(hiden_sizes = [n]).to(device)
  criterion_expB = nn.MSELoss()
  optimizer_expB = torch.optim.Adam(model_expB.parameters(), lr=0.002)

  # huấn luyện và đánh giá lưu vào output(map) dùng để vẽ
  file = WEIGHT_DIR / f"best_B{n}.pt"
  output = Train(train_loader_B, X_val_tensor_B, y_val_tensor_B, model_expB, optimizer_expB, criterion_expB, file, epochs)
  output.update(evaluate(model_expB, file, X_test_tensor_B, y_test_tensor_B))
  output["B"] = n
  output["total_data"] = data_
  output["hiden_sizes"] = [n]
  output["n_train"], output["n_val"], output["n_test"] = len(y_train_tensor_B), len(y_val_tensor_B), len(y_test_tensor_B)
  return output


# Thí nghiệm C: 1000 mẫu, mỗi hiden layer 3 perceptron, thay đổi số hiden layer
def exp_c(n, data_C, epochs = 1000):
  X_train_tensor_C, y_train_tensor_C, X_val_tensor_C, y_val_tensor_C, X_test_tensor_C, y_test_tensor_C, train_loader_C = data_C
  data_ = 1000
  # khai báo tham số model
  torch.manual_seed(42)
  hiden_sizes = []
  for i in range(n):
    hiden_sizes.append(3)

  model_expC = MLP(hiden_sizes = hiden_sizes).to(device)
  criterion_expC = nn.MSELoss()
  optimizer_expC = torch.optim.Adam(model_expC.parameters(), lr=0.002)

  # huấn luyện và đánh giá lưu vào output(map) dùng để vẽ
  file = WEIGHT_DIR / f"best_C{n}.pt"

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
def luu_ket_qua(res, ten_cot, ten_file):
  rows = []
  for r in res:
    tag = f"{ten_cot}{r[ten_cot]}" if ten_cot else "base"
    train_history = [to_float(v) for v in r["history"]["train"]]
    val_history = [to_float(v) for v in r["history"]["val"]]
    pd.DataFrame({
        "epoch": range(1, len(train_history) + 1),
        "train_mse": train_history,
        "val_mse": val_history
    }).to_csv(LOG_DIR / f"history_{tag}.csv", index=False)

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
    rows.append(row)
  pd.DataFrame(rows).to_csv(RESULT_DIR / ten_file, index=False)


def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--exp", default="all", choices=["base", "A", "B", "C", "all"])
  ap.add_argument("--epochs", type=int, default=1000)
  a = ap.parse_args()
  wanted = ["base", "A", "B", "C"] if a.exp == "all" else [a.exp]

  if "base" in wanted:
    luu_ket_qua([exp_base(a.epochs)], None, "base_results.csv")

  if wanted != ["base"]:
    X_all, y_all = tao_data_thi_nghiem()

  if "A" in wanted:
    res = []
    for n in cau_hinh_data:
      res.append(exp_A(n, X_all, y_all, a.epochs))
    luu_ket_qua(res, "A", "expA_results.csv")

  if "B" in wanted:
    data_ = 1000
    X_B = X_all[:data_]
    y_B = y_all[:data_]
    data_B = data_split_and_to_tensor(X_B, y_B)

    res_B = []
    for n in cau_hinh_perceptron:
      print("số perceptron cho mô hình: ",n)
      res_B.append(exp_B(n, data_B, a.epochs))
    luu_ket_qua(res_B, "B", "expB_results.csv")

  if "C" in wanted:
    data_ = 1000
    X_C = X_all[:data_]
    y_C = y_all[:data_]
    data_C = data_split_and_to_tensor(X_C, y_C)

    res_C = []
    for n in cau_hinh_hiden_layer:
      print("số hiden_layer cho mô hình: ",n)
      res_C.append(exp_c(n, data_C, a.epochs))
    luu_ket_qua(res_C, "C", "expC_results.csv")


if __name__ == "__main__":
  main()
