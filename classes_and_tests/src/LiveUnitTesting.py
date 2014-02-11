DEBUG = False
UNIT_TEST_DEBUG = False

import os
import fileinput
import re
import string
import sys

try:
    import sublime
    import sublime_plugin
except ImportError:
    try:
        from mocking.sublime import sublime
        from mocking import sublime_plugin
    except ImportError:
        from .mocking.sublime import sublime
        from .mocking import sublime_plugin
    if UNIT_TEST_DEBUG: 
        DEBUG = True
        print("LiveUnitTesting: sublime and sublime_plugin not imported in " + __file__)
    else:
        DEBUG = False

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
        self.fileSystem = FileSystem()

    def updateTempFiles(self, currentView):
        self._setActiveFile(currentView)
        if self._activeFile.getExtension() in self._commandFolders:
            lastModTempFile = os.stat(self._activeFile.getTestFileName()).st_mtime
            if lastModTempFile != self._lastModTempFile:
                currentTestFileContent = self.fileSystem.getFileContent(self._activeFile.getTestFileName())
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

    def _setActiveFile(self, currentView):
        md = MirroredDirectory()
        md.fileSystem = self.fileSystem
        md.set(currentView.file_name())
        self._activeFile = md

    def _getTempFileDir(self):
        folderName, completeFileName = os.path.split(self._activeFile.getFileName())
        fileName, extension = os.path.splitext(completeFileName)
        return os.path.join(folderName, "____liveUnitTesting_" + fileName + extension)

    def _getTempTestFileDir(self):
        folderName, completeFileName = os.path.split(self._activeFile.getTestFileName())
        fileName, extension = os.path.splitext(completeFileName)
        return os.path.join(folderName, "____liveUnitTesting_" + fileName + extension)

    def _saveToTempClassFile(self, curentViewContent):
        extension = self._activeFile.getExtension()
        self.fileSystem.replaceFile(self._getTempFileDir(), curentViewContent)

    def _saveToTempTestFile(self, testFileContent):
        self.fileSystem.replaceFile(self._getTempTestFileDir(), testFileContent)

        extension = self._activeFile.getExtension()
        if extension == "php":
            self._replacePhpTestFileLoadingStatements()
        elif extension == "py":
            self._replacePyTestFileLoadingStatements()
        else:
            pass

    def _replacePhpTestFileLoadingStatements(self):
        injected = False
        for line in fileinput.input(self._getTempTestFileDir(), inplace=True):
            sys.stdout.write(line)
            if not injected:
                if "require_once" in line:
                    sys.stdout.write("\trequire_once \"" + self._getTempFileDir() + "\";")
                    injected = True

    def _replacePyTestFileLoadingStatements(self):
        folderName, completeFileName = os.path.split(self._activeFile.getFileName())
        fileName, extension = os.path.splitext(completeFileName)
        newModule = "____liveUnitTesting_" + fileName
        
        replacementMade = False
        for line in fileinput.input(self._getTempTestFileDir(), inplace=True):
            if replacementMade == False and "import "in line:
                if fileName in line:
                    pos = line.find(fileName)
                    partialString = line[:pos]
                    regexString = "\\S+$"

                    match = re.search(regexString, partialString)
                    if match:
                        parentPackages = match.group()
                    else:
                        parentPackages = ""
                    if len(parentPackages) > 0 and parentPackages[-1] == ".":
                        newModule = parentPackages + newModule
                        line = "from " + newModule + " import *\n"
                        replacementMade = True
            
            sys.stdout.write(line)
    """

    def _replacePyClassFileLoadingStatements(self, text):
        fileName = self._activeFile.getFileName()
        result = str.replace(str(text), "__file__", "\"" + fileName + "\"")
        # import Class dependencies
        classDependencies  = "from os import sys, path\n"
        classDependencies += "sys.path.append(\"" + os.path.abspath(os.path.join(fileName, "..")) +"\")\n"
        result = classDependencies + result
        return result

    def _createPackageFiles(self):
        parentPackageInit = os.path.abspath(os.path.join(self._getTempTestFileDir(), "..", "..", "__init__.py"))
        classPackageInit = os.path.abspath(os.path.join(self._getTempFileDir(), "..", "__init__.py"))

        if not os.path.isfile(parentPackageInit):
            FileSystem.createFile(parentPackageInit, "")
        if not os.path.isfile(classPackageInit):
            FileSystem.createFile(classPackageInit, "")"""
