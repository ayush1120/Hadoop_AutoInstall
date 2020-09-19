import os

from systemData import HOME
from fileOperations import check_files, check_file
import logging
from logger import log

log.setLevel(logging.DEBUG)

SSH_DIR = os.path.join(HOME, '.ssh')
ID_RSA_PATH = os.path.join(SSH_DIR, 'id_rsa')
ID_RSA_PUB_PATH = os.path.join(SSH_DIR, 'id_rsa.pub')
AUTHORIZED_KEYS_PATH = os.path.join(SSH_DIR, 'authorized_keys')




def setup():
    if check_files([SSH_DIR, ID_RSA_PATH, ID_RSA_PUB_PATH, AUTHORIZED_KEYS_PATH]):
        a = input('Passphraseless SSH seems to be already setup.\n' + \
                   "Type 'ssh localhost' in a terminal if you are not required to enter password. Select No (n)" + \
                   "Selecting 'y' will overwrite the existing keys."
                   "Setup Again (y/n): ")
        if a != 'y':
            return
        else:
            log.info("Forcing keys overwrite.")
    
    log.info(f"ID_RSA_PATH : {ID_RSA_PATH}")
    log.info(f"ID_RSA_PUB_PATH : {ID_RSA_PUB_PATH}")
    log.info(f"AUTHORIZED_KEYS_PATH : {AUTHORIZED_KEYS_PATH}")


    if os.path.exists(ID_RSA_PATH):
        os.remove(ID_RSA_PATH)
    if os.path.exists(ID_RSA_PUB_PATH):
        os.remove(ID_RSA_PUB_PATH)
    if os.path.exists(AUTHORIZED_KEYS_PATH):
        os.remove(AUTHORIZED_KEYS_PATH)


    os.system(f"ssh-keygen -t rsa -P '' -f {ID_RSA_PATH}")
    os.system(f"cat {ID_RSA_PUB_PATH} >> {AUTHORIZED_KEYS_PATH}")
    os.system(f"chmod 0600 {AUTHORIZED_KEYS_PATH}")



def setupPassphraseLessSSH():
    setup()

if __name__ == '__main__':
    setupPassphraseLessSSH()
    