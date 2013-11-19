"""
@author Axel Ancona Esselmann
"""
import os

try:
    import sublime
except ImportError:
    from mocking.sublime import sublime

try:
    from UserSettings import UserSettings
    from FileSystem import FileSystem
    from Std import Std
except ImportError:
    from .UserSettings import UserSettings
    from .FileSystem import FileSystem
    from .Std import Std

class UserSettingsSetter():
    def __init__(self, window, fileName, userInput, userInputCaption):
        self.window = window
        self.fileSystem = FileSystem()
        self.fileName = fileName
        self.userInput = userInput
        self.userInputCaption = userInputCaption
        self.callback = None

        self.setUserSettings()

    def setCallbackWhenFinished(self, callback):
        self.callback = callback
    
    def setUserSettings(self):
        self.userSettings = UserSettings(self.fileName, self.fileSystem)
        userSettingsExist = self.fileSystem.isfile(self.fileName)

        self.userInputResponse = []
        self.currentInput = 0
        if userSettingsExist == True:
            self.captureInput(self.userInputCaption[self.currentInput], "")
        else:
            print("Error trying to write to " + self.fileName)

    def captureInput(self, caption, initial):
        if self.currentInput != None:
            self.inputPanelView = self.window.show_input_panel(
                caption, initial,
                self.settingEntered, self.settingEnteringChange, self.settingEnteringAbort
            )
            self.inputPanelView.set_name("InputPanel")
            self.inputPanelView.settings().set("caret_style", "solid")
            pass

    def settingEntered(self, command_string):
        self.userInputResponse.append(command_string)
        self.currentInput += 1
        if self.currentInput < len(self.userInput):
            self.captureInput(self.userInputCaption[self.currentInput], "")
        else:
            for x in range(0,len(self.userInput)):
                if len(self.userInputResponse[x]) > 0:
                    self.userSettings.set(self.userInput[x], self.userInputResponse[x])
            view = self.window.active_view()
            view.erase_status("InputPanel")

            if self.callback is not None:
                sublime.set_timeout(lambda: self.callback(), 100)

    def settingEnteringChange(self, command_string):
        view = self.window.active_view()
        view.set_status("InputPanel", command_string)

    def settingEnteringAbort(self):
        self.userSettings.deleteAll()
        view = self.window.active_view()
        view.erase_status("InputPanel")