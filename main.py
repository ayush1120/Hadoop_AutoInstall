import os
import sys
from logger import log
from reqCheck import reqCheck
from hadoopInstall import downloadHadoop, extractHadoop
from configureHadoop import configure
from standalone import standaloneOperation
from pseudoDistributedConfig import psedudoDistributedConfiguration
from pseudoDistributedExecution import executePseudoDistributedOperation, executeWordCount

DEBUG = True

if __name__ == "__main__":
    if not reqCheck():
        sys.exit()
    filepath = downloadHadoop(reDownload=False)
    extractHadoop(filepath, DEBUG=DEBUG)
    configure()
    psedudoDistributedConfiguration()
    executeWordCount()
    log.info("Check output.txt for word count results.")
    # executePseudoDistributedOperation()
    # standaloneOperation()