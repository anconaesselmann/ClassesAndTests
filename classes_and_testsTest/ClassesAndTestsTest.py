import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from classes_and_tests.ClassesAndTests import ClassesAndTestsCommand
from classes_and_tests.src.mocking.sublime import *

class ClassesAndTestsTest(unittest.TestCase):
	def test___init__(self):
		obj = ClassesAndTestsCommand()

	def test_getCurrentPath(self):
		fileName = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
		expected = os.path.join(os.sep, "MyProject", "library", "aae", "mvc") + os.sep
		mockedActiveView = MockSublimeView()
		mockedActiveView.fileName = fileName

		mockSublimeWindow = MockSublimeWindow()
		mockSublimeWindow.activeView = mockedActiveView

		cats = ClassesAndTestsCommand()
		cats.window = mockSublimeWindow
		result = cats.getCurrentPath()

		self.assertEqual(expected, result)

	def _getCurrentPath_helper(self, fileName, expected):
		mockedActiveView = MockSublimeView()
		mockedActiveView.fileName = fileName

		mockSublimeWindow = MockSublimeWindow()
		mockSublimeWindow.activeView = mockedActiveView

		mockSettings = MockSettings()
		mockSettings.set("base_path", expected)

		cats = ClassesAndTestsCommand()
		cats.window = mockSublimeWindow
		cats.settings = mockSettings
		result = cats.getCurrentPath()

		self.assertEqual(expected, result)

	def test_getCurrentPath_file_not_saved(self):
		fileName = None
		expected = os.path.join(os.sep, "Default", "path") + os.sep
		
		self._getCurrentPath_helper(fileName, expected)

	def test_getCurrentPath_empty_input(self):
		fileName = ""
		expected = os.path.join(os.sep, "Default", "path") + os.sep
		
		self._getCurrentPath_helper(fileName, expected)

	

if __name__ == '__main__':
    unittest.main()