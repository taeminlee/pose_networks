#%%
import os
import json
from PIL import Image, ImageDraw
import torchvision.transforms as transforms
import numpy as np

#%% AIChallenge class
class AICHALLENGE():
    def __init__(self, is_train=True, transform=None):
        print("loading annotations into memory...")
        self.is_train = is_train
        if(self.is_train):
            self.image_path = './datasets/ai_challenger/'
            self.ann_file_path = './datasets/ai_challenger/ai_challenger/ai_challenger_train.json'
        else:
            self.image_path = './datasets/ai_challenger/'
            self.ann_file_path = './datasets/ai_challenger/ai_challenger/ai_challenger_valid.json'
        with open(self.ann_file_path) as json_file:
            self.ann = json.load(json_file)
        self.num = len(self.ann['images'])
        self.categories = self.ann['categories']
        print('total %s images' % self.num)

        if(transform == None):
            self.transform = transforms.ToTensor()
        else:
            self.transform = transform

    def __getitem__(self, idx):
        image = self.ann['images'][idx]
        annotation = self.ann['annotations'][idx]
        
        target = {
            'keypoints' : list(np.array(annotation['keypoints']).reshape(-1,3)[:,0:2]),
            'is_visible' : list(np.array(annotation['keypoints']).reshape(-1,3)[:,2]-1),
            'bbox' : annotation['bbox'],
            'image_name' : image['file_name']
        }

        image_name = image['file_name']
        img = Image.open(os.path.join(self.image_path, image_name)).convert('RGB')
        if(self.transform is not None):
            img = self.transform(img)
        return img, target

    def __iter__(self, idxs = None):
        if(idxs is None):
            idxs = range(self.num)
        for idx in idxs:
            img, target = self[idx]
            yield img, target
        return None
    
    def draw_image(self, idx):
        bak_trans = self.transform
        self.transform = None
        img, target = self[idx]
        self.transform = bak_trans
        draw = ImageDraw.Draw(img)
        for keypoint in target['keypoints']:
            draw.rectangle(list(keypoint-5) + list(keypoint+5), outline='red')
        for bone in self.categories[0]['skeleton']:
            draw.line(list(target['keypoints'][bone[0]-1]) + list(target['keypoints'][bone[1]-1]), fill='red')
        img.show()
#%%
if __name__ == "__main__":
    from tqdm import tqdm
    f = AICHALLENGE()
    pbar = tqdm(total=f.num)
    for img, target in f:
        pbar.update(1)
        pbar.set_description(target['image_name'])