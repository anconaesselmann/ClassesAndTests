import os, fileinput, subprocess, re, sublime, sublime_plugin

#from src.FileCreator import FileCreator

PACKAGE_NAME = "ClassesAndTests"
PACKAGE_VERSION = "0.1.0"
PACKAGE_DIR = sublime.packages_path() + "/" + PACKAGE_NAME
settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')
TEMPLATES_DIR = PACKAGE_DIR + "/templates"
SPLIT_VIEW = settings.get("seperate_tests_and_sources_by_split_view")

USER_SETTINGS_TO_BE_INITIALIZED = ["author", "base_path", "current_php_test_suite_dir"]
USER_SETTINGS_TO_BE_INITIALIZED_PROMPTS = ["Enter author name:", "Enter code base directory:", "Enter unit-test-suite directory:"]

if settings.get("tests_on_right") == True:
    CLASS_WINDOW = 0
    TEST_WINDOW  = 1
else:
    CLASS_WINDOW = 1
    TEST_WINDOW  = 0

class FileCreator:
    KIND_IS_CLASS   = "class"
    KIND_IS_TEST    = "test"
    KIND_IS_DB_TEST = "dbTest"

    def __init__(self, basePath, relativeFileName = None, defaultFileExtension = "", templatesDir = ""):
        self.determineVersion(basePath, relativeFileName)
        self.set(basePath, relativeFileName, defaultFileExtension, templatesDir)

    def set(self, basePath, relativeFileName, defaultFileExtension, templatesDir):
        if relativeFileName is None:
            relativeFileName = basePath
        self.templatesDir = self.getStandardizedPath(templatesDir)
        self.tempBasePath = self.getStandardizedPath(basePath)
        if relativeFileName[0:1] == "/":
            self.tempBasePath = ""
        self.fileExtension = self.getFileExtension(relativeFileName, defaultFileExtension)
        self.relativeFileName = relativeFileName

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
                print(path[0:1])
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

    def getFileDir(self):
        fileDir = self.getParentDir() + "/" + self.getClassName() + self.getTestEnding() + self.fileExtension
        return fileDir

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
        if self.kind == FileCreator.KIND_IS_TEST:
            result = "Test"
        elif self.kind == FileCreator.KIND_IS_DB_TEST:
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

    def isTest(self, fileName):
        result = False
        temp = fileName[-4:]
        if temp == "Test":
            result = True
        return result

    def isDB_Test(self, fileName):
        result = False
        temp = fileName[-7:]
        if temp == "DB_Test":
            result = True
        return result

    def determineVersion(self, basePath, relativeFileName):
        if relativeFileName is None:
            relativeFileName = basePath
        fileName, fileExtension = os.path.splitext(relativeFileName)
        if self.isDB_Test(fileName):
            self.kind = FileCreator.KIND_IS_DB_TEST
        elif self.isTest(fileName):
            self.kind = FileCreator.KIND_IS_TEST
        else:
            self.kind = FileCreator.KIND_IS_CLASS

    def getBasePath(self):
        if self.kind == FileCreator.KIND_IS_TEST or self.kind == FileCreator.KIND_IS_DB_TEST:
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
            data = data.format(self.getNamespace(), className)
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

    def initialOpenFile(self, window, fileDir):
        leftColumnSize = settings.get("left_column_size")
        if fileDir is None:
            print("File Opening Failed.")
            return


        f = FileCreator(fileDir)

        fileExtension = f.fileExtension[1:]
        templateVariablesDir = FileCreator.getStandardizedPath(TEMPLATES_DIR) + fileExtension + "/" + f.kind + ".variables"
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
                variableValue = settings.get(variableName)
                if variableValue is not None:
                    variableCommand = templateVar["command"]
                    commandResult = eval(variableCommand + "(\"" + variableValue + "\", \"" + variableName + "\")")
                else:
                    commandResult = None
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
                replaced = False
                for variableName, replacementString in replacements.items():
                    searchString = "/* @" + variableName + " */"
                    if searchString in lineTemp:
                        replaced = True
                        if replacementString is not None:
                            index = lineTemp.find(searchString)
                            print(lineTemp[0:index] + replacementString + lineTemp[index + len(searchString):]),
                        else:
                            #column -= 1
                            pass
                if replaced == False:
                    print(lineTemp),
        openStatement = "%s:%d:%d" % (fileDir, line, column)
        import sublime

        if SPLIT_VIEW is True:
            sublime.active_window().run_command("set_layout", { "cols": [0.0, leftColumnSize, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1], [1, 0, 2, 1]] })
        else:
            sublime.active_window().run_command("set_layout", { "cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]] })

        if self.kind == self.KIND_IS_TEST or self.kind == self.KIND_IS_DB_TEST:
            if SPLIT_VIEW is True:
                sublime.active_window().run_command("focus_group", { "group": TEST_WINDOW })
        else:
            if SPLIT_VIEW is True:
                sublime.active_window().run_command("focus_group", { "group": CLASS_WINDOW })

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

            self.printToConsole("File " + fileDir + " created.")
            pass
        else:
            self.printToConsole("File " + fileDir + " opened.")
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
        if self.kind == FileCreator.KIND_IS_DB_TEST:
            classTemplateFileName = "/dbTest.template"
        elif self.kind == FileCreator.KIND_IS_TEST:
            classTemplateFileName = "/test.template"
        else:
            classTemplateFileName = "/class.template"
        return classTemplateFileName;

    def printToConsole(self, out):
        print("- FileCreator: " + out)


class Command():
    def __init__(self, commandString):
        self.commandString = commandString

    def run(self):
        process = subprocess.Popen(self.commandString, shell=True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
        returnCode = process.returncode
        return iter(process.stdout.readline, b'')

    def runAndPrintOutputLineByLine(self):
        for line in self.run():
            print(line.rstrip())

    def runAndGetOutputString(self):
        process = subprocess.Popen(self.commandString, shell=True, stdout = subprocess.PIPE)
        scriptResponse, scriptError = process.communicate()
        return scriptResponse

    def runAndPrintAllOutput(self):
        print(self.runAndGetOutputString())


class UserSettings():
    def __init__(self, fileName):
        self.fileName = fileName
        userSettingsExist = os.path.isfile(fileName)
        if userSettingsExist != True:
            fc = FileCreator(fileName)
            fc.create("{\n}")

    def set(self, variable, value):
        try:
            import json
            from pprint import pprint
            jsonData = open(self.fileName)
            settingsVariables = json.load(jsonData)
            jsonData.close()

            settingsVariables[variable] = value
            jsonData = json.dumps(settingsVariables)
            print(jsonData)
            fileHandle = open(self.fileName, "wb")
            fileHandle.write(jsonData);
            fileHandle.close()
        except Exception as e:
            print("Error when calling UserSettings.set():\n" + str(e))

    def deleteAll(self):
        os.remove(self.fileName)


class ClassesAndTestsCommand(sublime_plugin.WindowCommand):
    def run(self):
        userSettingsDir = FileCreator.getStandardizedPath(sublime.packages_path()) + "User/" + PACKAGE_NAME + ".sublime-settings"
        userSettingsExist = os.path.isfile(userSettingsDir)
        if userSettingsExist != True:
            self.userSettings = UserSettings(userSettingsDir)
            self.setUserSettings()
        else:
            self.displayNewFilePannel()

    def displayNewFilePannel(self):
        currentPath = SublimeWindowFunctions(self.window).getCurrentDirectory()

        caption = "Type in the name of a new file."
        initial = currentPath
        self.inputPanelView = self.window.show_input_panel(
            caption, initial,
            self.on_done, self.on_change, self.on_cancel
        )
        self.inputPanelView.tempInputPanelContent = currentPath
        self.inputPanelView.set_name("InputPannel")
        self.inputPanelView.settings().set("caret_style", "solid")

    def setUserSettings(self):
        userSettingsDir = FileCreator.getStandardizedPath(sublime.packages_path()) + "User/" + PACKAGE_NAME + ".sublime-settings"
        userSettingsExist = os.path.isfile(userSettingsDir)
        self.userInput = USER_SETTINGS_TO_BE_INITIALIZED
        self.userInputResponse = []
        self.userInputCaption = USER_SETTINGS_TO_BE_INITIALIZED_PROMPTS
        self.currentInput = 0
        if userSettingsExist == True:
            self.captureInput(self.userInputCaption[self.currentInput], "")
        else:
            print("Error trying to write to " + userSettingsDir)

    def captureInput(self, caption, initial):
        if self.currentInput != None:
            self.inputPanelView = self.window.show_input_panel(
                caption, initial,
                self.settingEntered, self.settingEnteringChange, self.settingEnteringAbort
            )
            self.inputPanelView.set_name("InputPannel")
            self.inputPanelView.settings().set("caret_style", "solid")
            pass

    def settingEntered(self, command_string):
        self.userInputResponse.append(command_string)
        self.currentInput += 1
        if self.currentInput < len(self.userInput):
            self.captureInput(self.userInputCaption[self.currentInput], "")
        else:
            for x in range(0,len(self.userInput)):
                if len(self.userInputResponse[x]) > 0:
                    self.userSettings.set(self.userInput[x], self.userInputResponse[x])
            view = self.window.active_view()
            view.erase_status("ClassesAndTests")
            self.displayNewFilePannel()

    def settingEnteringChange(self, command_string):
        view = self.window.active_view()
        view.set_status("ClassesAndTests", command_string)

    def settingEnteringAbort(self):
        self.userSettings.deleteAll()
        view = self.window.active_view()
        view.erase_status("ClassesAndTests")

    def on_done(self, command_string):
        view = self.window.active_view()
        view.erase_status("ClassesAndTests")

        fc = FileCreator(settings.get('base_path'), command_string, settings.get('default_file_extension'), TEMPLATES_DIR)
        fileDir = fc.createFromTemplate()
        if fileDir is None:
            fileDir = fc.create()
        fc.initialOpenFile(self.window, fileDir)

        # create corresponding test or source files
        if fc.kind == fc.KIND_IS_CLASS:
            if settings.get("create_tests_for_source_files") == True:
                fc.kind = FileCreator.KIND_IS_TEST
                fileDir = fc.createFromTemplate()
                fc.initialOpenFile(self.window, fileDir)
                pass
            pass
        elif fc.kind == fc.KIND_IS_TEST or fc.kind == fc.KIND_IS_DB_TEST:
            if settings.get("create_source_for_test_files") == True:
                fc.kind = FileCreator.KIND_IS_CLASS
                fileDir = fc.createFromTemplate()
                fc.initialOpenFile(self.window, fileDir)

    # TODO: Has an issue when clearing the whole input line....
    def detectBackOneFolder(self, newInputPanelContent):
        result = False
        if hasattr(self, 'inputPanelView'):
            newLength = len(newInputPanelContent)
            oldLength = len(self.inputPanelView.tempInputPanelContent)
            if newLength < oldLength:
                lastChar = self.inputPanelView.tempInputPanelContent[-1:]
                if lastChar == "/":
                    result = True
        return result

    def on_change(self, command_string):
        if hasattr(self, 'inputPanelView'):
            if self.inputPanelView is not None:
                backOneFolder = self.detectBackOneFolder(command_string)
                if backOneFolder == True:
                    window = self.inputPanelView.window()
                    self.inputPanelView.tempInputPanelContent = ""
                    window.run_command("manipulate_input_panel")
                else:
                    self.inputPanelView.tempInputPanelContent = command_string
                    basePath = settings.get("base_path")
                    fc = FileCreator(basePath, command_string, settings.get("default_file_extension"))
                    if len(command_string) > len(basePath):
                        possiblyBasePath = command_string[0:len(basePath)]
                        sublime.status_message(possiblyBasePath + " " + basePath)
                        if possiblyBasePath == basePath:
                            newCommandString = command_string[len(basePath):]
                            window = self.inputPanelView.window()
                            if window is not None:
                                window.run_command("replace_input_panel_content", {"replacementString": newCommandString})
                                command_string = command_string[len(basePath):]
                    statusMessage = "Creating file: " + fc.getFileDir()
                    view = self.window.active_view()
                    view.set_status("ClassesAndTests", statusMessage)
                    #sublime.status_message(statusMessage)

    def on_cancel(self):
        view = self.window.active_view()
        view.erase_status("ClassesAndTests")
        pass

    def printToConsole(self, out):
        print("- " + PACKAGE_NAME + ": " + out)


class SublimeWindowFunctions():
    def __init__(self, windowInstance):
        self.windowInstance = windowInstance
    def getCurrentDirectory(self):
        view = self.windowInstance.active_view()
        fileFolder = view.file_name()
        result = None
        if fileFolder is not None:
            fileFolder = os.path.dirname(fileFolder)
            fc = FileCreator(settings.get('base_path'), "")
            fc.kind = FileCreator.KIND_IS_TEST
            fc2 = FileCreator("", fileFolder)
            fc2.kind = FileCreator.KIND_IS_TEST
            basePath = fc.getBasePath()
            pathName = fc2.getBasePath()
            basePathLen = len(basePath)
            fileBeginning = pathName[0:basePathLen]
            if fileBeginning == basePath:
                pathName = pathName[basePathLen:]
                result = pathName
                if len(result) > 0:
                    result += "/"
        if result is None:
            result = FileCreator.getStandardizedPath(settings.get('current_path'), False, True)
            if result is None:
                result = ""
        return result.replace('//', '/') # TODO: This is a lazy fix for // appearing when not current_path was provided

    def getCurrentFileName(self):
        view = self.windowInstance.active_view()
        fileName = view.file_name()
        index = fileName.rfind("/")
        result = fileName[index + 1:]
        return result


class ManipulateInputPanelCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                lineRegion = self.view.line(region)
                lineText = self.view.substr(lineRegion)
                if len(lineText) > 0:
                    index = lineText.rfind('/');
                    newLine = lineText[0:index + 1]
                    if len(newLine) < 1:
                        newLine = settings.get('base_path')
                    self.view.replace(edit, lineRegion, newLine)
                    self.newLine = newLine


class ReplaceInputPanelContentCommand(sublime_plugin.TextCommand):
    def run(self, edit, replacementString):
        for region in self.view.sel():
            if region.empty():
                lineRegion = self.view.line(region)
                self.view.replace(edit, lineRegion, replacementString)


class ToggleSourceTestCommand(sublime_plugin.WindowCommand):
    def run(self):
        leftColumnSize = settings.get("left_column_size")
        if SPLIT_VIEW is True:
            sublime.active_window().run_command("set_layout", { "cols": [0.0, leftColumnSize, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1], [1, 0, 2, 1]] })
        else:
            sublime.active_window().run_command("set_layout", { "cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]] })

        currentPath = SublimeWindowFunctions(self.window).getCurrentDirectory()
        currentFileName = SublimeWindowFunctions(self.window).getCurrentFileName()
        fc = FileCreator(settings.get('base_path'), currentPath + currentFileName)
        if fc.kind == fc.KIND_IS_TEST or fc.kind == fc.KIND_IS_DB_TEST:
            fc.kind = fc.KIND_IS_CLASS
            if SPLIT_VIEW is True:
                sublime.active_window().run_command("focus_group", { "group": CLASS_WINDOW })
        else:
            fc.kind = fc.KIND_IS_TEST
            if SPLIT_VIEW is True:
                sublime.active_window().run_command("focus_group", { "group": TEST_WINDOW })
        fileDir = fc.getFileDir()
        if fileDir is not None:
            if os.path.isfile(fileDir) != True:
                createdFile = fc.createFromTemplate()
                if createdFile is not None:
                    fc.initialOpenFile(self.window, fileDir)
            else:
                fc.openFile(self.window, fileDir)
                self.window.run_command("exit_insert_mode")
        else:
            print("toggle_source_test experienced an error.")
        sublime.active_window().run_command("hide_panel", {"panel": "console"})


class OutputPanel():
    def run(self):
        pass
    def __init__(self, window, panelName):
        self.window = window
        self.panelName = panelName
        if not hasattr(self, 'outputView'):
            packageDir = FileCreator.getStandardizedPath(PACKAGE_DIR)
            tmLanguageDir = packageDir + PACKAGE_NAME + ".tmLanguage"
            colorTheme = settings.get("color_theme")
            tmThemeDir = packageDir + "colorThemes/" + PACKAGE_NAME + "_"
            self.outputView = self.window.get_output_panel(panelName)
            self.outputView.settings().set(panelName, True)
            self.outputView.set_syntax_file(tmLanguageDir)
            if colorTheme == "color":
                tmThemeDir +=  colorTheme + ".tmTheme"
                self.outputView.settings().set("color_scheme", tmThemeDir)
            self.outputView.settings().set("font_size", settings.get("output_font_size"))
            self.outputView.settings().set("line_numbers", False)
        self.window.run_command("show_panel", {"panel": "output." + panelName})

    def printToPanel(self, text):
        self.outputView.set_read_only(False)
        edit = self.outputView.begin_edit()
        self.outputView.insert(edit, self.outputView.size(), text)
        self.outputView.end_edit(edit)
        self.outputView.set_read_only(True)


class runPhpUnitTestsCommand(sublime_plugin.WindowCommand):
    def run(self, run_test_suite = False):
        if run_test_suite == False:
            testsPath = SublimeWindowFunctions(self.window).getCurrentDirectory()
        else:
            testsPath = FileCreator.getStandardizedPath(settings.get("current_php_test_suite_dir"))
        self.runTests(testsPath)

    def runTests(self, testsPath):
        phpUnitDir = FileCreator.getStandardizedPath(settings.get("php_unit_binary_dir"))

        fc = FileCreator(settings.get('base_path'), testsPath)
        fc.kind = fc.KIND_IS_TEST

        testsPath = os.path.dirname(fc.getFileDir())
        commandString = phpUnitDir + "phpunit \"" + testsPath + "\""

        op = OutputPanel(self.window, "php_unit_output_panel")

        if settings.get("show_executed_command") == True:
            credits = PACKAGE_NAME + " " + PACKAGE_VERSION + " by Axel Ancona Esselmann"
            import datetime
            ts = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
            op.printToPanel(credits + "\n" + "\nExecuting on " + ts + ":\n$ " + commandString + "\n\nResult:\n")

        scriptResponse = Command(commandString).runAndGetOutputString()
        op.printToPanel(scriptResponse)

def get_doc_block_tag(value, name):
    if value is not None:
        return "@" + name + " " + value

def get_php_autoloader(value, name):
    if value is not None:
        if value[0:1] == "/":
            result = "require_once \"" + value + "\";"
        else:
            result = "require_once strstr(__FILE__, 'Test', true).'/" + value + "';"
    else:
        result = ""
    return result

