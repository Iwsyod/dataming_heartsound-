import torch
import torch.nn as nn
import librosa
import numpy as np
from feature_extraction import get_pcg_features
from read_data import *
from torch.utils.data import DataLoader

 
# 定义神经网络模型类
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


def predict(input_data):
    # 创建模型实例
    model = CNN()
    # 加载保存的模型
    model_path = 'Mymodel_30.pkl'
    model.load_state_dict(torch.load(model_path))
    model.eval()

    audio, sr = librosa.load(input_data, sr=1000)
    if len(audio)<60000:
        v = audio
        while len(audio) < 60000:
            audio = np.append(audio,v)
        audio = audio[0:60000]
    else:  
        audio = audio[0:60000]

    AUDIO_FS = 1000#采样频率
    FEATURES_FS = 50#特征
    feature=get_pcg_features(audio,FEATURES_FS,AUDIO_FS)
    #fs 为特征采样频率，第一列为希尔伯特包络特征，第二列为同态包络特征
    feature=np.array([feature['pcg_features']])
    original_shape = feature.shape
    # print(original_shape)
    data = feature.reshape(original_shape[0],-1)
    # print(data.shape)

    predict_dataset = MyData(data)
    predict_data = DataLoader(predict_dataset, batch_size=1)
    with torch.no_grad():
        for data in predict_data:
            data = data.unsqueeze(1).float()
            # 使用模型进行预测
            output = model(data)


    # 处理输出结果
    # 假设你想要获取预测的类别
    predicted_class = torch.argmax(output, dim=1)
    if predicted_class == 0 :
        print("异常")
        return 0
    elif predicted_class == 1:
        print("健康")
        return 1

if __name__ == '__main__':
    import sys
    # 接收 Node.js 传递的参数
    argument = int(sys.argv[1])
    # 调用函数并将结果输出到标准输出流
    predict(argument)