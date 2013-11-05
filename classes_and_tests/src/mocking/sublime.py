"""
@author Axel

"""
import os

settings = dict()
error = []
activeWindow = None

class sublime():
    def __init__(self):
        pass
    
    @staticmethod
    def setSettings(aSettingDir, aSetting):
    	global settingis
        settings[aSettingDir] = aSetting
    
    @staticmethod
    def load_settings(aSettingDir):
    	global settings
    	try:
        	return settings[aSettingDir]
    	except Exception as e:
    		global error
    		error.append(aSettingDir)
    		return {}

    @staticmethod
    def getErrors():
    	global error
    	return error
    
    @staticmethod
    def packages_path():
        return os.path.join("A", "mock", "packages", "path")


    @staticmethod
    def active_window():
        global activeWindow
        return activeWindow
    
    @staticmethod
    def setActiveWindow(window):
        global activeWindow
        activeWindow = window

class MockSublimeWindow:
    def __init__(self, activeView=None):
        if activeView is None:
            self.activeView = MockSublimeView()
        else:
            self.activeView = activeView

    def active_view(self):
        return self.activeView

    def run_command(self, *args):
        pass

    def open_file(self, aPath):
        pass

class MockSublimeView:
    def __init__(self, fileName=None):
        self.fileName = fileName

    def file_name(self):
        return self.fileName


class MockSettings:
    def __init__(self):
        self._settings = dict()

    def set(self, varName, varValue):
        self._settings[varName] = varValue

    def get(self, varName):
        return self._settings[varName]
    