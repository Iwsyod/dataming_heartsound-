import torch
from torch import nn

# 搭建神经网络
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.model = nn.Sequential(
            nn.Conv1d(1, 5, kernel_size=10, stride=1, padding=9),
            nn.MaxPool1d(2),
            nn.Conv1d(5, 10, kernel_size=10, stride=1, padding=9), 
            nn.MaxPool1d(6),
            nn.Conv1d(10, 20, kernel_size=10, stride=1, padding=9),  
            nn.MaxPool1d(2),
            nn.Conv1d(20, 1, kernel_size=10, stride=1, padding=9),  
            nn.MaxPool1d(10),
            nn.Flatten(),
            nn.Linear(26, 20),
            nn.Linear(20, 2)
        )
        
    def forward(self, x):
        x = self.model(x)
        return x


# # 验证模型输出结构
# if __name__ == '__main__':
#     CNN = CNN()
#     input = torch.ones((1,1,6000))
#     # print(type(input))
#     output = CNN(input)
#     print(output.shape)
#     print(type(output))

