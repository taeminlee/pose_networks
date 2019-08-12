# Pose dataset manager

Tools to download and manage pose related datasets. (MPII and COCO 2017)

```sh
usage: main.py [-h] [--mpii] [--mpii_video] [--coco] [--overwrite] [-v]

optional arguments:
  -h, --help       show this help message and exit
  --mpii
  --mpii_video
  --coco
  --overwrite
  -v, --verbosity
```

#### Supported datasets

- MPII
    - http://human-pose.mpi-inf.mpg.de/
    - `python main.py --mpii -v`

- COCO keypoints
    - http://cocodataset.org/
    - `python main.py --coco -v`

#### tasks

- [x] download MPII
- [x] download COCO
- [ ] resume download
- [x] unzip
- [ ] read image and annotation
- [ ] manage train/val/test set