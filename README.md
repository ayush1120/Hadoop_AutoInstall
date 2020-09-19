---
# HADOOP AutoInstall & Word Count Example
######  Author: Ayush Sharma
---

  - Requires python 3.5.x or newer version.
  - For reference, **PROJECT_DIR** is directory which contains **main.py** file.
  - **To Stop the script from downloading hadoop, download & place hadoop-3.2.1.tar.gz in PROJECT_DIR**

## Before Installation
**Please make sure of the following:** 
 - Script is for linux OS only **(TESTED on Ubuntu 18.04.4 LTS)** 
 - Java (jdk) is installed version 8 or newer. **(If not found script will through error)** **(TESTED on open-jdk 9 open-jdk 10 & oracle-jdk 10).**
 (For installing jdk from  **[jdk_x.x.x.tar.gz](https://jdk.java.net/archive/)** file, instructions are given in **Java_Install_Instruction.txt**)
 - JAVA_HOME is set in environment variables & should be pointing to jdk . **(If not found script will through error)**.
 - **ssh** & **pdsh** are installed and working correctly.. **(If not found script will through error)**
    - If the current installation of ssh is not working install using the following command, 
        ```sh
        $ sudo apt-get install openssh-client openssh-server
        ```
    - Make sure the following line is added in your .bashrc file at /home/user/.bashrc (Replace user with your username)
         ```sh
         # Set pdsh rcmd type to ssh
        export PDSH_RCMD_TYPE=ssh
        ```
        And source your .bashrc file.
         ```sh
        $ source home/user/.bashrc
        ```
 - **Make sure no process is using PORT 9870.**
    - To list processes using port 9870
        ```sh
        $ sudo lsof -i :9870
        ```
    - If process are there, kill them using following command - 
        ```sh
        $ kill -9 <pid>
        ```
 - If you have run a hadoop exectuable recently or if the program fails, clear your root tmp directory via following command and try running the script again. 
    ```sh
        $ sudo rm -R /tmp/*
    ```
 - Make sure you have packages installed in your python environment which are listed in requirements.txt. Or install using following command.
    ```sh
        $ pip install -r PROJECT_DIR/requirements.txt
    ```

## Installation
 - Change your directory to PROJECT_DIR 
    ```sh
        $ cd PROJECT_DIR
    ```
 - Run main.py file
    ```sh
        $ python main.py
    ```


## Results

- Output of word count is saved in the file output.txt in PROJECT_DIR
- pyLog.log contains all the logs.
- Output of map reduce command (using hadoop:  mapred straming ) is stored in mapretOutput.txt 


### File Structure 
| File |  Objective |
| ------ | ------ |
| requirements.txt | List python packages required. | 
| logger.py| Initializes the logger | 
| systemData.py | It stores system variables like HOME directory.|
| fileOperations.py | Functions for easy access to file IO operation |
| javaCheck.py | This file checks if java is installed correctly and if JAVA_HOME is configured in the environment or not.|
| reqCheck.py  | Check All Requirements (Calls function from javaCheck) and also checks if ssh and pdsh are installed or not. |
| passphraselessSSH.py | Sets up passphraseless ssh. |
| hadoopInstall.py | Downloads and extract Hadoop 3.2.1. Provides variable: HADOOP_HOME|
| configureHadoop.py | Adds line “export JAVA_HOME={JAVA_HOME}” & "export HADOOP_OPTS="--add-modules java.activation" to /etc/hadoop/hadoop-env.sh.|
| standalone.py | Runs the standalone operation |
| backupFile.py | Provides function for backup and restore of config file in case of rerun. |
| pyLog.log | Debug Log File  |
| pseudoDistributedConfig.py | Configure hadoop for pseudo Distributed Operations. |
| pseudoDistributedExecution.py | Contains code for **word count map reduce function.** |
| word_count/mapper.py | Python script, mapper for map reduce word count program. |
| word_count/reducer.py | Python script, reducer for map reduce word count program. |
| texts | This directory contains texts file for word count. |
| main.py | Import from all the above files and runs them in sequence. |
