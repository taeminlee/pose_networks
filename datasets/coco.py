#%% import
import os
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

    def __iter__(self, idxs = None):
        if(idxs is None):
            idxs = range(self.num)
        for idx in idxs:
            yield self.cap[idx]
        return None