# Xuất hình và bảng giống notebook, từ logs/ và results/ (chạy sau run_experiments)
# python -m src.plots
import json
import numpy as np
import pandas as pd
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .config import device, FIG_DIR, RESULT_DIR, SEED_CHINH, weight_dir, log_dir
from .data_gen import tao_data_thi_nghiem, chia_data_chuan, chuyen_tensor_chuan, data_split_and_to_tensor
from .config import WEIGHT_DIR as WEIGHT_DIR_ROOT
from .model import MLP
from .evaluate import to_float


# thay cho plt.show() của notebook: lưu hình ra figures/
def luu_hinh(ten_file):
  plt.savefig(FIG_DIR / ten_file, dpi=130, bbox_inches="tight")
  plt.close()


# đọc lại kết quả đã lưu (results/, logs/) thành list dict giống res, res_B, res_C của notebook
def doc_ket_qua(ten_file, exp):
  df = pd.read_csv(RESULT_DIR / ten_file)
  res = []
  for _, row in df.iterrows():
    h = pd.read_csv(log_dir(exp, SEED_CHINH) / f"history_{row['tag']}.csv")
    r = row.to_dict()
    r["history"] = {"train": h["train_mse"].tolist(), "val": h["val_mse"].tolist()}
    res.append(r)
  return res


# vẽ 3D Scatter of Gaussian và sơ đồ phân bố dữ liệu (tập train của mô hình chuẩn)
def ve_data_chuan(X_train, y_train):
  X_train_1 = X_train["x1"]
  X_train_2 = X_train["x2"]
  print(X_train_1.head())
  print(X_train_2.head())
  fig = plt.figure(figsize=(9, 7))
  ax = fig.add_subplot(111, projection="3d")

  sc = ax.scatter(X_train_1, X_train_2, y_train, c=y_train, cmap="viridis", s=15)

  ax.set_xlabel("x1")
  ax.set_ylabel("x2")
  ax.set_zlabel("y")
  ax.set_title("3D Scatter of Gaussian Data")

  fig.colorbar(sc, ax=ax, label="y", shrink=0.7)
  plt.tight_layout()
  luu_hinh("fig01_data_3d.png")
  # ================================================================
  # vẽ sơ đồ phân bố dữ liệu
  fig, axes = plt.subplots(1, 3, figsize=(15, 4))
  axes[0].hist(X_train_1, bins=30, edgecolor="black")
  axes[0].set_title("Distribution of x1")
  axes[0].set_xlabel("x1")
  axes[0].set_ylabel("Frequency")

  axes[1].hist(X_train_2, bins=30, edgecolor="black")
  axes[1].set_title("Distribution of x2")
  axes[1].set_xlabel("x2")
  axes[1].set_ylabel("Frequency")

  axes[2].hist(y_train, bins=30, edgecolor="black")
  axes[2].set_title("Distribution of y")
  axes[2].set_xlabel("y")
  axes[2].set_ylabel("Frequency")

  plt.tight_layout()
  luu_hinh("fig02_data_hist.png")


# test mô hình với checkpoint có val nhỏ nhất, vẽ y thật - y dự đoán và bề mặt xấp xỉ (dùng cho mô hình chuẩn và mô hình được chọn)
def ve_ket_qua_test(model, file, X_test_tensor, y_test_tensor, ten_mo_hinh, file_pred, file_surface):
  criterion = torch.nn.MSELoss()
  # tải model với min_val để chạy test
  checkpoint = torch.load(
      file,
      map_location=device,
      weights_only=True
  )
  model.load_state_dict(checkpoint["model_state_dict"])
  model.eval()
  with torch.no_grad():
    y_test_pred = model(X_test_tensor).squeeze(-1)

    test_mse = criterion(y_test_pred, y_test_tensor).item()

    test_mae = torch.mean(
          torch.abs(y_test_pred - y_test_tensor)
      ).item()

    test_rmse = np.sqrt(test_mse)
  print(f"Test MSE  : {test_mse:.6f}")
  print(f"Test MAE  : {test_mae:.6f}")
  print(f"Test RMSE : {test_rmse:.6f}")
  # chuẩn bị vẽ hình
  y_true = y_test_tensor.numpy().ravel()
  y_pred = y_test_pred.cpu().numpy().ravel()
  print("số lượng test: ",len(y_true))

  # hình so sánh giữa y_true và y_pred
  plt.figure(figsize=(7, 6))
  plt.scatter(
      y_true,
      y_pred,
      alpha=0.7,
      label="Dữ liệu test"
  )

  lower = min(y_true.min(), y_pred.min())
  upper = max(y_true.max(), y_pred.max())

  plt.plot(
      [lower, upper],
      [lower, upper],
      "r--",
      label="Dự đoán hoàn hảo"
  )

  plt.xlabel("y thật")
  plt.ylabel("y dự đoán")
  plt.title(
      f"y thật và y dự đoán trên tập test ({ten_mo_hinh})\n"
      f"MSE={test_mse:.4f} | MAE={test_mae:.4f} "
      f"| RMSE={test_rmse:.4f}"
  )

  plt.legend()
  plt.grid(alpha=0.3)
  plt.tight_layout()
  luu_hinh(file_pred)

  # hình tạo lưới để kiểm tra xem mô hình có xấp sỉ được hàm Gaussian 2D không
  # Tạo lưới giá trị x1, x2
  x1_values = np.linspace(X_test_tensor.numpy()[:, 0].min(), X_test_tensor.numpy()[:, 0].max(), 60)
  x2_values = np.linspace(X_test_tensor.numpy()[:, 1].min(), X_test_tensor.numpy()[:, 1].max(), 60)

  X1_grid, X2_grid = np.meshgrid(x1_values, x2_values)

  # Ghép thành các cặp đầu vào [x1, x2]
  X_grid = np.column_stack([
      X1_grid.ravel(),
      X2_grid.ravel()
  ]).astype(np.float32)

  X_grid_tensor = torch.tensor(
      X_grid,
      dtype=torch.float32
  ).to(device)

  # MLP dự đoán trên toàn bộ lưới
  model.eval()

  with torch.no_grad():
      y_grid_pred = model(X_grid_tensor).cpu().numpy()

  Y_grid = y_grid_pred.reshape(X1_grid.shape)

  # Vẽ bề mặt và các điểm dữ liệu test
  fig = plt.figure(figsize=(11, 8))
  ax = fig.add_subplot(111, projection="3d")

  # bề mặt dự đoán của model
  surface = ax.plot_surface(
      X1_grid,
      X2_grid,
      Y_grid,
      cmap="viridis",
      alpha=0.7,
      linewidth=0
  )

  ax.scatter(
      X_test_tensor.numpy()[:, 0],
      X_test_tensor.numpy()[:, 1],
      y_true,
      color="red",
      s=22,
      label="Giá trị thật của test"
  )

  ax.set_xlabel("x1")
  ax.set_ylabel("x2")
  ax.set_zlabel("y / y dự đoán")
  ax.set_title(f"Bề mặt xấp xỉ của MLP ({ten_mo_hinh}) trên dữ liệu test")

  fig.colorbar(surface, ax=ax, shrink=0.6, label="y dự đoán")
  ax.legend()
  plt.tight_layout()
  luu_hinh(file_surface)
  return {"test_mse": test_mse, "test_mae": test_mae, "test_rmse": test_rmse}


# Thí nghiệm A: bảng MSE/MAE hoặc RMSE; đồ thị sai số theo A;
def ve_exp_A(res):
  df_expA = pd.DataFrame(res)
  df_expA = df_expA.sort_values("A").reset_index(drop=True)
  bang_ket_qua = df_expA[
      ["A", "test_mse", "test_mae", "test_rmse"]
  ].rename(columns={
      "test_mse": "MSE",
      "test_mae": "MAE",
      "test_rmse": "RMSE"
  })

  print("BẢNG ĐÁNH GIÁ THÍ NGHIỆM A")
  print(bang_ket_qua.round(6))
  bang_ket_qua.to_csv(RESULT_DIR / "table_expA.csv", index=False)

  # đồ thị sai số theo A
  fig, axes = plt.subplots(1, 3, figsize=(16, 4))
  metrics = [
      ("test_mse", "MSE"),
      ("test_mae", "MAE"),
      ("test_rmse", "RMSE")
  ]

  for ax, (col, name) in zip(axes, metrics):
      ax.plot(df_expA["A"], df_expA[col], marker="o")
      ax.set_xlabel("A - Số mẫu huấn luyện")
      ax.set_ylabel(name)
      ax.set_title(f"{name} theo A")
      ax.grid(True)

  plt.tight_layout()
  luu_hinh("fig03_expA_metrics.png")


# Thí nghiệm B
def ve_exp_B(res_B):
  # Tổng hợp kết quả từng cấu hình B
  rows = []

  for r in res_B:
      history = r["history"]
      best_epoch = int(r["best_epoch"])
      best_idx = best_epoch - 1

      train_history = [
          to_float(v) for v in history["train"]
      ]
      val_history = [
          to_float(v) for v in history["val"]
      ]

      rows.append({
          "B": r["B"],
          "Best epoch": best_epoch,
          "Train MSE": train_history[best_idx],
          "Validation MSE": val_history[best_idx],
          "Test MSE": to_float(r["test_mse"]),
          "Test MAE": to_float(r["test_mae"]),
          "Test RMSE": to_float(r["test_rmse"])
      })

  df_B = pd.DataFrame(rows).sort_values("B").reset_index(drop=True)

  print("BẢNG SO SÁNH THÍ NGHIỆM B")
  print(df_B.round(6))
  df_B.rename(columns={
      "Best epoch": "best_epoch", "Train MSE": "train_mse", "Validation MSE": "val_mse",
      "Test MSE": "test_mse", "Test MAE": "test_mae", "Test RMSE": "test_rmse"
  }).to_csv(RESULT_DIR / "table_expB.csv", index=False)

  # vẽ đồ thị so sánh các chỉ số metrics giữa các perceptron
  fig, axes = plt.subplots(1, 3, figsize=(16, 4))

  metrics = [
      ("Test MSE", "MSE"),
      ("Test MAE", "MAE"),
      ("Test RMSE", "RMSE")
  ]

  for ax, (column, metric) in zip(axes, metrics):
      ax.plot(
          df_B["B"],
          df_B[column],
          marker="o"
      )

      ax.set_xlabel("Số perceptron (B)")
      ax.set_ylabel(metric)
      ax.set_title(f"{metric} theo số perceptron")
      ax.set_xticks(df_B["B"])
      ax.grid(True)

  plt.tight_layout()
  luu_hinh("fig04_expB_metrics.png")

  # vẽ đồ thị so sánh Train MSE và Validation MSE giữa các perceptron
  plt.figure(figsize=(9, 5))

  plt.plot(
      df_B["B"],
      df_B["Train MSE"],
      marker="o",
      label="Train MSE"
  )

  plt.plot(
      df_B["B"],
      df_B["Validation MSE"],
      marker="s",
      label="Validation MSE"
  )

  plt.xlabel("Số perceptron (B)")
  plt.ylabel("MSE")
  plt.title("So sánh Train MSE và Validation MSE theo B")
  plt.xticks(df_B["B"])
  plt.grid(True)
  plt.legend()
  plt.tight_layout()
  luu_hinh("fig05_expB_train_val.png")

  # vẽ Learning curves theo số perceptron
  fig, axes = plt.subplots(2, 5, figsize=(18, 7))
  axes = axes.ravel()

  for i, r in enumerate(sorted(res_B, key=lambda x: x["B"])):
      train_loss = [
          to_float(v) for v in r["history"]["train"]
      ]

      val_loss = [
          to_float(v) for v in r["history"]["val"]
      ]

      epochs = range(1, len(train_loss) + 1)

      axes[i].plot(epochs, train_loss, label="Train")
      axes[i].plot(epochs, val_loss, label="Validation")

      axes[i].axvline(
          r["best_epoch"],
          linestyle="--",
          label="Best epoch"
      )

      axes[i].set_title(f'B = {r["B"]}')
      axes[i].set_xlabel("Epoch")
      axes[i].set_ylabel("MSE")
      axes[i].grid(True)
      axes[i].legend(fontsize=8)

  plt.suptitle("Learning curves theo số perceptron", y=1.02)
  plt.tight_layout()
  luu_hinh("fig06_expB_curves.png")


# Thí nghiệm C
def ve_exp_C(res_C):
  rows = []

  for r in res_C:
      best_epoch = int(r["best_epoch"])
      idx = best_epoch - 1

      train_history = r["history"]["train"]
      val_history = r["history"]["val"]

      rows.append({
          "Hidden layers": r["C"],
          "Neurons/layer": 3,
          "Best epoch": best_epoch,
          "Train MSE": to_float(train_history[idx]),
          "Validation MSE": to_float(val_history[idx]),
          "Test MSE": to_float(r["test_mse"]),
          "Test MAE": to_float(r["test_mae"]),
          "Test RMSE": to_float(r["test_rmse"]),
          "Training time (s)": r["train_time_sec"]
      })

  df_C = pd.DataFrame(rows).sort_values("Hidden layers").reset_index(drop=True)

  print("BẢNG SO SÁNH THÍ NGHIỆM C")
  print(df_C.round(6))
  df_C.drop(columns="Neurons/layer").rename(columns={
      "Hidden layers": "C", "Best epoch": "best_epoch", "Train MSE": "train_mse", "Validation MSE": "val_mse",
      "Test MSE": "test_mse", "Test MAE": "test_mae", "Test RMSE": "test_rmse", "Training time (s)": "train_time_sec"
  }).to_csv(RESULT_DIR / "table_expC.csv", index=False)

  # vẽ đồ thị so sánh metrics theo độ sâu mạng
  fig, axes = plt.subplots(1, 3, figsize=(16, 4))

  metrics = [
      ("Test MSE", "test_mse"),
      ("Test MAE", "test_mae"),
      ("Test RMSE", "test_rmse")
  ]

  for ax, (title, key) in zip(axes, metrics):
      values = [to_float(r[key]) for r in sorted(res_C, key=lambda x: x["C"])]
      depths = sorted([r["C"] for r in res_C])

      ax.plot(depths, values, marker="o")
      ax.set_title(title)
      ax.set_xlabel("Số tầng ẩn")
      ax.set_ylabel(title.replace("Test ", ""))
      ax.set_xticks(depths)
      ax.grid(True)

  plt.suptitle("So sánh Test Error theo độ sâu mạng")
  plt.tight_layout()
  luu_hinh("fig07_expC_metrics.png")

  # vẽ Learning curves theo độ sâu mạng
  fig, axes = plt.subplots(2, 2, figsize=(14, 9))
  axes = axes.flatten()

  for ax, r in zip(axes, sorted(res_C, key=lambda x: x["C"])):
      train_loss = [to_float(v) for v in r["history"]["train"]]
      val_loss = [to_float(v) for v in r["history"]["val"]]
      epochs = range(1, len(train_loss) + 1)

      ax.plot(epochs, train_loss, label="Train Loss")
      ax.plot(epochs, val_loss, label="Validation Loss")

      ax.axvline(
          r["best_epoch"],
          linestyle="--",
          label=f'Best epoch = {r["best_epoch"]}'
      )

      ax.set_title(f'{r["C"]} tầng ẩn, 3 neuron/tầng')
      ax.set_xlabel("Epoch")
      ax.set_ylabel("MSE Loss")
      ax.grid(True)
      ax.legend()

  plt.suptitle("Quá trình hội tụ của các mô hình MLP", fontsize=14)
  plt.tight_layout()
  luu_hinh("fig08_expC_curves.png")

  # Vẽ đồ thị thời gian huấn luyện
  df_time = df_C.sort_values("Hidden layers")

  plt.figure(figsize=(8, 5))

  plt.plot(
      df_time["Hidden layers"],
      df_time["Training time (s)"],
      marker="o"
  )

  plt.xlabel("Số tầng ẩn")
  plt.ylabel("Thời gian huấn luyện (giây)")
  plt.title("Thời gian huấn luyện theo độ sâu mạng")
  plt.xticks(df_time["Hidden layers"])
  plt.grid(True)
  plt.tight_layout()
  luu_hinh("fig09_expC_time.png")


def main():
  # hình dữ liệu và minh họa của mô hình chuẩn (notebook mục 1)
  X_train, X_val, X_test, y_train, y_val, y_test = chia_data_chuan()
  ve_data_chuan(X_train, y_train)
  tensors = chuyen_tensor_chuan(X_train, X_val, X_test, y_train, y_val, y_test)
  X_test_tensor, y_test_tensor = tensors[4], tensors[5]
  model = MLP(hiden_sizes = [3]).to(device)
  ve_ket_qua_test(model, weight_dir("base", SEED_CHINH) / "best_base.pt", X_test_tensor, y_test_tensor, "base", "fig10_base_pred_vs_true.png", "fig11_base_surface.png")

  # thí nghiệm A, B, C (notebook mục 2)
  ve_exp_A(doc_ket_qua("expA_results.csv", "A"))
  ve_exp_B(doc_ket_qua("expB_results.csv", "B"))
  ve_exp_C(doc_ket_qua("expC_results.csv", "C"))

  # minh họa mô hình được chọn (select_model.py): dùng dữ liệu 1000 mẫu giống B và C
  sel = json.loads((RESULT_DIR / "selected_model.json").read_text())
  hiden_sizes = json.loads(sel["hidden_sizes"])
  X_all, y_all = tao_data_thi_nghiem()
  data_sel = data_split_and_to_tensor(X_all[:1000], y_all[:1000])
  model_sel = MLP(hiden_sizes = hiden_sizes).to(device)
  
  mt = ve_ket_qua_test(model_sel, WEIGHT_DIR_ROOT / "selected_model.pt", data_sel[4], data_sel[5], sel["tag"], "fig13_selected_pred_vs_true.png", "fig14_selected_surface.png")
  pd.DataFrame([{**sel, **mt}]).to_csv(RESULT_DIR / "table_selected_model.csv", index=False)
  print("Đã xuất hình vào", FIG_DIR)


if __name__ == "__main__":
  main()
