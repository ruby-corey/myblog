import torch
from vit_pytorch import ViT
import torch.nn.functional as F

model = ViT(
    image_size=32,
    patch_size=4,
    num_classes=10,
    dim=128,
    depth=4,
    heads=4,
    mlp_dim=256,
    dropout=0.1,
    emb_dropout=0.1
)
model.load_state_dict(torch.load('./weight/vit_model_1.pth', map_location=torch.device('cuda')))
# torch.load是加载预训练的模型权重（这些权重通常保存在字典中） load_state_dict加载到模型中
model.eval()

from PIL import Image
from torchvision.transforms import transforms

transform = transforms.Compose(
    [transforms.Resize((32, 32)),
     transforms.ToTens20or(),  # transforms.ToTensor() 将图像格式转换为Pytorch张量 HxWxC -> CxHxW;
     # 将uint8(0-255) -> float32; 归一化 缩放到[0.0,1.0]
     transforms.Normalize((0.5,), (0.5,))  # 每个通道均值0.5 方差0.5 的标准化(归一化) output=(input-mean)/std
     ]
)
# transforms.Compose堆叠图像预处理步骤

img = Image.open('./image/dogs/1st_t.jpg')
img = transform(img).unsqueeze(0)  # [C,H,W] ->[N,C,H,W] N为batch批次数量，一次处理图像数量

CIFAR10_CLASSES = ["airplane", "automobile", "bird", "cat", "deer",
                   "dog", "frog", "horse", "ship", "truck"]

with torch.no_grad():
    output = model(img)
    probabilities = F.softmax(output, dim=1)  # 计算所有类别的概率
    predicted = torch.argmax(output, dim=1).item()  # 在第dim个维度(行）上查找最大值，返回每一行最大值的列索引
# torch.no_grad禁用梯度运算上下文管理器，加速计算减少显存占用 （梯度运算指微分，优化模型，参数更新方向与梯度方向相反）
print(f'预测类别: {predicted}({CIFAR10_CLASSES[predicted]})')
print(f'预测概率分布：{probabilities.squeeze()}')
"""CIFAR-10 的类别对应表：
类别编号	真实类别
0	🛵 飞机 (airplane)
1	🚗 汽车 (automobile)
2	🏢 鸟 (bird)
3	🐱 猫 (cat)
4	🦌 鹿 (deer)
5	🐕 狗 (dog)
6	🐸 青蛙 (frog)
7	🐎 马 (horse)
8	🚢 船 (ship)
9	🚚 卡车 (truck)"""
