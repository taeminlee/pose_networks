import urllib
import urllib.request
import os
import zipfile
import tarfile
from tqdm import tqdm

def printv(msg, verbosity):
    if(verbosity):
        print(msg)

class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""
    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_file(url, path, overwrite=False, verbosity=True):
    if (not os.path.exists(path) or overwrite):
        if (not os.path.exists(os.path.dirname(path))):
            os.makedirs(os.path.dirname(path))
        if(verbosity):
            with TqdmUpTo(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
                urllib.request.urlretrieve(url, filename=path, reporthook=t.update_to)
                printv("downloaded {} from {}".format(path, url), verbosity)
        else:
            urllib.request.urlretrieve(url, filename=path)
    else:
        printv("Skipping download ... {} already exists".format(path), verbosity)

def download_files(urls, dir_path, overwrite=False, verbosity=True):
    for url in urls:
        filename = url.split('/')[-1]
        download_file(url, os.path.join(dir_path, filename), overwrite, verbosity)

def extract_all_files_in_directory(dir_path, extension, f_ref, f_iter, f_name, overwrite=False, verbosity=True):
    for item in os.listdir(dir_path): # loop through items in dir
        item = os.path.join(dir_path, item)
        if item.endswith(extension): # check for ".zip" extension
            printv("unzipping {} ...".format(item), verbosity)
            file_name = os.path.abspath(item) # get full path of files
            ref = f_ref(file_name) # create zipfile object
            files = f_iter(ref)
            if(verbosity):
                files = tqdm(iterable=f_iter(ref), total=len(f_iter(ref)))
            for file in files:
                if (not os.path.exists(os.path.join(dir_path,f_name(file))) or overwrite):
                    ref.extract(member=file, path=dir_path) # extract file to dir
                else:
                    printv("Skipping unzipping ... {} already exists".format(file), verbosity)
            ref.close() # close file
            printv("finished unzipping {} ...".format(item), verbosity)

def unzip_all_files_in_directory(dir_path, overwrite=False, verbosity=True):
    extension = ".zip"
    f_ref = lambda file_name : zipfile.ZipFile(file_name)
    f_iter = lambda ref: ref.namelist()
    f_name = lambda file: file
    extract_all_files_in_directory(dir_path, extension, f_ref, f_iter, f_name, overwrite, verbosity)

def ungzip_all_files_in_directory(dir_path, overwrite=False, verbosity=True):
    extension = ".tar.gz"
    f_ref = lambda file_name : tarfile.open(file_name, "r:gz")
    f_iter = lambda ref: ref.getmembers()
    f_name = lambda file: file.name
    extract_all_files_in_directory(dir_path, extension, f_ref, f_iter, f_name, overwrite, verbosity)