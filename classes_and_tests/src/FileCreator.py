import os
import fileinput
import sublime
import sublime_plugin

from MirroredDirectory import MirroredDirectory
from FileComponents import FileComponents
from Std import Std

class FileCreator:
    KIND_IS_CLASS   = "class"
    KIND_IS_TEST    = "test"
    KIND_IS_DB_TEST = "dbTest"

    def __init__(self, basePath, relativeFileName = None, defaultFileExtension = "", templatesDir = ""):
        self.determineVersion(basePath, relativeFileName)
        self.set(basePath, relativeFileName, defaultFileExtension, templatesDir)

    def set(self, basePath, relativeFileName, defaultFileExtension, templatesDir):
        if relativeFileName is None:
            #ugly workaround....
            temp = basePath
            classNameIndex = temp.rfind('/');
            relativeFileName = temp[classNameIndex + 1:]
            basePath = temp[0:classNameIndex]
            #print "basePath: " + basePath
            #print "relativeFileName: " + relativeFileName
        self.templatesDir = self.getStandardizedPath(templatesDir)
        self.tempBasePath = self.getStandardizedPath(basePath)
        if relativeFileName[0:1] == "/":
            self.tempBasePath = ""
        self.fileExtension = self.getFileExtension(relativeFileName, defaultFileExtension)
        self.relativeFileName = relativeFileName
    """ """
    @staticmethod
    def getStandardizedPath(path, slashInFront = True, slashInBack = True):
        if slashInBack == True:
            if path[-1:] != "/":
                path += "/"
        elif slashInBack == False:
            if path[-1:] == "/":
                path = path[:-1]

        if slashInFront == True:
            if path[0:1] != "/":
                #print(path[0:1])
                path = "/" + path
        elif slashInFront == False:
            if path[0:1] == "/":
                path = path[1:]
        return path

    def getFileExtension(self, fileName, defaultFileExtension):
        fileName, fileExtension = os.path.splitext(fileName)
        if fileExtension == "":
            fileExtension = "." + defaultFileExtension
        return fileExtension

    """ """
    def getFileDir(self):
        fileDir = self.getParentDir() + "/" + self.getClassName() + self.getTestEnding() + self.fileExtension
        return fileDir
    """ """
    def getClassName(self):
        fileName, fileExtension = os.path.splitext(self.relativeFileName)
        classNameIndex = fileName.rfind('/');
        className = fileName[classNameIndex + 1:]
        if className[-7:] == "DB_Test":
            className = className[0:-7]
        elif className[-4:] == "Test":
            className = className[0:-4]
        return className

    def getTestEnding(self):
        if self.kind == self.KIND_IS_TEST:
            result = "Test"
        elif self.kind == self.KIND_IS_DB_TEST:
            result = "DB_Test"
        else:
            result = ""
        return result

    def getParentDir(self):
        fileName, fileExtension = os.path.splitext(self.getBasePath() + self.relativeFileName)
        classNameIndex = fileName.rfind('/');
        classDir = fileName[0:classNameIndex]
        return classDir

    def getNamespace(self):
        namespace = self.getParentDir()[len(self.getBasePath()):]
        namespace = namespace.replace('/', "\\")
        return namespace

    """ """
    def isTest(self, fileName):
        result = False
        temp = fileName[-4:]
        if temp == "Test":
            result = True
        return result
    """ """
    def isDB_Test(self, fileName):
        result = False
        temp = fileName[-7:]
        if temp == "DB_Test":
            result = True
        return result
    """ """
    def determineVersion(self, basePath, relativeFileName):
        if relativeFileName is None:
            relativeFileName = basePath
        fileName, fileExtension = os.path.splitext(relativeFileName)
        if self.isDB_Test(fileName):
            self.kind = self.KIND_IS_DB_TEST
        elif self.isTest(fileName):
            self.kind = self.KIND_IS_TEST
        else:
            self.kind = self.KIND_IS_CLASS

    def getBasePath(self):
        if self.kind == self.KIND_IS_TEST or self.kind == self.KIND_IS_DB_TEST:
            dirArray = self.tempBasePath.split("/")
            for (i, item) in enumerate(dirArray):
                tempDir = ""
                for x in range(1,i):
                    tempDir += "/" + dirArray[x]
                    pass
                tempDir += "Test"
                if os.path.exists(tempDir):
                    dirArray[x] = dirArray[x] + "Test"
                    #print i, tempDir
                    break
            result = "/".join(dirArray)
            pass
        else:
            result = self.tempBasePath
        return result

    def create(self, data = None):
        className = self.getClassName()
        if len(className) < 1:
            fileDir = None
            print("You entered a folder. File could not be created.")
            return fileDir
        try:
            if data == None:
                data = ""
            fileDir = self.getFileDir()
            self.createFolder(fileDir)
            self.saveFile(fileDir, data)
        except Exception as e:
            fileDir = None
        return fileDir

    def createFromTemplate(self):
        className = self.getClassName()
        if len(className) < 1:
            fileDir = None
            print("You entered a folder. File could not be created.")
            return fileDir
        try:
            data = self.getClassTemplate()
            #data = data.format(self.getNamespace(), className)
            fileDir = self.getFileDir()
            self.createFolder(fileDir)
            self.saveFile(fileDir, data)
        except Exception as e:
            fileDir = None
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
        templateVariablesDir = self.getStandardizedPath(self.templatesDir) + fileExtension + "/" + f.kind + ".variables"
        if os.path.isfile(templateVariablesDir):
            import json
            from pprint import pprint
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

                commandString = variableCommand + "(" + str(args) + ")"
                commandResult = eval(commandString)

                #print "executing:"
                #print commandString
                #print "result:"
                #print commandResult
                #else:
                #    commandResult = None
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
                print(lineTemp[0:column] + lineTemp[column + len(cursorString):]),
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
                print(lineTemp),
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
        templateDirFull = self.templatesDir + self.fileExtension[1:]
        try:
            classTemplateDir = templateDirFull + self.getTemplateFileName()
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



def getSettingNameValuePair(settings):
    if not isinstance(settings, dict): # I could check for string, but I would break x-compatibility between python 2 and 3
        settings = eval(settings)
    for key, value in settings.iteritems():
        if value is not None:
            return key, value
    return None, None

def getRelativePath(baseDir, absDir):
    if baseDir is None:
        baseDir = ""
    rc = FileComponents(MirroredDirectory(absDir).getFileDir())
    rc.setBasePath(baseDir)
    relPath = rc.getRelativePath()

    # TODO: relative path should not return / at the front, check why it is doing this and remove this workaround
    if relPath[0:len(os.sep)] == os.sep:
        relPath = relPath[len(os.sep):]

    return relPath

def get_project_folder(args):
    fileName = MirroredDirectory(args["dir"]).getFile()
    varName, baseDir = getSettingNameValuePair(args["settings"])
    relPath = getRelativePath(baseDir, args["dir"])
    #print "inside get_project_folder:"
    #print "relPath: " + relPath
    result = ""
    while 1:
        relPath, tail = os.path.split(relPath)
        result += ", \"..\""
        if len(tail) < 1:
            return result


def get_py_package_name(args):
    fileName = MirroredDirectory(args["dir"]).getFile()

    varName, baseDir = getSettingNameValuePair(args["settings"])
    relPath = getRelativePath(baseDir, args["dir"])

    root = os.path.basename(os.path.normpath(baseDir))
    #print "root: " + root
    #print "relPath: " + relPath
    relPath = os.path.join(root, relPath, fileName)
    result = relPath.replace(os.sep, ".")
    if result[0:1] == ".":
        result = result[1:]

    return result

def get_php_namespace(args):
    settings = eval(args["settings"])
    result = None
    base_dir = ""
    for key, value in settings.iteritems():
        if value is not None:
            base_dir = value
        break

    # TODO: make this part of MirroredDirecotry
    rc = FileComponents(MirroredDirectory(args["dir"]).getFileDir())
    rc.setBasePath(base_dir)
    relPath = rc.getRelativePath()

    result = relPath.replace(os.sep, "\\")
    if result[0:1] == "\\":
        result = result[1:]

    return result

def get_class_name(args):
    result = MirroredDirectory(args["dir"]).getFile()
    return result


def get_doc_block_tag(args):
    settings = eval(args["settings"])
    result = None
    for key, value in settings.iteritems():
        if value is not None:
            result = "@" + key + " " + value
        break

    #print "inside get_doc_block_tag: " + str(result)
    return result

def get_php_autoloader(args):
    settings = eval(args["settings"])
    result = None
    for key, value in settings.iteritems():
        if value is not None:
            if value[0:1] == "/":
                result = "require_once \"" + value + "\";"
            else:
                result = "require_once strstr(__FILE__, 'Test', true).'/" + value + "';"
        break

    return result