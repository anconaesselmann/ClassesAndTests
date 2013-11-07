import os

DEBUG = False

try:
    from FileComponents import FileComponents
    from Std import Std
    from FileManipulator import FileManipulator
except ImportError:
    from .FileComponents import FileComponents
    from .Std import Std
    from .FileManipulator import FileManipulator


class MirroredDirectory():
    KIND_IS_CLASS   = "class"
    KIND_IS_TEST    = "test"
    KIND_IS_DB_TEST = "db_Test"

    def _initializeDependencies(self):
        self.fileManipulator = FileManipulator()
        self.fileComponents = FileComponents(None)

    def __init__(self, fileName=""):
        self._initializeDependencies()
        self.set(fileName)

    def set(self, fileName):
        self.fileComponents.set(fileName)
        self._determineKind(self.fileComponents.getFile())

    def setDefaultExtension(self, fileExtension):
        self.fileComponents.setDefaultExtension(fileExtension)
        self._determineKind(self.fileComponents.getFile())

    def setBasePath(self, basePath):
        self.fileComponents.setBasePath(basePath)

    def getExtension(self):
        return self.fileComponents.getExtension()

    def getKind(self):
        return self._kind

    def setKind(self, kind):
        basePath = self.getBasePath()
        if kind == self.KIND_IS_CLASS:
            newFile = self.getFileName()
        elif kind == self.KIND_IS_TEST:
            newFile = self.getTestFileName()
        elif kind == self.KIND_IS_DB_TEST:
            newFile = self.getDBTestFileName()
        else:
            raise Exception("Unknown kind")
        self.set(newFile)
        self.setBasePath(basePath)
        
    def getFile(self):
        return self._getCleanFileName()

    def getTestFile(self):
        return self.fileComponents.getFile()

    def isFile(self):
        return self.fileComponents.isFile()

    def getFileDir(self):
        fileDir = self.fileComponents.getDir()
        if fileDir is None:
            return None
        folders = Std.dirExplode(fileDir)
        tempFolders = []
        for folder in folders:
            if folder[-7:] == "DB_Test":
                folder = folder[0:-7]
            elif folder[-4:] == "Test":
                folder = folder[0:-4]

            tempFolders.append(folder)
        return Std.dirImplode(tempFolders)

    def getTestFileDir(self):
        return self._getExistingFileDir("Test")

        """
        basePath = self.getBasePath()
        if basePath is not None:
            possibleTestDir = basePath + "Test"
            if self.fileManipulator.isdir(possibleTestDir):
                print("TestFolder Exists")
                print cleanFileName
                cleanFileName = os.path.join(possibleTestDir, cleanFileName[len(basePath):])
                print cleanFileName
        """

    def getDBTestFileDir(self):
        return self._getExistingFileDir("DB_Test")


    def getFileName(self):
        cleanFileName = self._getCleanFileName()
        if cleanFileName is None:
            return None
        fileName = cleanFileName + "." + self.fileComponents.getExtension()
        return os.path.join(self.getFileDir(), fileName)

    def getRelativeFileName(self):
        result = self.fileComponents.getRelativeFileName()
        if result is None:
            self._discoverBasePath()
            result = self.fileComponents.getRelativeFileName()
        return result 

    def getRelativePath(self):
        result = self.fileComponents.getRelativePath()
        if result is None:
            self._discoverBasePath()
            result = self.fileComponents.getRelativePath()
        return result 

    def getTestFileName(self):
        cleanFileName = self._getCleanFileName()
        if cleanFileName is None:
            return None
        fileName = cleanFileName + "Test." + self.fileComponents.getExtension()
        return os.path.join(self.getTestFileDir(), fileName)

    def getDBTestFileName(self):
        fileName = self._getCleanFileName() + "DB_Test." + self.fileComponents.getExtension()
        return os.path.join(self.getDBTestFileDir(), fileName)

    def getOriginalFileName(self):
        return self.fileComponents.getFileName()

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


    def _getExistingFileDir(self, searchTerm):
        folders = Std.dirExplode(self.fileComponents.getDir())
        tailFolders = []
        while len(folders) > 0:
            lastFolder = folders.pop()
            tempDir = os.path.join(Std.dirImplode(folders), lastFolder + searchTerm)
            if self.fileManipulator.isdir(tempDir):
                if len(tailFolders) > 0:
                    tailFolders.reverse()
                    tail = Std.dirImplode(tailFolders)
                    result = os.path.join(tempDir, tail)
                else:
                    result = tempDir
                return result
            tailFolders.append(lastFolder)
        return self.fileComponents.getDir()


    def _determineKind(self, fileName):
        if fileName != None:
            fileName, fileExtension = os.path.splitext(fileName)
            if self._isDB_Test(fileName):
                self._kind = self.KIND_IS_DB_TEST
            elif self._isTest(fileName):
                self._kind = self.KIND_IS_TEST
            else:
                self._kind = self.KIND_IS_CLASS
        else:
            self._kind = None

    def _getCleanFileName(self):
        if self.fileComponents.getFile() is None:
            return None
        if self._kind == self.KIND_IS_CLASS:
            return self.fileComponents.getFile()
        else:
            return self.fileComponents.getFile()[:-len(self._kind)]

    def _isTest(self, fileName):
        result = False
        temp = fileName[-4:]
        if temp == "Test":
            result = True
        return result

    def _isDB_Test(self, fileName):
        result = False
        temp = fileName[-7:]
        if temp == "DB_Test":
            result = True
        return result

    def _discoverBasePath(self):
        if not self.fileComponents.pathIsAbsolute():
            return
        searchTerm = "Test"
        folders = Std.dirExplode(self.fileComponents.getDir())
        result = False
        while len(folders) > 0:
            # Class files
            tempDir = Std.dirImplode(folders) + searchTerm
            if self.fileManipulator.isdir(tempDir):
                if DEBUG: print("MirroredDirectory: directory '" + tempDir + "' exists")
                result = Std.dirImplode(folders)
                break
            currentFolder = folders.pop()
            # Test files
            if currentFolder[-len(searchTerm):] == searchTerm:
                tempDir = os.path.join(Std.dirImplode(folders), currentFolder[:-4])
                if self.fileManipulator.isdir(tempDir):
                    if DEBUG: print("MirroredDirectory: directory '" + tempDir + "' exists")
                    result = tempDir + searchTerm
                    break
        if result is not False:
            self.setBasePath(result)
        else:
            if DEBUG: print("MirroredDirectory: base Path could not be discovered")  

    def _discoverBasePathFromTestFile(self):
        pass

    def getBasePath(self):
        result = self.fileComponents.getBasePath()
        if result is None:
            self._discoverBasePath()
            result = self.fileComponents.getBasePath()
        return result
