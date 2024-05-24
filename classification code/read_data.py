from torch.utils.data import Dataset


# 准备数据集                                     
class MyData(Dataset):
    def __init__(self, data, label):
        self.data = data
        self.label = label
        

    def __getitem__(self, idx):  
        return self.data[idx,:], self.label[idx]

    def __len__(self):
        assert len(self.data) == len(self.label)
        return len(self.label)
