from os import path, remove

try:
    from FileCreator import FileCreator
except ImportError:
    from .FileCreator import FileCreator
    from io import open

class UserSettings():
    def __init__(self, fileName):
        self.fileName = fileName
        userSettingsExist = path.isfile(fileName)
        if userSettingsExist != True:
            fc = FileCreator(fileName)
            fc.create("{\n}")

    def set(self, variable, value):
        try:
            import json
            from pprint import pprint
            jsonData = open(self.fileName)
            settingsVariables = json.load(jsonData)
            jsonData.close()

            settingsVariables[variable] = value
            jsonData = json.dumps(settingsVariables)
            print(jsonData)
            fileHandle = open(self.fileName, "wb")
            #fileHandle.write(jsonData);
            fileHandle.write(str.encode(jsonData));
            fileHandle.close()
        except Exception as e:
            print("Error when calling UserSettings.set():\n" + str(e))

    def deleteAll(self):
        remove(self.fileName)