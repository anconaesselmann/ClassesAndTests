import sublime
import sublime_plugin
from os import path

PACKAGE_NAME = "ClassesAndTests"

def plugin_loaded():
    global settings
    settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')

try:
    from src.UnitTestFunctions import UnitTestFunctions
    from src.MirroredDirectory import MirroredDirectory
except ImportError:
    from .src.UnitTestFunctions import UnitTestFunctions
    from .src.MirroredDirectory import MirroredDirectory
else:
    plugin_loaded()

globalInitiatingFile = None

# sometimes seems to be ignored by reloader. Restart sublime when updating!
class SyncronizeClosingClassAndTestTabsListener(sublime_plugin.EventListener):
    def on_close(self, view):
        global globalInitiatingFile
        print("called tab_syncronization_closes_files")
        if view is not None and self._settingsAllow():
            if UnitTestFunctions.classHasTest(view):
                fileNameActiveView = view.file_name()
                if globalInitiatingFile == fileNameActiveView:
                    return
                else:
                    globalInitiatingFile = fileNameActiveView
                md = MirroredDirectory(fileNameActiveView)
                fileName = md.getFileName()
                testFileName = md.getTestFileName()
                if fileNameActiveView == fileName:
                    fileNameInactiveView = testFileName
                else:
                    fileNameInactiveView = fileName
                windows = sublime.windows()
                success = self._closeFileInWindows(fileNameInactiveView, windows)
                if success:
                    return True

    def _settingsAllow(self):
        return ((settings.get("tab_syncronization_closes_files") == True) and (settings.get("seperate_tests_and_sources_by_split_view") == True))


    def _closeFileInWindows(self, fileName, windows):
        if windows is not None:
            for window in windows:
                views = window.views()
                success = self._closeFileInViews(fileName, views, window)
                if success:
                    return True
        return False

    def _closeFileInViews(self, fileName, views, window):
        if views is not None:
            for view in views:
                tempFileName = view.file_name()
                if tempFileName == fileName:
                    print("closing" + fileName)
                    sublime.set_timeout(lambda: self._closeTab(window, view), 100)
                    #self._closeTab(window, view) #crashes when called without timeout....
                    return True
        return False

    def _closeTab(self, window, view):
        global globalInitiatingFile
        group, index = window.get_view_index(view)
        window.run_command("close_by_index", { "group": group, "index": index })