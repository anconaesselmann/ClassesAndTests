import fileinput
import os

from FileCreator import FileCreator

class FileManipulation():
    @staticmethod
    def getFileContent(fileDir):
        fileHandle = open(fileDir, 'r')
        content = fileHandle.read()
        fileHandle.close()
        return content

    @staticmethod
    def saveToFile(fileDir, content):
        fc = FileCreator(fileDir)
        fc.create(content)

    @staticmethod
    def replaceFile(fileDir, content):
        if os.path.isfile(fileDir):
            os.remove(fileDir)
        FileManipulation.saveToFile(fileDir, content)