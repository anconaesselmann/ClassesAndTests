DEBUG = False
UNIT_TEST_DEBUG = False

PACKAGE_NAME = "ClassesAndTests"

from os import path
try:
    import sublime
    import sublime_plugin
except ImportError:
    from mocking.sublime import sublime
    from mocking import sublime_plugin
    if UNIT_TEST_DEBUG: 
        DEBUG = True
        print("UnitTestFunctions: sublime and sublime_plugin not imported in " + __file__)
    else:
        DEBUG = False

def plugin_loaded():
    global settings
    global PACKAGE_DIR
    global TEMPLATES_DIR
    settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')
    PACKAGE_DIR = path.join(sublime.packages_path(), PACKAGE_NAME)
    TEMPLATES_DIR = path.join(PACKAGE_DIR, "templates")

try:
    from MirroredDirectory import MirroredDirectory
except ImportError:
    from .MirroredDirectory import MirroredDirectory
else:
    plugin_loaded()

class UnitTestFunctions:
    @staticmethod
    def getCommandFolders(settingsFile):
        phpUnitDir = path.normpath(settingsFile.get("php_unit_binary_dir"))
        if phpUnitDir[-7:] == "phpunit":
            phpUnitDir = phpUnitDir[:-7]


        pythonDir = settingsFile.get("python_dir")
        if pythonDir is not None:
            pythonDir = path.normpath(pythonDir)
        else:
            pythonDir = ""

        return {
                    "php": phpUnitDir,
                    "py": pythonDir,
                    "js": ""
                }

    @staticmethod
    def getCommand(extension):
        extTemplateDir = path.join(TEMPLATES_DIR, extension)
        if path.exists(extTemplateDir):
            return path.join(extTemplateDir, "testRunner");
        else:
            return None


    @staticmethod
    def classHasTest(view):
        result = False
        if view is not None:
            viewFileName = view.file_name()
            if viewFileName is not None:
                md = MirroredDirectory(viewFileName)
                classFileName = md.getFileName()
                testFileName = md.getTestFileName()
                #print(classFileName)
                #print(testFileName)
                #print(path.isfile(classFileName))
                #print(path.isfile(testFileName))
                if path.isfile(classFileName) and path.isfile(testFileName):
                    result = True
        return result

    @staticmethod
    def bringViewsToFront(window, view, openingFilesAllowed=True):
        if not UnitTestFunctions.classHasTest(view):
            if DEBUG: print("UnitTestFunctions: file does not have a complement.")
            return
        fileNameActiveView = view.file_name()
        md = MirroredDirectory(fileNameActiveView)
        classFileName = md.getFileName()
        testFileName = md.getTestFileName()
        #print(classFileName)
        #print(testFileName)

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
            window.run_command("toggle_sources_tests")
        window.focus_view(view)

    @staticmethod
    def getClassView(window, view):
        classView = None
        classFileName = MirroredDirectory(view.file_name()).getFileName()
        if view.file_name == classFileName:
            classView = view
        else:
            for tempView in window.views():
                file_name = tempView.file_name()
                if file_name == classFileName:
                    classView = tempView
                    break
        return classView