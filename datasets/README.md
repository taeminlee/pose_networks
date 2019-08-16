# Pose dataset manager

Tools to download and manage pose related datasets. (MPII and COCO 2017)

## Dataset Downloader

```sh
usage: downloader.py [-h] [--mpii] [--mpii_video] [--coco] [--aichallenger]
               [--overwrite] [-v]

optional arguments:
  -h, --help       show this help message and exit
  --mpii
  --mpii_video
  --coco
  --aichallenger
  --overwrite
  -v, --verbosity
```

### Supported datasets

- MPII
  - http://human-pose.mpi-inf.mpg.de/
  - `python downloader.py --mpii -v`

- COCO keypoints
  - http://cocodataset.org/
  - `python downloader.py --coco -v`

- LSP
- http://sam.johnson.io/research/lsp.html
- `python downloader.py --lsp -v`

- FLIC
- https://bensapp.github.io/flic-dataset.html
- `python downloader.py --flic -v`

- AI Challenger
- https://drive.google.com/file/d/1zahjQWhuKIYWRRI2ZlHzn65Ug_jIiC4l/view
- `python downloader.py --aichallenger -v`

## tasks

- [x] download MPII
- [x] download COCO
- [x] download ai challenge
- [x] download LSP
- [x] download FLIC
- [x] resume download
- [x] unzip
- [ ] read image and annotation
- [ ] manage train/val/test set