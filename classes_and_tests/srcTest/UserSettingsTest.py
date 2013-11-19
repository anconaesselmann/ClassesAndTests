import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from src.UserSettings import UserSettings
from src.mocking.MockFileSystem import MockFileSystem

class UserSettingsTest(unittest.TestCase):
	def test___init__(self):
		obj = UserSettings()

	def test_setFile_create_file(self):
		aPath = os.path.join(os.path.sep, "a", "path", "UserSettings.settings")
		us = UserSettings()
		us.fileSystem = MockFileSystem()
		us.setFile(aPath)

		fileExists = us.fileSystem.isfile(aPath)

		self.assertEqual(True, fileExists)

	def test_set(self):
		settingVarName = "a_setting"
		settingValue = "a value"
		aPath = os.path.join(os.path.sep, "a", "path", "UserSettings.settings")
		us = UserSettings()
		us.fileSystem = MockFileSystem()
		us.setFile(aPath)

		us.set(settingVarName, settingValue)

		result = us.get(settingVarName)
		self.assertEqual(settingValue, result)

	

if __name__ == '__main__':
    unittest.main()