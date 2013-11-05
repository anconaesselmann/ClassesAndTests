"""
@author Axel Ancona Esselmann

"""
import os
import sys

try:
    from .Std import Std
except ImportError:
    from ..Std import Std

DEBUG = True

class MockFileManipulator():
    def __init__(self):
        self._mockedFileContent = dict()
        self._createdFiles = dict()
    
    def getFileContent(self, filePath):
        if filePath in self._createdFiles:
            return self._createdFiles[filePath]
        else:
            if filePath in self._mockedFileContent:
                return self._mockedFileContent[filePath]
        #return False
        raise Exception("Requestion the content from nonexisting file " + filePath)

    def createFile(self, filePath, content=""):
        if (filePath in self._createdFiles) or (filePath in self._mockedFileContent):
            return False
        else:
            self._createdFiles[filePath] = content
            return True

    #@staticmethod
    #def createFolder(aPath):
    #    return

    def addGetFileContentMock(self, fileDir, content):
        self._mockedFileContent[fileDir] = content
    
    def getCreatedFile(self, filePath):
        if filePath in self._createdFiles:
            return self._createdFiles[filePath]
        else:
            return False

    # TODO: currently does notwork for folders, just files that created folders
    def isdir(self, aDir):
        result = False
        aDir, extension = os.path.splitext(aDir)
        if extension != "":
            return False
        aDirArray = Std.dirExplode(aDir)
        
        for fileName in self._createdFiles:
            aPath, extension = os.path.splitext(fileName)
            if extension != "":
                aFileDirArray = Std.dirExplode(aPath)
                if len(aFileDirArray) >= len(aDirArray):
                    aFileDirArray = aFileDirArray[0:len(aDirArray)]
                    testDir = Std.dirImplode(aFileDirArray)
                    actualDir = Std.dirImplode(aDirArray)
                    if actualDir == testDir:
                        return True
        return result
    
    def isfile(self, aDir):
        return aDir in self._createdFiles