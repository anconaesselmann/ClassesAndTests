"""
@author Axel Ancona Esselmann

"""
import os
import sys

"""try:
    from .Std import Std
except ImportError:
    from ..Std import Std"""

from MockFileSystem import *

DEBUG = True

class MockFileSystem():
    def __init__(self):
        self.mockFileSystem = MockFileSystem()
    
    def getFileContent(self, filePath):
        return self.mockFileSystem.getFileContent(filePath)

    def createFile(self, filePath, content=""):
        return self.mockFileSystem.createFile(filePath, content)

    def isdir(self, aDir):
        return self.mockFileSystem.isdir(aDir)
    
    def isfile(self, aDir):
        return self.mockFileSystem.isfile(aDir)

    def createFolder(self, aFolder):
        return self.mockFileSystem.createFolder(aFolder)