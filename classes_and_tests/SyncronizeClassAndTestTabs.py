DEBUG = False
UNIT_TEST_DEBUG = False

PACKAGE_NAME = "ClassesAndTests"

from os import path
import time
try:
    import sublime
    import sublime_plugin
except ImportError:
    from src.mocking.sublime import sublime
    from src.mocking import sublime_plugin
    if UNIT_TEST_DEBUG: 
        DEBUG = True
        print("SyncronizeClassAndTestTabsListener: sublime and sublime_plugin not imported in " + __file__)
    else:
        DEBUG = False

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

#globalSyncHelper = None

class SyncHelper:
    def __init__(self):
        self.hotFiles = dict()

    def fileIsHot(self, fileName):
        return fileName in self.hotFiles
    
    def setHotFile(self, fileName):
        self.hotFiles[fileName] = time.clock()

    def coolFile(self, fileName):
        if fileName in self.hotFiles:
            del self.hotFiles[fileName]



# sometimes seems to be ignored by reloader. Restart sublime when updating!
# TODO: issues with tests opening twice when starting up and tab_syncronization_opens_files is true
class SyncronizeClassAndTestTabsListener(sublime_plugin.EventListener):
    def _initiateDependencies(self, view):
        if not hasattr(self, "settings"):
            self.settings = settings
        if not hasattr(self, "syncHelper"):
            #global globalSyncHelper
            #if globalSyncHelper is None:
            #    globalSyncHelper = SyncHelper()
            #self.syncHelper = globalSyncHelper
            self.syncHelper = SyncHelper()
        if not hasattr(self, "view"):
            self.view = view
        if not hasattr(self, "sublime"):
            self.sublime = sublime

    def on_activated(self, view):
        self._initiateDependencies(view)
        if not self._openingIsEnabled(): return
        activeViewFileName = self._getActiveViewFileName(view)
        if activeViewFileName is None: return
        if self._fileIsHot(activeViewFileName): return
        activeWindow = self.sublime.active_window()
        if activeWindow is None: return
        if DEBUG: print("SyncronizeClassAndTestTabsListener: hot file: '" + activeViewFileName + "'")
        self._setHotFile(activeViewFileName)
        self.sublime.set_timeout(lambda: self.syncHelper.coolFile(activeViewFileName), 100)
        
        allowOpeningOfFiles = self.settings.get("tab_syncronization_opens_files")
        UnitTestFunctions.bringViewsToFront(activeWindow, view, allowOpeningOfFiles)

    def on_close(self, view):
        self._initiateDependencies(view)
        if not self._closingIsEnabled(): return

        activeViewFileName = self._getActiveViewFileName(view)
        if activeViewFileName is None: return
        if self._fileIsHot(activeViewFileName): return
        self._setHotFile(activeViewFileName)
        self.sublime.set_timeout(lambda: self.syncHelper.coolFile(activeViewFileName), 100)

        md = MirroredDirectory(activeViewFileName)
        fileName = md.getFileName()
        testFileName = md.getTestFileName()
        if activeViewFileName == fileName:
            fileNameInactiveView = testFileName
        else:
            fileNameInactiveView = fileName

        windows = sublime.windows()
        success = self._closeFileInWindows(fileNameInactiveView, windows)

    def _openingIsEnabled(self):
        return self.settings.get("tab_syncronization") is True and self.settings.get("seperate_tests_and_sources_by_split_view") is True
    
    def _closingIsEnabled(self):
        return self.settings.get("tab_syncronization_closes_files") is True and self.settings.get("seperate_tests_and_sources_by_split_view") is True

    def _getActiveViewFileName(self, view):
        activeViewFileName = None
        if view is not None:
            activeViewFileName = view.file_name()
        return activeViewFileName
    
    def _fileIsHot(self, fileName):
        return self.syncHelper.fileIsHot(fileName)
    
    def _setHotFile(self, fileName):
        self.syncHelper.setHotFile(fileName)

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
                    if DEBUG: print("SyncronizeClassAndTestTabsListener: closing" + fileName)
                    #self._closeTab(window, view)
                    sublime.set_timeout(lambda: self._closeTab(window, view), 100)
                    return True
        return False

    def _closeTab(self, window, view):
        global globalInitiatingFile
        group, index = window.get_view_index(view)
        window.run_command("close_by_index", { "group": group, "index": index })
    
    