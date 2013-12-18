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



    def get_php_autoloader(self, args):
        settings = eval(args["settings"])
        result = None
        #for key, value in settings.iteritems():
        for key, value in Std.getIterItems(settings):
            if value is not None:
                if value[0:1] == "/":
                    result = "require_once \"" + value + "\";"
                else:
                    result = "require_once strstr(__FILE__, 'Test', true).'/" + value + "';"
            break

        return result


    def get_php_namespace(self, args):
        result = None
        md = MirroredDirectory("")
        md.fileSystem = self.fileSystem
        md.set(args["dir"])
        relativeFileName = md.getRelativeFileName()
        print(relativeFileName)
        if relativeFileName is not None:
            basePath = md.getBasePath()
            if DEBUG: print("functions.py: relative path: " + relativeFileName)
            untreatedNamespace, ext = path.split(relativeFileName)
            result = untreatedNamespace.replace(sep, "\\")
            if DEBUG: print("functions.py: package name: " + result)
        return result