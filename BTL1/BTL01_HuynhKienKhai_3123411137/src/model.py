# xây dựng mô hình MLP (copy từ notebook)
import torch.nn as nn

class MLP(nn.Module):
  def __init__(self, input_size = 2, hiden_sizes = [3], output_size = 1):
    super().__init__()
    layers = []
    prev_input = input_size

    for hiden_size in hiden_sizes:# tạo ra len(hiden_sizes) hiden layers
      layers.append(nn.Linear(prev_input, hiden_size))  # tạo ra hiden_size (với mặc định là 3) perceptron với công thức y = wx + b
      layers.append(nn.ReLU()) # hàm kích hoạt ReLU
      prev_input = hiden_size

    layers.append(nn.Linear(prev_input, output_size))
    self.network = nn.Sequential(*layers)

  def forward(self, x):
      return self.network(x)
