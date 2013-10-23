import os

class Std():
    @staticmethod
    def dirExplode(path):
        path = os.path.normpath(path)
        folders=[]
        while 1:
            path,folder=os.path.split(path)
            if folder!="":
                folders.append(folder)
            else:
                if path!="":
                    folders.append(path)
                break
        folders.reverse()
        return folders

    @staticmethod
    def dirImplode(array):
        path = ""
        for folder in array:
            if path != "":
                seperator = os.sep
            else:
                seperator = ""
            path = os.path.join(path, folder)
        return os.path.normpath(path)

    @staticmethod
    def isAllWhitespace(aString):
        return not bool(len(aString.strip()))