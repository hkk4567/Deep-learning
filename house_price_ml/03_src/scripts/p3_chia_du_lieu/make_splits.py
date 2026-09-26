#!/usr/bin/env python3
"""
make_splits.py - Chia train/val/test CO KIEM CHUNG khong ro ri, luu file chia de tai lap.

  python make_splits.py --table 01_data/audit/manifest.csv --out 01_data/splits --version v1 \
      [--id-col rel_path] [--label-col label] [--group-col G] [--time-col T] [--sha-col sha256] \
      [--val 0.15] [--test 0.15] [--seed 42] [--include-unusable]

Chien luoc (tu dong chon):
  --time-col        -> chia theo thoi gian (cu nhat = train, moi nhat = test), KHONG tron ngau nhien
  co nhom (group)   -> nhom khong bi tach qua nhieu split (StratifiedGroupKFold neu co nhan)
  chi co nhan       -> stratified
  khong co gi       -> ngau nhien
Neu khong co --group-col nhung co cot sha256, dung sha256 lam nhom => ban sao giong het luon nam CUNG mot split.

Dau ra: split_<version>.csv (them cot 'split'), split_<version>_summary.json (so luong, ty le lop, SHA256 file chia).
Kiem chung tu dong (thoat ma 2 neu that bai): id khong nam o >1 split; nhom/sha256 khong xuyen split; moi lop co mat o ca 3 split.
"""
import argparse
import hashlib
import json
import os
import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, StratifiedGroupKFold, train_test_split


def stage(df, frac, seed, label, group, has_group):
    """Tach 'frac' cua df thanh phan rieng. Tra (rest_idx, part_idx) la chi so vi tri."""
    n = len(df)
    pos = np.arange(n)
    y = df[label].values if label else None
    g = df[group].values if has_group else None
    if has_group and label:
        k = max(2, round(1 / frac))
        sgkf = StratifiedGroupKFold(n_splits=k, shuffle=True, random_state=seed)
        rest, part = next(sgkf.split(pos, y, g))
        return rest, part
    if has_group:
        gss = GroupShuffleSplit(n_splits=1, test_size=frac, random_state=seed)
        rest, part = next(gss.split(pos, groups=g))
        return rest, part
    try:
        rest, part = train_test_split(pos, test_size=frac, random_state=seed, stratify=y if label else None)
    except ValueError as e:
        print(f"CANH BAO: stratify that bai ({e}); dung chia ngau nhien.", file=sys.stderr)
        rest, part = train_test_split(pos, test_size=frac, random_state=seed)
    return rest, part


def verify(out, id_col, group, sha_col, label, n_expected=None, time_mode=False):
    """Tra ve list van de (rong = dat). Dung ca luc chia va khi --verify file co san."""
    problems = []
    by_split = {s_: set(out.loc[out["split"] == s_, id_col]) for s_ in ("train", "val", "test")}
    for x, y_ in (("train", "val"), ("train", "test"), ("val", "test")):
        ov = by_split[x] & by_split[y_]
        if ov:
            problems.append(f"id nam o ca {x} va {y_}: {len(ov)}")
    if n_expected is not None and len(out) != n_expected:
        problems.append(f"so dong sau chia ({len(out)}) != truoc chia ({n_expected})")
    cols = [c for c in (group, sha_col if sha_col in out.columns and (out[sha_col].astype(str) != "").all() else None) if c]
    for col in dict.fromkeys(cols):
        if time_mode and col != group:
            continue
        bad = int((out.groupby(col)["split"].nunique() > 1).sum())
        if bad:
            problems.append(f"{bad} gia tri cua '{col}' xuyen nhieu split (ro ri)")
    if label and label in out.columns:
        present = out.groupby(label)["split"].nunique()
        miss = present[present < 3].index.tolist()
        if miss:
            print(f"CANH BAO: lop khong co mat o du 3 split: {miss}", file=sys.stderr)
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--table")
    ap.add_argument("--out")
    ap.add_argument("--verify", help="chi kiem chung file chia co san (co cot 'split'), khong chia lai")
    ap.add_argument("--version", default="v1")
    ap.add_argument("--id-col", default="rel_path")
    ap.add_argument("--label-col")
    ap.add_argument("--group-col")
    ap.add_argument("--time-col")
    ap.add_argument("--sha-col", default="sha256")
    ap.add_argument("--val", type=float, default=0.15)
    ap.add_argument("--test", type=float, default=0.15)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--header", default="infer", choices=["infer", "none"], help="none: file bang khong co header (cot dat ten col0, col1...)")
    ap.add_argument("--include-unusable", action="store_true",
                    help="giu ca dong usable=False (rac/hong/khong nhan). Mac dinh: loai neu co cot 'usable'")
    a = ap.parse_args()

    if a.verify:
        v = pd.read_csv(a.verify, keep_default_na=False, low_memory=False)
        lab = a.label_col if a.label_col in v.columns else None
        probs = verify(v, a.id_col, a.group_col if a.group_col in v.columns else None, a.sha_col, lab)
        print("KIEM CHUNG:", "FAILED: " + "; ".join(probs) if probs else "PASSED", f"({len(v)} dong, {v['split'].value_counts().to_dict()})")
        sys.exit(2 if probs else 0)
    if not a.table or not a.out:
        sys.exit("Can --table va --out (hoac --verify FILE)")

    df = pd.read_csv(a.table, keep_default_na=False, low_memory=False, header=None if a.header == "none" else "infer")
    if a.header == "none":
        df.columns = [f"col{i}" for i in range(df.shape[1])]
    n0 = len(df)
    if a.id_col not in df.columns and a.id_col == "rel_path":
        # bang du lieu (moi dong = 1 mau), khong phai manifest file
        df["_row_id"] = np.arange(len(df))
        a.id_col = "_row_id"
        if a.sha_col not in df.columns:  # dong trung noi dung -> cung mot nhom, tranh ro ri
            feat = df.drop(columns=["_row_id"])
            df["_rowhash"] = pd.util.hash_pandas_object(feat, index=False).astype(str)
            a.sha_col = "_rowhash"
        print("Bang du lieu: tao _row_id va _rowhash (dong trung se nam cung split)")
    if "usable" in df.columns and not a.include_unusable:
        df = df[df["usable"].astype(str).str.lower().isin(["true", "1"])]
        print(f"Loai {n0 - len(df)} dong usable=False (rac/hong/khong nhan)")
    if a.id_col not in df.columns:
        sys.exit(f"Khong co cot id '{a.id_col}' trong {a.table}")
    if df[a.id_col].duplicated().any():
        sys.exit(f"Cot id '{a.id_col}' co gia tri trung; can id duy nhat.")
    label = a.label_col if a.label_col and a.label_col in df.columns else None
    if label and (df[label].astype(str) == "").all():
        label = None
    if a.label_col and not label:
        print(f"CANH BAO: cot nhan '{a.label_col}' khong co/rong -> khong stratify.", file=sys.stderr)
    df = df.reset_index(drop=True)

    group, strategy = None, None
    if a.time_col:
        strategy = "time"
    elif a.group_col and a.group_col in df.columns:
        group, strategy = a.group_col, "group" + ("+stratified" if label else "")
    elif a.sha_col in df.columns and (df[a.sha_col].astype(str) != "").all():
        group, strategy = a.sha_col, "sha256-group" + ("+stratified" if label else "")
    else:
        strategy = "stratified" if label else "random"
    has_group = group is not None

    if strategy == "time":
        d = df.sort_values(a.time_col, kind="stable").reset_index(drop=True)
        n = len(d)
        n_test, n_val = int(round(n * a.test)), int(round(n * a.val))
        split = np.array(["train"] * n, dtype=object)
        split[n - n_test:] = "test"
        split[n - n_test - n_val: n - n_test] = "val"
        d["split"] = split
        out = d
    else:
        rest_i, test_i = stage(df, a.test, a.seed, label, group, has_group)
        rest = df.iloc[rest_i].reset_index(drop=True)
        test = df.iloc[test_i]
        val_frac = a.val / (1 - a.test)
        tr_i, va_i = stage(rest, val_frac, a.seed + 1, label, group, has_group)
        train, val = rest.iloc[tr_i], rest.iloc[va_i]
        out = pd.concat([train.assign(split="train"), val.assign(split="val"), test.assign(split="test")])
        out = out.reset_index(drop=True)

    # ---- kiem chung ----
    problems = verify(out, a.id_col, group, a.sha_col, label, n_expected=len(df), time_mode=(strategy == "time"))

    os.makedirs(a.out, exist_ok=True)
    f_csv = os.path.join(a.out, f"split_{a.version}.csv")
    out.to_csv(f_csv, index=False)
    with open(f_csv, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    summ = {
        "version": a.version, "strategy": strategy, "seed": a.seed, "val_frac": a.val, "test_frac": a.test,
        "n_input": n0, "n_after_filter": len(df), "counts": out["split"].value_counts().to_dict(),
        "group_col": group, "label_col": label, "time_col": a.time_col,
        "class_counts": (out.groupby(["split", label]).size().unstack(0).fillna(0).astype(int).to_dict("index") if label else None),
        "split_file_sha256": sha, "verification": "FAILED: " + "; ".join(problems) if problems else "PASSED",
    }
    with open(os.path.join(a.out, f"split_{a.version}_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summ, f, ensure_ascii=False, indent=2, default=str)

    print(f"strategy={strategy}  counts={summ['counts']}  sha256={sha[:12]}...")
    if label:
        print(pd.DataFrame(summ["class_counts"]).T.to_string())
    print("KIEM CHUNG:", summ["verification"])
    if problems:
        sys.exit(2)


if __name__ == "__main__":
    main()
