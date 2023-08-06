import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import init

def init_weights(net, init_type='normal', gain=0.02):
    def init_func(m):
        classname = m.__class__.__name__
        if hasattr(m, 'weight') and (classname.find('Conv') != -1 or classname.find('Linear') != -1):
            if init_type == 'normal':
                init.normal_(m.weight.data, 0.0, gain)
            elif init_type == 'xavier':
                init.xavier_normal_(m.weight.data, gain=gain)
            elif init_type == 'kaiming':
                init.kaiming_normal_(m.weight.data, a=0, mode='fan_in')
            elif init_type == 'orthogonal':
                init.orthogonal_(m.weight.data, gain=gain)
            else:
                raise NotImplementedError('initialization method [%s] is not implemented' % init_type)
            if hasattr(m, 'bias') and m.bias is not None:
                init.constant_(m.bias.data, 0.0)
        elif classname.find('BatchNorm1d') != -1:
            init.normal_(m.weight.data, 1.0, gain)
            init.constant_(m.bias.data, 0.0)

    print('initialize network with %s' % init_type)
    net.apply(init_func)

class conv_block_1d(nn.Module):
    def __init__(self, ch_in, ch_out, batch_norm:bool=True, activation_fn=nn.ReLU):
        super().__init__()
        if batch_norm:
            self.conv = nn.Sequential(
                nn.Conv1d(ch_in, ch_out, kernel_size=3,stride=1,padding=1,bias=True),
                nn.BatchNorm1d(ch_out),
                activation_fn(inplace=True),
                nn.Conv1d(ch_out, ch_out, kernel_size=3,stride=1,padding=1,bias=True),
                nn.BatchNorm1d(ch_out),
                activation_fn(inplace=True)
            )       
        else:
            self.conv = nn.Sequential(
                nn.Conv1d(ch_in, ch_out, kernel_size=3,stride=1,padding=1,bias=True),
                activation_fn(inplace=True),
                nn.Conv1d(ch_out, ch_out, kernel_size=3,stride=1,padding=1,bias=True),
                activation_fn(inplace=True)
            )

    def forward(self,x):
        x = self.conv(x)
        return x

class up_conv_1d(nn.Module):
    def __init__(self, ch_in, ch_out, batch_norm:bool=True, activation_fn=nn.ReLU):
        super().__init__()
        if batch_norm:
            self.up = nn.Sequential(
                nn.Upsample(scale_factor=2),
                nn.Conv1d(ch_in,ch_out,kernel_size=3,stride=1,padding=1,bias=True),
		        nn.BatchNorm1d(ch_out),
			    activation_fn(inplace=True)
            )
        else:
            self.up = nn.Sequential(
                nn.Upsample(scale_factor=2),
                nn.Conv1d(ch_in,ch_out,kernel_size=3,stride=1,padding=1,bias=True),
			    activation_fn(inplace=True)
            )

    def forward(self,x):
        x = self.up(x)
        return x

class Recurrent_block_1d(nn.Module):
    def __init__(self, ch_out, t=2, batch_norm:bool=True, activation_fn=nn.ReLU):
        super().__init__()
        self.t = t
        self.ch_out = ch_out
        if batch_norm:
            self.conv = nn.Sequential(
                nn.Conv1d(ch_out,ch_out,kernel_size=3,stride=1,padding=1,bias=True),
	    	    nn.BatchNorm1d(ch_out),
			    activation_fn(inplace=True)
            )
        else:
            self.conv = nn.Sequential(
                nn.Conv1d(ch_out,ch_out,kernel_size=3,stride=1,padding=1,bias=True),
			    activation_fn(inplace=True)
            )

    def forward(self,x):
        for i in range(self.t):

            if i==0:
                x1 = self.conv(x)
            
            x1 = self.conv(x+x1)
        return x1
        
class RRCNN_block_1d(nn.Module):
    def __init__(self, ch_in, ch_out, t=2, batch_norm:bool=True, activation_fn=nn.ReLU):
        super().__init__()
        self.RCNN = nn.Sequential(
            Recurrent_block_1d(ch_out,t=t, batch_norm=batch_norm, activation_fn=activation_fn),
            Recurrent_block_1d(ch_out,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        )
        self.Conv_1x1 = nn.Conv1d(ch_in,ch_out,kernel_size=1,stride=1,padding=0)

    def forward(self,x):
        x = self.Conv_1x1(x)
        x1 = self.RCNN(x)
        return x+x1

class single_conv_1d(nn.Module):
    def __init__(self, ch_in, ch_out, batch_norm:bool=True, activation_fn=nn.ReLU):
        super().__init__()
        if batch_norm:
            self.conv = nn.Sequential(
                nn.Conv1d(ch_in, ch_out, kernel_size=3,stride=1,padding=1,bias=True),
                nn.BatchNorm1d(ch_out),
                activation_fn(inplace=True)
            )
        else:
            self.conv = nn.Sequential(
                nn.Conv1d(ch_in, ch_out, kernel_size=3,stride=1,padding=1,bias=True),
                activation_fn(inplace=True)
            )

    def forward(self,x):
        x = self.conv(x)
        return x

class Attention_block_1d(nn.Module):
    def __init__(self, F_g, F_l, F_int, batch_norm:bool=True, activation_fn=nn.ReLU):
        super().__init__()
        if batch_norm:
            self.W_g = nn.Sequential(
                nn.Conv1d(F_g, F_int, kernel_size=1,stride=1,padding=0,bias=True),
                nn.BatchNorm1d(F_int)
                )
            self.W_x = nn.Sequential(
                nn.Conv1d(F_l, F_int, kernel_size=1,stride=1,padding=0,bias=True),
                nn.BatchNorm1d(F_int)
            )
            self.psi = nn.Sequential(
                nn.Conv1d(F_int, 1, kernel_size=1,stride=1,padding=0,bias=True),
                nn.BatchNorm1d(1),
                nn.Sigmoid()
            )
        else:
            self.W_g = nn.Sequential(
                nn.Conv1d(F_g, F_int, kernel_size=1,stride=1,padding=0,bias=True),
                )
            self.W_x = nn.Sequential(
                nn.Conv1d(F_l, F_int, kernel_size=1,stride=1,padding=0,bias=True),
            )
            self.psi = nn.Sequential(
                nn.Conv1d(F_int, 1, kernel_size=1,stride=1,padding=0,bias=True),
                nn.Sigmoid()
            )
        
        self.relu = activation_fn(inplace=True)
        
    def forward(self,g,x):
        g1 = self.W_g(g)
        x1 = self.W_x(x)
        psi = self.relu(g1+x1)
        psi = self.psi(psi)

        return x*psi

class U_Net_1D(nn.Module):
    def __init__(self, img_ch=3, output_ch=1, batch_norm:bool=True, hidden_activation_fn=nn.ReLU, ending_activation_fn=torch.tanh):
        super().__init__()
        self.out_fn = ending_activation_fn
        activation_fn = hidden_activation_fn
        self.Maxpool = nn.MaxPool1d(kernel_size=2,stride=2)

        self.Conv1 = conv_block_1d(ch_in=img_ch,ch_out=64, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Conv2 = conv_block_1d(ch_in=64,ch_out=128, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Conv3 = conv_block_1d(ch_in=128,ch_out=256, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Conv4 = conv_block_1d(ch_in=256,ch_out=512, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Conv5 = conv_block_1d(ch_in=512,ch_out=1024, batch_norm=batch_norm, activation_fn=activation_fn)

        self.Up5 = up_conv_1d(ch_in=1024,ch_out=512, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_conv5 = conv_block_1d(ch_in=1024, ch_out=512, batch_norm=batch_norm, activation_fn=activation_fn)

        self.Up4 = up_conv_1d(ch_in=512,ch_out=256, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_conv4 = conv_block_1d(ch_in=512, ch_out=256, batch_norm=batch_norm, activation_fn=activation_fn)
        
        self.Up3 = up_conv_1d(ch_in=256,ch_out=128, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_conv3 = conv_block_1d(ch_in=256, ch_out=128, batch_norm=batch_norm, activation_fn=activation_fn)
        
        self.Up2 = up_conv_1d(ch_in=128,ch_out=64, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_conv2 = conv_block_1d(ch_in=128, ch_out=64, batch_norm=batch_norm, activation_fn=activation_fn)

        self.Conv_1x1 = nn.Conv1d(64,output_ch,kernel_size=1,stride=1,padding=0)

    def forward(self,x):
        # encoding path
        x1 = self.Conv1(x)

        x2 = self.Maxpool(x1)
        x2 = self.Conv2(x2)
        
        x3 = self.Maxpool(x2)
        x3 = self.Conv3(x3)

        x4 = self.Maxpool(x3)
        x4 = self.Conv4(x4)

        x5 = self.Maxpool(x4)
        x5 = self.Conv5(x5)

        # decoding + concat path
        d5 = self.Up5(x5)
        d5 = torch.cat((x4, d5), dim=1)
        
        d5 = self.Up_conv5(d5)
        
        d4 = self.Up4(d5)
        d4 = torch.cat((x3, d4), dim=1)
        d4 = self.Up_conv4(d4)

        d3 = self.Up3(d4)
        d3 = torch.cat((x2, d3), dim=1)
        d3 = self.Up_conv3(d3)

        d2 = self.Up2(d3)
        d2 = torch.cat((x1, d2), dim=1)
        d2 = self.Up_conv2(d2)

        d1 = self.Conv_1x1(d2)
       
        if self.out_fn == None:
            return d1
        else:
            return self.out_fn(d1)
        #return torch.tanh(d1)
        #return d1


class R2U_Net_1D(nn.Module):
    def __init__(self, img_ch=3, output_ch=1, t=2, batch_norm:bool=True, hidden_activation_fn=nn.ReLU, ending_activation_fn=torch.tanh):
        super().__init__()
        self.out_fn = ending_activation_fn
        activation_fn = hidden_activation_fn
        
        self.Maxpool = nn.MaxPool1d(kernel_size=2,stride=2)
        self.Upsample = nn.Upsample(scale_factor=2)

        self.RRCNN1 = RRCNN_block_1d(ch_in=img_ch,ch_out=64,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        self.RRCNN2 = RRCNN_block_1d(ch_in=64,ch_out=128,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        self.RRCNN3 = RRCNN_block_1d(ch_in=128,ch_out=256,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        self.RRCNN4 = RRCNN_block_1d(ch_in=256,ch_out=512,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        self.RRCNN5 = RRCNN_block_1d(ch_in=512,ch_out=1024,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        

        self.Up5 = up_conv_1d(ch_in=1024,ch_out=512, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_RRCNN5 = RRCNN_block_1d(ch_in=1024, ch_out=512,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        
        self.Up4 = up_conv_1d(ch_in=512,ch_out=256, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_RRCNN4 = RRCNN_block_1d(ch_in=512, ch_out=256,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        
        self.Up3 = up_conv_1d(ch_in=256,ch_out=128, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_RRCNN3 = RRCNN_block_1d(ch_in=256, ch_out=128,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        
        self.Up2 = up_conv_1d(ch_in=128,ch_out=64, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_RRCNN2 = RRCNN_block_1d(ch_in=128, ch_out=64,t=t, batch_norm=batch_norm, activation_fn=activation_fn)

        self.Conv_1x1 = nn.Conv1d(64,output_ch,kernel_size=1,stride=1,padding=0)


    def forward(self,x):
        # encoding path
        x1 = self.RRCNN1(x)

        x2 = self.Maxpool(x1)
        x2 = self.RRCNN2(x2)
        
        x3 = self.Maxpool(x2)
        x3 = self.RRCNN3(x3)

        x4 = self.Maxpool(x3)
        x4 = self.RRCNN4(x4)

        x5 = self.Maxpool(x4)
        x5 = self.RRCNN5(x5)

        # decoding + concat path
        d5 = self.Up5(x5)
        d5 = torch.cat((x4,d5),dim=1)
        d5 = self.Up_RRCNN5(d5)
        
        d4 = self.Up4(d5)
        d4 = torch.cat((x3,d4),dim=1)
        d4 = self.Up_RRCNN4(d4)

        d3 = self.Up3(d4)
        d3 = torch.cat((x2,d3),dim=1)
        d3 = self.Up_RRCNN3(d3)

        d2 = self.Up2(d3)
        d2 = torch.cat((x1,d2),dim=1)
        d2 = self.Up_RRCNN2(d2)

        d1 = self.Conv_1x1(d2)

        if self.out_fn == None:
            return d1
        else:
            return self.out_fn(d1)
        #return torch.tanh(d1)
        #return d1


class AttU_Net_1D(nn.Module):
    def __init__(self, img_ch=3, output_ch=1, batch_norm:bool=True, hidden_activation_fn=nn.ReLU, ending_activation_fn=torch.tanh):
        super().__init__()
        self.out_fn = ending_activation_fn
        activation_fn = hidden_activation_fn
        
        self.Maxpool = nn.MaxPool1d(kernel_size=2,stride=2)

        self.Conv1 = conv_block_1d(ch_in=img_ch,ch_out=64, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Conv2 = conv_block_1d(ch_in=64,ch_out=128, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Conv3 = conv_block_1d(ch_in=128,ch_out=256, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Conv4 = conv_block_1d(ch_in=256,ch_out=512, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Conv5 = conv_block_1d(ch_in=512,ch_out=1024, batch_norm=batch_norm, activation_fn=activation_fn)

        self.Up5 = up_conv_1d(ch_in=1024,ch_out=512, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Att5 = Attention_block_1d(F_g=512,F_l=512,F_int=256, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_conv5 = conv_block_1d(ch_in=1024, ch_out=512, batch_norm=batch_norm, activation_fn=activation_fn)

        self.Up4 = up_conv_1d(ch_in=512,ch_out=256, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Att4 = Attention_block_1d(F_g=256,F_l=256,F_int=128, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_conv4 = conv_block_1d(ch_in=512, ch_out=256, batch_norm=batch_norm, activation_fn=activation_fn)
        
        self.Up3 = up_conv_1d(ch_in=256,ch_out=128, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Att3 = Attention_block_1d(F_g=128,F_l=128,F_int=64, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_conv3 = conv_block_1d(ch_in=256, ch_out=128, batch_norm=batch_norm, activation_fn=activation_fn)
        
        self.Up2 = up_conv_1d(ch_in=128,ch_out=64, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Att2 = Attention_block_1d(F_g=64,F_l=64,F_int=32, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_conv2 = conv_block_1d(ch_in=128, ch_out=64, batch_norm=batch_norm, activation_fn=activation_fn)

        self.Conv_1x1 = nn.Conv1d(64,output_ch,kernel_size=1,stride=1,padding=0)

    def forward(self,x):
        # encoding path
        x1 = self.Conv1(x)

        x2 = self.Maxpool(x1)
        x2 = self.Conv2(x2)
        
        x3 = self.Maxpool(x2)
        x3 = self.Conv3(x3)

        x4 = self.Maxpool(x3)
        x4 = self.Conv4(x4)

        x5 = self.Maxpool(x4)
        x5 = self.Conv5(x5)

        # decoding + concat path
        d5 = self.Up5(x5)
        x4 = self.Att5(g=d5,x=x4)
        d5 = torch.cat((x4,d5),dim=1)        
        d5 = self.Up_conv5(d5)
        
        d4 = self.Up4(d5)
        x3 = self.Att4(g=d4,x=x3)
        d4 = torch.cat((x3,d4),dim=1)
        d4 = self.Up_conv4(d4)

        d3 = self.Up3(d4)
        x2 = self.Att3(g=d3,x=x2)
        d3 = torch.cat((x2,d3),dim=1)
        d3 = self.Up_conv3(d3)

        d2 = self.Up2(d3)
        x1 = self.Att2(g=d2,x=x1)
        d2 = torch.cat((x1,d2),dim=1)
        d2 = self.Up_conv2(d2)

        d1 = self.Conv_1x1(d2)
        
        if self.out_fn == None:
            return d1
        else:
            return self.out_fn(d1)
        #return torch.tanh(d1)
        #return d1

class R2AttU_Net_1D(nn.Module):
    def __init__(self, img_ch=3, output_ch=1, t=2, batch_norm:bool=True, hidden_activation_fn=nn.ReLU, ending_activation_fn=torch.tanh):
        super().__init__()
        self.out_fn = ending_activation_fn
        activation_fn = hidden_activation_fn
        
        self.Maxpool = nn.MaxPool1d(kernel_size=2,stride=2)
        self.Upsample = nn.Upsample(scale_factor=2)

        self.RRCNN1 = RRCNN_block_1d(ch_in=img_ch,ch_out=64,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        self.RRCNN2 = RRCNN_block_1d(ch_in=64,ch_out=128,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        self.RRCNN3 = RRCNN_block_1d(ch_in=128,ch_out=256,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        self.RRCNN4 = RRCNN_block_1d(ch_in=256,ch_out=512,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        self.RRCNN5 = RRCNN_block_1d(ch_in=512,ch_out=1024,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        

        self.Up5 = up_conv_1d(ch_in=1024,ch_out=512, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Att5 = Attention_block_1d(F_g=512,F_l=512,F_int=256, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_RRCNN5 = RRCNN_block_1d(ch_in=1024, ch_out=512,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        
        self.Up4 = up_conv_1d(ch_in=512,ch_out=256, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Att4 = Attention_block_1d(F_g=256,F_l=256,F_int=128, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_RRCNN4 = RRCNN_block_1d(ch_in=512, ch_out=256,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        
        self.Up3 = up_conv_1d(ch_in=256,ch_out=128, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Att3 = Attention_block_1d(F_g=128,F_l=128,F_int=64, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_RRCNN3 = RRCNN_block_1d(ch_in=256, ch_out=128,t=t, batch_norm=batch_norm, activation_fn=activation_fn)
        
        self.Up2 = up_conv_1d(ch_in=128,ch_out=64, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Att2 = Attention_block_1d(F_g=64,F_l=64,F_int=32, batch_norm=batch_norm, activation_fn=activation_fn)
        self.Up_RRCNN2 = RRCNN_block_1d(ch_in=128, ch_out=64,t=t, batch_norm=batch_norm, activation_fn=activation_fn)

        self.Conv_1x1 = nn.Conv1d(64,output_ch,kernel_size=1,stride=1,padding=0)


    def forward(self,x):
        # encoding path
        x1 = self.RRCNN1(x)

        x2 = self.Maxpool(x1)
        x2 = self.RRCNN2(x2)
        
        x3 = self.Maxpool(x2)
        x3 = self.RRCNN3(x3)

        x4 = self.Maxpool(x3)
        x4 = self.RRCNN4(x4)

        x5 = self.Maxpool(x4)
        x5 = self.RRCNN5(x5)

        # decoding + concat path
        d5 = self.Up5(x5)
        x4 = self.Att5(g=d5,x=x4)
        d5 = torch.cat((x4,d5),dim=1)
        d5 = self.Up_RRCNN5(d5)
        
        d4 = self.Up4(d5)
        x3 = self.Att4(g=d4,x=x3)
        d4 = torch.cat((x3,d4),dim=1)
        d4 = self.Up_RRCNN4(d4)

        d3 = self.Up3(d4)
        x2 = self.Att3(g=d3,x=x2)
        d3 = torch.cat((x2,d3),dim=1)
        d3 = self.Up_RRCNN3(d3)

        d2 = self.Up2(d3)
        x1 = self.Att2(g=d2,x=x1)
        d2 = torch.cat((x1,d2),dim=1)
        d2 = self.Up_RRCNN2(d2)

        d1 = self.Conv_1x1(d2)

        if self.out_fn == None:
            return d1
        else:
            return self.out_fn(d1)
        #return torch.tanh(d1)
        #return d1