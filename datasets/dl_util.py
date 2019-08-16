import requests
import os
import zipfile
import tarfile
from tqdm import tqdm
import requests
import math

def writev(f, chunks, chunk_size, pbar, verbosity):
    for chunk in chunks:
        if chunk:
            f.write(chunk)
            if(verbosity):
                pbar.update(chunk_size)

def printv(msg, verbosity):
    if(verbosity):
        print(msg)
                

def download(url, dst, verbosity=True):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    file_size = int(requests.head(url).headers["Content-Length"])
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1])
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        writev(f, req.iter_content(chunk_size=32768), 32768, pbar, verbosity)
    pbar.close()
    return file_size


def download_file_from_google_drive(id, path, filename, verbosity):
    URL = "https://docs.google.com/uc?export=download"
    CHUNK_SIZE = 32768
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
        make_directory(path)
        pbar = tqdm(unit='B', unit_scale=True, desc=filename)
        with open(os.path.join(path, filename), "wb") as f:
            writev(f, response.iter_content(chunk_size=CHUNK_SIZE), CHUNK_SIZE, pbar, verbosity) 
        pbar.close()

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def make_directory(path):
    if (not os.path.exists(os.path.dirname(path))):
        os.makedirs(os.path.dirname(path))

def download_file(url, path, overwrite=False, verbosity=True, resume=True):
    if (not os.path.exists(path) or overwrite or resume):
        make_directory(path)
        if(overwrite):
            os.remove(path)
        if(verbosity):
            download(url, path, verbosity)
            printv("downloaded {} from {}".format(path, url), verbosity)
        else:
            download(url, path, verbosity)
    else:
        printv("Skipping download ... {} already exists".format(path), verbosity)

def download_files(urls, dir_path, overwrite=False, verbosity=True, resume=True):
    for url in urls:
        filename = url.split('/')[-1]
        download_file(url, os.path.join(dir_path, filename), overwrite, verbosity, resume)

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
