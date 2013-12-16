"""
@author Axel Ancona Esselmann

"""
DEBUG = False

import os
try:
    import sublime
    import sublime_plugin
except:
    if DEBUG:
        print("sublime and sublime_plugin not imported in " + __file__)

try:
    from MirroredDirectory import MirroredDirectory
except ImportError:
    from .MirroredDirectory import MirroredDirectory

class SublimeWindowManipulator():
    def __init__(self, windowInstance, settings):
        self._windowInstance = windowInstance
        self._settings = settings

    def openFile(self, fileDir, cursors=None):
        if cursors is None:
            cursors = [(0,0)]
        fileComponents = MirroredDirectory(fileDir)
        if self._settings.get("tests_on_right") == True:
            classWindow = 0
            testWindow  = 1
        else:
            classWindow = 1
            testWindow  = 0

        leftColumnSize = self._settings.get("left_column_size")
        if leftColumnSize is None: # TODO: also check if between 0 and 1
            leftColumnSize = 0.5

        splitView = self._settings.get("seperate_tests_and_sources_by_split_view")
        if splitView is True:
            #sublime.active_window().run_command("set_layout", { "cols": [0.0, leftColumnSize, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1], [1, 0, 2, 1]] })
            sublime.active_window().run_command("set_layout", { "cols": [0.0, leftColumnSize, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1], [1, 0, 2, 1]] })
        else:
            #sublime.active_window().run_command("set_layout", { "cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]] })
            sublime.active_window().run_command("set_layout", { "cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]] })

        if fileComponents.getKind() == fileComponents.KIND_IS_TEST or fileComponents.getKind() == fileComponents.KIND_IS_DB_TEST:
            if splitView is True:
                #sublime.active_window().run_command("focus_group", { "group": testWindow })
                sublime.active_window().run_command("focus_group", { "group": testWindow })
        else:
            if splitView is True:
                #sublime.active_window().run_command("focus_group", { "group": classWindow })
                sublime.active_window().run_command("focus_group", { "group": classWindow })

        line, column = cursors[0]
        openStatement = "%s:%d:%d" % (fileComponents.getOriginalFileName(), line, column)
        if DEBUG: print("SublimeWindowManipulator: opening file '" + openStatement + "'")
        openedFile = sublime.active_window().open_file(openStatement, sublime.ENCODED_POSITION)
        return openedFile