import os
import subprocess
import logging
from tqdm import tqdm
import requests
# import tarfile
import shutil

from logger import log
from systemData import HOME


log.setLevel(logging.DEBUG)

HADOOP_NAME =  'hadoop-3.2.1'
HADOOP_ROOT = os.path.join(HOME, 'hadoop')
HADOOP_HOME = os.path.join(HADOOP_ROOT, HADOOP_NAME)

def bar_custom(current, total, width=80):
    print("Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total))


def downloadHadoop(reDownload=True, filename = 'hadoop-3.2.1.tar.gz', 
    url = 'http://apachemirror.wuchna.com/hadoop/common/stable/hadoop-3.2.1.tar.gz'):

    log.debug("Executing Function downloadHadoop.")

    filepath = os.path.join(os.getcwd(), filename)
    if(os.path.exists(filepath)) & reDownload:
        os.remove(filepath)
    if  os.path.exists(filepath):
        log.info(f"{filename} is already downloaded.")
        return filepath

    response = requests.get(url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(filepath, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        log.error("Downloading ERROR  | Something went wrong.")
        if os.path.exists(filepath):
            log.error("Removing downloaded file.")
            os.remove(filepath)
        return None
    
    return filepath    


def extractHadoop(filepath, DEBUG=True):
    log.debug("Executing Function extractHadoop.")

    if not os.path.exists(filepath):
        log.error('File Not Found')
        return

    if not os.path.exists(HADOOP_ROOT):
        os.mkdir(HADOOP_ROOT)
    
    if not DEBUG:
        if os.path.exists(HADOOP_HOME):
            shutil.rmtree(HADOOP_HOME)

        log.info('Unpacking Archive ...')
        shutil.unpack_archive(filepath, HADOOP_ROOT)

    log.info('Unpacked.')
    log.info(f"{HADOOP_NAME} is extracted to {HADOOP_ROOT}")



if __name__ == "__main__":
    filepath = downloadHadoop(reDownload=False)
    extractHadoop(filepath)
