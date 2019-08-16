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

def download_coco(config=None):
    image_urls = ['http://images.cocodataset.org/zips/train2017.zip', 'http://images.cocodataset.org/zips/val2017.zip', 'http://images.cocodataset.org/zips/test2017.zip']
    annotation_urls = ['http://images.cocodataset.org/annotations/image_info_test2017.zip', 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip']
    dl_path = './coco/'
    download_files(image_urls, dl_path, config.overwrite, config.verbosity)
    download_files(annotation_urls, dl_path, config.overwrite, config.verbosity)
    unzip_all_files_in_directory(dl_path, config.overwrite, config.verbosity)

def download_lsp(config=None):
    dl_path = './lsp/'
    download_url = ['http://sam.johnson.io/research/lsp_dataset_original.zip']
    download_files(download_url, dl_path, config.overwrite, config.verbosity)
    unzip_all_files_in_directory(dl_path, config.overwrite, config.verbosity)

def download_flic(config=None):
    dl_path = './flic/'
    download_file_from_google_drive('0B4K3PZp8xXDJN0Fpb0piVjQ3Y3M', dl_path, 'flic.zip', config.verbosity)
    download_file_from_google_drive('0B4K3PZp8xXDJd2VwblhhOVBfMDg', dl_path, 'flic_full.zip', config.verbosity)
    unzip_all_files_in_directory(dl_path, config.overwrite, config.verbosity)

def download_ai_challenger(config=None):
    dl_path = './ai_challenger/'
    download_file_from_google_drive('1zahjQWhuKIYWRRI2ZlHzn65Ug_jIiC4l', dl_path, 'ai_challenger.tar.gz', config.verbosity)
    ungzip_all_files_in_directory(dl_path, config.overwrite, config.verbosity)

def main(config):
    if(config.mpii):
        download_mpii(config)
    if(config.coco):
        download_coco(config)
    if(config.lsp):
        download_lsp(config)
    if(config.flic):
        download_flic(config)
    if(config.aichallenger):
        download_ai_challenger(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mpii', action='store_true')
    parser.add_argument('--mpii_video', action='store_true')
    parser.add_argument('--coco', action='store_true')
    parser.add_argument('--lsp', action='store_true')
    parser.add_argument('--flic', action='store_true')
    parser.add_argument('--aichallenger', action='store_true')
    parser.add_argument('--overwrite', action='store_true')
    parser.add_argument('-v', '--verbosity', action='store_true')
    config = parser.parse_args()
    main(config)