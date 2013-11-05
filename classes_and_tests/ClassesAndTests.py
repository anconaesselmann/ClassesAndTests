import os
import sublime
import sublime_plugin

DEBUG = True

PACKAGE_NAME = "ClassesAndTests"
PACKAGE_VERSION = "0.2.0"

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
    def run(self):
        self.windowManipulator = SublimeWindowManipulator(self.window, settings)
        self.fileManipulator = FileManipulator()

        userSettingsDir =  os.path.join(sublime.packages_path(), "User", PACKAGE_NAME + ".sublime-settings")
        userSettingsExist = os.path.isfile(userSettingsDir)
        if userSettingsExist != True:
            self.userSettings = UserSettings(userSettingsDir)
            self.setUserSettings()
        else:
            self.displayNewFilePannel()

    def displayNewFilePannel(self):
#currentPath = SublimeWindowFunctions(self.window, settings).getCurrentDirectory()
        currentPath = self.window.active_view().file_name()
        if currentPath == "":
            currentPath = os.path.normpath(settings.get("base_path"))

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
        fileDir = None
        view = self.window.active_view()
        view.erase_status("ClassesAndTests")

        if DEBUG:
            print("command_string in ClassesAndTests.on_done:")
            print(command_string)
        fc = TemplateFileCreator(command_string)
        fc.setBasePath(settings.get('base_path'))
        fc.setSettings(settings)
        fc.setDefaultExtension(settings.get('default_file_extension'))
        fc.setTemplateDir(TEMPLATES_DIR)
        if DEBUG:
            print("file name in ClassesAndTests.on_done:")
            print(fc.getFileName())
        fileCreated = fc.createFromTemplate()
        if fileCreated:
            fileDir = fc.getFileName()
            cursors = fc.getCursors()

        else:
            fileCreated = self.fileManipulator.createFile(command_string)
            fileDir = command_string
            cursors = [(0, 0)]

        if fileCreated:
            self.windowManipulator.openFile(fileDir, cursors)
        else:
            print("File " + command_string + " could not be created.")
            return


        #fc.initialOpenFile(self.window, fileDir, settings)

        # create corresponding test or source files
        if fc.classifyKind() == MirroredDirectory.KIND_IS_CLASS:
            if settings.get("create_tests_for_source_files") == True:
                if DEBUG: print("ClassesAndTestsCommand: creating corresponding test file")
                fc.setKind(MirroredDirectory.KIND_IS_TEST)
                fileCreated = fc.createFromTemplate()
        elif fc.classifyKind() == MirroredDirectory.KIND_IS_TEST or fc.getKind() == MirroredDirectory.KIND_IS_DB_TEST:
            if settings.get("create_source_for_test_files") == True:
                if DEBUG: print("ClassesAndTestsCommand: creating corresponding class file")
                fc.setKind(MirroredDirectory.KIND_IS_CLASS)
                fileCreated = fc.createFromTemplate()

        if fileCreated:
            if DEBUG: print("ClassesAndTestsCommand: file creation successful, opening file: " + fc.getFileName())
            self.windowManipulator.openFile(fc.getFileName(), fc.getCursors())

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
