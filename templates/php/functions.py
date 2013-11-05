"""
@author Axel Ancona Esselmann

"""
from os import sys, path, sep
sys.path.append(path.abspath(path.join(__file__, "..", "..", "..", "classes_and_tests")))

try:
    from src.Std import Std
    from src.FileComponents import FileComponents
    from src.MirroredDirectory import MirroredDirectory
except ImportError:
    from .src.Std import Std
    from .src.FileComponents import FileComponents
    from .src.MirroredDirectory import MirroredDirectory

class FunctionCollection(object):
    @staticmethod
    def getSettingNameValuePair(settings):
        if not isinstance(settings, dict): # I could check for string, but I would break x-compatibility between python 2 and 3
            settings = eval(settings)
        for key, value in Std.getIterItems(settings):
            if value is not None:
                return key, value
        return None, None

    @staticmethod
    def get_doc_block_tag(args):
        settings = eval(args["settings"])
        tagName, tagValue = FunctionCollection.getSettingNameValuePair(settings)
        if tagValue is not None:
            result = "@" + tagName + " " + tagValue
        else:
            result = None
        return result

    @staticmethod
    def get_class_name(args):
        result = MirroredDirectory(args["dir"]).getFile()
        return result





        
    @staticmethod
    def get_php_autoloader(args):
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

    @staticmethod
    def get_php_namespace(args):
        settings = eval(args["settings"])
        result = None
        base_dir = ""
        #for key, value in settings.iteritems():
        for key, value in Std.getIterItems(settings):
            if value is not None:
                base_dir = value
            break

        # TODO: make this part of MirroredDirecotry
        rc = FileComponents(MirroredDirectory(args["dir"]).getFileDir())
        rc.setBasePath(base_dir)
        relPath = rc.getRelativePath()

        result = relPath.replace(sep, "\\")
        if result[0:1] == "\\":
            result = result[1:]

        return result