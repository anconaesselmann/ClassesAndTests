import os

import sys
if sys.version_info < (3, ):
    from orderedDict import OrderedDict
else:
    from collections import OrderedDict

DEBUG = False

try:
    from FileComponents import FileComponents
    from Std import Std
    from FileSystem import FileSystem
except ImportError:
    from .FileComponents import FileComponents
    from .Std import Std
    from .FileSystem import FileSystem


class MirroredDirectory():
    KIND_IS_CLASS   = "class"
    KIND_IS_TEST    = "test"
    KIND_IS_DB_TEST = "db_Test"

    def _initializeDependencies(self):
        self.fileSystem = FileSystem()
        self.fileComponents = FileComponents(None)

    def __init__(self, fileName=None):
        self._kindDict = OrderedDict([
            ("db_Test", ["_db_test", "DB_Test"]),
            ("test", ["_test", "Test"])
        ])
        self._initializeDependencies()
        if fileName is not None:
            self.set(fileName)

    def set(self, fileName):
        kind = self._determineKind(fileName)
        self.setKind(kind)
        classFileName = self._scrubPath(fileName, kind)
        self.fileComponents.set(classFileName)
        self._discoverBasePath()

    def setDefaultExtension(self, fileExtension):
        self.fileComponents.setDefaultExtension(fileExtension)
    
    # returns the file name without extension or path
    def getFile(self):
        return self.fileComponents.getFile()

    # returns the Test file name without extension or path
    def getTestFile(self):
        return self.fileComponents.getFile() + "Test"

    # returns the file extension without leading period
    def getExtension(self):
        return self.fileComponents.getExtension()

    # returns true if instance is a file
    def isFile(self):
        return self.fileComponents.isFile()

    def getFileDir(self):
        return self.fileComponents.getDir()

    def getTestFileDir(self):
        searchTerm = "Test"
        basePath = self.getBasePath()
        relativePath = self.getRelativePath()
        if basePath is not None and relativePath is not None:
            return os.path.join(basePath + searchTerm, relativePath)
        else:
            return self.getFileDir()

    def getDBTestFileDir(self):
        searchTerm = "DB_Test"
        basePath = self.getBasePath()
        relativePath = self.getRelativePath()
        if basePath is not None and relativePath is not None:
            return os.path.join(basePath + searchTerm, relativePath)
        else:
            return self.getFileDir()

    def getRelativePath(self):
        return self.fileComponents.getRelativePath()

    def getFileName(self):
        return self.fileComponents.getFileName()

    def getTestFileName(self):
        searchTerm = "Test"
        testDir = self.getTestFileDir()
        if testDir is not None:
            return os.path.join(testDir, self.fileComponents.getFile() + searchTerm + "." + self.fileComponents.getExtension())
        else: return None

    def getDBTestFileName(self):
        searchTerm = "DB_Test"
        testDir = self.getDBTestFileDir()
        if testDir is not None:
            return os.path.join(testDir, self.fileComponents.getFile() + searchTerm + "." + self.fileComponents.getExtension())
        else: return None
    
    def getOriginalFileName(self):
        if self._kind == self.KIND_IS_CLASS:
            return self.getFileName()
        elif self._kind == self.KIND_IS_TEST:
            return self.getTestFileName()
        elif self._kind == self.KIND_IS_DB_TEST:
            return self.getDbFileName()
        else:
            raise Exception("Unknown file type")

    def getToggledDir(self):
        if self._kind == self.KIND_IS_CLASS:
            return self.getTestFileDir()
        elif self._kind == self.KIND_IS_TEST:
            return self.getFileDir()
        elif self._kind == self.KIND_IS_DB_TEST:
            return self.getFileDir()
        else:
            raise Exception("Unknown file type")

    def getToggledFileName(self):
        if self._kind == self.KIND_IS_CLASS:
            return self.getTestFileName()
        elif self._kind == self.KIND_IS_TEST:
            return self.getFileName()
        elif self._kind == self.KIND_IS_DB_TEST:
            return self.getFileName()
        else:
            raise Exception("Unknown file type")

    def setBasePath(self, basePath):
        self.fileComponents.setBasePath(basePath)

    def getBasePath(self):
        result = self.fileComponents.getBasePath()
        if result is None:
            self._discoverBasePath()
            result = self.fileComponents.getBasePath()
        return result

    def getRelativeFileName(self):
        result = self.fileComponents.getRelativeFileName()
        if result is None:
            self._discoverBasePath()
            result = self.fileComponents.getRelativeFileName()
        return result 

    def setKind(self, kind):
        self._kind = kind

    def getKind(self):
        return self._kind

    def _discoverBasePathFromClassFile(self, aPath, searchTerm):
        folders = Std.dirExplode(aPath)
        result = False
        while len(folders) > 0:
            tempDir = Std.dirImplode(folders) + searchTerm
            if self.fileSystem.isdir(tempDir):
                if DEBUG: print("MirroredDirectory: directory '" + tempDir + "' exists")
                result = Std.dirImplode(folders)
                break
            currentFolder = folders.pop()
        return result 

    def _discoverBasePath(self):
        if not self.fileComponents.pathIsAbsolute(): return
        searchTerm = "Test"
        result = self._discoverBasePathFromClassFile(self.fileComponents.getDir(), searchTerm)
        if not result:
            if DEBUG: print("MirroredDirectory: base Path could not be discovered.")
        else:
            self.setBasePath(result)

    def _determineKind(self, fileName):
        result = MirroredDirectory.KIND_IS_CLASS
        fileName, ext = os.path.splitext(fileName)
        for kind, endings in Std.getIterItems(self._kindDict):
            for ending in endings:
                endingLen = len(ending)
                if len(fileName) > endingLen:
                    if fileName[-endingLen:] == ending:
                        result = kind
                        return result
        return result

    def _scrubPath(self, aPath, kind):
        if kind == MirroredDirectory.KIND_IS_CLASS:
            return aPath
        fileName, ext = os.path.splitext(aPath)
        folders = Std.dirExplode(fileName)
        result = False
        for searchTerm in self._kindDict[kind]:
            for i in range(len(folders)):
                currentFolder = folders[i]
                if len(currentFolder) > len(searchTerm):
                    ending = currentFolder[-len(searchTerm):]
                    if ending == searchTerm:
                        folders[i] = currentFolder[:-len(searchTerm)]
        return Std.dirImplode(folders) + ext