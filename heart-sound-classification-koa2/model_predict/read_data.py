from torch.utils.data import Dataset


# 准备数据集                                     
class MyData(Dataset):
    def __init__(self, data):
        self.data = data
        
    def __getitem__(self, idx):  
        return self.data[idx,:]

    def __len__(self):
        return len(self.data)
