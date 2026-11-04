# tạo dữ liệu Gaussian 2D, chia train/val/test và chuyển sang tensor (copy từ notebook)
import numpy as np
import pandas as pd
import torch
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split

from .config import DATA_DIR

# khởi tạo hàm Gaussian_2D và debug dữ liệu
U = np.array([0,0])
C = np.array([
    [0.3,-0.5],
    [-0.5,2]
  ])
# Gaussian 2D
def Gaussian_2D(x):
  x = np.array(x)
  k = x - U # tính x - U trước
  he_so_nhan = 1/(2 * np.pi * np.sqrt(np.linalg.det(C)))
  return he_so_nhan * np.exp(-0.5 * k.T @ np.linalg.inv(C) @ k)
def gen_data_set(n = 1000):
  print(n)
  x1 = np.random.uniform(-2,2,n)
  x2 = np.random.uniform(-4,4,n)
  x = np.column_stack((x1,x2))
  print("x: ",x[:10])
  y = np.array([])
  for x in x:
    y = np.append(y,Gaussian_2D(x))
  print("Y: ",y[:10])
  return x1,x2,y


# Tạo dữ liệu của mô hình chuẩn (seed = 42, 1000 mẫu) rồi lưu ra DataSet.csv
def tao_data_chuan():
  np.random.seed(42)
  x1,x2,y = gen_data_set()
  df = pd.DataFrame({
      "x1":x1,
      "x2":x2,
      "y_real":y,
  })
  df.to_csv(DATA_DIR / "DataSet.csv", index=False)
  return df


# chia tập theo công thức 10% test/ 90% còn lại trong đó có (20% val, 80% train), random seed = 42
def chia_data_chuan():
  df_new = pd.read_csv(DATA_DIR / "DataSet.csv")
  print(df_new.head())
  print(df_new.shape)

  X_df = df_new[["x1","x2"]]
  y_df = df_new["y_real"]
  print("dữ liệu X: ")
  print(X_df.head())
  print("=====================================")
  print("dữ liệu y: ")
  print(y_df.head())
  # chia lấy 100 phần tử cho tập test tương ứng 10%
  X_temp, X_test, y_temp, y_test = train_test_split(
      X_df, y_df,
      test_size = 0.1,
      random_state=42
  )
  print("=====================================")
  print("Tập test với 100 phần tử")
  print("X: ", X_test.shape)
  print("y: ", y_test.shape)
  print("=====================================")
  print("Các phần tử còn lại sau khi trừ đi 100 phần tử của tập test, được gọi là tập Temp")
  print("X: ", X_temp.shape)
  print("y: ", y_temp.shape)
  print("=====================================")

  X_train, X_val, y_train, y_val = train_test_split(
      X_temp, y_temp,
      test_size = 0.2,
      random_state=42
  )

  print("Tập val với 180 phần tử (trên tập Temp)")
  print("X: ", X_val.shape)
  print("y: ", y_val.shape)
  print("=====================================")
  print("Tập train với 720 phần tử (trên tập Temp)")
  print("X: ", X_train.shape)
  print("y: ", y_train.shape)
  return X_train, X_val, X_test, y_train, y_val, y_test


# chuyển sang tensor
def chuyen_tensor_chuan(X_train, X_val, X_test, y_train, y_val, y_test):
  X_train_tensor = torch.tensor(X_train.to_numpy(), dtype=torch.float32)
  y_train_tensor = torch.tensor(y_train.to_numpy(), dtype=torch.float32)
  print("X_train_tensor (5 phần tử đầu):")
  print(X_train_tensor[:5])
  print("y_train_tensor (5 phần tử đầu):")
  print(y_train_tensor[:5])

  X_val_tensor = torch.tensor(X_val.to_numpy(), dtype=torch.float32)
  y_val_tensor = torch.tensor(y_val.to_numpy(), dtype=torch.float32)

  X_test_tensor = torch.tensor(X_test.to_numpy(), dtype=torch.float32)
  y_test_tensor = torch.tensor(y_test.to_numpy(), dtype=torch.float32)

  train_dataset = TensorDataset(X_train_tensor, y_train_tensor)

  train_loader = DataLoader(
      train_dataset,
      batch_size=len(train_dataset), # 1 batch và toàn bộ data
      shuffle=True
  )
  print("kiểm tra thử train_loader:")
  idx_batch_train_loader_log = 1
  for X_batch, y_batch in train_loader:
    print("====================")
    print(idx_batch_train_loader_log,":")
    print("X: ",X_batch.shape)
    print("y: ",y_batch.shape)
    idx_batch_train_loader_log += 1
  return X_train_tensor, y_train_tensor, X_val_tensor, y_val_tensor, X_test_tensor, y_test_tensor, train_loader


def data_split_and_to_tensor(X, y):
  X_temp, X_test, y_temp, y_test = train_test_split(
    X, y,
    test_size = 0.1,
    random_state=42
  )
  X_train, X_val, y_train, y_val = train_test_split(
      X_temp, y_temp,
      test_size = 0.2,
      random_state=42
  )
  X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
  y_train_tensor = torch.tensor(y_train, dtype=torch.float32)

  X_val_tensor = torch.tensor(X_val, dtype=torch.float32)
  y_val_tensor = torch.tensor(y_val, dtype=torch.float32)

  X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
  y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

  train_dataset = TensorDataset(X_train_tensor, y_train_tensor)

  train_loader = DataLoader(
      train_dataset,
      batch_size=32, # 1 batch và toàn bộ data
      shuffle=True
  )
  print("X_train: ",len(X_train_tensor))
  print("y_train: ",len(y_train_tensor))
  print("X_val: ",len(X_val_tensor))
  print("y_val: ",len(y_val_tensor))
  print("X_test: ",len(X_test_tensor))
  print("y_test: ",len(y_test_tensor))
  return X_train_tensor, y_train_tensor, X_val_tensor, y_val_tensor, X_test_tensor, y_test_tensor, train_loader


# tạo dữ liệu huấn luyện và kiểm tra cho các thí nghiệm
def tao_data_thi_nghiem():
  np.random.seed(42)
  torch.manual_seed(42)

  x1_all, x2_all, y_all = gen_data_set(3000)
  X_all = np.column_stack([
      x1_all.ravel(),
      x2_all.ravel()
  ]).astype(np.float32)

  y_all = np.asarray(y_all).reshape(-1).astype(np.float32)
  rng = np.random.default_rng(42)
  indices = rng.permutation(len(y_all))

  X_all = X_all[indices]
  y_all = y_all[indices]

  print("Kích thước X:", X_all.shape)
  print("Kích thước y:", y_all.shape)
  return X_all, y_all
