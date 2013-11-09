"""
@author Axel
"""
import os
try:
    from .Std import Std
except ImportError:
    from ..Std import Std
"""
class Std():
    @staticmethod
    def dirExplode(path):
        path = os.path.normpath(path)
        folders=[]
        while 1:
            path,folder=os.path.split(path)
            if folder!="":
                folders.append(folder)
            else:
                if path!="":
                    folders.append(path)
                break
        folders.reverse()
        return folders

    @staticmethod
    def dirImplode(array):
        path = ""
        for folder in array:
            if path != "":
                seperator = os.sep
            else:
                seperator = ""
            path = os.path.join(path, folder)
        return os.path.normpath(path)

    @staticmethod
    def getIterItems(aDict):
        if sys.version_info < (3, ):
            return aDict.iteritems()
        else:
            return aDict.items()"""

class MockFile():
	def __init__(self, fileName, content=""):
		self.fileName = fileName
		self.content = content


class MockFileSystem():
    def __init__(self):
        self.root = {os.sep: {}}
    
    def getFileContent(self, fileName):
    	content = False
    	if self.isfile(fileName):
    		aPath, aFileName = os.path.split(fileName)
    		parentFolder = self._getFolder(aPath)
    		content = parentFolder[aFileName].content
        return content

    def createFile(self, fileName, content=""):
    	created = False
    	aPath, aFileName = os.path.split(fileName)
    	if not self.isdir(aPath):
    		self.createFolder(aPath)
    	parentFolder = self._getFolder(aPath)
    	if parentFolder is not False:
    		created = self._createFileInFolder(parentFolder, aFileName, content)
        return created

    def isdir(self, aFolder):
    	result = False
    	currentFolder = self._getFolder(aFolder)
    	if currentFolder is not False:
    		if not isinstance(currentFolder, MockFile):
	    		result = True
    	return result
    
    def isfile(self, fileName):
    	result = False
    	aPath, aFileName = os.path.split(fileName)
    	parentFolder = self._getFolder(aPath)
    	if parentFolder is not False:
    		if aFileName in parentFolder:
    			if isinstance(parentFolder[aFileName], MockFile):
    				result = True
        return result
    
    def createFolder(self, aFolder):
    	currentFolder = self.root
    	folders = Std.dirExplode(aFolder)
    	if folders[0] != os.sep: return False
    	result = False
    	for folder in folders:
    		if folder in currentFolder:
    			exists = True
    		else:
    			exists = self._createFolderNonRecursive(currentFolder, folder)
    			if exists: result = True
    		if exists:
    			currentFolder = currentFolder[folder]
    		else:
    			raise Exception("Folder should exist or should have been created....")
        return result
    
    def printTree(self):
    	print(self.root)

    def getRoot(self):
    	return self.root[os.sep]

    def _getFolder(self, aFolder):
    	currentFolder = self.root
    	folders = Std.dirExplode(aFolder)
    	if folders[0] != os.sep: return False
    	result = False
    	for folder in folders:
    		if folder in currentFolder:
    			exists = True
    			currentFolder = currentFolder[folder]
    		else:
    			currentFolder = False
    			break
        return currentFolder

    def _createFolderNonRecursive(self, parentFolder, aFolder):
    	if aFolder in parentFolder:
    		return False
    	else:
    		parentFolder[aFolder] = {}
	        return True

    def _createFileInFolder(self, parentFolder, fileName, content):
    	if fileName in parentFolder:
    		return False
    	else:
    		newFile = MockFile(fileName, content)
    		parentFolder[fileName] = newFile
    		return True
    