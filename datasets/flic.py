#%% import
import os
import numpy as np
from scipy import io
from PIL import Image, ImageDraw
import torchvision.transforms as transforms

#%% FLIC class
class FLIC():
    def __init__(self, is_train=True, transform=None, is_full=False):
        print("loading annotations into memory...")
        self.is_train = is_train
        self.flic_path = './datasets/flic/FLIC/'
        if(is_full):
            self.flic_path = './datasets/flic/FLIC-full/'
        self.mat = io.loadmat(self.flic_path + 'examples.mat')['examples']
        
        self.num = self.mat.shape[-1]
        print('total %s images' % self.num)

        if(transform == None):
            self.transform = transforms.ToTensor()
        else:
            self.transform = transform

    def __getitem__(self, idx):
        item = self.mat[0,idx]
        target = {
            'image_name' : item['filepath'][0],
            'movie_name' : item['moviename'][0],
            'is_train' : bool(item['istrain'][0,0]),
            'is_test' : bool(item['istest'][0,0]),
            'torso_box' : item['torsobox'][0],
            'keypoints' : list(zip(item['coords'][0], item['coords'][1]))
        }
        image_name = item['filepath'][0]
        img = Image.open(os.path.join(self.flic_path, 'images/', image_name)).convert('RGB')
        if(self.transform is not None):
            img = self.transform(img)
        return img, target

    def __iter__(self, idxs = None):
        if(idxs is None):
            idxs = range(self.num)
        for idx in idxs:
            img, target = self[idx]
            if(self.is_train and target['is_train']):
                yield img, target
            elif(self.is_train == False and target['is_test']):
                yield img, target
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
    f = FLIC(is_full=True)
    pbar = tqdm(total=f.num)
    for img, target in f:
        pbar.update(1)
        pbar.set_description(target['image_name'])