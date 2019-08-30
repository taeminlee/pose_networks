#%% import
import os
import numpy as np
from scipy import io
from PIL import Image, ImageDraw
import torchvision.transforms as transforms

#%% LSP class
class LSP():
    def __init__(self, is_train=True, transform=None, et=False):
        print("loading annotations into memory...")
        self.et = et
        if(et):
            self.dataset_path = './datasets/lspet/'
        else:
            self.dataset_path = './datasets/lsp/'
        self.joints = io.loadmat(os.path.join(self.dataset_path, 'joints.mat'))['joints']

        self.num = self.joints.shape[-1]
        print('total %s images' % self.num)

        if(transform == None):
            self.transform = transforms.ToTensor()
        else:
            self.transform = transform
        
    def __getitem__(self, idx):
        if(self.et):
            image_name = 'im%05d.jpg' % (idx+1)
        else:
            image_name = 'im%04d.jpg' % (idx+1)
        img = Image.open(os.path.join(self.dataset_path + 'images/', image_name)).convert('RGB')
        if(self.transform is not None):
            img = self.transform(img)
        points = list(zip(self.joints[0,:,idx], self.joints[1,:,idx]))
        is_visible = self.joints[2,:,idx]
        target = {'image_name':image_name, 'keypoints':points, 'is_visible':is_visible}
        return img, target

    def __iter__(self, idxs = None):
        if(idxs is None):
            idxs = range(self.num)
        for idx in idxs:
            yield self[idx]
        return None
    
    def get_image(self, idx):
        bak_trans = self.transform
        self.transform = None
        img, target = self[idx]
        self.transform = bak_trans
        draw = ImageDraw.Draw(img)
        for keypoint in target['keypoints']:
            if(np.isnan(keypoint[0])):
                continue
            draw.rectangle([p-5 for p in keypoint] + [p+5 for p in keypoint], outline='red')
        return img
    
    def show_image(self, idx):
        img = self.get_image(idx)
        img.show()

#%%
if __name__ == "__main__":
    from tqdm import tqdm
    f = LSP()
    pbar = tqdm(total=f.num)
    for img, target in f:
        pbar.update(1)
        pbar.set_description(target['image_name'])