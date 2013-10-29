import os
import sys
import fileinput
import json
#from pprint import pprint

try:
    from MirroredDirectory import MirroredDirectory
    from FileComponents import FileComponents
    from Std import Std
except ImportError:
    from .MirroredDirectory import MirroredDirectory
    from .FileComponents import FileComponents
    from .Std import Std
    from io import open

class FileCreator:


    def __init__(self, fileName, defaultFileExtension = ""):
        pass



    def setTempatesDir(self, dirName):
        self.templatesDir = os.path.normpath(dirName)







    def create(self, data = None):
        className = self._fileComponents.getFile()
        if len(className) < 1:
            fileDir = None
            print("You entered a folder. File could not be created.")
            return fileDir
        try:
            if data == None:
                data = ""
            fileDir = self._fileComponents.getFileDir()
            self.createFolder(fileDir)
            self.saveFile(fileDir, data)
        except Exception as e:
            fileDir = None
            raise Exception("file creation unsuccessful")
        return fileDir

    def createFromTemplate(self):
        className = self._fileComponents.getFile()
        if len(className) < 1:
            fileDir = None
            print("You entered a folder. File could not be created.")
            return fileDir
        try:
            data = self.getClassTemplate()
            #data = data.format(self.getNamespace(), className)
            fileDir = self._fileComponents.getFileDir()
            self.createFolder(fileDir)
            self.saveFile(fileDir, data)
        except Exception as e:
            fileDir = None
            raise Exception("file creation unsuccessful")
        return fileDir

    def getReplacementString(self, replacementKeyWord, replacementString):
        if len(replacementString) > 0:
            replacementString = "@" + replacementKeyWord + " " + replacementString
        return replacementString

    def getReplacementLine(self, keyWord, replacementString, line):
        searchString = '/* @' + keyWord + ' */'
        if len(replacementString) > 0:
            index = line.find(searchString)
            result = line[0:index] + replacementString + line[index + len(searchString):]
        else:
            result = ""
        return result

    def _executeTemplateFunctionSublime2(self, fileExtension, functionName, args):
        from os import sys, path
        importPath = path.abspath(path.join(self.templatesDir))
        sys.path.append(importPath)
        packageString = fileExtension + ".functions"
        _temp = __import__(packageString, globals(), locals(), [functionName], 0)
        function = eval("_temp." + functionName)
        return function(args)

    def _executeTemplateFunctionSublime3(self, fileExtension, functionName, args):
        import importlib
        packageString = "ClassesAndTests.templates." + fileExtension + ".functions"
        module = importlib.import_module(packageString)
        function = getattr(module, functionName)
        commandResult = function(args)
        return commandResult

    # This is a stupid hack, but I just can't figure out how to do this neatly in Sublime 2....
    def _executeTemplateFunction(self, fileExtension, variableCommand, args):
        if sys.version_info >= (3, 0):
            try:
                commandResult = self._executeTemplateFunctionSublime3(fileExtension, variableCommand, args)
            except Exception as e:
                try:
                    commandResult = self._executeTemplateFunctionSublime3("general", variableCommand, args)
                except Exception as e:
                    raise Exception("Custom variable " + variableCommand + " does not exist")
        else:

            try:
                commandResult = self._executeTemplateFunctionSublime2(fileExtension, variableCommand, args)
            except Exception as e:
                try:
                    commandResult = self._executeTemplateFunctionSublime2("general", variableCommand, args)
                except Exception as e:
                    raise Exception("Custom variable " + variableCommand + " does not exist")
        return commandResult


    def initialOpenFile(self, window, fileDir, settings):
        if settings.get("tests_on_right") == True:
            classWindow = 0
            testWindow  = 1
        else:
            classWindow = 1
            testWindow  = 0

        leftColumnSize = settings.get("left_column_size")
        if fileDir is None:
            print("File Opening Failed.")
            return


        f = FileCreator(fileDir)

        fileExtension = f.fileExtension[1:]
        templateVariablesDir = os.path.join(self.templatesDir, fileExtension, f.kind + ".variables")


        if os.path.isfile(templateVariablesDir):

            jsonData = open(templateVariablesDir)
            templateVariables = json.load(jsonData)
            jsonData.close()

            #pprint(templateVariables)

            replacements = dict()
            for templateVar in templateVariables:
                variableName = templateVar["variable"]

                settingsValues = dict()
                if "fromSettings" in templateVar:
                    for settingsVariable in templateVar["fromSettings"]:
                        settingsValues[settingsVariable] = settings.get(settingsVariable)

                variableCommand = templateVar["command"]

                args = dict()
                args["settings"] = str(settingsValues)
                args["name"] = variableName
                args["dir"] = fileDir

                commandResult = self._executeTemplateFunction(fileExtension, variableCommand, args)

                replacements[variableName] = commandResult

        cursorString = '/* @cursor */'
        line = 0
        column = 0
        i = 0
        for lineTemp in fileinput.input(fileDir, inplace=True):
            i += 1
            if cursorString in lineTemp:
                line = i
                column = lineTemp.find(cursorString)
                sys.stdout.write (lineTemp[0:column] + lineTemp[column + len(cursorString):]),
                column += 1
            else:
                #replaced = False
                for variableName, replacementString in replacements.items():
                    searchString = "/* @" + variableName + " */"

                    if searchString in lineTemp:
                        #replaced = True
                        index = lineTemp.find(searchString)

                        if replacementString is None:
                            lineTemp = lineTemp[0:index] + lineTemp[index + len(searchString):]
                            if Std.isAllWhitespace(lineTemp):
                                break #this doesn't seem to work
                        else:
                            lineTemp = lineTemp[0:index] + str(replacementString) + lineTemp[index + len(searchString):]
                sys.stdout.write (lineTemp),
        openStatement = "%s:%d:%d" % (fileDir, line, column)
        import sublime

        splitView = settings.get("seperate_tests_and_sources_by_split_view")
        if splitView is True:
            sublime.active_window().run_command("set_layout", { "cols": [0.0, leftColumnSize, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1], [1, 0, 2, 1]] })
        else:
            sublime.active_window().run_command("set_layout", { "cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]] })

        if self.kind == self.KIND_IS_TEST or self.kind == self.KIND_IS_DB_TEST:
            if splitView is True:
                sublime.active_window().run_command("focus_group", { "group": testWindow })
        else:
            if splitView is True:
                sublime.active_window().run_command("focus_group", { "group": classWindow })

        openedFile = window.open_file(openStatement, sublime.ENCODED_POSITION)
        return openedFile

    def openFile(self, window, fileDir):
        openedFile = window.open_file(fileDir)
        return openedFile

    def saveFile(self, fileDir, data):
        if not os.path.exists(fileDir):
            newFile = open(fileDir, "wb")
            if sys.version_info >= (3, 0):
                newFile.write(str.encode(data));
            else:
                newFile.write(data);
            newFile.close()

            #self.printToConsole("File " + fileDir + " created.")
            pass
        else:
            #self.printToConsole("File " + fileDir + " opened.")
            pass

    def createFolder(self, fileDir):
        folderIndex = fileDir.rfind('/');
        folder = fileDir[0:folderIndex]
        if not os.path.isdir(folder):
            self.printToConsole("Creating folder " + folder)
            os.makedirs(folder)
            pass

    def getClassTemplate(self):
        templateDirFull = os.path.join(self.templatesDir, self.fileExtension[1:])
        try:
            classTemplateDir = os.path.join(templateDirFull, self.getTemplateFileName())
            classTemplateFile = open(classTemplateDir, "r")
        except Exception as e:
            print("No templates for source code ending with " + self.fileExtension)
            raise e
        else:
            pass

        data = classTemplateFile.read()
        return data

    def getTemplateFileName(self):
        if self.kind == self.KIND_IS_DB_TEST:
            classTemplateFileName = "/dbTest.template"
        elif self.kind == self.KIND_IS_TEST:
            classTemplateFileName = "/test.template"
        else:
            classTemplateFileName = "/class.template"
        return classTemplateFileName;

    def printToConsole(self, out):
        print("- FileCreator: " + out)


