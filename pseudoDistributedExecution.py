import os
import logging
import shutil
import subprocess

from logger import log
from hadoopInstall import HADOOP_HOME, HADOOP_NAME
from systemData import USER
from fileOperations import writeToFile, appendToFile


log.setLevel(logging.DEBUG)

HADOOP_EXECUTABLE = os.path.join(HADOOP_HOME, 'bin/hadoop') 
HDFS_EXECUTABLE  = os.path.join(HADOOP_HOME, 'bin/hdfs')
MAPRED_EXECUTABLE = os.path.join(HADOOP_HOME, 'bin/mapred')

START_DFS = os.path.join(HADOOP_HOME, 'sbin/start-dfs.sh')
STOP_DFS = os.path.join(HADOOP_HOME, 'sbin/stop-dfs.sh')

CWD = os.getcwd()

INPUT_PATH = os.path.join(CWD, 'texts')
MAPPER_PATH = os.path.join(CWD, 'word_count', 'mapper.py')
REDUCER_PATH = os.path.join(CWD, 'word_count', 'reducer.py')
OUTPUT_DIR = os.path.join(CWD, 'output')
OUTPUT_FILE_PATH = os.path.join(CWD, 'output.txt')

MAPRED_OUTPUT_FILE_PATH = os.path.join(CWD, 'mapredOutput.txt')
MAPRED_OUTPUT_ERROR_FILE_PATH = os.path.join(CWD, 'mapredError.txt')

def runCommand(command, skipError=False):
    log.debug(f"Running command : {command}")

    result = subprocess.run([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)  
    stderr = result.stderr.decode()
    stdout = result.stdout.decode()

    if stderr.strip() is not '' and not skipError:
        raise ValueError(stderr)

    return (stdout, stderr)



def execute():
    # os.system(f"{HDFS_EXECUTABLE} namenode -format")
    # os.system(f"{START_DFS}")
    # log.info("Browse the web interface for the NameNode; by default it is available at: NameNode - http://localhost:9870")
    # print("Browse the web interface for the NameNode; by default it is available at: NameNode - http://localhost:9870")
    # os.system(f"{HDFS_EXECUTABLE} dfs -mkdir /user")
    # os.system(f"{HDFS_EXECUTABLE} dfs -mkdir /user/{USER}")
    # os.system(f"{HDFS_EXECUTABLE} dfs -mkdir input")


    runCommand(f"echo Y | {HDFS_EXECUTABLE} namenode -format", skipError=True)
    runCommand(f"{START_DFS}")
    log.info("Browse the web interface for the NameNode; by default it is available at: NameNode - http://localhost:9870")
    print("Browse the web interface for the NameNode; by default it is available at: NameNode - http://localhost:9870")
    runCommand(f"{HDFS_EXECUTABLE} dfs -mkdir /user")
    runCommand(f"{HDFS_EXECUTABLE} dfs -mkdir /user/{USER}")
    runCommand(f"{HDFS_EXECUTABLE} dfs -mkdir input")

    word_count()
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    
    if os.path.exists(OUTPUT_FILE_PATH):
        os.remove(OUTPUT_FILE_PATH)

    runCommand(f"{HDFS_EXECUTABLE} dfs -get output {OUTPUT_DIR}", skipError=True)
    runCommand(f"cat output/* > {OUTPUT_FILE_PATH}")
    runCommand(f"{STOP_DFS}",skipError=True)

def runExample():
    example_path = os.path.join(HADOOP_HOME, 'share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar')
    print(f"{HADOOP_EXECUTABLE} jar {example_path} grep input output 'dfs[a-z.]+'")

def word_count(REDUCES  = 4):
    os.system(f"{HDFS_EXECUTABLE} dfs -put {INPUT_PATH}/* input")
    log.debug(f"Adding executable permissions to mapper file:  {MAPPER_PATH}")
    os.system(f"chmod +x {MAPPER_PATH}")
    log.debug(f"Adding executable permissions to reducer file:  {REDUCER_PATH}")
    os.system(f"chmod +x {REDUCER_PATH}")
    
    WORD_COUNT_COMMAND  = f"{MAPRED_EXECUTABLE} streaming  " +  \
                          f"-D mapreduce.job.reduces={REDUCES}  " + \
                          "-input input  " +\
                          "-output output  " +  \
                          f"-mapper {MAPPER_PATH}  " + \
                          f"-reducer  {REDUCER_PATH}"
    
    log.debug('Executing Word Count Map Reduce command.')
    result = subprocess.run([WORD_COUNT_COMMAND], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)  
    stderr = result.stderr.decode()
    stdout = result.stdout.decode()

    if stderr.strip() is not '':
        log.info(f"stdout:\n{stdout}")
        log.info(f"stderr:\n{stderr}")

    writeToFile(stdout, MAPRED_OUTPUT_FILE_PATH)
    appendToFile(stderr, MAPRED_OUTPUT_FILE_PATH)
    log.info(f"Output of mapreduce step saved to {MAPRED_OUTPUT_FILE_PATH}.")




def executePseudoDistributedOperation():
    log.warning('If this job fails make sure you empty the /tmp folder, or run command : sudo rm -R /tmp/* . And run the program again.')
    log.info('Executing Pseudo-Distributed Operation')
    execute()

def executeWordCount():
    log.info('Executing WordCount program.')
    log.warning('If this job fails make sure you empty the /tmp folder, or run command : sudo rm -R /tmp/* . And run the program again.')
    execute()

if __name__ == '__main__':
    # executePseudoDistributedOperation()
    execute()
    