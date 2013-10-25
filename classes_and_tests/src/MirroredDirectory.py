import os
from FileComponents import FileComponents
from Std import Std

class MirroredDirectory():
    KIND_IS_CLASS   = "class"
    KIND_IS_TEST    = "test"
    KIND_IS_DB_TEST = "db_Test"

    def __init__(self, fileName):
        self.fileComponents = FileComponents(fileName)
        self._determineKind(self.fileComponents.getFile())

    def getExtension(self):
        return self.fileComponents.getExtension()

    def getKind(self):
        return self._kind

    def getFile(self):
        return self._getCleanFileName()

    def getTestFile(self):
        return self.fileComponents.getFile()

    def isFile(self):
        return self.fileComponents.isFile()

    def getFileDir(self):
        folders = Std.dirExplode(self.fileComponents.getDir())
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

    def getDBTestFileDir(self):
        return self._getExistingFileDir("DB_Test")


    def getFileName(self):
        fileName = self._getCleanFileName() + "." + self.fileComponents.getExtension()
        return os.path.join(self.getFileDir(), fileName)

    def getTestFileName(self):
        fileName = self._getCleanFileName() + "Test." + self.fileComponents.getExtension()
        return os.path.join(self.getTestFileDir(), fileName)

    def getDBTestFileName(self):
        fileName = self._getCleanFileName() + "DB_Test." + self.fileComponents.getExtension()
        return os.path.join(self.getDBTestFileDir(), fileName)


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
        tempFolders = []
        for folder in folders:
            tempParentDir = Std.dirImplode(tempFolders)
            testName = folder + searchTerm
            tempDir = os.path.join(tempParentDir, testName)
            if os.path.isdir(tempDir):
                tempFolders.append(testName)
            else:
                tempFolders.append(folder)
        return Std.dirImplode(tempFolders)

    def _determineKind(self, fileName):
        fileName, fileExtension = os.path.splitext(fileName)
        if self._isDB_Test(fileName):
            self._kind = self.KIND_IS_DB_TEST
        elif self._isTest(fileName):
            self._kind = self.KIND_IS_TEST
        else:
            self._kind = self.KIND_IS_CLASS

    def _getCleanFileName(self):
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