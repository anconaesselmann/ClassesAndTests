"""
@author Axel Ancona Esselmann

"""
import os
import sys

DEBUG = True

class FileManipulator():
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
        FileManipulator.createFolder(filePath)
        if not os.path.exists(filePath):
            newFile = open(filePath, "wb")
            if sys.version_info >= (3, 0):
                newFile.write(str.encode(content));
            else:
                newFile.write(content);
            newFile.close()
            if DEBUG: print("FileManipulator: Created file " + filePath)
            return True
        else:
            if DEBUG: print("FileManipulator: File " + filePath + " exists.")
        return False

    @staticmethod
    def createFolder(aPath):
        folder, extension = os.path.splitext(aPath)
        if extension != "":
        	folder = os.path.dirname(folder)
        if not os.path.isdir(folder):
            if DEBUG: print("FileManipulator: Created folder " + folder)
            os.makedirs(folder)

    @staticmethod
    def isdir(aPath):
        return os.path.isdir(aPath)

    @staticmethod
    def isfile(aPath):
        return os.path.isfile(aPath)