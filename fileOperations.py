import os
from logger import log


def check_file(filePath):
    if not os.path.exists(filePath):
        return False
    return True


def check_files(files):
    for filePath in files:
        if not check_file(filePath):
            return False
    return True


def readFile(filepath):
    if not os.path.exists(filepath):
        log.error(f"File Not Found at {filepath}.")
        return
    with open(filepath, 'r') as fp:
        data = fp.readlines()
    print(f"Data at {filepath} : \n{data}")



def writeToFile(data, filepath):
    with open(filepath, 'w') as fp:
        fp.write(data)


def appendToFile(lines, filepath):
    with open(filepath, 'a') as fp:
        for line in lines:
            fp.write(line)