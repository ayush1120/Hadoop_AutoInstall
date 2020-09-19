import os
import shutil 

from logger import log
from hadoopInstall import HADOOP_HOME, HADOOP_NAME, HADOOP_ROOT


BACKUP_DIR = os.path.join(HADOOP_HOME, "backup")

def backupFile(filePath):
    if not os.path.exists(filePath):
        log.critical("FILE NOT FOUND : {filePath}")
        return

    filename = os.path.basename(filePath)
    src = filePath

    if not os.path.exists(BACKUP_DIR):
        log.info
        os.mkdir(BACKUP_DIR)
    
    dst = filePath.replace(HADOOP_HOME, BACKUP_DIR)  
    dstFolder = os.path.dirname(dst)
    if not os.path.exists(dst):
        log.info("Intializing Backup for {filename}")
        if not os.path.exists(dstFolder):
            log.debug(f"Creating Directory Tree {dstFolder}")
            os.makedirs(dstFolder)
        shutil.copy(src, dst)
        log.debug(f"Successfully Copied {src} to {dstFolder}.")
        log.info(f"Backup Created for {filename}.")
        return
    log.debug(f"Backup Already Found for {filename}.")

def restoreFile(filePath):
    filename = os.path.basename(filePath)
    src = filePath.replace(HADOOP_HOME, BACKUP_DIR)
    
    if not os.path.exists(src):
        log.info(f"BACKUP NOT FOUND FOR: {filename}.")
        log.info(f"CHANGES WILL BE MADE ON EXISTING VERSION.")
        log.info(f"Creating Backup for {filename}.")
        backupFile(filePath)
        return
    
    log.info(f"Backup Found for {filename} at: {src}.")
    log.info(f"Restoring {filename} from backup.")
    shutil.copyfile(src, filePath)
    log.info(f"{filename} Restored.")