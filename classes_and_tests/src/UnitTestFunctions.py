import sublime
import sublime_plugin
from os import path

class UnitTestFunctions:
	@staticmethod
	def getCommandFolders(settingsFile):
		return {
            		"php": path.normpath(settingsFile.get("php_unit_binary_dir")),
            		"py": path.normpath(settingsFile.get("python_dir"))
        		}