import os
import subprocess
# from logger import log
import logging
from logger import log

log.setLevel(logging.INFO)

# Check for version is remaining
def checkJREVersion(output):
    version = output.split('"')[1]
    if 'OpenJDK' in output:
        log.debug(f"OpenJDK Runtime Environment Version : {version}")
        version = int(version.strip().split('.')[0])
        if version>7 and version<=11:
            return True
        log.error("JRE version is not supported.")
        return False

    log.debug(f"Java Version : {version}")
    version = int(version.strip().split('.')[1])
    if version>7 and version<=11:
        return True
    log.error("JRE version is not supported.")
    return False
    


def jreIsInstalled():
    log.info("Checking for JRE.")
    log.debug("On running command 'java -version' the output messege is thrown to stderr, whether java is installed or not.")
    result = subprocess.run(["java -version"], stderr=subprocess.PIPE, shell=True)
    stderr = result.stderr.decode()
    log.debug(f'java -version  : {stderr}')
    if 'not' in stderr:
        log.error("JRE installation not found.")
        return False
    if checkJREVersion(stderr):
        return True   
    return False



def checkJDKVersion(output):
    version = output.strip().split(' ')[1]
    versionBreakDown = version.split('.')

    if int(versionBreakDown[0]) > 1 :
        v = int(versionBreakDown[0])
        log.debug(f"OpenJDK Version : {version}")
        if v>7:
            return True
        log.error('OpenJDK version not supported.')
        return False
    
    v =  versionBreakDown[1]
    log.debug(f"JDK Version : {version}")
    if v>7:
        return True
    log.error('JDK version not supported.')
    return False




def jdkIsInstalled():
    # Check if path JAVA_HOME is configured
    log.info("Checking for JDK.")

    msg = "Make Sure JDK (v1.8.x to v1.10.x) or OpenJDK (version > 7) is installed and Environment Variables are set up properly."

    if 'JAVA_HOME' not in os.environ.keys():
        log.error("JAVA_HOME Environment Variable is not set. \n" + msg)
        return False

    JAVA_HOME =  os.path.join( os.environ["JAVA_HOME"] )
    log.info(f'JAVA_HOME : {JAVA_HOME}')

    if not os.path.exists(JAVA_HOME):
        log.error("JAVA_HOME directory does not exist. \n" + msg)
        return False

    javac_path = os.path.join(JAVA_HOME, 'bin', 'javac')
    log.debug(f"javac Path : {javac_path}")

    if not os.path.exists(javac_path):
        log.error(f"Cannot locate javac at {JAVA_HOME}/bin/javac.\n" + msg)
        return False

    result = subprocess.run(["javac -version"], stderr=subprocess.PIPE, stdout=subprocess.PIPE,  shell=True)
    stderr = result.stderr.decode()    
    if stderr is '':
        stderr = result.stdout.decode()

    log.debug(f"javac -version : {stderr}")

    if 'not' in stderr:
        log.error("JDK installation not found.")
        log.error(msg)
        return False
    if checkJDKVersion(stderr):
        return True   
    log.error(msg)
    return False


def isJavaInstalled():
    if not jreIsInstalled():
        log.error("Java Runtime Environment installation missing. Please Install JRE & ensure if you have the correct version (1.8.x or 1.7.x).\n" + \
            "Use command 'java -version' to check version of jre.")
        return False
    
    if not jdkIsInstalled():
        log.error("JDK is either not installed or configured correctly. Please Install & Configure JDK 1.8.x.x+." + \
            "\nSee logs for more details." )
        
        return False
    
    log.debug("JRE & JDK are installed correctly.")
    log.info("Java is working propely.")

    return True


if __name__ == "__main__":
    isJavaInstalled()