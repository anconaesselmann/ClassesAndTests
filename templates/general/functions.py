"""
@author Ancona Esselmann

"""
from os import sys, path
sys.path.append(path.abspath(path.join(__file__, "..", "..", "..", "classes_and_tests")))

try:
    from src.Std import Std
    from src.MirroredDirectory import MirroredDirectory
except ImportError:
    from .src.Std import Std
    from .src.MirroredDirectory import MirroredDirectory

def getSettingNameValuePair(settings):
    if not isinstance(settings, dict): # I could check for string, but I would break x-compatibility between python 2 and 3
        settings = eval(settings)
    for key, value in Std.getIterItems(settings):
        if value is not None:
            return key, value
    return None, None

def get_doc_block_tag(args):
    settings = eval(args["settings"])
    tagName, tagValue = getSettingNameValuePair(settings)
    if tagValue is not None:
        result = "@" + tagName + " " + tagValue
    else:
        result = None
    return result

def get_class_name(args):
    result = MirroredDirectory(args["dir"]).getFile()
    return result