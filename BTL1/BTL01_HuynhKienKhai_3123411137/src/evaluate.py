# đánh giá trên tập test bằng checkpoint có val MSE nhỏ nhất (copy từ notebook)
import torch
from .config import device

# Chuyển tensor hoặc giá trị số về float
def to_float(value):
    if isinstance(value, torch.Tensor):
        return value.item()
    return float(value)

def evaluate(model, file, X_test, y_test):
    checkpoint = torch.load(file, map_location=device, weights_only=True)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    with torch.no_grad():
        pred = model(X_test.to(device)).squeeze(-1).cpu()

    err = pred - y_test
    mse = (err ** 2).mean().item()
    return {"test_mse": mse, "test_rmse": mse ** 0.5, "test_mae": err.abs().mean().item()}
