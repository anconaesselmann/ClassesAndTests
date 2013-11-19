import json

try:
    from FileSystem import FileSystem
except ImportError:
    from .FileSystem import FileSystem
    from io import open

class UserSettings():
    def __init__(self, fileName=None, fileSystem=None):
        if fileSystem is not None:
            self.fileSystem = FileSystem()
        self._settingsVariables = dict()
        if fileName is not None:
            self.setFile(fileName)

    def set(self, variable, value):
        self._settingsVariables[variable] = value
        settingsNewContent = json.dumps(self._settingsVariables)

        return self.fileSystem.replaceFile(self.fileName, settingsNewContent)
    
    def get(self, variableName):
        return self._settingsVariables[variableName]

    def deleteAll(self):
        self.fileSystem.remove(self.fileName)

    def setFile(self, fileName):
        self.fileName = fileName
        userSettingsExist = self.fileSystem.isfile(fileName)
        if userSettingsExist != True:
            settingsContent = "{\n}"
            created = self.fileSystem.createFile(fileName, settingsContent)
        else:
            settingsContent = self.fileSystem.getFileContent(self.fileName)
        self._settingsVariables = json.loads(settingsContent)
    