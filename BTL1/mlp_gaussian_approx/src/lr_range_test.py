# Bước 1 tìm learning rate: LR range test trên mô hình chuẩn (base: hiden_sizes = [3], 720 train / 180 val)
# python -m src.lr_range_test                       # mặc định: 3 seed, 400 step, lr 1e-5 -> 1
# python -m src.lr_range_test --steps 50 --seeds 42 # chạy thử nhanh
# Ý tưởng: cho lr tăng theo hàm mũ sau mỗi step (full-batch nên 1 step = 1 epoch), ghi lại loss, vẽ loss theo lr.
import argparse
import contextlib
import io
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .config import device, RESULT_DIR, FIG_DIR, LOG_DIR
from .data_gen import tao_data_chuan, chia_data_chuan, chuyen_tensor_chuan
from .model import MLP


def lay_data_chuan():
  # dùng lại đúng dữ liệu và cách chia của mô hình chuẩn (tắt print của các hàm cũ cho gọn log)
  with contextlib.redirect_stdout(io.StringIO()):
    tao_data_chuan()
    X_train, X_val, X_test, y_train, y_val, y_test = chia_data_chuan()
    out = chuyen_tensor_chuan(X_train, X_val, X_test, y_train, y_val, y_test)
  X_train_tensor, y_train_tensor, X_val_tensor, y_val_tensor = out[0], out[1], out[2], out[3]
  return X_train_tensor.to(device), y_train_tensor.to(device), X_val_tensor.to(device), y_val_tensor.to(device)


def range_test(seed, steps, lr_min, lr_max, data, hiden_sizes = [3]):
  X_train, y_train, X_val, y_val = data
  torch.manual_seed(seed)
  model = MLP(hiden_sizes = hiden_sizes).to(device)
  criterion = nn.MSELoss()
  optimizer = torch.optim.Adam(model.parameters(), lr=lr_min)
  gamma = (lr_max / lr_min) ** (1 / (steps - 1)) # hệ số nhân lr sau mỗi step
  rows = []
  lr = lr_min
  for step in range(steps):
    for g in optimizer.param_groups:
      g["lr"] = lr
    model.train()
    optimizer.zero_grad()
    loss = criterion(model(X_train).squeeze(-1), y_train) # full-batch giống mô hình chuẩn
    loss.backward()
    optimizer.step()
    model.eval()
    with torch.no_grad():
      val_loss = criterion(model(X_val).squeeze(-1), y_val)
    rows.append({"seed": seed, "step": step, "lr": lr, "train_loss": loss.item(), "val_loss": val_loss.item()})
    lr *= gamma
  return pd.DataFrame(rows)


def lam_muot(x, beta = 0.9):
  # trung bình trượt mũ (có hiệu chỉnh bias) để giảm nhiễu trước khi tìm điểm đặc trưng
  out, avg = [], 0.0
  for i, v in enumerate(x):
    avg = beta * avg + (1 - beta) * v
    out.append(avg / (1 - beta ** (i + 1)))
  return np.array(out)


def phan_tich(df_seed):
  # 3 điểm đặc trưng trên đường loss (đã làm mượt) của 1 seed
  lr = df_seed["lr"].to_numpy()
  sm = lam_muot(df_seed["train_loss"].to_numpy())
  i_min = int(np.argmin(sm))                         # lr cho loss thấp nhất
  slope = np.gradient(sm, np.log10(lr))              # đạo hàm loss theo log10(lr)
  i_steep = int(np.argmin(slope[:max(i_min, 1) + 1])) # dốc xuống mạnh nhất, trước điểm loss thấp nhất
  # điểm phân kỳ: loss mượt đầu tiên vượt 4 lần loss nhỏ nhất sau khi đã đạt min
  sau = np.where(sm[i_min:] > 4 * sm[i_min])[0]
  lr_div = float(lr[i_min + sau[0]]) if len(sau) else None
  return {"lr_steepest": float(lr[i_steep]), "lr_min_loss": float(lr[i_min]), "lr_min_loss_div10": float(lr[i_min]) / 10,
          "lr_diverge": lr_div, "min_loss_smooth": float(sm[i_min])}


if __name__ == "__main__":
  ap = argparse.ArgumentParser()
  ap.add_argument("--steps", type=int, default=400)
  ap.add_argument("--lr_min", type=float, default=1e-5)
  ap.add_argument("--lr_max", type=float, default=1.0)
  ap.add_argument("--seeds", type=int, nargs="+", default=[42, 43, 44])
  a = ap.parse_args()

  data = lay_data_chuan()
  dfs = [range_test(s, a.steps, a.lr_min, a.lr_max, data) for s in a.seeds]
  df = pd.concat(dfs, ignore_index=True)
  df.to_csv(LOG_DIR / "lr_range_test_history.csv", index=False)

  summary = {int(s): phan_tich(d) for s, d in zip(a.seeds, dfs)}
  for s, r in summary.items():
    print(f"seed {s}: ", {k: (None if v is None else float(f"{v:.3g}")) for k, v in r.items()})
  (RESULT_DIR / "lr_range_test.json").write_text(json.dumps({"config": vars(a), "per_seed": summary}, indent=2))

  # vẽ loss theo lr (trục x log)
  fig, axes = plt.subplots(1, 2, figsize = (12, 4.5))
  for s, d in zip(a.seeds, dfs):
    axes[0].plot(d["lr"], lam_muot(d["train_loss"].to_numpy()), label = f"seed {s}")
    axes[1].plot(d["lr"], d["val_loss"], label = f"seed {s}")
  for ax, t in zip(axes, ["Train loss (làm mượt)", "Validation loss"]):
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Learning rate"); ax.set_ylabel("MSE"); ax.set_title(f"LR range test - {t}")
    ax.grid(True, which = "both", alpha = 0.3); ax.legend()
  plt.tight_layout()
  plt.savefig(FIG_DIR / "fig15_lr_range_test.png", dpi = 150)
  print("Đã lưu figures/fig15_lr_range_test.png, results/lr_range_test.json, logs/lr_range_test_history.csv")
