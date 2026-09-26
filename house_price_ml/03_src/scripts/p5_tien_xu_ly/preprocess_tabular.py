#!/usr/bin/env python3
"""
preprocess_tabular.py - Tiền xử lý dữ liệu bảng: HỌC trên train, ÁP DỤNG lên val/test, có kiểm chứng.

  fit    đọc file chia (có cột 'split'), fit CHỈ trên dòng split=='train', lưu bộ tiền xử lý và áp lên cả 3 split
  check  nạp lại bộ tiền xử lý và kiểm chứng nó chỉ học từ train (thoát mã 2 nếu thất bại)
  apply  áp bộ tiền xử lý đã lưu lên file mới (vd dữ liệu lúc suy luận) - chỉ transform, không fit

Ví dụ:
  python preprocess_tabular.py fit --split-csv 01_data/splits/split_v1.csv --out-dir 01_data/processed \
      --label-col label --label-type class --id-col _row_id --impute median --scaler standard \
      [--dedup-train] [--valid-range luong:0:None] [--drop-missing-thresh 0.5] \
      [--select-anova-thresh 0.05] [--bin Tuoi:equal-width:5 Luong:equal-frequency:4] [--pca 10]
  (--valid-range và --bin nhận NHIỀU giá trị sau MỘT cờ, không lặp lại cờ nhiều lần)
  python preprocess_tabular.py check --split-csv 01_data/splits/split_v1.csv --out-dir 01_data/processed
  python preprocess_tabular.py apply --new-csv new.csv --out-dir 01_data/processed --out new_processed.csv

Đầu ra trong --out-dir:
  preprocessor.joblib         ColumnTransformer (hoặc Pipeline nếu có --pca) đã fit (chỉ từ train)
  preprocess_meta.json        cột, chiến lược, giá trị học được, số dòng train, SHA256 file chia, cảnh báo
  processed_{train,val,test}.csv   đặc trưng đã xử lý + cột id, split, label (và label_idx nếu là phân loại)

Quy tắc áp dụng (mọi bước có HỌC đều chỉ fit trên train, val/test/apply chỉ transform):
  - --valid-range col:min:max  (B4) đánh dấu giá trị NGOÀI miền hợp lệ thành thiếu (NaN), TRƯỚC khi điền.
    Đây là quy tắc nghiệp vụ cố định (không học từ dữ liệu) nên áp như nhau cho mọi split.
  - --impute mean|median|most_frequent: fit trên train. --impute min|max: điền bằng min/max của TRAIN.
  - --drop-missing-thresh T  (B7) loại cột có tỉ lệ thiếu > T tính trên TRAIN (sau khi đánh dấu valid-range).
  - --select-anova-thresh P / --select-corr-thresh R  (B7) loại cột số có độ liên quan với nhãn (ANOVA
    p-value hoặc Pearson |r|, tính trên TRAIN) không đạt ngưỡng. Cần --label-col.
  - --bin col:strategy:nbins  (B6, rời rạc hóa) strategy = equal-width | equal-frequency. Biên khoảng học
    từ TRAIN (KBinsDiscretizer), áp cùng biên đó cho val/test. Cột được điền thiếu bằng median của TRAIN
    trước khi chia khoảng.
  - --pca N  (B7, giảm chiều) PCA fit trên đặc trưng train ĐÃ điền/chuẩn hóa/mã hóa, áp cùng phép chiếu
    cho val/test. Đặc trưng đầu ra đổi thành pca0..pca{N-1}.
  - --dedup-train: bỏ dòng trùng CHỈ ở train, không áp lên val/test.
"""
import argparse
import hashlib
import json
import os
import sys

import joblib
import numpy as np
import pandas as pd
import sklearn
from scipy import stats
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import KBinsDiscretizer, MinMaxScaler, OneHotEncoder, StandardScaler

HELPER_COLS = {"split", "_row_id", "_rowhash", "sha256", "rel_path", "ext", "size", "orig_split",
               "usable", "is_junk", "corrupt", "width", "height", "mode"}


def sha256_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def make_scaler(kind):
    return {"standard": StandardScaler(), "minmax": MinMaxScaler(), "none": None}[kind]


def parse_valid_range(specs):
    """['col:min:max', ...] -> [(col, lo_or_None, hi_or_None), ...]. min/max rỗng hoặc 'None' = không giới hạn phía đó."""
    out = []
    for spec in specs or []:
        parts = spec.split(":")
        if len(parts) != 3:
            sys.exit(f"--valid-range không hợp lệ (cần col:min:max): {spec}")
        col, lo, hi = parts
        lo_v = None if lo in ("", "None") else float(lo)
        hi_v = None if hi in ("", "None") else float(hi)
        out.append([col, lo_v, hi_v])
    return out


def apply_valid_range(df, specs):
    """Đánh dấu giá trị ngoài miền hợp lệ thành NaN. specs: [(col, lo, hi), ...]. Trả về (df mới, {col: số ô bị đánh dấu})."""
    df = df.copy()
    counts = {}
    for col, lo, hi in specs:
        if col not in df.columns:
            continue
        bad = pd.Series(False, index=df.index)
        if lo is not None:
            bad |= df[col] < lo
        if hi is not None:
            bad |= df[col] > hi
        bad &= df[col].notna()
        counts[col] = int(bad.sum())
        df.loc[bad, col] = np.nan
    return df, counts


def parse_bin_specs(specs):
    """['col:equal-width:5', ...] -> [(col, 'uniform'|'quantile', n_bins), ...]"""
    out = []
    strat_map = {"equal-width": "uniform", "equal-frequency": "quantile"}
    for spec in specs or []:
        parts = spec.split(":")
        if len(parts) != 3 or parts[1] not in strat_map:
            sys.exit(f"--bin không hợp lệ (cần col:equal-width|equal-frequency:n_bins): {spec}")
        out.append((parts[0], strat_map[parts[1]], int(parts[2])))
    return out


def build_preprocessor(train, num_cols, cat_cols, impute, scaler, bin_specs):
    """Trả về ColumnTransformer chưa fit. min/max: bộ điền riêng cho từng cột với giá trị lấy từ TRAIN.
    bin_specs: [(col, sklearn_strategy, n_bins), ...] - các cột này KHÔNG được có mặt trong num_cols."""
    transformers = []
    if num_cols:
        if impute in ("mean", "median", "most_frequent"):
            steps = [("imp", SimpleImputer(strategy=impute))]
            if scaler != "none":
                steps.append(("sc", make_scaler(scaler)))
            transformers.append(("num", Pipeline(steps), num_cols))
        elif impute in ("min", "max"):
            for i, c in enumerate(num_cols):
                fv = train[c].min() if impute == "min" else train[c].max()
                if pd.isna(fv):
                    fv = 0.0
                steps = [("imp", SimpleImputer(strategy="constant", fill_value=float(fv)))]
                if scaler != "none":
                    steps.append(("sc", make_scaler(scaler)))
                transformers.append((f"num{i}", Pipeline(steps), [c]))
        else:
            sys.exit(f"--impute không hợp lệ: {impute}")
    if cat_cols:
        transformers.append(("cat", Pipeline([
            ("imp", SimpleImputer(strategy="most_frequent")),
            ("oh", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]), cat_cols))
    for col, strat, n_bins in bin_specs:
        transformers.append((f"bin_{col}", Pipeline([
            ("imp", SimpleImputer(strategy="median")),
            ("bin", KBinsDiscretizer(n_bins=n_bins, encode="ordinal", strategy=strat)),
        ]), [col]))
    return ColumnTransformer(transformers, remainder="drop", verbose_feature_names_out=False)


def get_ct(pre):
    """pre có thể là ColumnTransformer thuần, hoặc Pipeline([("pre", ColumnTransformer), ("pca", PCA)])."""
    if isinstance(pre, Pipeline) and "pre" in pre.named_steps:
        return pre.named_steps["pre"]
    return pre


def feature_names(pre):
    ct = get_ct(pre)
    try:
        names = list(ct.get_feature_names_out())
    except Exception:  # noqa: BLE001
        names = [f"f{i}" for i in range(ct.transform(pd.DataFrame(columns=ct.feature_names_in_)).shape[1])]
    if isinstance(pre, Pipeline) and "pca" in pre.named_steps:
        n = pre.named_steps["pca"].n_components_
        return [f"pca{i}" for i in range(n)]
    return names


def compute_relevance(tr, num_cols, label_col, label_type):
    """Trả {col: relevance} - Pearson |r| (label numeric) hoặc ANOVA p-value (label phân loại, càng nhỏ càng liên quan)."""
    out = {}
    for c in num_cols:
        m = tr[[c, label_col]].dropna()
        if label_type == "numeric":
            if len(m) > 2 and m[c].std() > 0:
                out[c] = abs(float(np.corrcoef(m[c], m[label_col])[0, 1]))
        else:
            groups = [g[c].values for _, g in m.groupby(label_col) if len(g) > 1]
            if len(groups) >= 2:
                try:
                    _, p = stats.f_oneway(*groups)
                    out[c] = float(p)
                except Exception:  # noqa: BLE001
                    pass
    return out


def load_meta(out_dir):
    with open(os.path.join(out_dir, "preprocess_meta.json"), encoding="utf-8") as f:
        return json.load(f)


def cmd_fit(a):
    df = pd.read_csv(a.split_csv, keep_default_na=True, low_memory=False)
    if "split" not in df.columns:
        sys.exit("File chia phải có cột 'split'")

    # B4: giá trị ngoài miền hợp lệ -> NaN (quy tắc nghiệp vụ, áp như nhau mọi split, không học từ dữ liệu)
    valid_range = parse_valid_range(a.valid_range)
    df, invalid_counts = apply_valid_range(df, valid_range)

    tr = df[df["split"] == "train"].copy()
    n_train_raw = len(tr)
    dedup_removed = 0
    if a.dedup_train:  # bước CHỈ cho train
        feat_cols_all = [c for c in tr.columns if c not in HELPER_COLS]
        before = len(tr)
        tr = tr.drop_duplicates(subset=feat_cols_all)
        dedup_removed = before - len(tr)

    drop = set(a.drop_cols or []) | HELPER_COLS | {a.id_col, a.label_col}
    feats = [c for c in df.columns if c not in drop and c is not None]
    cat_cols = [c for c in (a.cat_cols or []) if c in feats]
    num_cols = [c for c in feats if c not in cat_cols and pd.api.types.is_numeric_dtype(df[c])]
    auto_cat = [c for c in feats if c not in num_cols and c not in cat_cols]
    if auto_cat:
        print(f"Cột không phải số, xử lý như hạng mục: {auto_cat}")
        cat_cols += auto_cat

    # B7a: loại cột thiếu quá nhiều, tính tỉ lệ thiếu trên TRAIN
    dropped_missing = []
    if a.drop_missing_thresh is not None:
        for c in list(num_cols) + list(cat_cols):
            ratio = tr[c].isna().mean()
            if ratio > a.drop_missing_thresh:
                dropped_missing.append((c, round(float(ratio), 3)))
        for c, _ in dropped_missing:
            if c in num_cols:
                num_cols.remove(c)
            if c in cat_cols:
                cat_cols.remove(c)

    # B7b: loại cột số ít liên quan tới nhãn, tính trên TRAIN
    dropped_relevance = []
    if a.label_col and (a.select_anova_thresh is not None or a.select_corr_thresh is not None):
        rel = compute_relevance(tr, num_cols, a.label_col, a.label_type)
        for c, v in rel.items():
            keep = (v <= a.select_anova_thresh) if a.label_type == "class" else (v >= a.select_corr_thresh)
            if not keep:
                dropped_relevance.append((c, round(v, 4)))
        for c, _ in dropped_relevance:
            num_cols.remove(c)

    # B6: rời rạc hóa - tách các cột --bin ra khỏi num_cols để xử lý riêng
    bin_specs = parse_bin_specs(a.bin)
    bin_specs = [(c, s, n) for c, s, n in bin_specs if c in num_cols]
    for c, _, _ in bin_specs:
        num_cols.remove(c)

    ct = build_preprocessor(tr, num_cols, cat_cols, a.impute, a.scaler, bin_specs)
    all_cols = num_cols + cat_cols + [c for c, _, _ in bin_specs]
    if a.pca:
        pre = Pipeline([("pre", ct), ("pca", PCA(n_components=a.pca, random_state=42))])
    else:
        pre = ct
    pre.fit(tr[all_cols])                       # <-- CHỈ train
    names = feature_names(pre)

    os.makedirs(a.out_dir, exist_ok=True)
    classes = None
    if a.label_col and a.label_type == "class":
        classes = sorted(tr[a.label_col].dropna().astype(str).unique())
    c2i = {c: i for i, c in enumerate(classes)} if classes else None

    warns = []
    processed = {}
    for sp in ("train", "val", "test"):
        part = df[df["split"] == sp].copy()
        if sp == "train" and a.dedup_train:
            part = tr
        n_nan = int(part[all_cols].isna().sum().sum())
        X = pre.transform(part[all_cols])
        out = pd.DataFrame(X, columns=names, index=part.index)
        for extra in (a.id_col, "split"):
            if extra in part.columns:
                out[extra] = part[extra].values
        if a.label_col:
            out[a.label_col] = part[a.label_col].values
            if c2i is not None:
                idx = part[a.label_col].astype(str).map(c2i)
                if idx.isna().any():
                    warns.append(f"{sp}: {int(idx.isna().sum())} nhãn không có trong train")
                out["label_idx"] = idx.values
        out.to_csv(os.path.join(a.out_dir, f"processed_{sp}.csv"), index=False)
        processed[sp] = {"rows": len(out), "nan_before": n_nan, "nan_after": int(pd.DataFrame(X).isna().sum().sum())}
        if cat_cols and sp != "train":
            for c in cat_cols:
                unseen = set(part[c].dropna().astype(str)) - set(tr[c].dropna().astype(str))
                if unseen:
                    warns.append(f"{sp}: cột '{c}' có giá trị chưa thấy ở train {sorted(unseen)[:5]} (mã hóa thành 0)")
    joblib.dump(pre, os.path.join(a.out_dir, "preprocessor.joblib"))

    learned = {}
    for name, tf, cols in get_ct(pre).transformers_:
        if name == "remainder":
            continue
        for step_name, step in tf.steps:
            if step_name == "imp":
                learned[f"{name}.impute_value"] = np.asarray(step.statistics_).tolist()
            if step_name == "sc":
                if hasattr(step, "mean_"):
                    learned[f"{name}.scaler_mean"] = step.mean_.tolist()
                    learned[f"{name}.scaler_scale"] = step.scale_.tolist()
                if hasattr(step, "data_min_"):
                    learned[f"{name}.scaler_min"] = step.data_min_.tolist()
                    learned[f"{name}.scaler_max"] = step.data_max_.tolist()
            if step_name == "bin":
                learned[f"{name}.bin_edges"] = [e.tolist() for e in step.bin_edges_]
    pca_info = None
    if a.pca:
        p = pre.named_steps["pca"]
        pca_info = {"n_components": p.n_components_, "explained_variance_ratio": p.explained_variance_ratio_.round(4).tolist(),
                   "total_explained_variance": round(float(p.explained_variance_ratio_.sum()), 4)}

    meta = {
        "sklearn_version": sklearn.__version__, "split_csv": a.split_csv,
        "split_csv_sha256": sha256_file(a.split_csv),
        "n_train_rows_fit": len(tr), "n_train_rows_before_dedup": n_train_raw, "dedup_train_removed": dedup_removed,
        "num_cols": num_cols, "cat_cols": cat_cols, "impute": a.impute, "scaler": a.scaler,
        "id_col": a.id_col, "label_col": a.label_col, "label_type": a.label_type, "classes": classes,
        "valid_range": valid_range, "invalid_value_counts_train": invalid_counts,
        "drop_missing_thresh": a.drop_missing_thresh, "dropped_missing_cols": dropped_missing,
        "select_anova_thresh": a.select_anova_thresh, "select_corr_thresh": a.select_corr_thresh,
        "dropped_relevance_cols": dropped_relevance,
        "bin_specs": bin_specs, "pca_n": a.pca, "pca_info": pca_info,
        "feature_names_out": names, "learned": learned, "processed": processed, "warnings": warns,
    }
    with open(os.path.join(a.out_dir, "preprocess_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"FIT xong trên {len(tr)} dòng train (loại {dedup_removed} dòng trùng, chỉ ở train).")
    print(f"  số cột: {len(num_cols)} số + {len(cat_cols)} hạng mục + {len(bin_specs)} rời rạc hóa -> {len(names)} đặc trưng; impute={a.impute}, scaler={a.scaler}")
    if invalid_counts:
        print(f"  giá trị ngoài miền hợp lệ (đã đánh dấu thiếu): {invalid_counts}")
    if dropped_missing:
        print(f"  loại vì thiếu quá {a.drop_missing_thresh:.0%}: {dropped_missing}")
    if dropped_relevance:
        print(f"  loại vì ít liên quan tới nhãn: {dropped_relevance}")
    if pca_info:
        print(f"  PCA: {pca_info['n_components']} thành phần, giữ {pca_info['total_explained_variance']:.1%} phương sai")
    for sp, v in processed.items():
        print(f"  {sp}: {v['rows']} dòng, NaN trước={v['nan_before']} sau={v['nan_after']}")
    for w in warns:
        print("  CẢNH BÁO:", w)


def cmd_check(a):
    meta = load_meta(a.out_dir)
    pre = joblib.load(os.path.join(a.out_dir, "preprocessor.joblib"))
    df = pd.read_csv(a.split_csv, low_memory=False)
    problems = []
    if sha256_file(a.split_csv) != meta["split_csv_sha256"]:
        problems.append("file chia đã thay đổi so với lúc fit (SHA256 khác)")

    valid_range = [tuple(x) for x in meta.get("valid_range", [])]
    df, invalid_counts = apply_valid_range(df, valid_range)

    tr = df[df["split"] == "train"]
    if meta["dedup_train_removed"]:
        tr = tr.drop_duplicates(subset=[c for c in tr.columns if c not in HELPER_COLS])
    n_tr = len(tr)
    if n_tr != meta["n_train_rows_fit"]:
        problems.append(f"số dòng train hiện tại {n_tr} != lúc fit {meta['n_train_rows_fit']}")
    for c, expected in meta.get("invalid_value_counts_train", {}).items():
        if invalid_counts.get(c, 0) != expected:
            problems.append(f"'{c}': số giá trị ngoài miền hợp lệ hiện tại {invalid_counts.get(c, 0)} != lúc fit {expected}")

    ct = get_ct(pre)
    for name, tf, cols in ct.transformers_:
        if name == "remainder":
            continue
        for step_name, step in tf.steps:
            if step_name == "sc" and hasattr(step, "n_samples_seen_"):
                seen = int(np.max(np.atleast_1d(step.n_samples_seen_)))
                # scaler nhìn thấy dòng sau khi điền thiếu -> phải bằng số dòng train
                if seen != n_tr:
                    problems.append(f"{name}: scaler thấy {seen} dòng != {n_tr} dòng train (có thể đã fit trên dữ liệu khác)")
            if step_name == "imp" and meta["impute"] in ("mean", "median", "min", "max") and name.startswith("num"):
                exp = getattr(tr[cols], {"mean": "mean", "median": "median", "min": "min", "max": "max"}[meta["impute"]])()
                got = np.asarray(step.statistics_, dtype=float)
                if not np.allclose(exp.values.astype(float), got, equal_nan=True, rtol=1e-6, atol=1e-9):
                    problems.append(f"{name}: giá trị điền không khớp {meta['impute']} của TRAIN (mong đợi {exp.values}, có {got})")
            if step_name == "bin":
                col = cols[0]
                imp_step = tf.named_steps["imp"]
                filled = tr[[col]].fillna(float(np.asarray(imp_step.statistics_)[0]))
                ref = KBinsDiscretizer(n_bins=step.n_bins_[0], encode="ordinal", strategy=step.strategy).fit(filled)
                if not all(np.allclose(a_, b_, rtol=1e-6, atol=1e-9) for a_, b_ in zip(step.bin_edges_, ref.bin_edges_)):
                    problems.append(f"{name}: biên khoảng (bin_edges) không khớp lúc fit lại trên TRAIN hiện tại")

    # đặc trưng train đã lưu phải tái tạo được từ bộ tiền xử lý (bao trùm cả bin/PCA/feature-selection)
    p_train = pd.read_csv(os.path.join(a.out_dir, "processed_train.csv"))
    all_cols = meta["num_cols"] + meta["cat_cols"] + [c for c, _, _ in meta.get("bin_specs", [])]
    re = pre.transform(tr[all_cols])
    saved = p_train[meta["feature_names_out"]].values
    if re.shape != saved.shape:
        problems.append(f"số đặc trưng khác lúc fit ({re.shape[1]} vs {saved.shape[1]}): bộ tiền xử lý có thể đã fit lại trên dữ liệu khác (vd có cả val/test)")
    elif not np.allclose(saved, re, atol=1e-6):
        problems.append("processed_train.csv không tái tạo được từ preprocessor.joblib")

    # thông tin (không phải lỗi): độ lệch phân bố giữa train và test
    te = df[df["split"] == "test"]
    for c in meta["num_cols"]:
        if te[c].notna().any() and tr[c].std() > 0:
            z = abs(te[c].mean() - tr[c].mean()) / tr[c].std()
            if z > 1:
                print(f"  LƯU Ý: cột '{c}' trung bình test lệch {z:.1f} độ lệch chuẩn so với train (kiểm tra dịch chuyển phân bố)")
    print("KIỂM CHỨNG:", "FAILED: " + "; ".join(problems) if problems else "PASSED (bộ tiền xử lý chỉ học từ train)")
    sys.exit(2 if problems else 0)


def cmd_apply(a):
    meta = load_meta(a.out_dir)
    pre = joblib.load(os.path.join(a.out_dir, "preprocessor.joblib"))
    new = pd.read_csv(a.new_csv, low_memory=False)
    valid_range = [tuple(x) for x in meta.get("valid_range", [])]
    new, _ = apply_valid_range(new, valid_range)
    need = meta["num_cols"] + meta["cat_cols"] + [c for c, _, _ in meta.get("bin_specs", [])]
    miss = [c for c in need if c not in new.columns]
    if miss:
        sys.exit(f"Thiếu cột: {miss}")
    X = pre.transform(new[need])
    out = pd.DataFrame(X, columns=meta["feature_names_out"], index=new.index)
    out.to_csv(a.out, index=False)
    print(f"APPLY (chỉ transform): {len(out)} dòng -> {a.out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fit")
    f.add_argument("--split-csv", required=True)
    f.add_argument("--out-dir", required=True)
    f.add_argument("--label-col")
    f.add_argument("--label-type", default="class", choices=["class", "numeric"])
    f.add_argument("--id-col", default="_row_id")
    f.add_argument("--drop-cols", nargs="*")
    f.add_argument("--cat-cols", nargs="*")
    f.add_argument("--impute", default="median", choices=["mean", "median", "most_frequent", "min", "max"])
    f.add_argument("--scaler", default="standard", choices=["standard", "minmax", "none"])
    f.add_argument("--dedup-train", action="store_true", help="bỏ dòng trùng CHỈ ở train")
    f.add_argument("--valid-range", nargs="*", default=[], help="col:min:max (B4) - vd luong:0:None; nhiều cột trong CÙNG một --valid-range (không lặp cờ)")
    f.add_argument("--drop-missing-thresh", type=float, help="B7: loại cột có tỉ lệ thiếu (trên train) > ngưỡng này")
    f.add_argument("--select-anova-thresh", type=float, help="B7: giữ cột có p-value ANOVA <= ngưỡng (cần --label-col, label-type=class)")
    f.add_argument("--select-corr-thresh", type=float, help="B7: giữ cột có |Pearson r| >= ngưỡng (cần --label-col, label-type=numeric)")
    f.add_argument("--bin", nargs="*", default=[], help="B6: col:equal-width|equal-frequency:n_bins, nhiều cột trong CÙNG một --bin (không lặp cờ)")
    f.add_argument("--pca", type=int, help="B7: số thành phần PCA giữ lại (fit trên train)")
    c = sub.add_parser("check")
    c.add_argument("--split-csv", required=True)
    c.add_argument("--out-dir", required=True)
    p = sub.add_parser("apply")
    p.add_argument("--new-csv", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--out", required=True)
    a = ap.parse_args()
    {"fit": cmd_fit, "check": cmd_check, "apply": cmd_apply}[a.cmd](a)


if __name__ == "__main__":
    main()
