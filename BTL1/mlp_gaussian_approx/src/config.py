# cấu hình chung: đường dẫn lưu file, device và các cấu hình thí nghiệm (lấy từ notebook)
from pathlib import Path
import torch

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR, LOG_DIR = ROOT / "data", ROOT / "logs"
FIG_DIR, WEIGHT_DIR, RESULT_DIR = ROOT / "figures", ROOT / "weights", ROOT / "results"
for d in (DATA_DIR, LOG_DIR, FIG_DIR, WEIGHT_DIR, RESULT_DIR):
  d.mkdir(parents=True, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Thí nghiệm A: hiden layer = 1, perceptron = 3, thay đổi số mẫu
cau_hinh_data = [278, 556, 834, 1112, 1389, 1667, 1945, 2223, 2500, 2778]
# Thí nghiệm B: 1000 mẫu, 1 hiden layer, thay đổi số perceptron
cau_hinh_perceptron = [1,2,3,4,5,6,7,8,9,10]
# Thí nghiệm C: 1000 mẫu, mỗi tầng 3 perceptron, thay đổi số hiden layer
cau_hinh_hiden_layer = [1,2,3,4]
