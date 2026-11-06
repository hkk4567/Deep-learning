"""Vẽ sơ đồ kiến trúc của mô hình được chọn (đọc results/selected_model.json) -> figures/fig12_mlp_architecture.png
  python -m src.select_model   # tạo selected_model.json
  python -m src.diagram
"""
import json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from . import config as cfg


def draw(hidden, name="fig12_mlp_architecture.png"):
    sizes = [2] + list(hidden) + [1]
    n_params = sum((a + 1) * b for a, b in zip(sizes[:-1], sizes[1:]))
    fig, ax = plt.subplots(figsize=(10, 4.6)); ax.axis("off")
    xs = [i * 2.2 for i in range(len(sizes))]
    top = (max(sizes) - 1) / 2
    pos = [[(x, (n - 1) / 2 - j) for j in range(n)] for x, n in zip(xs, sizes)]
    for a, b in zip(pos[:-1], pos[1:]):
        for p in a:
            for q in b:
                ax.plot([p[0], q[0]], [p[1], q[1]], c="#9aa5b1", lw=.8, zorder=1)
    cols = ["#4c78a8"] + ["#f58518"] * len(hidden) + ["#54a24b"]
    for layer, c in zip(pos, cols):
        for (x, y) in layer:
            ax.scatter([x], [y], s=640, c=c, edgecolors="k", zorder=2)
    labels = ["Đầu vào\n(x1, x2)"]
    for i, (a, b) in enumerate(zip(sizes[:-2], sizes[1:-1]), 1):
        labels.append(f"Tầng ẩn {i}\nLinear({a}→{b}) + ReLU")
    labels.append(f"Đầu ra\nLinear({sizes[-2]}→1) → ŷ")
    for x, t in zip(xs, labels):
        ax.text(x, top + 0.75, t, ha="center", va="bottom", fontsize=9.5)
    ax.text(xs[len(xs) // 2], -top - 0.95, f"MLP {'-'.join(map(str, sizes))}  ·  {n_params} tham số  ·  hàm mất mát MSE",
            ha="center", va="top", fontsize=11, fontweight="bold")
    ax.set_xlim(-.7, xs[-1] + .7); ax.set_ylim(-top - 1.6, top + 1.9)
    plt.tight_layout(); plt.savefig(cfg.FIG_DIR / name, dpi=150, bbox_inches="tight"); plt.close()


if __name__ == "__main__":
    sel = json.loads((cfg.RESULT_DIR / "selected_model.json").read_text())
    draw(json.loads(sel["hidden_sizes"]))
