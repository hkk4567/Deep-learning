# Chọn mô hình có sai số nhỏ nhất trong 3 thí nghiệm A, B, C rồi kiểm tra lại (đề yêu cầu, notebook chưa có)
# Chạy sau run_experiments:  python -m src.select_model
# - Chọn theo VALIDATION MSE nhỏ nhất (test chỉ dùng để đối chiếu).
# - Kiểm tra: (1) nạp lại trọng số và tính lại MSE test/val; (2) train/val/test không giao nhau;
#   (3) cấu trúc lớp và số tham số khớp cấu hình.
# Ghi: weights/selected_model.pt, results/selected_model.json, results/selection_check.json, results/table_selection.csv
import json
import shutil
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split

from .config import device, RESULT_DIR, WEIGHT_DIR, SEED_CHINH, N_CO_DINH, weight_dir
from .data_gen import tao_data_thi_nghiem, data_split_and_to_tensor
from .model import MLP
from .evaluate import evaluate

R, W = RESULT_DIR, WEIGHT_DIR


def main():
  parts = []
  for name, f in (("A", "expA_results.csv"), ("B", "expB_results.csv"), ("C", "expC_results.csv")):
    d = pd.read_csv(R / f)
    d.insert(0, "exp", name)
    parts.append(d)
  df = pd.concat(parts, ignore_index=True)
  cols = ["exp", "tag", "hidden_sizes", "n_train", "val_mse", "test_mse", "test_mae", "test_rmse"]

  print("== Mô hình tốt nhất của từng thí nghiệm ==")
  best_rows = []
  for name in "ABC":
    g = df[df.exp == name]
    bv, bt = g.loc[g.val_mse.idxmin()], g.loc[g.test_mse.idxmin()]
    best_rows.append(bv)
    print(f"{name}: theo val -> {bv.tag} (val {bv.val_mse:.3e}, test {bv.test_mse:.3e}); theo test -> {bt.tag} (test {bt.test_mse:.3e})")
  pd.DataFrame(best_rows)[cols].to_csv(R / "table_selection.csv", index=False)

  best = df.loc[df.val_mse.idxmin()]
  best_by_test = df.loc[df.test_mse.idxmin()]
  print(f"\n== Chọn toàn cục (val MSE nhỏ nhất): {best.tag}, hidden={best.hidden_sizes}, val={best.val_mse:.3e}, test={best.test_mse:.3e}")
  print(f"   Mô hình có test MSE nhỏ nhất: {best_by_test.tag} -> {'trùng' if best_by_test.tag == best.tag else 'KHÁC'} với mô hình chọn theo val")

  shutil.copy(weight_dir(best.exp, SEED_CHINH) / f"best_{best.tag}.pt", W / "selected_model.pt")  # seed chính
  hs = json.loads(best.hidden_sizes)
  (R / "selected_model.json").write_text(json.dumps(
      {"tag": best.tag, "experiment": best.exp, "hidden_sizes": best.hidden_sizes, "val_mse": best.val_mse, "test_mse": best.test_mse}, indent=2))

  # ---------- kiểm tra ----------
  # val và test của mọi thí nghiệm (A, B, C) cùng chia từ 1000 mẫu đầu; train của B, C là 720 mẫu còn lại, train của A lấy từ mẫu thứ 1000 trở đi
  X_all, y_all = tao_data_thi_nghiem()
  X_train_tensor, y_train_tensor, X_val_tensor, y_val_tensor, X_test_tensor, y_test_tensor, train_loader = data_split_and_to_tensor(X_all[:N_CO_DINH], y_all[:N_CO_DINH])
  model = MLP(hiden_sizes = hs)
  m_test = evaluate(model, W / "selected_model.pt", X_test_tensor, y_test_tensor)
  with torch.no_grad():
    val_mse = nn.MSELoss()(model(X_val_tensor).squeeze(-1), y_val_tensor).item()
  ck = torch.load(W / "selected_model.pt", map_location=device, weights_only=True)

  idx = np.arange(N_CO_DINH)  # cùng random_state nên cho cùng chỉ số với data_split_and_to_tensor
  tmp, te = train_test_split(idx, test_size=0.1, random_state=42)
  tr, va = train_test_split(tmp, test_size=0.2, random_state=42)
  if best.exp == "A":
    tr = np.arange(N_CO_DINH, N_CO_DINH + int(best.n_train))
  shapes = {k: list(v.shape) for k, v in model.state_dict().items()}
  n_params = sum(p.numel() for p in model.parameters())
  expected = sum((a + 1) * b for a, b in zip([2] + hs[:-1], hs)) + hs[-1] + 1
  checks = {
      "test_mse_tai_lap": bool(np.isclose(m_test["test_mse"], best.test_mse, rtol=1e-4)),
      "val_mse_tai_lap": bool(np.isclose(val_mse, best.val_mse, rtol=1e-4)),
      "val_mse_checkpoint_khop": bool(np.isclose(ck["val_loss"], best.val_mse, rtol=1e-4)),
      "train_val_test_khong_giao_nhau": bool(not (set(tr) & set(va)) and not (set(tr) & set(te)) and not (set(va) & set(te))),
      "tong_kich_thuoc_bang_n": bool(len(tr) + len(va) + len(te) == best.n_train + best.n_val + best.n_test),
      "kich_thuoc_khop_cau_hinh": bool((len(tr), len(va), len(te)) == (best.n_train, best.n_val, best.n_test)),
      "so_tham_so_khop_cong_thuc": bool(n_params == expected),
      "du_doan_huu_han": bool(torch.isfinite(model(X_test_tensor)).all().item()),
  }
  out = {"tag": best.tag, "hidden_sizes": hs, "n_params": n_params, "layer_shapes": shapes,
         "val_mse_nap_lai": val_mse, "val_mse_da_luu": float(best.val_mse), "test_nap_lai": m_test,
         "test_mse_da_luu": float(best.test_mse), "kich_thuoc": {"train": len(tr), "val": len(va), "test": len(te)}, "checks": checks}
  (R / "selection_check.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
  print("\n== Kiểm tra lại mô hình được chọn ==")
  print(f"Cấu trúc 2-{'-'.join(map(str, hs))}-1, {n_params} tham số; kích thước train/val/test = {len(tr)}/{len(va)}/{len(te)}")
  print(f"Test nạp lại: MSE={m_test['test_mse']:.4e} RMSE={m_test['test_rmse']:.4f} MAE={m_test['test_mae']:.4f}  (đã lưu: {best.test_mse:.4e})")
  for k, v in checks.items():
    print(f"  [{'OK' if v else 'LỖI'}] {k}")
  assert all(checks.values()), "Có kiểm tra không đạt"


if __name__ == "__main__":
  main()
