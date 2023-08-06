import torch
import torch.nn as nn
import torchvision
import numpy as np
import torch.nn.functional as F
import math
from torch.autograd import Variable

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def models(name = None):
    if name is None:
        return "No Models loaded"
    else:
        return f"{name} model loaded successfully"

''' UNet Model'''

class U_Net(nn.Module):
    def __init__(self):
        super(U_Net, self).__init__()
        self.conv1 = nn.Conv2d(in_channels = 1, out_channels = 64, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv1.weight, mean=0.0, std=np.sqrt(2/(3*3*64)))
        self.conv2 = nn.Conv2d(in_channels = 64, out_channels = 64, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv2.weight, mean=0.0, std=np.sqrt(2/(3*3*64)))
        self.maxpool1 = nn.MaxPool2d(kernel_size = 2, stride = 2, padding = 0)
        self.conv3 = nn.Conv2d(in_channels = 64, out_channels = 128, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv3.weight, mean=0.0, std=np.sqrt(2/(3*3*128)))
        self.conv4 = nn.Conv2d(in_channels = 128, out_channels = 128, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv4.weight, mean=0.0, std=np.sqrt(2/(3*3*128)))
        self.maxpool2 = nn.MaxPool2d(kernel_size = 2, stride = 2, padding = 0)
        self.conv5 = nn.Conv2d(in_channels = 128, out_channels = 256, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv5.weight, mean=0.0, std=np.sqrt(2/(3*3*256)))
        self.conv6 = nn.Conv2d(in_channels = 256, out_channels = 256, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv6.weight, mean=0.0, std=np.sqrt(2/(3*3*256)))
        self.maxpool3 = nn.MaxPool2d(kernel_size = 2, stride = 2, padding = 0)
        self.conv7 = nn.Conv2d(in_channels = 256, out_channels = 512, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv7.weight, mean=0.0, std=np.sqrt(2/(3*3*512)))
        self.conv8 = nn.Conv2d(in_channels = 512, out_channels = 512, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv8.weight, mean=0.0, std=np.sqrt(2/(3*3*512)))
        self.maxpool4 = nn.MaxPool2d(kernel_size = 2, stride = 2, padding = 0)
        self.conv9 = nn.Conv2d(in_channels = 512, out_channels = 1024, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv9.weight, mean=0.0, std=np.sqrt(2/(3*3*1024)))
        self.conv10 = nn.Conv2d(in_channels = 1024, out_channels = 1024, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv2.weight, mean=0.0, std=np.sqrt(2/(3*3*1024)))
        self.upconv1 = nn.ConvTranspose2d(in_channels = 1024, out_channels = 512, kernel_size = 2, stride = 2)
        nn.init.normal_(self.upconv1.weight, mean=0.0, std=np.sqrt(2/(2*2*512)))
        self.conv11 = nn.Conv2d(in_channels = 1024, out_channels = 512, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv11.weight, mean=0.0, std=np.sqrt(2/(3*3*512)))
        self.conv12 = nn.Conv2d(in_channels = 512, out_channels = 512, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv12.weight, mean=0.0, std=np.sqrt(2/(3*3*512)))
        self.upconv2 = nn.ConvTranspose2d(in_channels = 512, out_channels = 256, kernel_size = 2, stride = 2)
        nn.init.normal_(self.upconv2.weight, mean=0.0, std=np.sqrt(2/(2*2*256)))
        self.conv13 = nn.Conv2d(in_channels = 512, out_channels = 256, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv13.weight, mean=0.0, std=np.sqrt(2/(3*3*256)))
        self.conv14 = nn.Conv2d(in_channels = 256, out_channels = 256, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv14.weight, mean=0.0, std=np.sqrt(2/(3*3*256)))
        self.upconv3 = nn.ConvTranspose2d(in_channels = 256, out_channels = 128, kernel_size = 2, stride = 2)
        nn.init.normal_(self.upconv3.weight, mean=0.0, std=np.sqrt(2/(2*2*128)))
        self.conv15 = nn.Conv2d(in_channels = 256, out_channels = 128, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv15.weight, mean=0.0, std=np.sqrt(2/(3*3*128)))
        self.conv16 = nn.Conv2d(in_channels = 128, out_channels = 128, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv16.weight, mean=0.0, std=np.sqrt(2/(3*3*128)))
        self.upconv4 = nn.ConvTranspose2d(in_channels = 128, out_channels = 64, kernel_size = 2, stride = 2)
        nn.init.normal_(self.upconv4.weight, mean=0.0, std=np.sqrt(2/(2*2*64)))
        self.conv17 = nn.Conv2d(in_channels = 128, out_channels = 64, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv17.weight, mean=0.0, std=np.sqrt(2/(3*3*64)))
        self.conv18 = nn.Conv2d(in_channels = 64, out_channels = 64, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv18.weight, mean=0.0, std=np.sqrt(2/(3*3*64)))
        self.conv19 = nn.Conv2d(in_channels = 64, out_channels = 1, kernel_size = 1, stride = 1, padding = 0)
        nn.init.normal_(self.conv19.weight, mean=0.0, std=np.sqrt(2/(1*1*1)))
        self.relu = nn.ReLU()
        self.gn1 = nn.GroupNorm(16, 64)
        self.gn2 = nn.GroupNorm(16, 128)
        self.gn3 = nn.GroupNorm(16, 256)
        self.gn4 = nn.GroupNorm(16, 512)
        self.gn5 = nn.GroupNorm(16, 1024)
        self.dropout = nn.Dropout(0.5)
        self.dropout1 = nn.Dropout(0.25)

    def forward(self, x):
        x = self.conv1(x)
        x = self.gn1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.gn1(x)
        x = self.relu(x)
        out1 = x
        x = self.maxpool1(x)
        x = self.dropout1(x)
        x = self.conv3(x)
        x = self.gn2(x)
        x = self.relu(x)
        x = self.conv4(x)
        x = self.gn2(x)
        x = self.relu(x)
        out2 = x
        x = self.maxpool2(x)
        x = self.dropout(x)
        x = self.conv5(x)
        x = self.gn3(x)
        x = self.relu(x)
        x = self.conv6(x)
        x = self.gn3(x)
        x = self.relu(x)
        out3 = x
        x = self.maxpool3(x)
        x = self.dropout(x)
        x = self.conv7(x)
        x = self.gn4(x)
        x = self.relu(x)
        x = self.conv8(x)
        x = self.gn4(x)
        x = self.relu(x)
        out4 = x
        x = self.maxpool4(x)
        x = self.dropout(x)
        x = self.conv9(x)
        x = self.gn5(x)
        x = self.relu(x)
        x = self.conv10(x)
        x = self.gn5(x)
        x = self.relu(x)
        x = self.upconv1(x)
        x = torch.cat((x, out4), 1)
        x = self.dropout(x)
        x = self.conv11(x)
        x = self.gn4(x)
        x = self.relu(x)
        x = self.conv12(x)
        x = self.gn4(x)
        x = self.relu(x)
        x = self.upconv2(x)
        x = torch.cat((x, out3), 1)
        x = self.dropout(x)
        x = self.conv13(x)
        x = self.gn3(x)
        x = self.relu(x)
        x = self.conv14(x)
        x = self.gn3(x)
        x = self.relu(x)
        x = self.upconv3(x)
        x = torch.cat((x, out2), 1)
        x = self.dropout(x)
        x = self.conv15(x)
        x = self.gn2(x)
        x = self.relu(x)
        x = self.conv16(x)
        x = self.gn2(x)
        x = self.relu(x)
        x = self.upconv4(x)
        x = torch.cat((x, out1), 1)
        x = self.dropout(x)
        x = self.conv17(x)
        x = self.gn1(x)
        x = self.relu(x)
        x = self.conv18(x)
        x = self.gn1(x)
        x = self.relu(x)
        x = self.conv19(x)

        return x

''' UNet++ Model'''

class DenseBlock(nn.Module):
    
    def __init__(self, inplanes, planes):
        super().__init__()

        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=3, stride=1, padding=1)
        nn.init.normal_(self.conv1.weight, mean=0.0, std=np.sqrt(2/(3*3*planes)))
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1)
        nn.init.normal_(self.conv2.weight, mean=0.0, std=np.sqrt(2/(3*3*planes)))
        self.conv3 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1)
        nn.init.normal_(self.conv3.weight, mean=0.0, std=np.sqrt(2/(3*3*planes)))
        self.relu = nn.ReLU()
        self.gn = nn.GroupNorm(16, planes)
        self.dropout = nn.Dropout(0.5)
    def forward(self, x):

        out = self.conv1(x)
        out = self.gn(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.gn(out)
        out = self.relu(out)
        out = self.conv3(out)
        out = self.gn(out)
        out = self.relu(out)
        out = self.dropout(out)
        return out

class BasicDownBlock(nn.Module):
    def __init__(self, inplanes, planes):
        super().__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv1.weight, mean=0.0, std=np.sqrt(2/(3*3*planes)))
        self.conv2 = nn.Conv2d(planes, planes, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv2.weight, mean=0.0, std=np.sqrt(2/(3*3*planes)))
        self.maxpool = nn.MaxPool2d(kernel_size = 2, stride = 2)
        self.relu = nn.ReLU()
        self.gn = nn.GroupNorm(16, planes)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):

        out = self.conv1(x)
        out - self.gn(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.gn(out)
        out = self.relu(out)
        out1 = out
        out = self.maxpool(out)
        out = self.dropout(out)

        return out1, out

class BasicUpBlock(nn.Module):
    def __init__(self, inplanes, planes):
        super().__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv1.weight, mean=0.0, std=np.sqrt(2/(3*3*planes)))
        self.conv2 = nn.Conv2d(planes, planes, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv2.weight, mean=0.0, std=np.sqrt(2/(3*3*planes)))
        self.upconv = nn.ConvTranspose2d(in_channels = planes, out_channels = (planes//2), kernel_size = 2, stride = 2)
        nn.init.normal_(self.upconv.weight, mean=0.0, std=np.sqrt(2/(3*3*(planes//2))))
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):

        out = self.conv1(x)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.relu(out)
        out = self.upconv(out)
        out = self.dropout(out)

        return out

class UNet_PP(nn.Module):
    def __init__(self, denseblock, basicdownblock, basicupblock):
        super(UNet_PP, self).__init__()
        self.downlayer1 = basicdownblock(inplanes = 1, planes = 64)
        self.downlayer2 = basicdownblock(inplanes = 64, planes = 128)
        self.downlayer3 = basicdownblock(inplanes = 128, planes = 256)
        self.downlayer4 = basicdownblock(inplanes = 256, planes = 512)

        self.dense01 = denseblock(inplanes = 64*3, planes = 64)
        self.dense02 = denseblock(inplanes = 64*4, planes = 64)
        self.dense03 = denseblock(inplanes = 64*5, planes = 64)
        self.dense11 = denseblock(inplanes = 128*3, planes = 128)
        self.dense12 = denseblock(inplanes = 128*4, planes = 128)
        self.dense21 = denseblock(inplanes = 256*3, planes = 256)

        self.uplayer1 = basicupblock(inplanes = 512, planes = 1024)
        self.uplayer2 = basicupblock(inplanes = 1024, planes = 512)
        self.uplayer3 = basicupblock(inplanes = 256*3, planes = 256)
        self.uplayer4 = basicupblock(inplanes = 128*4, planes = 128)

        self.upconv1 = nn.ConvTranspose2d(in_channels = 128, out_channels = 128, kernel_size = 2, stride = 2)
        nn.init.normal_(self.upconv1.weight, mean=0.0, std=np.sqrt(2/(3*3*128)))
        self.upconv2 = nn.ConvTranspose2d(in_channels = 256, out_channels = 256, kernel_size = 2, stride = 2)
        nn.init.normal_(self.upconv2.weight, mean=0.0, std=np.sqrt(2/(3*3*256)))
        self.upconv3 = nn.ConvTranspose2d(in_channels = 512, out_channels = 512, kernel_size = 2, stride = 2)
        nn.init.normal_(self.upconv3.weight, mean=0.0, std=np.sqrt(2/(3*3*512)))

        #self.convds = nn.Conv2d(in_channels = 64, out_channels = 1, kernel_size = 1, stride = 1)

        self.conv1 = nn.Conv2d(in_channels = 64*5, out_channels = 64, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv1.weight, mean=0.0, std=np.sqrt(2/(3*3*64)))
        self.conv2 = nn.Conv2d(in_channels = 64, out_channels = 64, kernel_size = 3, stride = 1, padding = 1)
        nn.init.normal_(self.conv2.weight, mean=0.0, std=np.sqrt(2/(3*3*64)))
        self.conv3 = nn.Conv2d(in_channels = 64, out_channels = 1, kernel_size = 1, stride = 1)
        nn.init.normal_(self.conv3.weight, mean=0.0, std=np.sqrt(2/(1*1*1)))
        self.relu = nn.ReLU()
        self.gn = nn.GroupNorm(16, 64)
        self.dropout = nn.Dropout(0.5)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):

        out00, x = self.downlayer1(x)
        out10, x = self.downlayer2(x)
        out10_u = self.upconv1(out10)
        out01 = torch.cat((out00, out10_u), 1)
        out01 = self.dense01(out01)
        #seg1 = self.sigmoid(self.convds(out01))
        out20, x = self.downlayer3(x)
        out20_u = self.upconv2(out20)
        out11 = torch.cat((out10, out20_u), 1)
        out11 = self.dense11(out11)
        out30, x = self.downlayer4(x)
        out30_u = self.upconv3(out30)
        out21 = torch.cat((out20, out30_u), 1)
        out21 = self.dense21(out21)
        out11_u = self.upconv1(out11)
        out02 = torch.cat((out00, out01, out11_u), 1)
        out02 = self.dense02(out02)
        #seg2 = self.sigmoid(self.convds(out02))
        out21_u = self.upconv2(out20)
        out12 = torch.cat((out10, out11, out21_u), 1)
        out12 = self.dense12(out12)
        out12_u = self.upconv1(out12)
        out03 = torch.cat((out00, out01, out02, out12_u), 1)
        out03 = self.dense03(out03)
        #seg3 = self.sigmoid(self.convds(out03))

        x = self.uplayer1(x)
        x = torch.cat((out30, x), 1)
        x = self.uplayer2(x)
        x = torch.cat((out20, out21, x), 1)
        x = self.uplayer3(x)
        x = torch.cat((out10, out11, out12, x), 1)
        x = self.uplayer4(x)
        x = torch.cat((out00, out01, out02, out03, x), 1)
        x = self.conv1(x)
        x = self.gn(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.gn(x)
        x = self.relu(x)
        x = self.conv3(x)
        #seg4 = x
        seg4 = self.sigmoid(x)
        #seg = (seg1 + seg2 + seg3 + seg4)/4
        
        return seg4

''' PointNet Part Segmentation'''

def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv2d') != -1:
        torch.nn.init.xavier_normal_(m.weight.data)
        torch.nn.init.constant_(m.bias.data, 0.0)
    elif classname.find('Linear') != -1:
        torch.nn.init.xavier_normal_(m.weight.data)
        torch.nn.init.constant_(m.bias.data, 0.0)

def to_categorical(y, num_classes):
    """ 1-hot encodes a tensor """
    new_y = torch.eye(num_classes)[y.cpu().data.numpy(),]
    if (y.is_cuda):
        return new_y.cuda()
    return new_y

class T_Net(nn.Module):
    def __init__(self, out):
        super(T_Net, self).__init__()
        # In : (batch_size, n, 3)

        self.conv1 = nn.Conv1d(out, 64, kernel_size = 1, stride = 1)
        self.batchnorm1 = nn.BatchNorm1d(64)

        # (batch_size, n, 64)
        self.conv2 = nn.Conv1d(64, 128, kernel_size = 1, stride = 1)
        self.batchnorm2 = nn.BatchNorm1d(128)

        # (batch_size, n, 128)
        self.conv3 = nn.Conv1d(128, 1024, kernel_size = 1, stride = 1)
        self.batchnorm3 = nn.BatchNorm1d(1024)

        # (batch_size, 1024)
        self.fc1 = nn.Linear(1024, 512)
        self.batchnorm4 = nn.BatchNorm1d(512)
        # (batch_size, 512)
        self.fc2 = nn.Linear(512, 256)
        self.batchnorm5 = nn.BatchNorm1d(256)
        # (batch_size, 512)
        self.fc3 = nn.Linear(256, out*out) # out = 3 if input transform, else out = 128 if feature transform
        self.relu = nn.ReLU()
        

    def forward(self, x):
    
        x = x.to(device)
        x = self.relu(self.batchnorm1(self.conv1(x)))
        x = self.relu(self.batchnorm2(self.conv2(x)))
        x = self.relu(self.batchnorm3(self.conv3(x)))
        x = torch.max(x, 2, keepdim=True)[0]
        x = x.view(-1, 1024)
        x = self.relu(self.batchnorm4(self.fc1(x)))
        x = self.relu(self.batchnorm5(self.fc2(x)))
        x = self.fc3(x)

        out = int(math.sqrt(x.shape[1]))
        iden = Variable(torch.from_numpy(np.eye(out).flatten().astype(np.float32))).view(1, out * out).repeat(x.shape[0], 1)
        iden = iden.to(device)
        x = x + iden
        x = torch.reshape(x,(-1, out, out))
        return x

class Point_Net(nn.Module):
    def __init__(self, tnet):
        super(Point_Net,self).__init__()
        # In : (batch_size, n, 3)
        self.tnet1 = tnet(3)
        self.conv1 = nn.Conv1d(3, 64, 1)
        self.batchnorm1 = nn.BatchNorm1d(64)

        # (batch_size, n, 64)
        self.conv2 = nn.Conv1d(64, 128, 1) 
        self.batchnorm2 = nn.BatchNorm1d(128)

        # (batch_size, n, 128)
        self.conv3 = nn.Conv1d(128, 128, 1) 
        self.batchnorm3 = nn.BatchNorm1d(128)
        
        self.tnet2 = tnet(128)

        # (batch_size, n, 128)
        self.conv4 = nn.Conv1d(128, 512, 1)
        self.batchnorm4 = nn.BatchNorm1d(512)
        
        # (batch_size, n, 512)
        self.conv5 = nn.Conv1d(512, 2048, 1)
        self.batchnorm5 = nn.BatchNorm1d(2048)

        # (batch_size, 1088)        # We concatenate the global and local features
        self.conv6 = nn.Conv1d(4944 ,256, 1)
        self.batchnorm6 = nn.BatchNorm1d(256)

        # (batch_size, 512)        # We concatenate the global and local features
        self.conv7 = nn.Conv1d(256 ,256, 1)
        self.batchnorm7 = nn.BatchNorm1d(256)

        # (batch_size, 256)        # We concatenate the global and local features
        self.conv8 = nn.Conv1d(256 ,128, 1)
        self.batchnorm8 = nn.BatchNorm1d(128)

        # (batch_size, 128)
        self.conv9 = nn.Conv1d(128, 50, 1)
        self.relu = nn.ReLU()
    
    def forward(self, x, label):

        x = x.to(device)
        out_tnet1 = self.tnet1(x)
        x = x.transpose(2, 1)
        x = torch.bmm(x, out_tnet1)
        x = x.transpose(2, 1)
        x = self.relu(self.batchnorm1(self.conv1(x)))
        out1 = x
        x = self.relu(self.batchnorm2(self.conv2(x)))
        out2 = x
        x = self.relu(self.batchnorm3(self.conv3(x)))
        out3 = x
        out_tnet2 = self.tnet2(x)
        x = x.transpose(2, 1)
        x = torch.bmm(x, out_tnet2)
        x = x.transpose(2, 1)
        x = self.relu(self.batchnorm4(self.conv4(x)))
        out4 = x
        x = self.batchnorm5(self.conv5(x))
        out5 = x
        x = torch.max(x, 2, keepdim=True)[0]
        x = x.view(-1, 2048)
        x = torch.cat([x,label.squeeze(1)],1)
        x = x.view(-1, 2048+16, 1).repeat(1, 1, 2048)
        x = torch.cat((x, out1, out2, out3, out4, out5), 1)
        x = self.relu(self.batchnorm6(self.conv6(x)))
        x = self.relu(self.batchnorm7(self.conv7(x)))
        x = self.relu(self.batchnorm8(self.conv8(x)))
        x = self.conv9(x)
        x = x.transpose(2, 1).contiguous()
        x = F.log_softmax(x.view(-1, 50), dim=-1)
        x = x.view(out1.shape[0], 2048, 50) # [B, N, 50]

        return x, out_tnet2

def UNet():
    model = U_Net()
    return model

def UNetPP():
    model = UNet_PP(DenseBlock, BasicDownBlock, BasicUpBlock)
    return model

def PointNet():
    model = Point_Net(T_Net).to(device)
    model = model.apply(weights_init)
    return model
