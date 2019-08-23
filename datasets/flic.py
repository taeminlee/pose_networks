#%% import
import os
from scipy import io
from PIL import Image
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

        if(transform == None):
            self.transform = transforms.ToTensor()
        else:
            self.transform = transform
        print("loaded annotations into memory...")

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


#%%
if __name__ == "__main__":
    f = FLIC(is_full=True)
    for img, target in f:
        print(target['image_name'])