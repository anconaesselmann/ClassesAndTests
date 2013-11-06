import os
import sys
import re
import ast

DEBUG = False

try:
    from MirroredDirectory import MirroredDirectory
    from Std import Std
    from FileManipulator import FileManipulator
    from Importer import Importer
except ImportError:
    from .MirroredDirectory import MirroredDirectory
    from .Std import Std
    from .FileManipulator import FileManipulator
    from .Importer import Importer

class TemplateFileCreator:
    def __init__(self, fileName = "", defaultFileExtension = ""):
        self._settings = None
        self.fileManipulator = FileManipulator()
        self.importer = Importer()
        self._templateDir = None
        self.set(fileName, defaultFileExtension)


    def set(self, fileName, defaultFileExtension = ""):
        if DEBUG: print("TemplateFileCreator: setting dir to: '" + fileName + "'")
        self._fileComponents = MirroredDirectory(fileName)
        if DEBUG: print("TemplateFileCreator: dir set to: '" + str(self._fileComponents.getOriginalFileName()) + "'")
        self._cursors = []

    def createFromTemplate(self):
        templatePath = os.path.join(self.getTemplateDir(), self._fileComponents.getExtension(), self.classifyKind() + ".template")
        variablePath = os.path.join(self.getTemplateDir(), self._fileComponents.getExtension(), self.classifyKind() + ".variables")
        functionPath = os.path.join(self.getTemplateDir(), self._fileComponents.getExtension(), "functions.py")

        templateContent = self.fileManipulator.getFileContent(templatePath)
        variableContent = self.fileManipulator.getFileContent(variablePath)
        functionCollectionObject = self.importer.getObjectInstance(functionPath, "FunctionCollection")()
        content = self.getReplacementContent(templateContent, variableContent,
                                             functionCollectionObject)

        if DEBUG: print("TemplateFileCreator: creating file: " + self._fileComponents.getOriginalFileName())
        return self.fileManipulator.createFile(self._fileComponents.getOriginalFileName(), content)

    def setBasePath(self, basePath):
        self._fileComponents.setBasePath(basePath)

    def setSettings(self, settings):
        self._settings = settings

    def setTemplateDir(self, templateDir):
        self._templateDir = templateDir

    def getCursors(self):
        return self._cursors

    def getFileName(self):
        return self._fileComponents.getOriginalFileName()

    #def open(self, window):
    #    self.fileManipulator.open(self._fileComponents.getFileName(), self._settings, window, self.getCursors())

    def setDefaultExtension(self, fileExtension):
        self._fileComponents.setDefaultExtension(fileExtension)


    def getArgsDictFromVarContent(self, VarContent):
        result = dict()
        try:
            varDictionary = ast.literal_eval(VarContent)
        except:
            raise TypeError("the content of VarContent could not be converted to a dict.")
        for templateVar in varDictionary:
            variableName = templateVar["variable"]

            settingsValues = dict()
            if "fromSettings" in templateVar:
                for settingsVariable in templateVar["fromSettings"]:
                    settingsValues[settingsVariable] = self._settings.get(settingsVariable)

            args = dict()
            args["settings"] = str(settingsValues)
            args["name"] = variableName
            args["dir"] = self._fileComponents.getFileName()
            #args["basePath"] = ""
            args["command"] = templateVar["command"]

            result[variableName] = args
        return result

    """def getReplacements(self, args, functionCollectionObject):
        # TODO: this check has loopholes...
        if isinstance(functionCollectionObject, (int, float, complex, str)) or functionCollectionObject is None:
            raise Exception("The functionCollectionObject argument must be an instance of an object, " + str(type(functionCollectionObject)) + " passed instead.")
        result = dict()
        for name, arg in Std.getIterItems(args):
            function = getattr(functionCollectionObject, arg["command"])
            result["/* @" + name + " */"] = function(arg)
        return result"""

    def getReplacements(self, args, functionCollectionObject):
        # TODO: this check has loopholes...
        if isinstance(functionCollectionObject, (int, float, complex, str)) or functionCollectionObject is None:
            raise Exception("The functionCollectionObject argument must be an instance of an object, " + str(type(functionCollectionObject)) + " passed instead.")
        result = dict()
        for name, arg in Std.getIterItems(args):
            function = getattr(functionCollectionObject, arg["command"])
            result["/* @" + name + " */"] = function(arg)
        return result

    def getCursorsFromContent(self, templateContent):
        lines = templateContent.splitlines()
        cursorString = "/* @cursor */"
        lineNbr = 0
        cursors = []
        for line in lines:
            while cursorString in line:
                row = line.find(cursorString)
                line = line[:row] + line[row + len(cursorString):]
                cursors.append((lineNbr, row))
            lineNbr += 1
        return cursors

    def getSearchStringForNone(self, templateContent, searchString):
        regexSearchString = searchString.replace("/", "\\/")
        regexSearchString = regexSearchString.replace("*", "\\*")
        regexString = ".*(" + regexSearchString + ").*\\n?\\r?"
        match = re.search(regexString, templateContent)
        if match:
            line = match.group()
            lineRemoved1 = line.replace(searchString, "")
            lineRemoved2 = lineRemoved1.replace("*", "")
            lineRemoved3 = lineRemoved2.replace("/", "")
            lineRemoved4 = lineRemoved3.replace("#", "")
            lineRemoved5 = lineRemoved4.replace("\"\"\"", "")
            lineRemoved6 = lineRemoved5.replace("'''", "")
            lineRemoved7 = lineRemoved6.strip(' \n\r\t')
            if len(lineRemoved7) < 1:
                searchString = line
        return searchString

    def getReplacementContent(self, templateContent, variableContent, functionCollectionObject):
        args = self.getArgsDictFromVarContent(variableContent)
        replacements = self.getReplacements(args, functionCollectionObject)
        for searchString, replacement in Std.getIterItems(replacements):
            if replacement is None:
                replacement = ""
                searchString = self.getSearchStringForNone(templateContent, searchString)
            templateContent = templateContent.replace(searchString, replacement)
        self._cursors = self.getCursorsFromContent(templateContent)
        templateContent = templateContent.replace("/* @cursor */", "")
        return templateContent

    def getTemplateDir(self):
        return self._templateDir

    def classifyKind(self):
        return self._fileComponents.getKind()

    def setKind(self, kind):
        self._fileComponents.setKind(kind)