#!/usr/bin/env python3
"""
explore_tabular.py - Khám phá dữ liệu bảng (P4), CHỈ trên split=='train'. Không sửa dữ liệu.

  python explore_tabular.py --split-csv 01_data/splits/split_v1.csv --out-dir 06_reports/eda \
      --label-col label [--id-col rel_path] [--ordinal-cols col1,col2] \
      [--valid-range luong:0:None] [--iqr-k 1.5]

Làm theo đúng 7 bước khai phá dữ liệu bảng kinh điển (bước 1-3 và 5; bước 4,6,7 thuộc P5 - tiền xử lý):
  B1 Tổng quan: số mẫu, số thuộc tính (loại ID), kiểu dữ liệu, biến mục tiêu, thang đo suy luận
     (định danh/thứ bậc cho hạng mục; khoảng/tỷ lệ cho số - tỷ lệ nếu min >= 0)
  B2 Thống kê mô tả: bỏ giá trị thiếu trước khi tính; mean, median, mode, Q1, Q3, IQR
  B3 Phân phối & quan hệ: skewness (độ lệch), ma trận tương quan Pearson, biểu đồ
     histogram/boxplot mỗi cột số, heatmap tương quan, scatter cặp tương quan mạnh nhất
  B5 Ngoại lai: biên dưới/trên = Q1 - k*IQR / Q3 + k*IQR (mặc định k=1.5), đếm số ngoài biên
  + phát hiện giá trị ngoài miền hợp lệ nếu khai --valid-range (vd lương không được âm)
  + độ liên quan giữa từng cột số với nhãn: Pearson (nhãn số) hoặc ANOVA F/p-value
    (nhãn phân loại) - gợi ý cho bước chọn đặc trưng ở P5, KHÔNG tự loại cột nào ở đây

Đầu ra trong --out-dir: eda.json, eda_report.md, eda_plots/*.png
"""
import argparse
import json
import os

import numpy as np
import pandas as pd
from scipy import stats

HELPER_COLS = {"split", "_row_id", "_rowhash", "sha256", "rel_path", "ext", "size", "orig_split",
               "usable", "is_junk", "corrupt", "width", "height", "mode"}


def infer_scale(s: pd.Series, is_ordinal: bool):
    if pd.api.types.is_numeric_dtype(s):
        return "tỷ lệ (ratio)" if s.dropna().ge(0).all() else "khoảng (interval)"
    return "thứ bậc (ordinal)" if is_ordinal else "định danh (nominal)"


def mode_of(s: pd.Series):
    m = s.dropna().mode()
    return None if m.empty else (m.iloc[0].item() if hasattr(m.iloc[0], "item") else m.iloc[0])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split-csv", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--label-col")
    ap.add_argument("--label-type", default="class", choices=["class", "numeric"])
    ap.add_argument("--id-col")
    ap.add_argument("--ordinal-cols", default="", help="danh sách cột thứ bậc, cách nhau bởi dấu phẩy")
    ap.add_argument("--valid-range", nargs="*", default=[],
                     help="col:min:max (min/max để trống hoặc 'None' nếu không giới hạn một phía), vd luong:0:None")
    ap.add_argument("--iqr-k", type=float, default=1.5)
    a = ap.parse_args()

    df = pd.read_csv(a.split_csv, low_memory=False)
    if "split" not in df.columns:
        raise SystemExit("File chia phải có cột 'split'")
    tr = df[df["split"] == "train"].copy()
    ordinal = {c.strip() for c in a.ordinal_cols.split(",") if c.strip()}
    drop = HELPER_COLS | {a.id_col} if a.id_col else HELPER_COLS
    attrs = [c for c in tr.columns if c not in drop]  # bao gồm cả label_col trong tổng quan, tách riêng bên dưới
    num_cols = [c for c in attrs if c != a.label_col and pd.api.types.is_numeric_dtype(tr[c])]
    cat_cols = [c for c in attrs if c != a.label_col and c not in num_cols]

    os.makedirs(a.out_dir, exist_ok=True)
    plot_dir = os.path.join(a.out_dir, "eda_plots")
    os.makedirs(plot_dir, exist_ok=True)

    # ---- B1: Tổng quan ----
    overview = {
        "n_samples_train": len(tr),
        "n_attributes": len(attrs) - (1 if a.label_col in attrs else 0),
        "id_col_excluded": a.id_col,
        "label_col": a.label_col,
        "dtypes": {c: str(tr[c].dtype) for c in attrs},
        "scales": {c: infer_scale(tr[c], c in ordinal) for c in attrs if c != a.label_col},
    }
    if a.label_col:
        overview["label_distribution"] = {str(k): int(v) for k, v in tr[a.label_col].value_counts(dropna=False).items()}

    # ---- B2: Thống kê mô tả (bỏ thiếu trước khi tính) ----
    desc = {}
    for c in num_cols:
        s = tr[c].dropna()
        if s.empty:
            continue
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        desc[c] = {"n_non_missing": int(s.shape[0]), "n_missing": int(tr[c].isna().sum()),
                   "mean": round(float(s.mean()), 4), "median": round(float(s.median()), 4),
                   "mode": mode_of(s), "q1": round(float(q1), 4), "q3": round(float(q3), 4),
                   "iqr": round(float(q3 - q1), 4), "std": round(float(s.std()), 4)}

    # ---- B5: Ngoại lai (IQR) ----
    outliers = {}
    for c, d in desc.items():
        lower, upper = d["q1"] - a.iqr_k * d["iqr"], d["q3"] + a.iqr_k * d["iqr"]
        s = tr[c].dropna()
        n_out = int(((s < lower) | (s > upper)).sum())
        outliers[c] = {"lower_bound": round(lower, 4), "upper_bound": round(upper, 4),
                       "n_outliers": n_out, "pct_outliers": round(100 * n_out / len(s), 2) if len(s) else 0.0}

    # ---- giá trị ngoài miền hợp lệ (nếu khai) ----
    invalid = {}
    for spec in a.valid_range:
        parts = spec.split(":")
        if len(parts) != 3:
            print(f"CẢNH BÁO: bỏ qua --valid-range không hợp lệ: {spec}")
            continue
        col, lo, hi = parts
        if col not in tr.columns:
            print(f"CẢNH BÁO: cột '{col}' không tồn tại, bỏ qua --valid-range")
            continue
        lo_v = None if lo in ("", "None") else float(lo)
        hi_v = None if hi in ("", "None") else float(hi)
        s = tr[col]
        bad = pd.Series(False, index=s.index)
        if lo_v is not None:
            bad |= s < lo_v
        if hi_v is not None:
            bad |= s > hi_v
        bad &= s.notna()
        invalid[col] = {"valid_min": lo_v, "valid_max": hi_v, "n_invalid": int(bad.sum()),
                        "suggestion": "coi là thiếu (NaN) rồi điền theo P5, hoặc loại dòng nếu ảnh hưởng nhỏ"}

    # ---- B3: Phân phối & quan hệ ----
    skew = {c: round(float(stats.skew(tr[c].dropna())), 3) for c in num_cols if tr[c].dropna().shape[0] > 2}
    skew_note = {c: ("lệch phải mạnh" if v > 1 else "lệch trái mạnh" if v < -1 else "gần đối xứng") for c, v in skew.items()}
    corr = tr[num_cols].corr(numeric_only=True).round(3) if len(num_cols) >= 2 else None

    relevance = {}
    if a.label_col and num_cols:
        y = tr[a.label_col]
        if a.label_type == "numeric":
            for c in num_cols:
                m = tr[[c, a.label_col]].dropna()
                if len(m) > 2:
                    r = np.corrcoef(m[c], m[a.label_col])[0, 1]
                    relevance[c] = {"method": "pearson_vs_label", "value": round(float(r), 3)}
        else:
            for c in num_cols:
                groups = [g[c].dropna().values for _, g in tr[[c, a.label_col]].dropna().groupby(a.label_col) if len(g) > 1]
                if len(groups) >= 2:
                    f, p = stats.f_oneway(*groups)
                    relevance[c] = {"method": "anova_f_vs_label", "f": round(float(f), 3), "p_value": round(float(p), 4)}

    # ---- vẽ biểu đồ ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    for c in num_cols:
        s = tr[c].dropna()
        if s.empty:
            continue
        fig, axes = plt.subplots(1, 2, figsize=(8, 3))
        axes[0].hist(s, bins=30)
        axes[0].set_title(f"Histogram: {c}")
        axes[1].boxplot(s, vert=False)
        axes[1].set_title(f"Boxplot: {c}")
        fig.tight_layout()
        fig.savefig(os.path.join(plot_dir, f"dist_{c}.png"), dpi=100)
        plt.close(fig)

    if corr is not None:
        fig, ax = plt.subplots(figsize=(1 + 0.6 * len(num_cols), 1 + 0.6 * len(num_cols)))
        im = ax.imshow(corr.values, vmin=-1, vmax=1, cmap="coolwarm")
        ax.set_xticks(range(len(num_cols))); ax.set_xticklabels(num_cols, rotation=45, ha="right")
        ax.set_yticks(range(len(num_cols))); ax.set_yticklabels(num_cols)
        fig.colorbar(im)
        fig.tight_layout()
        fig.savefig(os.path.join(plot_dir, "correlation_heatmap.png"), dpi=100)
        plt.close(fig)

        # scatter cho cặp tương quan mạnh nhất (loại đường chéo)
        c2 = corr.copy()
        vals = c2.values.copy()
        np.fill_diagonal(vals, 0)
        if vals.size and np.abs(vals).max() > 0:
            i, j = np.unravel_index(np.argmax(np.abs(vals)), vals.shape)
            x_col, y_col = num_cols[i], num_cols[j]
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.scatter(tr[x_col], tr[y_col], s=10, alpha=0.6)
            ax.set_xlabel(x_col); ax.set_ylabel(y_col)
            ax.set_title(f"Tương quan mạnh nhất: {x_col} vs {y_col} (r={corr.loc[x_col, y_col]:.2f})")
            fig.tight_layout()
            fig.savefig(os.path.join(plot_dir, "top_correlation_scatter.png"), dpi=100)
            plt.close(fig)

    # ---- lưu JSON ----
    result = {"overview": overview, "descriptive_stats": desc, "outliers_iqr": outliers,
              "invalid_values": invalid, "skewness": skew, "skewness_note": skew_note,
              "correlation": corr.to_dict() if corr is not None else None,
              "feature_relevance_to_label": relevance}
    with open(os.path.join(a.out_dir, "eda.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # ---- báo cáo markdown ----
    L = ["# Báo cáo khám phá dữ liệu (EDA) — chỉ trên train", "",
         f"- Số mẫu (train): **{overview['n_samples_train']}**; số thuộc tính (đã loại ID): **{overview['n_attributes']}**", ""]
    L += ["## Thang đo từng thuộc tính", "", "| Thuộc tính | Kiểu | Thang đo |", "|---|---|---|"]
    L += [f"| {c} | {overview['dtypes'][c]} | {overview['scales'][c]} |" for c in overview["scales"]]
    L += [""]
    if invalid:
        L += ["> **Lưu ý:** thang đo ở bảng trên suy đoán từ dữ liệu quan sát được (tỷ lệ nếu mọi giá trị ≥ 0); "
              "cột có giá trị ngoài miền hợp lệ (mục dưới) có thể bị suy đoán sai thang đo — dựa vào ý nghĩa nghiệp vụ, không chỉ bảng này.", ""]
    if a.label_col:
        L += [f"## Biến mục tiêu: `{a.label_col}`", "", f"Phân bố: {overview['label_distribution']}", ""]
    if desc:
        L += ["## Thống kê mô tả (đã bỏ giá trị thiếu)", "",
              "| Cột | N | Thiếu | Mean | Median | Mode | Q1 | Q3 | IQR |", "|---|---|---|---|---|---|---|---|---|"]
        for c, d in desc.items():
            L.append(f"| {c} | {d['n_non_missing']} | {d['n_missing']} | {d['mean']} | {d['median']} | {d['mode']} | {d['q1']} | {d['q3']} | {d['iqr']} |")
        L.append("")
    if outliers:
        L += ["## Ngoại lai (IQR, k={:.1f})".format(a.iqr_k), "", "| Cột | Biên dưới | Biên trên | Số ngoại lai | % |", "|---|---|---|---|---|"]
        for c, d in outliers.items():
            L.append(f"| {c} | {d['lower_bound']} | {d['upper_bound']} | {d['n_outliers']} | {d['pct_outliers']}% |")
        L.append("")
    if invalid:
        L += ["## Giá trị ngoài miền hợp lệ", ""]
        for c, d in invalid.items():
            L.append(f"- `{c}` (hợp lệ: [{d['valid_min']}, {d['valid_max']}]): {d['n_invalid']} giá trị vi phạm — {d['suggestion']}")
        L.append("")
    if skew:
        L += ["## Độ lệch phân phối (skewness)", ""] + [f"- `{c}`: {v} ({skew_note[c]})" for c, v in skew.items()] + [""]
    if relevance:
        L += ["## Độ liên quan với biến mục tiêu (gợi ý chọn đặc trưng ở P5)", ""]
        for c, d in relevance.items():
            L.append(f"- `{c}`: {d}")
        L.append("")
    L += ["## Biểu đồ", "", f"Xem thư mục `eda_plots/` ({len(num_cols)} histogram+boxplot" +
          (", 1 heatmap tương quan, 1 scatter cặp mạnh nhất" if corr is not None else "") + ")", ""]
    with open(os.path.join(a.out_dir, "eda_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    print(f"Số mẫu train: {overview['n_samples_train']}, số thuộc tính: {overview['n_attributes']}")
    print(f"Cột số: {len(num_cols)}, cột hạng mục: {len(cat_cols)}")
    for c, d in outliers.items():
        if d["n_outliers"]:
            print(f"  CẢNH BÁO: '{c}' có {d['n_outliers']} ngoại lai ({d['pct_outliers']}%)")
    for c, d in invalid.items():
        print(f"  CẢNH BÁO: '{c}' có {d['n_invalid']} giá trị ngoài miền hợp lệ")
    print(f"Đã ghi {os.path.join(a.out_dir, 'eda_report.md')} và eda.json")


if __name__ == "__main__":
    main()
