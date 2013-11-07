"""
@author Axel
"""
import os
class MockMirroredDirectory():
    def __init__(self):
        self.activeFile = None
        self.kinds = dict()
        self.mockGetOriginalFileName = None
        self.mockBasePaths = dict()
        self.mockRelativeFileNames = dict()

    def set(self, path):
        self.activeFile = path

    def setMockKind(self, fileName, kind):
    	self.kinds[fileName] = kind

    def getKind(self):
    	return self.kinds[self.activeFile]

    def setKind(self, kind):
    	pass

    def setMockOriginalFileName(self, fileName):
    	self.mockGetOriginalFileName = fileName

    def getOriginalFileName(self):
    	return self.mockGetOriginalFileName

    def setMockBasePath(self, fileName, basePath):
        self.mockBasePaths[fileName] = basePath

    def getBasePath(self):
        return self.mockBasePaths[self.activeFile]

    def setMockRelativeFileName(self, fileName, relativeFileName):
        self.mockRelativeFileNames[fileName] = relativeFileName

    def getRelativeFileName(self):
        return self.mockRelativeFileNames[self.activeFile]

    def getExtension(self):
        aFile, ext = os.path.splitext(self.activeFile)
        return ext[1:]
