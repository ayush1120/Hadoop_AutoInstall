import os
import logging
import shutil
from logger import  log
from distutils.dir_util import  copy_tree
from hadoopInstall import HADOOP_HOME, HADOOP_ROOT, HADOOP_NAME

from fileOperations import readFile, writeToFile, appendToFile
from backupFile import restoreFile


BACKUP_PATH = os.path.join(os.getcwd(), 'backup', HADOOP_NAME)
HADOOP_ENV_PATH = os.path.join(HADOOP_HOME, 'etc', 'hadoop', 'hadoop-env.sh')
JAVA_HOME = os.environ["JAVA_HOME"]
BACKUP_DIR = os.path.join(HADOOP_HOME, "backup")



def configure():
    restoreFile(HADOOP_ENV_PATH)
    javaHomeData = "# set to the root of your Java installation\n" + f"export JAVA_HOME={JAVA_HOME}"
    log.debug(f"Adding Following Line to {HADOOP_ENV_PATH}\n{javaHomeData}")
    appendToFile(javaHomeData, HADOOP_ENV_PATH)
    line2 = '\n\nexport HADOOP_OPTS="--add-modules java.activation"'
    log.debug(f"Adding Following Line to {HADOOP_ENV_PATH}\n{line2}")
    appendToFile(line2, HADOOP_ENV_PATH)
    


if __name__ == "__main__":
    configure()