import torch
import torch.nn as nn
import numpy as np
from skimage import io

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 8, 3)
        self.conv2 = nn.Conv2d(8, 16, 3)
        self.conv3 = nn.Conv2d(16, 8, 3)
        self.bn1 = nn.BatchNorm2d(8)
        self.bn2 = nn.BatchNorm2d(16)
        self.bn3 = nn.BatchNorm2d(8)
        self.act = nn.ReLU()
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(4*4*8, 10)

    def forward(self, x):
        out1 = self.bn1(self.pool(self.act(self.conv1(x))))
        out2 = self.bn2(self.act(self.conv2(out1)))
        out3 = self.bn3(self.pool(self.act(self.conv3(out2))))
        out = self.fc(out3.flatten(start_dim=-3, end_dim=-1))
        return out
        
def normalize(img):
    out = img.copy()
    out -= np.min(out)
    out /= np.max(out)
    return out

def get_idc(modelout):
    return [i.item() for i in torch.argmax(modelout, axis=-1)]

def get_blocks(img):
    out = img.copy()
    xx, yy = out.shape
    out = np.reshape(out, (-1, 9, xx//9))
    out = np.transpose(out, axes=(1,0,2))
    out = np.reshape(out, (9, 9, xx//9, yy//9))
    out = np.transpose(out, axes=(1,0,2,3))
    out = np.reshape(out, (-1, xx//9, yy//9))
    r = 15
    out = out[:, r:-r, r:-r]
    _, xx, yy = out.shape
    xx = [int(i*xx//28) for i in range(28)]
    yy = [int(i*yy//28) for i in range(28)]
    out = out[:, xx]
    out = out[:,:,yy]
    return out

def classify(url, model):
    img = normalize(io.imread(url).astype(float))
    xx, yy, cc = img.shape
    img = 1-img[:xx//9*9, :yy//9*9]@np.array([2126, 7152, 722])/10000
    blocks = get_blocks(img)
    blocks -= np.mean(blocks, axis=(1,2), keepdims=True)
    blocks /= (np.std(blocks, axis=(1,2), keepdims=True)+1e-8)
    return get_idc(model(torch.tensor(blocks.astype(np.float32)).unsqueeze(1)))
