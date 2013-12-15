import sublime
import sublime_plugin
import os
import fileinput

try:
    from FileSystem import FileSystem
    from SublimeFunctions import SublimeFunctions
    from MirroredDirectory import MirroredDirectory
    from TemplateFileCreator import TemplateFileCreator
except ImportError:
    from .FileSystem import FileSystem
    from .SublimeFunctions import SublimeFunctions
    from .MirroredDirectory import MirroredDirectory
    from .TemplateFileCreator import TemplateFileCreator

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
                currentTestFileContent = FileSystem.getFileContent(self._activeFile.getTestFileName())
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

    def _getTestingDir(self):
        return os.path.join(sublime.packages_path(), "User", "UnitTesting", "continuousTestingTemp")

    def _getTempFileDir(self):
        return os.path.join(self._getTestingDir(), "classFiles", "TemporaryClass." + self._activeFile.getExtension())

    def _getTempTestFileDir(self):
        return os.path.join(self._getTestingDir(), "testFiles", "TemporaryClassTest." + self._activeFile.getExtension())

    def _saveToTempClassFile(self, curentViewContent):
        extension = self._activeFile.getExtension()
        if extension == "php":
            pass
        elif extension == "py":
            curentViewContent = self._replacePyClassFileLoadingStatements(curentViewContent)
        else:
            pass

        FileSystem.replaceFile(self._getTempFileDir(), curentViewContent)

    def _saveToTempTestFile(self, testFileContent):
        FileSystem.replaceFile(self._getTempTestFileDir(), testFileContent)

        extension = self._activeFile.getExtension()
        if extension == "php":
            self._replacePhpTestFileLoadingStatements()
        elif extension == "py":
            self._replacePyTestFileLoadingStatements()
            self._createPackageFiles()
        else:
            pass

    def _replacePhpTestFileLoadingStatements(self):
        injected = False
        for line in fileinput.input(self._getTempTestFileDir(), inplace=True):
            if '__FILE__' in line:
                line = line.replace('__FILE__', "'" + self._activeFile.getTestFileName() + "'")
            if not injected and "require_once" in line:
                # strstr(__FILE__, 'Test', true).'
                print("\trequire_once\"" + self._getTempFileDir() + "\";\n"),
                print(line)
                injected = True
            else:
                print(line),

    def _replacePyClassFileLoadingStatements(self, text):
        fileName = self._activeFile.getFileName()
        result = str.replace(str(text), "__file__", "\"" + fileName + "\"")
        # import Class dependencies
        classDependencies  = "from os import sys, path\n"
        classDependencies += "sys.path.append(\"" + os.path.abspath(os.path.join(fileName, "..")) +"\")\n"
        result = classDependencies + result
        return result

    def _replacePyTestFileLoadingStatements(self):
        injected = False
        fileName = self._activeFile.getFileName()
        for line in fileinput.input(self._getTempTestFileDir(), inplace=True):
            if not injected and "sys.path.append(" in line:
                parentToPyPath = "    sys.path.append(" + "\"" + self._getTestingDir() + "\"" + ")\n"
                includeTempClass = "    from classFiles.TemporaryClass import *\n"
                line =  parentToPyPath + includeTempClass + line
                injected = True
            if "__file__" in line:
                line = str.replace(str(line), "__file__", "\"" + fileName + "\"")
            if "import " + self._activeFile.getFile() in line:
                pass
            else:
                print(line),

    def _createPackageFiles(self):
        parentPackageInit = os.path.abspath(os.path.join(self._getTempTestFileDir(), "..", "..", "__init__.py"))
        classPackageInit = os.path.abspath(os.path.join(self._getTempFileDir(), "..", "__init__.py"))

        if not os.path.isfile(parentPackageInit):
            FileSystem.createFile(parentPackageInit, "")
        if not os.path.isfile(classPackageInit):
            FileSystem.createFile(classPackageInit, "")
