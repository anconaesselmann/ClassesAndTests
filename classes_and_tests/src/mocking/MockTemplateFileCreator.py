"""
@author Axel Ancona Esselmann
"""
class MockTemplateFileCreator:
    def __init__(self, files):
    	#print(files)
    	self.files = files
    	self.activeFile = None

    def set(self, path):
        self.activeFile = path

    def getFileName(self):
        return self.activeFile

    def getCursors(self):
    	cursors, fileCreationSucceeds = self.files[self.activeFile]
        return cursors

    def createFromTemplate(self):
        cursors, fileCreationSucceeds = self.files[self.activeFile]
        return fileCreationSucceeds
