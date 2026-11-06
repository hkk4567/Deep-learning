# Tổng hợp kết quả thử nghiệm trên nhiều seed (chạy sau run_experiments):  python -m src.summarize_seeds
# Đọc results/seeds/exp*_results_seed<s>.csv, ghi:
#   results/seeds_summary_{base,A,B,C}.csv : mean/std của từng cấu hình qua các seed
#   results/seeds_best_config.csv          : cấu hình có val MSE nhỏ nhất của từng thí nghiệm ở từng seed
#   figures/fig15_expA_seeds.png, fig16_expB_seeds.png, fig17_expC_seeds.png : test MSE từng seed + mean ± std
#   figures/slides/fig1{5,6,7}_*_slide.png : cùng hình, tỉ lệ khác để đặt vào slide
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .config import FIG_DIR, RESULT_DIR, SEED_DIR, SEEDS

THONG_SO = {"base": None, "A": "A", "B": "B", "C": "C"}
CHI_SO = ["best_epoch", "train_mse", "val_mse", "test_mse", "test_rmse", "test_mae"]


# đọc kết quả của tất cả seed thành 1 bảng (thêm cột seed)
def doc_tat_ca(exp):
  ten = "base_results" if exp == "base" else f"exp{exp}_results"
  parts = []
  for s in SEEDS:
    f = SEED_DIR / f"{ten}_seed{s}.csv"
    if f.exists():
      parts.append(pd.read_csv(f))
  return pd.concat(parts, ignore_index=True)


# bảng mean ± std theo từng cấu hình (std lấy với ddof=1, mẫu nhỏ nên là độ lệch chuẩn mẫu)
def tong_hop(df, cot):
  cols = CHI_SO + (["train_time_sec"] if "train_time_sec" in df else [])
  keys = ["tag"] + ([cot] if cot else [])
  g = df.groupby(keys, sort=False)[cols].agg(["mean", "std"])
  g.columns = [f"{c}_{m}" for c, m in g.columns]
  g.insert(0, "n_seeds", df.groupby(keys, sort=False).size())
  return g.reset_index()


def ve_seeds(df, tong, cot, nhan_x, tieu_de, ten_file, kich_thuoc = (9, 5)):
  fig, ax = plt.subplots(figsize=kich_thuoc)
  x = tong[cot].to_numpy()
  for s in sorted(df.seed.unique()):
    d = df[df.seed == s].sort_values(cot)
    ax.plot(d[cot], d["test_mse"], marker="o", alpha=0.45, label=f"seed {s}")
  ax.errorbar(x, tong["test_mse_mean"], yerr=tong["test_mse_std"], color="black", marker="s", capsize=4, linewidth=2, label="mean ± std")
  ax.set_yscale("log")
  ax.set_xlabel(nhan_x)
  ax.set_ylabel("Test MSE (log)")
  ax.set_title(tieu_de)
  ax.set_xticks(x)
  ax.grid(True, which="both", alpha=0.3)
  ax.legend()
  plt.tight_layout()
  (FIG_DIR / ten_file).parent.mkdir(parents=True, exist_ok=True)
  plt.savefig(FIG_DIR / ten_file, dpi=130, bbox_inches="tight")
  plt.close()


def main():
  best_rows = []
  for exp, cot in THONG_SO.items():
    df = doc_tat_ca(exp)
    tong = tong_hop(df, cot)
    tong.to_csv(RESULT_DIR / f"seeds_summary_{exp}.csv", index=False)
    print(f"== {exp}: {df.seed.nunique()} seed {sorted(df.seed.unique())} ==")
    print(tong[["tag", "val_mse_mean", "val_mse_std", "test_mse_mean", "test_mse_std"]].to_string(index=False, float_format=lambda v: f"{v:.3e}"))
    if exp != "base":
      for s in sorted(df.seed.unique()):
        d = df[df.seed == s]
        b = d.loc[d.val_mse.idxmin()]
        best_rows.append({"exp": exp, "seed": s, "tag": b.tag, "val_mse": b.val_mse, "test_mse": b.test_mse})
  pd.DataFrame(best_rows).to_csv(RESULT_DIR / "seeds_best_config.csv", index=False)

  for exp, cot, nhan_x, tieu_de in (("A", "A", "A - Số mẫu huấn luyện", "Thí nghiệm A: Test MSE theo A trên các seed"),
                                    ("B", "B", "Số perceptron (B)", "Thí nghiệm B: Test MSE theo B trên các seed"),
                                    ("C", "C", "Số tầng ẩn (C)", "Thí nghiệm C: Test MSE theo C trên các seed")):
    df, tong = doc_tat_ca(exp), pd.read_csv(RESULT_DIR / f"seeds_summary_{exp}.csv")
    ten = {"A": "fig15_expA_seeds", "B": "fig16_expB_seeds", "C": "fig17_expC_seeds"}[exp]
    ve_seeds(df, tong, cot, nhan_x, tieu_de, f"{ten}.png")  # hình cho báo cáo
    ve_seeds(df, tong, cot, nhan_x, tieu_de, f"slides/{ten}_slide.png", (6.2, 5.0))  # hình vuông hơn cho slide
  print("\nCấu hình tốt nhất (theo val MSE) của từng seed:")
  print(pd.DataFrame(best_rows).to_string(index=False, float_format=lambda v: f"{v:.3e}"))


if __name__ == "__main__":
  main()
