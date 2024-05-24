import torch
from torch import nn
from torch.utils.tensorboard import SummaryWriter
import numpy as np
import os
from sklearn.metrics import recall_score, confusion_matrix, accuracy_score
from torch.utils.data import DataLoader
from model import *
from read_data import *

all_data_3dim = np.load('data_feature.npy')
all_label = np.load('data_label.npy').astype(np.int64)
# for ii in range(len(all_label)):
#     all_label[ii] = all_label[ii].long()

original_shape = all_data_3dim.shape
print(original_shape)
all_data = all_data_3dim.reshape(original_shape[0],-1)
print(all_data.shape)


train_dataset = MyData(all_data[:1600,:], all_label[:1600])
validation_dataset = MyData(all_data[1600:1828,:], all_label[1600:1828])
test_dataset = MyData(all_data[1828:,:], all_label[1828:])

train_data = DataLoader(train_dataset, batch_size=20)
validation_data = DataLoader(validation_dataset, batch_size=20)
test_data = DataLoader(test_dataset, batch_size=20)


# length 长度
train_data_size = 1600
validation_data_size = 458
test_data_size = 228


# 如果train_data_size=10, 训练数据集的长度为：10
print("训练数据集的长度为：{}".format(train_data_size))
print("验证数据集的长度为：{}".format(validation_data_size))
print("测试数据集的长度为：{}".format(test_data_size))


device = 'cuda'
Mymodel = CNN().to(device)

# 损失函数
loss_fn = nn.CrossEntropyLoss().to(device)

# 优化器
learning_rate = 0.01
optimizer = torch.optim.SGD(Mymodel.parameters(), lr=learning_rate)

# 设置训练网络的一些参数
# 记录训练的次数
total_train_step = 0
# 记录验证的次数
total_validation_step = 0
# 记录测试的次数
total_test_step = 0
#记录验证时全部epoch的uar
result_v = []
#记录验证时全部epoch的loss
loss_v_all = []
#记录验证时最大uar
max_uar = 0
#记录验证时最大uar的epoch
max_uar_epoch = 0

# 训练的轮数
epoch = 30

# 添加tensorboard
writer = SummaryWriter("../logs_train")

for i in range(epoch):
    print("-------第 {} 轮训练开始-------".format(i+1))

    # 训练步骤开始
    Mymodel.train()
    for data in train_data:
        audio, label = data
        audio = audio.unsqueeze(1).cuda()
        label = label.long().cuda()
        outputs = Mymodel(audio.float()).cuda()
        # print(outputs.shape,label.shape)
        loss = loss_fn(outputs, label)

        # 优化器优化模型
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_train_step = total_train_step + 1
        if total_train_step % 50 == 0:
            print("训练次数：{}, Loss: {}".format(total_train_step, loss.item()))
            writer.add_scalar("train_loss", loss.item(), total_train_step)



    # 验证步骤开始
    Mymodel.eval()
    total_validation_loss = 0
    total_accuracy = 0
    pred = []
    with torch.no_grad():
        for data in validation_data:
            audio, label = data
            # print("audio",audio)
            # print("label",label)
            audio = audio.unsqueeze(1).cuda()
            label = label.cuda()
            outputs = Mymodel(audio.float()).cuda()
            # print("output",outputs)
            # print("取最大：",torch.argmax(outputs, dim=1))
            loss = loss_fn(outputs, label.long())
            total_validation_loss = total_validation_loss + loss.item()
            predLabels = outputs.argmax(dim=1).cpu().numpy().tolist()
            pred.extend(predLabels)

            
    print("整体验证集上的Loss: {}".format(total_validation_loss))


    torch.save(Mymodel.state_dict(), "./log/Mymodel_{}.pkl".format(i+1))
    print("模型已保存")

    uar_scores = recall_score(all_label[1600:1828], pred, labels=[0,1], average='macro')
    if uar_scores > max_uar:
        max_uar = uar_scores
        max_uar_epoch = i+1
    result_v.append(uar_scores)
    loss_v_all.append(total_validation_loss)
    print("-------第 {} 轮训练的UAR:{}-------".format(i+1,uar_scores))

print("验证阶段平均loss：{}".format(sum(loss_v_all)/len(loss_v_all)))
print("验证阶段平均uar：{}".format(sum(result_v)/len(result_v)))
print("验证阶段第{}个epoch获得了最高uar：{}".format(max_uar_epoch,max_uar))



print("######################################################################################")
print("######################################################################################")
print("######################################################################################")
print("######################################################################################")
print("######################################################################################")


print('！！！测试开始！！！')
result_t = []
loss_t_all = []
max_uar_epoch_t = 0
max_uar_t = 0
for i in range(30):
    # 测试步骤开始
    print("-------第 {} 个epoch model的测试开始".format(i+1))
    Mymodel.eval()
    Mymodel.load_state_dict(torch.load('./log/Mymodel_{}.pkl'.format(i+1)))#./log/Mymodel_%d.pth' % 19))

    pred = []
    total_test_loss = 0
    with torch.no_grad():
        for data in test_data:
            audio, label = data
            audio = audio.unsqueeze(1).cuda()
            label = label.cuda()
            outputs = Mymodel(audio.float()).cuda()
            loss = loss_fn(outputs, label.long())
            total_test_loss = total_test_loss + loss.item()
            predLabels = outputs.argmax(dim=1).cpu().numpy().tolist()
            pred.extend(predLabels)

            
    print("整体测试集上的Loss: {}".format(total_test_loss))
    # writer.add_scalar("test_loss", total_test_loss, total_test_step)
    # writer.add_scalar("test_accuracy", total_accuracy/test_data_size, total_test_step)
    total_test_step = total_test_step + 1

    uar_scores = recall_score(all_label[1828:], pred, labels=[0,1], average='macro')
    accuracy = accuracy_score(all_label[1828:], pred)

    if uar_scores > max_uar_t:
        max_uar_t = uar_scores
        max_uar_epoch_t = i+1
        max_acc = accuracy
    result_t.append(uar_scores)
    loss_t_all.append(total_test_loss)
    CM = confusion_matrix(all_label[1828:], pred)
    print("混淆矩阵:")
    print(CM)
    if i == (max_uar_epoch-1):
        print("！！！该模型是验证集效果最好模型！！！")
    print("-------第 {} 个epoch model的UAR:{}-------".format(i+1,uar_scores))

print("测试阶段平均uar：{}".format(sum(result_t)/len(result_t)))
print("测试阶段平均loss：{}".format(sum(loss_t_all)/len(loss_t_all)))
print("测试阶段第{}个epoch获得了最高uar：{}".format(max_uar_epoch_t,max_uar_t))
print("acc为：{}".format(max_acc))


writer.close()

