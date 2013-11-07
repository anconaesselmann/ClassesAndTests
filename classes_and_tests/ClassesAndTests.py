DEBUG = True
UNIT_TEST_DEBUG = False

PACKAGE_NAME = "ClassesAndTests"
PACKAGE_VERSION = "0.2.0"

import os
try:
    import sublime
    import sublime_plugin
except ImportError:
    from src.mocking.sublime import sublime
    from src.mocking import sublime_plugin
    if UNIT_TEST_DEBUG: 
        DEBUG = True
        print("ClassesAndTestsCommand: sublime and sublime_plugin not imported in " + __file__)
    else:
        DEBUG = False


def plugin_loaded():
    global settings
    global PACKAGE_DIR
    global TEMPLATES_DIR
    settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')
    PACKAGE_DIR = os.path.join(sublime.packages_path(), PACKAGE_NAME)
    #PACKAGE_DIR = os.path.join("Packages", PACKAGE_NAME)
    TEMPLATES_DIR = os.path.join(PACKAGE_DIR, "templates")

try:
    from src.TemplateFileCreator import TemplateFileCreator
    from src.FileComponents import FileComponents
    from src.InputPanel import InputPanel
    from src.SublimeWindowFunctions import SublimeWindowFunctions
    from src.UserSettings import UserSettings
    from src.SublimeWindowManipulator import SublimeWindowManipulator
    from src.FileManipulator import FileManipulator
    from src.MirroredDirectory import MirroredDirectory
except ImportError:
    from .src.TemplateFileCreator import TemplateFileCreator
    from .src.FileComponents import FileComponents
    from .src.InputPanel import InputPanel
    from .src.SublimeWindowFunctions import SublimeWindowFunctions
    from .src.UserSettings import UserSettings
    from .src.SublimeWindowManipulator import SublimeWindowManipulator
    from .src.FileManipulator import FileManipulator
    from .src.MirroredDirectory import MirroredDirectory
else:
    plugin_loaded()


USER_SETTINGS_TO_BE_INITIALIZED = ["author", "base_path", "current_php_test_suite_dir"]
USER_SETTINGS_TO_BE_INITIALIZED_PROMPTS = ["Enter author name:", "Enter code base directory:", "Enter unit-test-suite directory:"]


class ClassesAndTestsCommand(sublime_plugin.WindowCommand):
    def _initializeDependencies(self):
        # allows for unit testing by injecting a mocked instances of dependencies
        if not hasattr(self, "sublime"):
            self.sublime = sublime
        if not hasattr(self, "settings"):
            self.settings = settings
        if not hasattr(self, "windowManipulator"):
            self.windowManipulator = SublimeWindowManipulator(self.window, settings)
        if not hasattr(self, "fileManipulator"):
            self.fileManipulator = FileManipulator()
        if not hasattr(self, "mirroredDirectory"):
            self.mirroredDirectory = MirroredDirectory()
            self.mirroredDirectory.setDefaultExtension(settings.get('default_file_extension'))
        if not hasattr(self, "templateFileCreator"):
            self.templateFileCreator = TemplateFileCreator()
            #self.templateFileCreator.setBasePath(settings.get('base_path'))
            self.templateFileCreator.setSettings(settings)
            self.templateFileCreator.setDefaultExtension(settings.get('default_file_extension'))
            self.templateFileCreator.setTemplateDir(TEMPLATES_DIR)

        self.splitView = self.settings.get("seperate_tests_and_sources_by_split_view")

    def run(self):
        self._initializeDependencies()

        userSettingsDir =  os.path.join(sublime.packages_path(), "User", PACKAGE_NAME + ".sublime-settings")
        userSettingsExist = os.path.isfile(userSettingsDir)
        if userSettingsExist != True:
            self.userSettings = UserSettings(userSettingsDir)
            self.setUserSettings()
        else:
            self.displayNewFilePannel()

    # Unit Tested
    def getCurrentPath(self):
        result = ""
        currentPath = self.window.active_view().file_name()
        if currentPath is None or currentPath == "":
            defaultPath = self.settings.get("base_path")
            if defaultPath is not None:
                result = os.path.normpath(defaultPath) + os.sep
        else:
            currentPath, fileName = os.path.split(currentPath)
            result = currentPath + os.sep
            
        return result

    def displayNewFilePannel(self):
        currentPath = self.getCurrentPath()
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
#TODO: change to path.join
        userSettingsDir = os.path.normpath(sublime.packages_path()) + "User/" + PACKAGE_NAME + ".sublime-settings"
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
            possibleTestSuitePath = os.path.normpath(settings.get("base_path"), True, False) + "Test"
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
        if DEBUG: print("ClassesAndTests: command_string in on_done:" + command_string)
        self._openFilesCreateIfNecessary(command_string)

    def _openFilesCreateIfNecessary(self, fileName):
        compFileDir = None
        fileDir, cursors = self._getTemplateFile(fileName)
        if fileDir is not None:
            if DEBUG: print("ClassesAndTestsCommand: file creation successful, opening file: " + self.templateFileCreator.getFileName())
            self.windowManipulator.openFile(fileDir, cursors)

            compFileDirTemp = self._getCorrespondingTemplateFilePath(fileDir)
            compFileDir, compFileCursors = self._getTemplateFile(compFileDirTemp)
        else:
            print("File " + fileName + " could not be created.")

        if compFileDir is not None:
            if DEBUG: print("ClassesAndTestsCommand: file creation successful, opening file: " + self.templateFileCreator.getFileName())
            self.windowManipulator.openFile(compFileDir, compFileCursors)
        else:
            print("Complementary file for " + fileName + " could not be created.")

    # Unit Tested
    def _getTemplateFile(self, fileName):
        fileCreated = False
        fileDir = None
        cursors = None
        if fileName is not None:
            self.templateFileCreator.set(fileName)
            if DEBUG: print("ClassesAndTestsCommand: _getTemplateFile fileName: '" + str(self.templateFileCreator.getFileName()) + "'")
            if not self.fileManipulator.isfile(fileName):
                fileCreated = self.templateFileCreator.createFromTemplate()
                if fileCreated:
                    fileDir = self.templateFileCreator.getFileName()
                    cursors = self.templateFileCreator.getCursors()
                else:
                    if DEBUG: print("ClassesAndTestsCommand: No templates, creating empty file.")
                    fileCreated = self.fileManipulator.createFile(fileName)
                    if fileCreated:
                        fileDir = fileName
                        cursors = [(0, 0)]
            else:
                if DEBUG: print("ClassesAndTestsCommand: File exists, just open.")
                fileDir = fileName
                cursors = [(0, 0)]

        return fileDir, cursors

    # Unit Tested
    def _getCorrespondingTemplateFilePath(self, fileName):
        if DEBUG: print("ClassesAndTestsCommand: corresponding file creation called for '" + fileName + "'")
        fileDir = None

        self.mirroredDirectory.set(fileName)
        if self.mirroredDirectory.getKind() == MirroredDirectory.KIND_IS_CLASS:
            if self.settings.get("create_tests_for_source_files") == True:
                self.mirroredDirectory.setKind(MirroredDirectory.KIND_IS_TEST)
                fileDir = self.mirroredDirectory.getOriginalFileName()
        elif self.mirroredDirectory.getKind() == MirroredDirectory.KIND_IS_TEST or self.mirroredDirectory.getKind() == MirroredDirectory.KIND_IS_DB_TEST:
            if self.settings.get("create_source_for_test_files") == True:
                self.mirroredDirectory.setKind(MirroredDirectory.KIND_IS_CLASS)
                fileDir = self.mirroredDirectory.getOriginalFileName()

        return fileDir


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
            """if command_string == "":
                replacementString = os.path.normpath(settings.get("base_path"))
                self.window.run_command("replace_input_panel_content", {"replacementString": replacementString})
                return"""
            backOneFolder = self.detectBackOneFolder(command_string)
            if backOneFolder == True:
                self.inputPanelView.tempInputPanelContent = ""
                self.window.run_command("remove_last_folder_from_input_panel")
            else:
                self.inputPanelView.tempInputPanelContent = command_string
                basePath = os.path.normpath(settings.get("base_path"))
                fc = FileComponents(command_string)
                try:
                    fc.setBasePath(basePath)
                except Exception as e:
                    pass
                fc.setDefaultExtension(settings.get("default_file_extension"))
                print(fc.getFileName())
                """if len(command_string) > len(basePath):
                    possiblyBasePath = command_string[0:len(basePath)]
                    sublime.status_message(possiblyBasePath + " " + basePath)
                    if possiblyBasePath == basePath:
                        newCommandString = command_string[len(basePath):]
                        self.window.run_command("replace_input_panel_content", {"replacementString": newCommandString})
                        command_string = command_string[len(basePath):]"""
                fileName = fc.getFileName()
                if fileName is not None:
                    statusMessage = "Creating file: " + fileName
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
            replacementString = os.path.normpath(settings.get("base_path"))
            ip.replaceAllText(replacementString)


class ReplaceInputPanelContentCommand(sublime_plugin.TextCommand):
    def run(self, edit, replacementString):
        ip = InputPanel(self.view, edit)
        ip.replaceAllText(replacementString)
    