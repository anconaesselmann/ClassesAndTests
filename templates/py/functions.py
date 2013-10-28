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

""" copy from general.functions """
def getSettingNameValuePair(settings):
    if not isinstance(settings, dict): # I could check for string, but I would break x-compatibility between python 2 and 3
        settings = eval(settings)
    #for key, value in settings.iteritems():
    for key, value in Std.getIterItems(settings):
        if value is not None:
            return key, value
    return None, None

def getRelativePath(baseDir, absDir):
    if baseDir is None:
        baseDir = ""
    rc = FileComponents(MirroredDirectory(absDir).getFileDir())
    rc.setBasePath(baseDir)
    relPath = rc.getRelativePath()

    # TODO: relative path should not return / at the front, check why it is doing this and remove this workaround
    if relPath[0:len(sep)] == sep:
        relPath = relPath[len(sep):]

    return relPath

def get_project_folder(args):
    fileName = MirroredDirectory(args["dir"]).getFile()
    varName, baseDir = getSettingNameValuePair(args["settings"])
    relPath = getRelativePath(baseDir, args["dir"])
    #print "inside get_project_folder:"
    #print "relPath: " + relPath
    result = ""
    while 1:
        relPath, tail = path.split(relPath)
        result += ", \"..\""
        if len(tail) < 1:
            return result


def get_py_package_name(args):
    fileName = MirroredDirectory(args["dir"]).getFile()

    varName, baseDir = getSettingNameValuePair(args["settings"])
    relPath = getRelativePath(baseDir, args["dir"])

    root = path.basename(path.normpath(baseDir))
    #print "root: " + root
    #print "relPath: " + relPath
    relPath = path.join(root, relPath, fileName)
    result = relPath.replace(sep, ".")
    if result[0:1] == ".":
        result = result[1:]

    return result