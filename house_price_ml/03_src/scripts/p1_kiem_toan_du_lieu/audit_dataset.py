#!/usr/bin/env python3
"""
audit_dataset.py - Kiem toan dataset tho (khong sua gi trong thu muc raw).

  python audit_dataset.py --raw 00_raw --out 01_data/audit \
      [--label-col LABEL] [--table-header infer|none] [--no-image-check] [--no-hash]

Dau ra trong --out:
  manifest.csv     moi file: rel_path, ext, size, sha256, label (suy ra tu thu muc), orig_split, width, height, mode, corrupt
  duplicates.csv   nhom file trung noi dung (sha256)
  corrupt.csv      file hong (neu co)
  audit.json       so lieu may doc duoc (kem dataset_fingerprint)
  data_report.md   bao cao tieng Viet, kem danh sach CANH BAO tu dong

Nhan duoc suy ra tu cau truc  raw/<lop>/...  hoac  raw/<train|val|test>/<lop>/...  (cho anh/audio).
Voi bang (.csv/.tsv/.xlsx/.parquet): thong ke cot, null, dong trung, cot hang so, phan bo nhan (--label-col).
"""
import argparse
import hashlib
import json
import os
import statistics
import wave
from collections import Counter, defaultdict

import pandas as pd

IMG = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tif", ".tiff"}
TAB = {".csv", ".tsv", ".xlsx", ".xls", ".parquet"}
AUD = {".wav"}
TXT = {".txt"}
JUNK_NAMES = {"desktop.ini", ".ds_store", "thumbs.db"}
SPLIT_NAMES = {"train", "training", "val", "valid", "validation", "test", "testing"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def infer_label(parts):
    """parts = phan cua duong dan tuong doi. Tra (label, orig_split)."""
    if len(parts) >= 3 and parts[0].lower() in SPLIT_NAMES:
        return parts[1], parts[0]
    if len(parts) >= 2:
        return parts[0], ""
    return "", ""


def check_image(path):
    from PIL import Image
    try:
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            im.load()
            return im.width, im.height, im.mode, False
    except Exception:
        return None, None, None, True


def audit_table(path, label_col, header):
    ext = os.path.splitext(path)[1].lower()
    kw = {"header": None} if header == "none" else {}
    try:
        if ext in (".csv", ".tsv"):
            df = pd.read_csv(path, sep="\t" if ext == ".tsv" else ",", **kw)
        elif ext in (".xlsx", ".xls"):
            df = pd.read_excel(path, **kw)
        else:
            df = pd.read_parquet(path)
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:200]}
    if header == "none":
        df.columns = [f"col{i}" for i in range(df.shape[1])]
    info = {
        "shape": list(df.shape),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "nulls": {c: int(n) for c, n in df.isna().sum().items() if n},
        "duplicate_rows": int(df.duplicated().sum()),
        "constant_cols": [c for c in df.columns if df[c].nunique(dropna=False) <= 1],
        "high_card_object_cols": [c for c in df.select_dtypes(include=["object", "string"]).columns if df[c].nunique() > 0.5 * len(df)],
    }
    num = df.select_dtypes("number")
    if not num.empty:
        d = num.describe().T[["min", "max", "mean", "std"]].round(4)
        info["numeric_summary"] = d.to_dict("index")
    lc = label_col
    if header == "none" and label_col is None:
        lc = None
    if lc and lc in df.columns:
        info["label_distribution"] = {str(k): int(v) for k, v in df[lc].value_counts(dropna=False).items()}
    return info


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--label-col", help="ten cot nhan trong file bang")
    ap.add_argument("--table-header", default="infer", choices=["infer", "none"])
    ap.add_argument("--no-image-check", action="store_true")
    ap.add_argument("--no-hash", action="store_true")
    a = ap.parse_args()

    raw = os.path.abspath(a.raw)
    os.makedirs(a.out, exist_ok=True)
    rows, junk = [], []
    for dp, _, fs in os.walk(raw):
        for f in sorted(fs):
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, raw).replace(os.sep, "/")
            ext = os.path.splitext(f)[1].lower()
            if f.lower() in JUNK_NAMES or "__macosx" in rel.lower():
                junk.append(rel)
            rows.append({"rel_path": rel, "ext": ext, "size": os.path.getsize(p),
                         "sha256": "" if a.no_hash else sha256(p)})
    man = pd.DataFrame(rows)
    if man.empty:
        raise SystemExit("Thu muc raw rong")

    # nhan suy ra tu cau truc thu muc (chi cho anh/audio)
    media = man["ext"].isin(IMG | AUD)
    # bo qua thu muc boc ngoai duy nhat (zip thuong co 1 thu muc goc), khong tinh file rac
    depth = 0
    real = [r.split("/") for r in man["rel_path"] if os.path.basename(r).lower() not in JUNK_NAMES and "__macosx" not in r.lower()]
    while real and all(len(p_) > depth + 1 for p_ in real) and len({p_[depth] for p_ in real}) == 1:
        depth += 1
    wrapper = "/".join(real[0][:depth]) if real and depth else ""
    lab, osp = [], []
    for rel, is_media in zip(man["rel_path"], media):
        l, s = infer_label(rel.split("/")[depth:]) if is_media else ("", "")
        lab.append(l)
        osp.append(s)
    man["label"], man["orig_split"] = lab, osp
    n_labels = man.loc[man["label"] != "", "label"].nunique()
    if n_labels < 2:  # khong phai cau truc folder-per-class
        man["label"], man["orig_split"] = "", ""

    # anh
    for c in ("width", "height", "mode"):
        man[c] = None
    man["corrupt"] = False
    if not a.no_image_check:
        for i, r in man[man["ext"].isin(IMG)].iterrows():
            w, h, m, bad = check_image(os.path.join(raw, r["rel_path"]))
            man.loc[i, ["width", "height", "mode", "corrupt"]] = [w, h, m, bad]

    # danh dau file dung duoc: khong rac, khong hong, va (neu du lieu co nhan theo thu muc) phai co nhan
    man["is_junk"] = [(os.path.basename(r).lower() in JUNK_NAMES or "__macosx" in r.lower()) for r in man["rel_path"]]
    labeled = man["label"].ne("").any()
    man["usable"] = ~man["is_junk"] & ~man["corrupt"].astype(bool) & (man["label"].ne("") if labeled else True)

    # trung lap
    dups, conflicts = [], []
    if not a.no_hash:
        for sha, g in man.groupby("sha256"):
            if len(g) > 1:
                labels = sorted(set(g["label"]) - {""})
                dups.append({"sha256": sha, "n": len(g), "labels": ";".join(labels), "paths": ";".join(g["rel_path"])})
                if len(labels) > 1:
                    conflicts.append(sha)
    dup_df = pd.DataFrame(dups, columns=["sha256", "n", "labels", "paths"])
    corrupt_df = man[man["corrupt"] == True]  # noqa: E712

    man.to_csv(os.path.join(a.out, "manifest.csv"), index=False)
    dup_df.to_csv(os.path.join(a.out, "duplicates.csv"), index=False)
    if len(corrupt_df):
        corrupt_df.to_csv(os.path.join(a.out, "corrupt.csv"), index=False)

    fp = ""
    if not a.no_hash:
        fp = hashlib.sha256("\n".join(sorted(f"{r}:{s}" for r, s in zip(man.rel_path, man.sha256))).encode()).hexdigest()

    res = {
        "n_files": int(len(man)), "total_bytes": int(man["size"].sum()),
        "by_ext": {k: int(v) for k, v in man["ext"].value_counts().items()},
        "junk_files": junk, "wrapper_dir_ignored": wrapper, "dataset_fingerprint": fp,
        "n_duplicate_groups": len(dups), "n_duplicate_extra_files": int(sum(d["n"] - 1 for d in dups)),
        "label_conflict_groups": len(conflicts), "n_corrupt": int(len(corrupt_df)),
        "n_usable": int(man["usable"].sum()),
    }
    if man["label"].ne("").any():
        cc = man[man["label"] != ""]["label"].value_counts()
        res["class_counts"] = {k: int(v) for k, v in cc.items()}
        res["imbalance_ratio"] = round(float(cc.max() / cc.min()), 2)
        res["pre_existing_splits"] = sorted(set(man["orig_split"]) - {""})
    imgs = man[(man["ext"].isin(IMG)) & (~man["corrupt"].astype(bool))]
    if len(imgs):
        w, h = imgs["width"].astype(int), imgs["height"].astype(int)
        res["images"] = {
            "n": int(len(imgs)), "width": [int(w.min()), int(w.median()), int(w.max())],
            "height": [int(h.min()), int(h.median()), int(h.max())],
            "modes": {k: int(v) for k, v in imgs["mode"].value_counts().items()},
            "distinct_sizes": int(len(set(zip(w, h)))),
        }
    tables = {}
    for rel in man[man["ext"].isin(TAB)]["rel_path"]:
        tables[rel] = audit_table(os.path.join(raw, rel), a.label_col, a.table_header)
    if tables:
        res["tables"] = tables
    auds = []
    for rel in man[man["ext"].isin(AUD)]["rel_path"][:2000]:
        try:
            with wave.open(os.path.join(raw, rel)) as w_:
                auds.append((w_.getnframes() / w_.getframerate(), w_.getframerate(), w_.getnchannels()))
        except Exception:  # noqa: BLE001
            pass
    if auds:
        d = [x[0] for x in auds]
        res["audio"] = {"n": len(auds), "duration_s": [round(min(d), 2), round(statistics.median(d), 2), round(max(d), 2)],
                        "sample_rates": dict(Counter(x[1] for x in auds)), "channels": dict(Counter(x[2] for x in auds))}
    n_txt = int(man["ext"].isin(TXT).sum())
    if n_txt:
        res["text_files"] = n_txt

    # canh bao tu dong
    warn = []
    if junk:
        warn.append(f"Co {len(junk)} file rac ({', '.join(sorted(set(os.path.basename(j) for j in junk)))}); loai khoi pipeline.")
    if res["n_corrupt"]:
        warn.append(f"{res['n_corrupt']} anh hong (xem corrupt.csv); loai truoc khi chia.")
    if res["n_duplicate_groups"]:
        warn.append(f"{res['n_duplicate_groups']} nhom file trung noi dung ({res['n_duplicate_extra_files']} file thua). Phai cho cac ban sao vao CUNG mot split.")
    if res["label_conflict_groups"]:
        warn.append(f"{res['label_conflict_groups']} nhom trung noi dung nhung KHAC nhan -> nhan sai/mo ho; can xu ly thu cong.")
    if res.get("imbalance_ratio", 1) >= 3:
        warn.append(f"Mat can bang lop: ty le lop lon nhat/nho nhat = {res['imbalance_ratio']}. Dung F1/recall theo lop, class weight hoac sampler.")
    if res.get("class_counts") and min(res["class_counts"].values()) < 30:
        warn.append("Co lop < 30 mau: split va metric theo lop se nhieu; can stratified va CI/nhieu seed.")
    if res.get("pre_existing_splits"):
        warn.append(f"Dataset da co thu muc chia san {res['pre_existing_splits']}: kiem tra ro rang truoc khi tin (co the roi ranh, trung lap giua cac split).")
    if res.get("images", {}).get("distinct_sizes", 1) > 1:
        warn.append(f"Anh co {res['images']['distinct_sizes']} kich thuoc khac nhau: can chien luoc resize/crop nhat quan.")
    if res.get("images", {}).get("modes") and len(res["images"]["modes"]) > 1:
        warn.append(f"Nhieu che do mau {res['images']['modes']}: chuan hoa ve cung so kenh.")
    for rel, t in tables.items():
        if "error" in t:
            warn.append(f"Khong doc duoc {rel}: {t['error']}")
            continue
        if t["duplicate_rows"]:
            warn.append(f"{rel}: {t['duplicate_rows']} dong trung.")
        if t["nulls"]:
            warn.append(f"{rel}: co gia tri thieu o cot {list(t['nulls'])}.")
        if t["constant_cols"]:
            warn.append(f"{rel}: cot hang so {t['constant_cols']}.")
    if res["n_files"] and not any(k in res for k in ("images", "tables", "audio", "text_files")):
        warn.append("Khong nhan dien duoc dinh dang du lieu chinh (anh/bang/audio/text).")
    res["warnings"] = warn
    with open(os.path.join(a.out, "audit.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

    # bao cao markdown
    L = ["# Bao cao du lieu (tu dong)", "",
         f"- So file: **{res['n_files']}** (dung duoc: {res['n_usable']}), tong dung luong: **{res['total_bytes']/1e6:.2f} MB**",
         f"- Dinh dang: {res['by_ext']}",
         f"- Dataset fingerprint (SHA256): `{fp or '(bo qua --no-hash)'}`", ""]
    if "class_counts" in res:
        L += ["## Lop / nhan (suy ra tu thu muc)", "", "| Lop | So mau |", "|---|---|"]
        L += [f"| {k} | {v} |" for k, v in res["class_counts"].items()]
        L += ["", f"Ty le mat can bang: {res['imbalance_ratio']}", ""]
    if "images" in res:
        i = res["images"]
        L += ["## Anh", "", f"- So anh doc duoc: {i['n']}; rong [min/median/max]: {i['width']}; cao: {i['height']}",
              f"- Che do mau: {i['modes']}; so kich thuoc khac nhau: {i['distinct_sizes']}", ""]
    for rel, t in tables.items():
        L += [f"## Bang `{rel}`", ""]
        if "error" in t:
            L += [f"Loi doc: {t['error']}", ""]
            continue
        L += [f"- shape: {t['shape']}; dong trung: {t['duplicate_rows']}; cot thieu: {t['nulls'] or 'khong'}"]
        if "label_distribution" in t:
            L += [f"- phan bo nhan: {t['label_distribution']}"]
        L += [""]
    if "audio" in res:
        L += ["## Audio", "", f"{res['audio']}", ""]
    L += ["## Canh bao", ""] + ([f"- {w}" for w in warn] or ["- (khong co)"]) + [""]
    with open(os.path.join(a.out, "data_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    print(json.dumps({k: res[k] for k in ("n_files", "by_ext", "n_corrupt", "n_duplicate_groups", "label_conflict_groups") if k in res}, ensure_ascii=False))
    print("CANH BAO:" if warn else "Khong co canh bao.")
    for w in warn:
        print(" -", w)


if __name__ == "__main__":
    main()
