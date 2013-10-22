import os
import fileinput
import re
import sublime
import sublime_plugin

from src.FileCreator import FileCreator
#from src.FileComponents import FileComponents
from src.MirroredDirectory import MirroredDirectory
#from src.Std import Std
from src.OutputPanel import OutputPanel
#from src.Command import Command
from src.MultipleCommandExecutionThread import MultipleCommandExecutionThread
from src.CommandExecutionThread import CommandExecutionThread
from src.SublimeWindowFunctions import SublimeWindowFunctions
from src.LiveUnitTest import LiveUnitTest
from src.InputPanel import InputPanel

DEBUG = True


PACKAGE_NAME = "ClassesAndTests"
PACKAGE_VERSION = "0.2.0"
PACKAGE_DIR = sublime.packages_path() + "/" + PACKAGE_NAME
settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')
TEMPLATES_DIR = PACKAGE_DIR + "/templates"
SPLIT_VIEW = settings.get("seperate_tests_and_sources_by_split_view")

USER_SETTINGS_TO_BE_INITIALIZED = ["author", "base_path", "current_php_test_suite_dir"]
USER_SETTINGS_TO_BE_INITIALIZED_PROMPTS = ["Enter author name:", "Enter code base directory:", "Enter unit-test-suite directory:"]

INTERVAL_BETWEEN_CONTINUOUS_UNIT_TESTS = settings.get("interval_between_continuous_unit_tests")


if settings.get("tests_on_right") == True:
    CLASS_WINDOW = 0
    TEST_WINDOW  = 1
else:
    CLASS_WINDOW = 1
    TEST_WINDOW  = 0


class ClassesAndTestsCommand(sublime_plugin.WindowCommand):
    def run(self):
        userSettingsDir =  os.path.join(sublime.packages_path(), "User", PACKAGE_NAME + ".sublime-settings")
        userSettingsExist = os.path.isfile(userSettingsDir)
        if userSettingsExist != True:
            self.userSettings = UserSettings(userSettingsDir)
            self.setUserSettings()
        else:
            self.displayNewFilePannel()

    def displayNewFilePannel(self):
        currentPath = SublimeWindowFunctions(self.window, settings).getCurrentDirectory()
        if currentPath == "":
            currentPath = FileCreator.getStandardizedPath(settings.get("base_path"))

        caption = "Type in the name of a new file."
        initial = currentPath
        self.inputPanelView = self.window.show_input_panel(
            caption, initial,
            self.on_done, self.on_change, self.on_cancel
        )
        self.inputPanelView.tempInputPanelContent = currentPath
        self.inputPanelView.set_name("InputPanel")
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
            self.inputPanelView.set_name("InputPanel")
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

            # get settings that depend on other settings
            possibleTestSuitePath = FileCreator.getStandardizedPath(settings.get("base_path"), True, False) + "Test"
            print(possibleTestSuitePath)












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
        fc.initialOpenFile(self.window, fileDir, settings)

        # create corresponding test or source files
        if fc.kind == fc.KIND_IS_CLASS:
            if settings.get("create_tests_for_source_files") == True:
                fc.kind = FileCreator.KIND_IS_TEST
                fileDir = fc.createFromTemplate()
                fc.initialOpenFile(self.window, fileDir, settings)
                pass
            pass
        elif fc.kind == fc.KIND_IS_TEST or fc.kind == fc.KIND_IS_DB_TEST:
            if settings.get("create_source_for_test_files") == True:
                fc.kind = FileCreator.KIND_IS_CLASS
                fileDir = fc.createFromTemplate()
                fc.initialOpenFile(self.window, fileDir, settings)

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
        #listening = "noting"
        if hasattr(self, 'inputPanelView') and self.inputPanelView.window() is not None:
            if command_string == "":
                replacementString = FileCreator.getStandardizedPath(settings.get("base_path"))
                self.window.run_command("replace_input_panel_content", {"replacementString": replacementString})
                return
            backOneFolder = self.detectBackOneFolder(command_string)
            if backOneFolder == True:
                self.inputPanelView.tempInputPanelContent = ""
                self.window.run_command("remove_last_folder_from_input_panel")
            else:
                self.inputPanelView.tempInputPanelContent = command_string
                basePath = FileCreator.getStandardizedPath(settings.get("base_path"))
                fc = FileCreator(basePath, command_string, settings.get("default_file_extension"))
                if len(command_string) > len(basePath):
                    possiblyBasePath = command_string[0:len(basePath)]
                    sublime.status_message(possiblyBasePath + " " + basePath)
                    if possiblyBasePath == basePath:
                        newCommandString = command_string[len(basePath):]
                        self.window.run_command("replace_input_panel_content", {"replacementString": newCommandString})
                        command_string = command_string[len(basePath):]
                statusMessage = "Creating file: " + fc.getFileDir()
                view = self.window.active_view()
                view.set_status("ClassesAndTests", statusMessage)

    def on_cancel(self):
        view = self.window.active_view()
        view.erase_status("ClassesAndTests")
        pass

    def printToConsole(self, out):
        print("- " + PACKAGE_NAME + ": " + out)





class RemoveLastFolderFromInputPanelCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        ip = InputPanel(self.view, edit)
        newLine = ip.deleteUntil("/")
        if len(newLine) < 1:
            replacementString = FileCreator.getStandardizedPath(settings.get("base_path"))
            ip.replaceAllText(replacementString)


class ReplaceInputPanelContentCommand(sublime_plugin.TextCommand):
    def run(self, edit, replacementString):
        ip = InputPanel(self.view, edit)
        ip.replaceAllText(replacementString)


class ToggleSourceTestCommand(sublime_plugin.WindowCommand):
    def createColumns(self):
        leftColumnSize = settings.get("left_column_size")
        if SPLIT_VIEW is True:
            sublime.active_window().run_command("set_layout", { "cols": [0.0, leftColumnSize, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1], [1, 0, 2, 1]] })
        else:
            sublime.active_window().run_command("set_layout", { "cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]] })

    def giveColumnFocus(self, fileName):
        fc = MirroredDirectory(fileName)
        if fc.getKind() == fc.KIND_IS_TEST or fc.getKind() == fc.KIND_IS_DB_TEST:
            if SPLIT_VIEW is True:
                sublime.active_window().run_command("focus_group", { "group": TEST_WINDOW })
        else:
            if SPLIT_VIEW is True:
                sublime.active_window().run_command("focus_group", { "group": CLASS_WINDOW })

    def openWindow(self, fileDir):
        if fileDir is not None:
            fc = FileCreator(fileDir, None, "", TEMPLATES_DIR)
            if os.path.isfile(fileDir) != True:
                createdFile = fc.createFromTemplate()
                if createdFile is not None:
                    fc.initialOpenFile(self.window, fileDir, settings)
            else:
                fc.openFile(self.window, fileDir)
                self.window.run_command("exit_insert_mode")
        else:
            print("toggle_source_test experienced an error.")

    def toggleFileName(self, fileName):
        md = MirroredDirectory(fileName)
        return md.getToggledFileName()

    def getCurrentFileName(self):
        view = self.window.active_view()
        currentFileName = view.file_name()
        return currentFileName

    def run(self):
        currentFileName = self.getCurrentFileName()
        if currentFileName is not None:
            self.createColumns()
            toogledFileName = self.toggleFileName(currentFileName)
            self.giveColumnFocus(toogledFileName)
            self.openWindow(toogledFileName)
        else:
            print("To toggle between test and class, save the current file.")
        #sublime.active_window().run_command("hide_panel", {"panel": "console"})


class RunPhpUnitTestsCommand(sublime_plugin.WindowCommand):
    def run(self, run_test_suite = False):
        if run_test_suite == False:
            view = self.window.active_view() # ????
            fileName = view.file_name()
            if fileName is not None:
                md = MirroredDirectory(fileName)
                testsPath = md.getTestFileDir()
            else :
                print("Tests can only be run on files that have been saved.")
                return
        elif run_test_suite == True:
            testsPath = FileCreator.getStandardizedPath(settings.get("current_php_test_suite_dir"))
        else:
            testsPath = run_test_suite
        self.runTests(testsPath)

    def runTests(self, testsPath):
        phpUnitDir = os.path.normpath(settings.get("php_unit_binary_dir")) + os.sep
        commandString = phpUnitDir + "phpunit \"" + testsPath + "\""
        self.outputPanel = OutputPanel(self.window, "php_unit_output_panel", PACKAGE_NAME)
        if settings.get("show_executed_command") == True:
            credits = PACKAGE_NAME + " " + PACKAGE_VERSION + " by Axel Ancona Esselmann"
            import datetime
            ts = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
            self.outputPanel.printToPanel(credits + "\n" + "\nExecuting on " + ts + ":\n$ " + commandString + "\n\nResult:\n")
        thread = CommandExecutionThread(commandString)
        thread.start()
        self.handleCommandThread(thread)

    def handleCommandThread(self, thread):
        if thread.is_alive():
            sublime.set_timeout(lambda: self.handleCommandThread(thread), 100)
        else:
            self.outputPanel.printToPanel( thread.result )

























class CreateMissingFunctionsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.classView = self.view # possibly try to find the classes view
        self.edit = edit

        self._runUnitTest()

    def _runUnitTest(self):
        if DEBUG:
            print("Running tests to determine if all functions have been declared:")
        classView = self.classView
        liveUnitTest = LiveUnitTest(settings.get("php_unit_binary_dir"))
        liveUnitTest.updateTempFiles(classView)
        commandString = liveUnitTest.getCommandString()

        thread = CommandExecutionThread(commandString)
        thread.start()
        self._handleCommandThread(thread)

    def _handleCommandThread(self, thread):
        if thread.is_alive():
            sublime.set_timeout(lambda: self._handleCommandThread(thread), 100)
        else:
            functionName = self._getFunctionName(thread.result)
            if functionName is not None:
                self._insertFunction(functionName)
            else:
                if DEBUG:
                    print("No functions have to be declared.")

    def _getFunctionName(self, testResult):
        matches = re.findall("(?<=Fatal\\serror:)(?:[\\s\\w\\\\]+undefined\\smethod)(?:[\\s\\w\\\\]+::)([\\w]+)(?=\\(\\))", testResult)
        if len(matches) > 0:
            result = matches[0]
        else:
            result = None
        return result

    def _insertFunction(self, functionName):
        classView = self.classView

        region = classView.find("\\}[^\\}]*\\}[^\\}]*\\z", 0)
        if region is not None:
            #print classView.substr(region)
            insertionPoint = region.begin()
            indentation = classView.substr(classView.line(insertionPoint))[:-1] # fails when some idiot does some wacky formatting that puts code on the same line before or after the closing bracket of a class
            classView.insert(self.edit, insertionPoint, self._getFunctionBody(functionName, indentation))


            sublime.set_timeout(lambda: self._runUnitTest(), 100)
        else:
            print("File is not formatted correctly. A class{} needs to be inside a namespace{}")

    def _getFunctionBody(self, functionName, indent):
        if DEBUG:
            print("Creating function \"" + functionName + "()\"")
        indent2 = indent + indent
        indent3 = indent2 + indent

        out =  "\n"
        out += indent2 + "public function " + functionName + "() {\n"
        out += indent3 + "return ;\n"
        out += indent2 + "}\n"
        out += indent

        return out










continuousUnitTestingThread = None


class ContinuousUnitTestingCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.outputPanel = OutputPanel(self.view.window(), "php_unit_output_panel", PACKAGE_NAME)
        self.liveUnitTest = LiveUnitTest(settings.get("php_unit_binary_dir"))

        self.initCommandThread()
        self.liveUnitTest.updateTempFiles(self.view)
        self.outputProgramStart()
        self.runTests()

    def runTests(self):
        view = sublime.active_window().active_view()
        self.liveUnitTest.updateTempFiles(view)
        self.updateCommandThread()
        self.handleCommandThread()

    def initCommandThread(self):
        global continuousUnitTestingThread
        if continuousUnitTestingThread is None:
            continuousUnitTestingThread = MultipleCommandExecutionThread()
            print "Starting continuousUnitTestingThread"
            continuousUnitTestingThread.start()

    def updateCommandThread(self):
        global continuousUnitTestingThread
        continuousUnitTestingThread.setCommandString(self.liveUnitTest.getCommandString())

    def outputProgramStart(self):
        if settings.get("show_executed_command") == True:
            credits = PACKAGE_NAME + " " + PACKAGE_VERSION + " by Axel Ancona Esselmann"
            import datetime
            ts = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
            self.outputPanel.printToPanel(credits + "\n" + "\nExecuting on " + ts + ":\n$ " + self.liveUnitTest.getCommandString() + "\n\nResult:\n")

    def handleCommandThread(self):
        global continuousUnitTestingThread
        if continuousUnitTestingThread.is_alive():
            if not continuousUnitTestingThread.hasRun():
                sublime.set_timeout(lambda: self.handleCommandThread(), 100)
            else:
                viewPosition = self.outputPanel.getViewPosition()
                #viewPosition = (0, 100)
                #print "viewPosition: " + str(viewPosition)
                self.outputPanel.clear()
                #self.outputPanel.printToPanel("Tests for " + self.liveUnitTest.activeFile.getFileName() + ": ")
                self.outputPanel.printToPanel("Tests for " + self.liveUnitTest.activeFile.getFileName() + ": "+ str(continuousUnitTestingThread.getResult()))
                #print "view positint is loading: " + str(self.outputPanel.outputView.is_loading())
                self.outputPanel.setViewPosition(viewPosition)
                continuousUnitTestingThread.reset()
                if self.outputPanel.isVisible():
                    sublime.set_timeout(lambda: self.runTests(), INTERVAL_BETWEEN_CONTINUOUS_UNIT_TESTS)







