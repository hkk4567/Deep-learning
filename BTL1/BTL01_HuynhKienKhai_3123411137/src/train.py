# Train dữ liệu (copy từ notebook)
import torch
from .config import device

def Train(train_loader, X_val_tensor, y_val_tensor, model, optimizer, criterion, file, epochs = 1000):
  min_vali_loss = float("inf")
  best_epoch = 0
  history = {"train": [], "val": []}
  X_val_tensor, y_val_tensor = X_val_tensor.to(device), y_val_tensor.to(device)

  for epoch in range(epochs):
    model.train()
    running_loss = 0.0

    for X_batch, y_batch in train_loader:
      X_batch, y_batch = X_batch.to(device), y_batch.to(device)
      optimizer.zero_grad() # reset grad về 0 để không bị cộng dồn

      y_pred = model(X_batch).squeeze(-1) # train + predict
      # print(y_pred.shape, y_batch.shape)

      loss = criterion(y_pred, y_batch) # tính loss

      loss.backward() # backpropagation

      optimizer.step() # cặp nhật trọng số

      running_loss += loss.item() * X_batch.size(0) # cộng dồn loss của từng batch

    train_loss = running_loss / len(train_loader.dataset) # tính trung bình loss

    # validation
    model.eval()
    with torch.no_grad():
      y_val_pred = model(X_val_tensor).squeeze(-1)
      val_loss = criterion(y_val_pred, y_val_tensor)

    # lưu lại train_loss và val_loss
    history["train"].append(train_loss)
    history["val"].append(val_loss)

    if (epoch + 1) % 100 == 0:
      print("=" * 50)
      print(f"Epoch {epoch + 1}, "f"Loss: {train_loss:.6f}, "f"Validation MSE: {val_loss.item():.6f}")

    # lưu checkpoint min_vali_loss
    if val_loss.item() < min_vali_loss:
      min_vali_loss = val_loss.item()
      best_epoch = epoch + 1
      torch.save({
              "epoch": epoch + 1,
              "model_state_dict": model.state_dict(),
              "optimizer_state_dict": optimizer.state_dict(),
              "val_loss": min_vali_loss
          }, file)
      if (epoch + 1) % 100 == 0:
        print(f"Đã lưu checkpoint {epoch + 1}")
  return {
        "history": history,
        "best_val_loss": min_vali_loss,
        "best_epoch": best_epoch,
    }
