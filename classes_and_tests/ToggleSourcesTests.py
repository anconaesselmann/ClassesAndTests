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
        print("sublime and sublime_plugin not imported in " + __file__)
    else:
        DEBUG = False

def plugin_loaded():
    global settings
    global CLASS_WINDOW
    global TEST_WINDOW
    global PACKAGE_DIR
    global TEMPLATES_DIR
    settings = sublime.load_settings(PACKAGE_NAME + '.sublime-settings')
    if settings.get("tests_on_right") == True:
        CLASS_WINDOW = 0
        TEST_WINDOW  = 1
    else:
        CLASS_WINDOW = 1
        TEST_WINDOW  = 0
    PACKAGE_DIR = os.path.join(sublime.packages_path(), PACKAGE_NAME)
    TEMPLATES_DIR = os.path.join(PACKAGE_DIR, "templates")

try:
    from src.FileManipulator import FileManipulator
    from src.MirroredDirectory import MirroredDirectory
    from src.SublimeWindowManipulator import SublimeWindowManipulator
    from src.TemplateFileCreator import TemplateFileCreator
except ImportError:
    from .src.FileManipulator import FileManipulator
    from .src.MirroredDirectory import MirroredDirectory
    from .src.SublimeWindowManipulator import SublimeWindowManipulator
    from .src.TemplateFileCreator import TemplateFileCreator
else:
    plugin_loaded()



class ToggleSourcesTestsCommand(sublime_plugin.WindowCommand):
    def _initializeDependencies(self):
        # allows for unit testing by injecting a mocked instances of dependencies
        if not hasattr(self, "sublime"):
            self.sublime = sublime
        if not hasattr(self, "fileManipulator"):
            self.fileManipulator = FileManipulator()
        if not hasattr(self, "settings"):
            self.settings = settings
        if not hasattr(self, "templatesDir"):
            self.templatesDir = TEMPLATES_DIR
        if not hasattr(self, "templateFileCreator"):
            self.templateFileCreator = TemplateFileCreator("")
            self.templateFileCreator.setSettings(self.settings)
            self.templateFileCreator.setTemplateDir(self.templatesDir)
        if not hasattr(self, "windowManipulator"):
            self.windowManipulator = SublimeWindowManipulator(self.window, self.settings)

        self.splitView = self.settings.get("seperate_tests_and_sources_by_split_view")

    def run(self):
        if DEBUG: print("toggle_sources_tests called")
        self._initializeDependencies()

        currentFileName = self.getCurrentFileName()
        if currentFileName is not None:
            self.createColumns()
            toogledFileName = self.toggleFileName(currentFileName)
            self.giveColumnFocus(toogledFileName)
            return self.openWindow(toogledFileName)
        else:
            print("To toggle between test and class, save the current file.")
            return False
        #self.sublime.active_window().run_command("hide_panel", {"panel": "console"})


    def createColumns(self):
        leftColumnSize = settings.get("left_column_size")
        if self.splitView is True:
            self.sublime.active_window().run_command("set_layout", { "cols": [0.0, leftColumnSize, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1], [1, 0, 2, 1]] })
        else:
            self.sublime.active_window().run_command("set_layout", { "cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]] })

    def giveColumnFocus(self, fileName):
        fc = MirroredDirectory(fileName)
        if fc.getKind() == fc.KIND_IS_TEST or fc.getKind() == fc.KIND_IS_DB_TEST:
            if self.splitView is True:
                self.sublime.active_window().run_command("focus_group", { "group": TEST_WINDOW })
        else:
            if self.splitView is True:
                self.sublime.active_window().run_command("focus_group", { "group": CLASS_WINDOW })

    # returns a file directory and cursor position, or creates a file from template
    def getFileDirAndCursors(self, fileDir):
        cursors = [(0, 0)]
        if fileDir is not None:
            fileExists = self.fileManipulator.isfile(fileDir)
            if fileExists != True:
                if DEBUG: print("creating file: " + fileDir)
                self.templateFileCreator.set(fileDir)
                fileExists = self.templateFileCreator.createFromTemplate()
                if fileExists:
                    if DEBUG: print("file creation successfull")
                    fileDir = self.templateFileCreator.getFileName()
                    cursors = self.templateFileCreator.getCursors()
                else:
                    if DEBUG: print("file creation failed")
                    fileDir = None
            elif DEBUG is True: print("file " + fileDir + " exists")
        return fileDir, cursors

    def openWindow(self, fileDir):
        fileDir, cursors = self.getFileDirAndCursors(fileDir)
        if fileDir is not None:
            if DEBUG: print("opening file: " + fileDir)
            return self.windowManipulator.openFile(fileDir, cursors)
        else:
            print("toggle_sources_tests experienced an error.")
            return False

    def toggleFileName(self, fileName):
        md = MirroredDirectory(fileName)
        md.fileManipulator = self.fileManipulator
        return md.getToggledFileName()

    def getCurrentFileName(self):
        view = self.window.active_view()
        currentFileName = view.file_name()
        return currentFileName

