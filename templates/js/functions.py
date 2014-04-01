"""
@author Axel Ancona Esselmann

"""
DEBUG = True
from os import sys, path, sep
sys.path.append(path.abspath(path.join(__file__, "..", "..", "..", "classes_and_tests")))

try:
    from src.Std import Std
    from src.MirroredDirectory import *
    from src.FileSystem import FileSystem
except ImportError:
    from .src.Std import Std
    from .src.MirroredDirectory import *
    from .src.FileSystem import FileSystem

class FunctionCollection(object):


    def __init__(self):
        self.fileSystem = FileSystem()

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
