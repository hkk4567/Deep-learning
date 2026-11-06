# cấu hình chung: đường dẫn lưu file, device và các cấu hình thí nghiệm (lấy từ notebook)
from pathlib import Path
import torch

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR, LOG_DIR = ROOT / "data", ROOT / "logs"
FIG_DIR, WEIGHT_DIR, RESULT_DIR = ROOT / "figures", ROOT / "weights", ROOT / "results"
for d in (DATA_DIR, LOG_DIR, FIG_DIR, WEIGHT_DIR, RESULT_DIR):
  d.mkdir(parents=True, exist_ok=True)

# Thử nghiệm trên nhiều seed: seed quyết định khởi tạo trọng số và thứ tự shuffle của DataLoader
# (dữ liệu và cách chia train/val/test giữ cố định, seed 42 như notebook). SEED_CHINH = seed của kết quả chính.
SEEDS = [42, 123, 2024]
SEED_CHINH = 42
SEED_DIR = RESULT_DIR / "seeds"  # kết quả từng seed + bảng tổng hợp mean ± std
SEED_DIR.mkdir(parents=True, exist_ok=True)

# Trọng số và log lưu theo từng thí nghiệm: weights/expA_weight/seed_42/..., logs/expA_log/seed_42/...
# exp ∈ {"base", "A", "B", "C"}
def ten_thu_muc(exp):
  return "base" if exp == "base" else f"exp{exp}"

def weight_dir(exp, seed = SEED_CHINH):
  d = WEIGHT_DIR / f"{ten_thu_muc(exp)}_weight" / f"seed_{seed}"
  d.mkdir(parents=True, exist_ok=True)
  return d

def log_dir(exp, seed = SEED_CHINH):
  d = LOG_DIR / f"{ten_thu_muc(exp)}_log" / f"seed_{seed}"
  d.mkdir(parents=True, exist_ok=True)
  return d

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Thí nghiệm A: hiden layer = 1, perceptron = 3, thay đổi số mẫu train (cách chia mới: val và test cố định như B, C)
cau_hinh_data = [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
# 1000 mẫu đầu của bộ 3000 mẫu được chia 720/180/100 (train/val/test) cho B, C và cho val/test của A;
# train của A lấy từ phần còn lại của bộ 3000 mẫu (mẫu thứ 1000 trở đi)
N_CO_DINH = 1000
# Thí nghiệm B: 1000 mẫu, 1 hiden layer, thay đổi số perceptron
cau_hinh_perceptron = [1,2,3,4,5,6,7,8,9,10]
# Thí nghiệm C: 1000 mẫu, mỗi tầng 3 perceptron, thay đổi số hiden layer
cau_hinh_hiden_layer = [1,2,3,4]
