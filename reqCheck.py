import os
import subprocess
import logging
from logger import log
from javaCheck import isJavaInstalled
from systemData import HOME
from fileOperations import appendToFile


log.setLevel(logging.DEBUG)

BASHRC_PATH = os.path.join(HOME, '.bashrc')

def pdsh_rcmd():
    result = subprocess.run(["pdsh -q -w localhost"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout = result.stdout.decode()

    lines = stdout.split('\n')

    cmd = 'export PDSH_RCMD_TYPE=ssh'
    for line in lines:
        if 'Rcmd' in line:
            shell = line.strip().split()[-1]
            if shell!='ssh':
                log.error("Your pdsh default rcmd is not ssh.")
                log.error(f"To resolve this, add following line to {BASHRC_PATH} file : {cmd}")
                raise ValueError(f"Your pdsh default rcmd is not ssh.\nTo resolve this, add following line to {BASHRC_PATH} file : {cmd}")
    log.debug("pdsh rcmd type is set to ssh")
    return True


def checkOther(soft='ssh'):
    log.info(f"Checking for {soft}.")
    result = subprocess.run([f"{soft} -V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout = result.stdout.decode()
    stderr = result.stderr.decode()

    log.debug(f"stdout : {stdout}")
    log.debug(f"stderr : {stderr}")

    if 'not' in stderr or 'not' in stdout:
        log.error(f"{soft} is not installed.")
        log.error(f"To install {soft} using apt package manager, run the following command : ")
        if soft=='ssh':
            log.error(f"$ sudo apt-get install openssh-client openssh-server")
        else:
            log.error(f"$ sudo apt-get install {soft}")
        return False
    return True


def reqCheck():
    if isJavaInstalled() and checkOther(soft="ssh") and checkOther(soft='pdsh') and pdsh_rcmd():
        log.info("Required softwares are installed.")
        return True
    raise ValueError("Required softwares are not correctly installed. See logs for more details.")

if __name__ == "__main__":
    reqCheck()