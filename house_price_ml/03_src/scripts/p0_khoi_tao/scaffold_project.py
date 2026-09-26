#!/usr/bin/env python3
"""
scaffold_project.py - Dựng khung dự án Deep Learning từ dataset thô.

  python scaffold_project.py --root /home/claude/myproj [--name myproj] \
      [--raw-src /mnt/user-data/uploads/data.zip | /path/to/folder] \
      [--task image_classification] [--requested-by "Tên người dùng"]

Làm gì:
  1. Tạo cây thư mục chuẩn (00_raw ... 08_backups).
  2. Nếu có --raw-src: SAO CHÉP (không di chuyển) vào 00_raw (giải nén nếu là zip), đặt file chỉ-đọc.
  3. Ghi 04_configs/base.yaml, README.md, requirements.txt, .gitignore (chỉ tạo nếu chưa có).
  4. Khởi tạo 07_logs/change_log.xlsx và ghi các dòng log đầu tiên.
"""
import argparse
import os
import shutil
import stat
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import log_change as LC  # noqa: E402
from openpyxl import load_workbook  # noqa: E402

DIRS = [
    "00_raw", "01_data/audit", "01_data/splits", "01_data/processed", "02_notebooks", "03_src",
    "04_configs", "05_experiments", "06_reports", "07_logs", "08_backups",
]

BASE_YAML = """\
# Cấu hình cơ sở. Mỗi thí nghiệm = 1 bản sao của file này (04_configs/exp_XXX.yaml),
# chỉ đổi MỘT thứ so với thí nghiệm cha. Ghi Exp_ID + hash file này vào sheet Experiments.
project: {name}
task: {task}            # image_classification | text_classification | tabular | time_series | audio | segmentation | detection
seed: 42

data:
  raw_dir: 00_raw
  split_file: 01_data/splits/split_v1.csv     # tạo bằng scripts/make_splits.py
  num_workers: 2
  input_size: [224, 224]                      # đối với ảnh; bỏ qua nếu không áp dụng

model:
  name: resnet18
  pretrained: true                            # dữ liệu nhỏ -> ưu tiên transfer learning
  num_classes: null                           # điền sau khi audit nhãn

train:
  epochs: 20
  batch_size: 64
  optimizer: adamw
  lr: 3.0e-4
  weight_decay: 1.0e-2
  scheduler: cosine
  warmup_epochs: 1
  amp: true
  grad_clip: 1.0
  early_stopping: {{monitor: val_metric, mode: max, patience: 5}}

augment:
  train: []                                   # chỉ áp dụng cho train
  eval: []                                    # chỉ resize/normalize

eval:
  metric: macro_f1                            # chọn theo bài toán (xem references/task_playbooks.md)
  threshold: null

output:
  dir: 05_experiments/EXP-XXXX
"""

README = """\
# {name}

Dự án Deep Learning xây dựng từ dataset thô. Cấu trúc:

| Thư mục | Nội dung |
|---|---|
| 00_raw | Dataset gốc, chỉ đọc, không sửa |
| 01_data | audit/ (manifest, báo cáo dữ liệu), splits/ (file chia), processed/ |
| 02_notebooks | EDA, phân tích lỗi |
| 03_src | Mã nguồn (data, models, train, evaluate, predict) |
| 04_configs | YAML cho từng thí nghiệm |
| 05_experiments | Kết quả từng thí nghiệm (config, metrics.csv, checkpoint) |
| 06_reports | data_report, experiment_summary, final_report, model_card |
| 07_logs | change_log.xlsx (Change_Log, Findings, File_Registry, Experiments, Summary) |
| 08_backups | Bản sao trước mỗi lần sửa file |

Tái lập: xem `06_reports/final_report.md` mục "Cách chạy lại".

"""

GITIGNORE = "05_experiments/**/*.pt\n05_experiments/**/*.pth\n05_experiments/**/*.ckpt\n01_data/processed/\n__pycache__/\n*.pyc\n.ipynb_checkpoints/\n"


def write_if_absent(path, text):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return True
    return False


def make_readonly(root):
    n = 0
    for dp, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(dp, f)
            os.chmod(p, os.stat(p).st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
            n += 1
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True)
    ap.add_argument("--name")
    ap.add_argument("--raw-src")
    ap.add_argument("--task", default="image_classification")
    ap.add_argument("--actor", default="Claude")
    ap.add_argument("--requested-by", default="")
    a = ap.parse_args()

    root = os.path.abspath(a.root)
    name = a.name or os.path.basename(root)
    for d in DIRS:
        os.makedirs(os.path.join(root, d), exist_ok=True)

    created = []
    if write_if_absent(os.path.join(root, "04_configs/base.yaml"), BASE_YAML.format(name=name, task=a.task)):
        created.append("04_configs/base.yaml")
    if write_if_absent(os.path.join(root, "README.md"), README.format(name=name)):
        created.append("README.md")
    if write_if_absent(os.path.join(root, ".gitignore"), GITIGNORE):
        created.append(".gitignore")
    if write_if_absent(os.path.join(root, "requirements.txt"), "# ghim phiên bản thật sự dùng (pip freeze) sau khi chạy xong thí nghiệm đầu tiên\n"):
        created.append("requirements.txt")

    log = os.path.join(root, "07_logs/change_log.xlsx")
    LC.init_workbook(log)
    wb = load_workbook(log)
    LC.ensure_sheets(wb)
    base = dict(actor=a.actor, requested_by=a.requested_by)

    LC.add_entry(wb, {**base, "action": "CREATE", "step": "P0 Khởi tạo",
                      "file": os.path.basename(root), "path": ".",
                      "desc": f"Tạo khung dự án '{name}' ({len(DIRS)} thư mục) + {', '.join(created) or 'không tạo file mới'}",
                      "reason": "Khung thư mục chuẩn của skill dl-project-from-raw-data",
                      "tool": "scripts/scaffold_project.py"})

    if a.raw_src:
        src = os.path.abspath(a.raw_src)
        dst = os.path.join(root, "00_raw")
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
            how = "copytree"
        elif zipfile.is_zipfile(src):
            with zipfile.ZipFile(src) as z:
                n_files = len([i for i in z.infolist() if not i.is_dir()])
                z.extractall(dst)
            shutil.copy2(src, os.path.join(root, "08_backups", os.path.basename(src)))
            how = f"giải nén zip ({n_files} file); zip gốc lưu ở 08_backups/"
        else:
            shutil.copy2(src, dst)
            how = "sao chép 1 file"
        n_ro = make_readonly(dst)
        LC.add_entry(wb, {**base, "action": "CREATE", "step": "P1 Nhập dữ liệu",
                          "file": os.path.basename(src), "path": "00_raw",
                          "desc": f"Nhập dataset thô vào 00_raw ({how}); đặt {n_ro} file ở chế độ chỉ-đọc",
                          "reason": "Dữ liệu gốc bất biến; mọi xử lý ghi sang 01_data/",
                          "tool": "scripts/scaffold_project.py"})
    wb.save(log)
    print(f"OK: {root}")
    for d in DIRS:
        print("  ", d)
    print("log:", log)


if __name__ == "__main__":
    main()
