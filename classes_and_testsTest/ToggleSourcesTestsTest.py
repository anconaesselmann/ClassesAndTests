import unittest
import os
from cStringIO import StringIO
import sys
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from classes_and_tests.ToggleSourcesTests import ToggleSourcesTestsCommand
from classes_and_tests.src.mocking.sublime import *
from classes_and_tests.src.mocking.MockFileManipulator import MockFileManipulator
from classes_and_tests.src.mocking.MockTemplateFileCreator import MockTemplateFileCreator
from classes_and_tests.src.mocking.MockSublimeWindowManipulator import MockSublimeWindowManipulator

class ToggleSourcesTestsCommandTest(unittest.TestCase):
	def test___init__(self):
		obj = ToggleSourcesTestsCommand()
	
	def test_run_with_no_file_name(self):
		expectedOutput = 'TSTC: To toggle between test and class, save the current file.\n'
		tst = ToggleSourcesTestsCommand()
		mockSublimeWindow = MockSublimeWindow()
		tst.window = mockSublimeWindow

		old_stdout = sys.stdout
		sys.stdout = mystdout = StringIO()

		tst.run()
		
		sys.stdout = old_stdout

		self.assertEqual(expectedOutput, mystdout.getvalue())


	def test_toggleFileName_no_test_folder(self):
		aFileName = os.path.join(os.sep, "User", "Projects", "MyProject", "codeBase", "src", "aae", "mvc", "Controller.php")
		fileNameResult = os.path.join(os.sep, "User", "Projects", "MyProject", "codeBase", "src", "aae", "mvc", "ControllerTest.php")
		mockFileManipulator = MockFileManipulator()
		tst = ToggleSourcesTestsCommand()
		tst.fileManipulator = mockFileManipulator
		result = tst.toggleFileName(aFileName)
		self.assertEqual(fileNameResult, result)

	def test_toggleFileName_class_to_test(self):
		aFileName = os.path.join(os.sep, "User", "Projects", "MyProject", "codeBase", "src", "aae", "mvc", "Controller.php")
		fileNameResult = os.path.join(os.sep, "User", "Projects", "MyProject", "codeBase", "srcTest", "aae", "mvc", "ControllerTest.php")
		mockFileManipulator = MockFileManipulator()
		mockFileManipulator.createFile(fileNameResult)
		tst = ToggleSourcesTestsCommand()
		tst.fileManipulator = mockFileManipulator
		result = tst.toggleFileName(aFileName)
		self.assertEqual(fileNameResult, result)

	def test_toggleFileName_test_to_class(self):
		aFileName = os.path.join(os.sep, "User", "Projects", "MyProject", "codeBase", "srcTest", "aae", "mvc", "ControllerTest.php")
		fileNameResult = os.path.join(os.sep, "User", "Projects", "MyProject", "codeBase", "src", "aae", "mvc", "Controller.php")
		mockFileManipulator = MockFileManipulator()
		mockFileManipulator.createFile(fileNameResult)
		tst = ToggleSourcesTestsCommand()
		tst.fileManipulator = mockFileManipulator
		result = tst.toggleFileName(aFileName)
		self.assertEqual(fileNameResult, result)


	def test_getFileDirAndCursors_file_exists(self):
		aFileName = os.path.join(os.sep, "User", "Projects", "MyProject", "codeBase", "src", "aae", "mvc", "Controller.php")
		mockFileManipulator = MockFileManipulator()
		mockFileManipulator.createFile(aFileName)
		tst = ToggleSourcesTestsCommand()
		tst.fileManipulator = mockFileManipulator
		resultFileName, resultCursors = tst.getFileDirAndCursors(aFileName)
		self.assertEqual(aFileName, resultFileName)
		self.assertEqual([(0, 0)], resultCursors)

	def test_getFileDirAndCursors_file_dosent_exist(self):
		aFileName = os.path.join(os.sep, "User", "Projects", "MyProject", "codeBase", "src", "aae", "mvc", "Controller.php")
		cursors = [(0, 0)]
		mockFileManipulator = MockFileManipulator()
		tst = ToggleSourcesTestsCommand()
		tst.fileManipulator = mockFileManipulator
		tst.templateFileCreator = MockTemplateFileCreator({aFileName: (cursors, True)})
		resultFileName, resultCursors = tst.getFileDirAndCursors(aFileName)
		self.assertEqual(aFileName, resultFileName)
		self.assertEqual(cursors, resultCursors)

	def _run_helper(self, file1, file2, cursors):
		tst = ToggleSourcesTestsCommand()

		mockFileManipulator = MockFileManipulator()

		mockedActiveView = MockSublimeView()
		mockedActiveView.fileName = file1

		mockSublimeWindow = MockSublimeWindow()
		mockSublimeWindow.activeView = mockedActiveView

		mockSublimeWindowManipulator = MockSublimeWindowManipulator()

		mockSublime = sublime
		mockSublime.setActiveWindow(mockSublimeWindow)
		
		tst.window = mockSublimeWindow
		tst.sublime = mockSublime
		tst.fileManipulator = mockFileManipulator
		tst.templateFileCreator = MockTemplateFileCreator({file2: (cursors, True)})
		tst.windowManipulator = mockSublimeWindowManipulator
		
		tst.run()
		
		#assert that test file was opened with the given cursors
		self.assertEqual(file2, mockSublimeWindowManipulator.fileOpened)
		self.assertEqual(cursors, mockSublimeWindowManipulator.cursors)

#TODO: Make this test pass!	
	def test_run_class_file_open_creates_test_file(self):
		theClassFileName = os.path.join(os.sep, "User", "Projects", "MyProject", "codeBase", "src", "aae", "mvc", "Controller.php")
		theTestFileName = os.path.join(os.sep, "User", "Projects", "MyProject", "codeBase", "srcTest", "aae", "mvc", "ControllerTest.php")
		cursors = [(11, 19)]	

		self._run_helper(theClassFileName, theTestFileName, cursors)

	def test_run_test_file_open_creates_class_file(self):
		theClassFileName = os.path.join(os.sep, "User", "Projects", "MyProject", "codeBase", "src", "aae", "mvc", "Controller.php")
		theTestFileName = os.path.join(os.sep, "User", "Projects", "MyProject", "codeBase", "srcTest", "aae", "mvc", "ControllerTest.php")
		cursors = [(11, 19)]	

		self._run_helper(theTestFileName, theClassFileName, cursors)

if __name__ == '__main__':
    unittest.main()