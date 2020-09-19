import os 
import shutil
import logging

from logger import log
from hadoopInstall import HADOOP_HOME

INPUT_DIR = os.path.join(os.getcwd(), 'input')

def standaloneOperation():
    log.debug("Executing Function standaloneOperation.")

    if os.path.exists(INPUT_DIR):
        log.debug(f"{INPUT_DIR}, already exists.")
        log.debug(f"Removing, {INPUT_DIR}")
        shutil.rmtree(INPUT_DIR)

    os.mkdir(INPUT_DIR)
    os.system(f'cp {HADOOP_HOME}/etc/hadoop/*.xml  {INPUT_DIR}')
    os.system(f"{HADOOP_HOME}/bin/hadoop jar {HADOOP_HOME}/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar grep input output 'dfs[a-z.]+'")
    os.system(f"cat {os.getcwd()}/output/*")
    

if __name__ == "__main__":
    standaloneOperation()