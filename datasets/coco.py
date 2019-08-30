#%% import
import os
import numpy as np
from PIL import ImageDraw
import torchvision.datasets as dset
import torchvision.transforms as transforms

#%% COCO class (wrap torchvision dataset)
class COCO():
    def __init__(self, is_train=True, transform=None):
        if(is_train):
            self.root = './datasets/coco/train2017'
            self.annFile = './datasets/coco/annotations/person_keypoints_train2017.json'
        else:
            self.root = './datasets/coco/val2017'
            self.annFile = './datasets/coco/annotations/person_keypoints_val2017.json'
        if(transform == None):
            self.transform = transforms.ToTensor()
        else:
            self.transform = transform
        self.cap = dset.CocoDetection(root = self.root, annFile = self.annFile, transform = self.transform)
        self.num = len(self.cap)
    
    def __getitem__(self, idx):
        img, target = self.cap[idx]
        for annotation in target:
            if 'is_visible' in annotation: # already pre-processed
                continue
            temp = np.array(annotation['keypoints']).reshape(-1,3)
            annotation['is_visible'] = temp[:,-1] - 1
            annotation['draw_keypoints'] = temp[:,0:2]
        return img, target

    def __iter__(self, idxs = None):
        if(idxs is None):
            idxs = range(self.num)
        for idx in idxs:
            yield self[idx]
        return None
    
    def get_image(self, idx):
        bak_trans = self.cap.transforms
        self.cap.transforms = None
        img, target = self[idx]
        self.cap.transforms = bak_trans
        draw = ImageDraw.Draw(img)
        for annotation in target:
            for keypoint in annotation['draw_keypoints']:
                if(keypoint[0] == 0 and keypoint[1] == 0):
                    continue
                draw.rectangle(list(keypoint-5) + list(keypoint+5), outline='red')
        return img
    
    def show_image(self, idx):
        img = self.get_image(idx)
        img.show()

#%%
if __name__ == "__main__":
    from tqdm import tqdm
    f = COCO()
    pbar = tqdm(total=f.num)
    idx = 0
    for img, target in f:
        #print(idx, target)
        #idx = idx + 1
        pbar.update(1)

#%%
