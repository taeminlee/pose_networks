# pose networks

Human Pose Estimation using neural network

- [ ] dataset downloader
- [ ] trainer
- [ ] evaluator

## Dataset Downloader

```sh
usage: downloader.py [-h] [--mpii] [--mpii_video] [--coco] [--lsp] [--flic]
                     [--aichallenger] [--overwrite] [-v]

optional arguments:
  -h, --help       show this help message and exit
  --mpii
  --mpii_video
  --coco
  --lsp
  --flic
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
