import sublime
import sublime_plugin
import os
import fileinput

from FileManipulation import FileManipulation
from SublimeFunctions import SublimeFunctions
from MirroredDirectory import MirroredDirectory
from FileCreator import FileCreator

class LiveUnitTesting():
    def __init__(self, commandFolders):
        if not isinstance(commandFolders, dict):
            raise Exception("CommandFolders is a dictionary")
        self._commandFolders = commandFolders
        self._lastModTempFile = None

    def updateTempFiles(self, currentView):
        self._activeFile = MirroredDirectory(currentView.file_name())
        if self._activeFile.getExtension() in self._commandFolders:
            lastModTempFile = os.stat(self._activeFile.getTestFileName()).st_mtime
            if lastModTempFile != self._lastModTempFile:
                # only save copy of test file, if it has been modified and saved
                currentTestFileContent = FileManipulation.getFileContent(self._activeFile.getTestFileName())
                self._saveToTempTestFile(currentTestFileContent)
                self._lastModTempFile = lastModTempFile

            if self._activeFile.getKind() == self._activeFile.KIND_IS_CLASS:
                curentViewContent = SublimeFunctions.getViewContent(currentView)
                self._saveToTempClassFile(curentViewContent)

    def getCommand(self):
        extension = self._activeFile.getExtension()
        if extension == "php":
            result = os.path.join(os.path.normpath(self._commandFolders["php"]), "phpunit")
        elif extension == "py":
            result = os.path.join(os.path.normpath(self._commandFolders["py"]), "python")
        else:
            result = None
        return result

    def getArgument(self):
        return self._getTempTestFileDir()

    def getActiveFile(self):
        return self._activeFile

    def _getTempFileDir(self):
        return os.path.join(sublime.packages_path(), "User", "UnitTesting", "continuousTestingTemp", "classFiles", "TemporaryClass." + self._activeFile.getExtension())

    def _getTempTestFileDir(self):
        return os.path.join(sublime.packages_path(), "User", "UnitTesting", "continuousTestingTemp", "testFiles", "TemporaryClassTest." + self._activeFile.getExtension())

    def _saveToTempClassFile(self, curentViewContent):
        FileManipulation.replaceFile(self._getTempFileDir(), curentViewContent)

    def _saveToTempTestFile(self, testFileContent):
        FileManipulation.replaceFile(self._getTempTestFileDir(), testFileContent)

        extension = self._activeFile.getExtension()
        if extension == "php":
            self._replacePhpLoadingStatements()
        elif extension == "py":
            self._replacePyLoadingStatements()
            self._createPackageFiles()
        else:
            pass

    def _replacePhpLoadingStatements(self):
        injected = False
        for line in fileinput.input(self._getTempTestFileDir(), inplace=True):
            if not injected and "require_once" in line:
                print "\trequire_once\"" + self._getTempFileDir() + "\";\n",
                injected = True
            else:
                print line,

    def _replacePyLoadingStatements(self):
        injected = False
        #print "active file: " + self._activeFile.getFile()
        for line in fileinput.input(self._getTempTestFileDir(), inplace=True):
            if not injected and "sys.path.append(path.abspath(path.join(__file__" in line:
                print "    sys.path.append(path.abspath(path.join(__file__, \"..\", \"..\")))\n",
                print "    sys.path.append(path.abspath(path.join(\"" + self._activeFile.getFileDir() + "\")))"
                print "    from classFiles.TemporaryClass import *\n",
                injected = True
            elif "import " + self._activeFile.getFile() in line:
                pass
            else:
                print line,

    def _createPackageFiles(self):
        parentPackageInit = os.path.abspath(os.path.join(self._getTempTestFileDir(), "..", "..", "__init__.py"))
        classPackageInit = os.path.abspath(os.path.join(self._getTempFileDir(), "..", "__init__.py"))

        if not os.path.isfile(parentPackageInit):
            FileCreator(parentPackageInit).create()
        if not os.path.isfile(classPackageInit):
            FileCreator(classPackageInit).create()
