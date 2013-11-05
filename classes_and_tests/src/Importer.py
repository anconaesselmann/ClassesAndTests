"""
@author Axel Ancona Esselmann

"""
import imp

class Importer():
    def __init__(self):
        pass

    @staticmethod
    def getObjectInstance(filePath, objectName):
        module = imp.load_source('tempObjects', filePath)
        obj = getattr(module, objectName)
        return obj


        