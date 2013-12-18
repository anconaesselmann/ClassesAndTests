"""
@author Axel Ancona Esselmann

"""
DEBUG = False


import os
import sys
import inspect
import re

class FileSystem():
    def __init__(self):
        pass

    @staticmethod
    def getFileContent(fileDir):
        fileHandle = open(fileDir, 'r')
        content = fileHandle.read()
        fileHandle.close()
        return content

    @staticmethod
    def createFile(filePath, content):
        FileSystem.createFolder(filePath)
        if not os.path.exists(filePath):
            newFile = open(filePath, "wb")
            if sys.version_info >= (3, 0):
                newFile.write(str.encode(content));
            else:
                newFile.write(content);
            newFile.close()
            if DEBUG: print("FileSystem: Created file " + filePath)
            return True
        else:
            if DEBUG: print("FileSystem: File " + filePath + " exists.")
        return False

    @staticmethod
    def replaceFile(fileDir, content):
        if os.path.isfile(fileDir):
            os.remove(fileDir)
        return FileSystem.createFile(fileDir, content)

    @staticmethod
    def createFolder(aPath):
        folder, extension = os.path.splitext(aPath)
        if extension != "":
        	folder = os.path.dirname(folder)
        if not os.path.isdir(folder):
            if DEBUG: print("FileSystem: Created folder " + folder)
            os.makedirs(folder)

    @staticmethod
    def isdir(aPath):
        return os.path.isdir(aPath)

    @staticmethod
    def isfile(aPath):
        return os.path.isfile(aPath)

    @staticmethod
    def remove(aPath):
        return os.path.remove(aPath)

    @staticmethod
    def getExecutingFileName():
        return inspect.stack()[-1][1]

    @staticmethod
    def _getTestDataFileName(executedFile, fileName):
        temp, tempClassName = os.path.split(executedFile)
        tempClassName, ext = os.path.splitext(tempClassName)
        regExpString = '(?:___liveUnitTesting_)([\w\d]+)'
        result = re.findall(regExpString, tempClassName)
        if len(result) > 0:
            className = result[0]
        else:
            className = tempClassName
        testDataDirectoryName = className + "Data"
        #print(testDataDirectoryName)
        directory = os.path.dirname(executedFile)
        dataFile = os.path.join(directory, testDataDirectoryName, fileName)
        return dataFile

    @staticmethod
    def getFileContentFromTestDataFile(fileName):
        executedFile = FileSystem.getExecutingFileName()
        dataFile = FileSystem._getTestDataFileName(executedFile, fileName)
        fileContent = FileSystem.getFileContent(dataFile)
        return fileContent
