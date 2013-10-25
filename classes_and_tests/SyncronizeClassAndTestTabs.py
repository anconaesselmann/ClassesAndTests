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
    def plugin_loaded():
        global settings
        settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')
else:
    plugin_loaded()


globalActiveClassFileName = None
globalActiveTestFileName = None

# seems to be ignored by reloader. Restart sublime when updating!
# TODO: issues with tests opening twice when starting up and tab_syncronization_opens_files is true
class SyncronizeClassAndTestTabsListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        if settings.get("tab_syncronization") is True and settings.get("seperate_tests_and_sources_by_split_view") is True:
            if view is not None:
                global globalActiveClassFileName
                global globalActiveTestFileName
                fileNameActiveView = view.file_name()
                if fileNameActiveView is not None and fileNameActiveView != globalActiveClassFileName and fileNameActiveView != globalActiveTestFileName:
                    activeWindow = sublime.active_window()
                    if activeWindow is not None:
                        activeView = activeWindow.active_view()
                        if activeView is not None:
                            md = MirroredDirectory(fileNameActiveView)
                            globalActiveClassFileName = md.getFileName()
                            globalActiveTestFileName = md.getTestFileName()
                            allowOpeningOfFiles = settings.get("tab_syncronization_opens_files")
                            UnitTestFunctions.bringViewsToFront(activeWindow, view, allowOpeningOfFiles)