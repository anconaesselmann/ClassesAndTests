import sublime
import sublime_plugin
from os import path

from src.MirroredDirectory import MirroredDirectory

class UnitTestFunctions:
    @staticmethod
    def getCommandFolders(settingsFile):
        return {
                    "php": path.normpath(settingsFile.get("php_unit_binary_dir")),
                    "py": path.normpath(settingsFile.get("python_dir"))
                }

    @staticmethod
    def classHasTest(view):
        result = False
        if view is not None:
            viewFileName = view.file_name()
            if viewFileName is not None:
                md = MirroredDirectory(viewFileName)
                classFileName = md.getFileName()
                testFileName = md.getTestFileName()
                if path.isfile(classFileName) and path.isfile(testFileName):
                    result = True
        return result

    @staticmethod
    def bringViewsToFront(window, view, openingFilesAllowed=True):
        if not UnitTestFunctions.classHasTest(view):
            return
        fileNameActiveView = view.file_name()
        md = MirroredDirectory(fileNameActiveView)
        classFileName = md.getFileName()
        testFileName = md.getTestFileName()

        if fileNameActiveView == classFileName:
            fileNameInactiveView = testFileName
        else:
            fileNameInactiveView = classFileName

        views = window.views()
        inactiveViewIsOpen = False
        for tempView in views:
            file_name = tempView.file_name()
            if file_name == fileNameInactiveView:
                window.focus_view(tempView)
                inactiveViewIsOpen = True
                break
        if not inactiveViewIsOpen and openingFilesAllowed is True:
            window.run_command("toggle_source_test")
        window.focus_view(view)