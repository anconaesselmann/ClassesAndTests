"""
@author Axel
"""
class MockMirroredDirectory():
    def __init__(self):
        self.activeFile = None
        self.kinds = dict()
        self.mockGetOriginalFileName = None

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