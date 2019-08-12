import argparse
from dl_util import *

def download_mpii(config=None):
    image_url = ['https://datasets.d2.mpi-inf.mpg.de/andriluka14cvpr/mpii_human_pose_v1.tar.gz']
    annotation_url = ['https://datasets.d2.mpi-inf.mpg.de/andriluka14cvpr/mpii_human_pose_v1_u12_2.zip']
    video_urls = ['https://datasets.d2.mpi-inf.mpg.de/andriluka14cvpr/mpii_human_pose_v1_sequences_batch%d.tar.gz' % (idx+1) for idx in range(25)]
    video_image_map_url = ['https://datasets.d2.mpi-inf.mpg.de/andriluka14cvpr/mpii_human_pose_v1_sequences_keyframes.mat']
    dl_path = './mpii/'
    download_files(image_url, dl_path, config.overwrite, config.verbosity)
    download_files(annotation_url, dl_path, config.overwrite, config.verbosity)
    unzip_all_files_in_directory(dl_path, config.overwrite, config.verbosity)
    ungzip_all_files_in_directory(dl_path, config.overwrite, config.verbosity)

def download_coco(config_None):
    image_urls = ['http://images.cocodataset.org/zips/train2017.zip', 'http://images.cocodataset.org/zips/val2017.zip', 'http://images.cocodataset.org/zips/test2017.zip']
    annotation_urls = ['http://images.cocodataset.org/annotations/image_info_test2017.zip', 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip']
    dl_path = './coco/'
    download_files(image_urls, dl_path, config.overwrite, config.verbosity)
    download_files(annotation_urls, dl_path, config.overwrite, config.verbosity)
    unzip_all_files_in_directory(dl_path, config.overwrite, config.verbosity)

def main(config):
    if(config.mpii):
        download_mpii(config)
    if(config.coco):
        download_coco(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mpii', action='store_true')
    parser.add_argument('--mpii_video', action='store_true')
    parser.add_argument('--coco', action='store_true')
    parser.add_argument('--overwrite', action='store_true')
    parser.add_argument('-v', '--verbosity', action='store_true')
    config = parser.parse_args()
    main(config)