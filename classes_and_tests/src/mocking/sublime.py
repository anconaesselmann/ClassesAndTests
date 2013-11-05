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
    