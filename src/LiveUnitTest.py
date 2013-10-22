import sublime
import sublime_plugin
import os
import fileinput

from FileManipulation import FileManipulation
from SublimeFunctions import SublimeFunctions
from MirroredDirectory import MirroredDirectory

class LiveUnitTest():
    def __init__(self, phpUnitDir):
        self.phpUnitDir = os.path.normpath(phpUnitDir) + os.sep
        self.lastModTempFile = None
        self.tempFileDir = os.path.join(sublime.packages_path(), "User", "UnitTesting", "continuousTestingTemp", "class", "TemporaryClass.php")
        self.tempTestFileDir = os.path.join(sublime.packages_path(), "User", "UnitTesting", "continuousTestingTemp", "test", "TemporaryClassTest.php")

    def updateTempFiles(self, currentView):
        self.activeFile = MirroredDirectory(currentView.file_name())
        if self.activeFile.getExtension() == "php":
            lastModTempFile = os.stat(self.activeFile.getTestFileName()).st_mtime
            if lastModTempFile != self.lastModTempFile:
                # only save copy of test file, if it has been modified and saved
                currentTestFileContent = FileManipulation.getFileContent(self.activeFile.getTestFileName())
                self._saveToTempTestFile(currentTestFileContent)
                self.lastModTempFile = lastModTempFile

            if self.activeFile.getKind() == self.activeFile.KIND_IS_CLASS:
                curentViewContent = SublimeFunctions.getViewContent(currentView)
                self._saveToTempClassFile(curentViewContent)

    def getCommandString(self):
        return self.phpUnitDir + "phpunit \"" + self.tempTestFileDir + "\""

    def _saveToTempClassFile(self, curentViewContent):
        FileManipulation.replaceFile(self.tempFileDir, curentViewContent)

    def _saveToTempTestFile(self, testFileContent):
        FileManipulation.replaceFile(self.tempTestFileDir, testFileContent)

        injected = False
        for line in fileinput.input(self.tempTestFileDir, inplace=True):
            if not injected and "require_once" in line:
                print "\trequire_once\"" + self.tempFileDir + "\";\n",
                injected = True
            else:
                print line,