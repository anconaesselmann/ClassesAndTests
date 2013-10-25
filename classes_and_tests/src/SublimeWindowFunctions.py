import os
import sublime
import sublime_plugin

try:
    from FileCreator import FileCreator
except ImportError:
    from .FileCreator import FileCreator



class SublimeWindowFunctions():
    def __init__(self, windowInstance, settings):
        self.windowInstance = windowInstance
        self.settings = settings

# This function is horrible!!!!
    def getCurrentDirectory(self):
        view = self.windowInstance.active_view()
        fileFolder = view.file_name()
        result = None
        if fileFolder is not None:
            fileFolder = os.path.dirname(fileFolder)
            fc = FileCreator(self.settings.get('base_path'), "")
            fc.kind = FileCreator.KIND_IS_TEST
            fc2 = FileCreator("", fileFolder)
            fc2.kind = FileCreator.KIND_IS_TEST
            basePath = fc.getBasePath()
            pathName = fc2.getBasePath()
            basePathLen = len(basePath)
            fileBeginning = pathName[0:basePathLen]
            if fileBeginning == basePath:
                pathName = pathName[basePathLen:]
                result = pathName
                if len(result) > 0:
                    result += "/"
        if result is None:
            result = FileCreator.getStandardizedPath(self.settings.get('current_path'), False, True)
            if result is None:
                result = ""
        return result.replace('//', '/') # TODO: This is a lazy fix for // appearing when not current_path was provided

#reexamine if still in use
    def getCurrentFileName(self):
        view = self.windowInstance.active_view()
        fileName = view.file_name()
        index = fileName.rfind("/")
        result = fileName[index + 1:]
        return result