"""
@author Axel Ancona Esselmann

"""
DEBUG = False
from os import sys, path, sep
sys.path.append(path.abspath(path.join(__file__, "..", "..", "..", "classes_and_tests")))

try:
    from src.Std import Std
    from src.MirroredDirectory import *
    from src.FileManipulator import FileManipulator
except ImportError:
    from .src.Std import Std
    from .src.MirroredDirectory import *
    from .src.FileManipulator import FileManipulator

class FunctionCollection(object):
    def __init__(self):
        self.fileManipulator = FileManipulator()
    
    def get_doc_block_tag(self, args):
        settings = eval(args["settings"])
        tagName, tagValue = Std.getSettingNameValuePair(settings)
        if tagValue is not None:
            result = "@" + tagName + " " + tagValue
        else:
            result = None
        return result
    
    def get_class_name(self, args):
        result = MirroredDirectory(args["dir"]).getFile()
        return result




    def get_project_folder(self, args):
        md = MirroredDirectory(args["dir"])
        relPath = md.getRelativePath()
        result = ""
        while 1:
            relPath, tail = path.split(relPath)
            result += ", \"..\""
            if len(tail) < 1:
                return result

    def get_py_package_name(self, args):
        result = None
        md = MirroredDirectory("")
        md.fileManipulator = self.fileManipulator
        md.set(args["dir"])
        relativeFileName = md.getRelativeFileName()
        basePath = md.getBasePath()
        if DEBUG: print("functions.py: relative path: " + relativeFileName)
        root = path.basename(path.normpath(basePath))
        relativeFileNameWithoutExt, ext = path.splitext(relativeFileName)
        untreatedPackageName = path.join(root, relativeFileNameWithoutExt)
        result = untreatedPackageName.replace(sep, ".")
        if DEBUG: print("functions.py: package name: " + result)
        return result