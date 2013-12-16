DEBUG = False
UNIT_TEST_DEBUG = False

PACKAGE_NAME = "ClassesAndTests"
PACKAGE_VERSION = "0.5.0"

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
    TEMPLATES_DIR = os.path.join(PACKAGE_DIR, "templates")

try:
    from src.TemplateFileCreator import TemplateFileCreator
    from src.FileComponents import FileComponents
    from src.InputPanel import InputPanel
    from src.SublimeWindowManipulator import SublimeWindowManipulator
    from src.FileSystem import FileSystem
    from src.MirroredDirectory import MirroredDirectory
    from src.Std import Std
    from src.UserSettingsSetter import UserSettingsSetter
except ImportError:
    from .src.TemplateFileCreator import TemplateFileCreator
    from .src.FileComponents import FileComponents
    from .src.InputPanel import InputPanel
    from .src.SublimeWindowManipulator import SublimeWindowManipulator
    from .src.FileSystem import FileSystem
    from .src.MirroredDirectory import MirroredDirectory
    from .src.Std import Std
    from .src.UserSettingsSetter import UserSettingsSetter
else:
    plugin_loaded()

USER_SETTINGS_TO_BE_INITIALIZED = ["author", "base_path", "php_autoloader_path"]
USER_SETTINGS_TO_BE_INITIALIZED_PROMPTS = ["Enter author name:", "Enter default directory:", "If auto-loading php classes, provide path to autoloader class file:"]

class ClassesAndTestsCommand(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        sublime_plugin.WindowCommand.__init__(self, *args, **kwargs)

    def _initializeDependencies(self):
        if not hasattr(self, "sublime"):
            self.sublime = sublime
        if not hasattr(self, "settings"):
            self.settings = settings
        if not hasattr(self, "windowManipulator"):
            self.windowManipulator = SublimeWindowManipulator(self.window, self.settings)
        if not hasattr(self, "fileSystem"):
            self.fileSystem = FileSystem()
        if not hasattr(self, "mirroredDirectory"):
            self.mirroredDirectory = MirroredDirectory()
        if not hasattr(self, "templateFileCreator"):
            self.templateFileCreator = TemplateFileCreator()

        self.mirroredDirectory.fileSystem = self.fileSystem
        self.mirroredDirectory.setDefaultExtension(self.settings.get('default_file_extension'))

        self.splitView = self.settings.get("seperate_tests_and_sources_by_split_view")

        self.templateFileCreator.fileSystem = self.fileSystem
        self.templateFileCreator.setSettings(self.settings)
        self.templateFileCreator.setDefaultExtension(self.settings.get('default_file_extension'))
        self.templateFileCreator.setTemplateDir(TEMPLATES_DIR)
        #self.templateFileCreator.setBasePath(self.settings.get('base_path')))

    def run(self):
        self._initializeDependencies()

        userSettingsDir =  os.path.join(sublime.packages_path(), "User", PACKAGE_NAME + ".sublime-settings")
        userSettingsExist = os.path.isfile(userSettingsDir)
        if userSettingsExist != True:
            self.setUserSettings()
        else:
            self.displayNewFilePannel()

    def setUserSettings(self):
        userSettingsDir = os.path.join(os.path.normpath(sublime.packages_path()), "User", PACKAGE_NAME + ".sublime-settings")
        userSettingsSetter = UserSettingsSetter(self.window,
                                                userSettingsDir,
                                                USER_SETTINGS_TO_BE_INITIALIZED,
                                                USER_SETTINGS_TO_BE_INITIALIZED_PROMPTS)
        userSettingsSetter.setCallbackWhenFinished(self.displayNewFilePannel)

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
            self._createPythonPackageFiles(fileDir)

            compFileDirTemp = self._getCorrespondingTemplateFilePath(fileDir)
            compFileDir, compFileCursors = self._getTemplateFile(compFileDirTemp)
        else:
            print("File " + fileName + " could not be created.")

        if compFileDir is not None:
            if DEBUG: print("ClassesAndTestsCommand: file creation successful, opening file: " + self.templateFileCreator.getFileName())
            self.windowManipulator.openFile(compFileDir, compFileCursors)
            self._createPythonPackageFiles(compFileDir)
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
            if not self.fileSystem.isfile(fileName):
                fileCreated = self.templateFileCreator.createFromTemplate()
                if fileCreated:
                    fileDir = self.templateFileCreator.getFileName()
                    cursors = self.templateFileCreator.getCursors()
                else:
                    if DEBUG: print("ClassesAndTestsCommand: No templates, creating empty file.")
                    fileCreated = self.fileSystem.createFile(fileName)
                    if fileCreated:
                        fileDir = fileName
                        cursors = [(0, 0)]
            else:
                if DEBUG: print("ClassesAndTestsCommand: File exists, just open.")
                fileDir = fileName
                cursors = [(0, 0)]

        return fileDir, cursors

    # Unit Tested (general case, no possible failures except non py file)
    def _createPythonPackageFiles(self, fileName):
        if DEBUG: print("ClassesAndTestsCommand: Creating py package file.")
        self.mirroredDirectory.set(fileName)
        extension = self.mirroredDirectory.getExtension()
        kind = self.mirroredDirectory.getKind()
        if extension == "py" and kind == MirroredDirectory.KIND_IS_CLASS:
            if DEBUG: print("ClassesAndTestsCommand: is py file: " + fileName)
            basePath = self.mirroredDirectory.getBasePath()
            basePathParent = os.path.dirname(basePath) #TODO: throws exception with test files
            relativeFileName = self.mirroredDirectory.getRelativeFileName()
            root = os.path.basename(os.path.normpath(basePath))
            relativeFileNameWithoutExt, ext = os.path.splitext(relativeFileName)
            untreatedPackageName = os.path.join(root, relativeFileNameWithoutExt)
            packageFoldersString = os.path.dirname(untreatedPackageName)
            packageFolders = Std.dirExplode(packageFoldersString)
            packageFolders.reverse()

            workingDir = basePathParent
            while len(packageFolders) > 0:
                currentDir = packageFolders.pop()
                workingDir = os.path.join(workingDir, currentDir)
                tempFileName = os.path.join(workingDir, "__init__.py")
                if not self.fileSystem.isfile(tempFileName):
                    if DEBUG: print ("ClassesAndTestsCommand: Creating package file: " + tempFileName)
                    self.fileSystem.createFile(tempFileName, "")
                else:
                    if DEBUG: print("ClassesAndTestsCommand: py file exists.")

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
                #print(fc.getFileName())
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

