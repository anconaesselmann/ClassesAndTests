import os
import sublime
import sublime_plugin

from src.FileCreator import FileCreator
from src.MirroredDirectory import MirroredDirectory

DEBUG = True

PACKAGE_NAME = "ClassesAndTests"
PACKAGE_VERSION = "0.2.0"
PACKAGE_DIR = sublime.packages_path() + "/" + PACKAGE_NAME
settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')
TEMPLATES_DIR = PACKAGE_DIR + "/templates"
SPLIT_VIEW = settings.get("seperate_tests_and_sources_by_split_view")

if settings.get("tests_on_right") == True:
    CLASS_WINDOW = 0
    TEST_WINDOW  = 1
else:
    CLASS_WINDOW = 1
    TEST_WINDOW  = 0

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