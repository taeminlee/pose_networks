#%% import
import os
from scipy import io
from PIL import Image
import torchvision.transforms as transforms

#%% LSP class
class LSP():
    def __init__(self, is_train=True, transform=None):
        print("loading annotations into memory...")
        self.joints = io.loadmat('./datasets/lsp/joints.mat')['joints']

        self.num = self.joints.shape[-1]

        if(transform == None):
            self.transform = transforms.ToTensor()
        else:
            self.transform = transform
    def __getitem__(self, idx):
        image_name = 'im%04d.jpg' % (idx+1)
        img = Image.open(os.path.join('./datasets/lsp/images/', image_name)).convert('RGB')
        if(self.transform is not None):
            img = self.transform(img)
        points = list(zip(self.joints[0,:,idx], self.joints[1,:,idx]))
        is_visible = self.joints[2,:,idx]
        target = {'points':points, 'is_visible':is_visible}
        return img, target

    def __iter__(self, idxs = None):
        if(idxs is None):
            idxs = range(self.num)
        for idx in idxs:
            yield self[idx]
        return None
