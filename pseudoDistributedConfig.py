import os
import errno
from xml.dom import minidom

from logger import log
from hadoopInstall import HADOOP_HOME
from backupFile import restoreFile
from fileOperations import readFile



CORE_SITE_XML_PATH = os.path.join(HADOOP_HOME, 'etc', 'hadoop', 'core-site.xml')
HDFS_SITE_XML_PATH = os.path.join(HADOOP_HOME, 'etc', 'hadoop', 'hdfs-site.xml')




def configureCoreSiteXML():

    if not os.path.exists(CORE_SITE_XML_PATH):
        filename = os.path.basename(CORE_SITE_XML_PATH)
        log.critical(f"File not found: {CORE_SITE_XML_PATH}")
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    restoreFile(CORE_SITE_XML_PATH)

    filename = os.path.basename(CORE_SITE_XML_PATH)
    log.info(f"Configuring {filename}")

    doc = minidom.parse(CORE_SITE_XML_PATH)
    configurationElement = doc.getElementsByTagName('configuration')[0]
    propertyElement = doc.createElement('property')
    
    nameElement = doc.createElement("name")
    nameElementData = doc.createTextNode('fs.defaultFS')
    nameElement.appendChild(nameElementData)

    valueElement = doc.createElement("value")
    valueElementData =  doc.createTextNode('hdfs://localhost:9000')  
    valueElement.appendChild(valueElementData)

    propertyElement.appendChild(nameElement)
    propertyElement.appendChild(valueElement)

    configurationElement.appendChild(propertyElement)

    with open(CORE_SITE_XML_PATH, 'w') as fp: 
        fp.write(doc.toprettyxml())

    log.info(f"{filename} configuration done.")


"""
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
"""

def configureHdfsSiteXML():
    if not os.path.exists(HDFS_SITE_XML_PATH):
        filename = os.path.basename(HDFS_SITE_XML_PATH)
        log.critical(f"File not found: {HDFS_SITE_XML_PATH}")
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    restoreFile(HDFS_SITE_XML_PATH)
    filename = os.path.basename(HDFS_SITE_XML_PATH)
    
    log.info(f"Configuring {filename}")
    
    doc = minidom.parse(HDFS_SITE_XML_PATH)
    
    configurationElement = doc.getElementsByTagName('configuration')[0]
    propertyElement = doc.createElement('property')
    
    nameElement = doc.createElement("name")
    nameElementData = doc.createTextNode('dfs.replication')
    nameElement.appendChild(nameElementData)

    valueElement = doc.createElement("value")
    valueElementData =  doc.createTextNode('1')  
    valueElement.appendChild(valueElementData)

    propertyElement.appendChild(nameElement)
    propertyElement.appendChild(valueElement)

    configurationElement.appendChild(propertyElement)

    with open(HDFS_SITE_XML_PATH, 'w') as fp: 
        fp.write(doc.toprettyxml())

    log.info(f"{filename} configuration done.")

def psedudoDistributedConfiguration():
    configureCoreSiteXML()
    configureHdfsSiteXML()

if __name__ == '__main__':
    psedudoDistributedConfiguration()