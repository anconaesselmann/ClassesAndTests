import unittest
import os

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..", "..", "..")))

from classes_and_tests.src.mocking.sublime import sublime

class sublimeTest(unittest.TestCase):
	def test___init__(self):
		obj = sublime()

	def test_set_and_load_settings(self):
		aSettingDir = "/MyProject/aSetting.sublime-settings"
		aSetting = {"setting1": "a Setting", "setting2": 5}
		sublime.setSettings(aSettingDir, aSetting)
		result = sublime.load_settings(aSettingDir)
		self.assertEqual(aSetting, result)

	def test_loading_non_existant_setting(self):
		aNonExistantSettingsDir = "/MyProject/aSetting.sublime-settings"
		result = sublime.load_settings(aNonExistantSettingsDir)
		self.assertEqual({}, result)
		errors = sublime.getErrors()
		self.assertEqual(aNonExistantSettingsDir, errors[0])

	def test_get_packagePath(self):
		expected = os.path.join("A", "mock", "packages", "path")
		result = sublime.packages_path()
		self.assertEqual(expected, result)

	def test_set_get_active_window(self):
		activeWindow = "window"
		resultBefore = sublime.active_window()
		sublime.setActiveWindow(activeWindow)
		resultAfter = sublime.active_window()

		self.assertEqual(None, resultBefore)
		self.assertEqual(activeWindow, resultAfter)

if __name__ == '__main__':
    unittest.main()