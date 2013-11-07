import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from classes_and_tests.ClassesAndTests import ClassesAndTestsCommand
from classes_and_tests.src.mocking.sublime import *
from classes_and_tests.src.mocking.MockFileManipulator import MockFileManipulator
from classes_and_tests.src.mocking.MockTemplateFileCreator import MockTemplateFileCreator
from classes_and_tests.src.mocking.MockMirroredDirectory import MockMirroredDirectory

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

    def _getFileManipulatorWithTestDir_helper(self):
        testDir = os.path.join(os.sep, "MyProject", "library", "aaeTest")
        mockFileManipulator = MockFileManipulator()
        mockFileManipulator.createFile(os.path.join(testDir, "someTest.php")) #TODO: simplify once directories can be mocked

        return mockFileManipulator

    def _getrInstanceWithMockedDependencies(self):
    	fileName = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
    	mockFileCreatorReturns = {
    		fileName: ([(11, 15)], True)
    	}
    	mockFileManipulator = self._getFileManipulatorWithTestDir_helper()

        cats = ClassesAndTestsCommand()
        cats.fileManipulator = mockFileManipulator
        cats.mirroredDirectory = MockMirroredDirectory()
        cats.templateFileCreator = MockTemplateFileCreator(mockFileCreatorReturns)
        #cats.templateFileCreator.fileManipulator = mockFileManipulator
        cats.settings = self._getMockSettings_helper()

        return cats

    def _getMockSettings_helper(self):
    	settings = MockSettings()
    	settings.set("create_tests_for_source_files", True)
    	settings.set("create_source_for_test_files", True)
    	return settings

##################################################
#   TESTING _getTemplateFile, called in on_done  #
##################################################

    def test__getTemplateFile_create_the_file_from_template(self):
    	fileName = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
        cursors = [(11, 15)]

        cats = self._getrInstanceWithMockedDependencies()
        returnFileDir, returnCursor = cats._getTemplateFile(fileName)

        self.assertEqual(fileName, returnFileDir)
        self.assertEqual(cursors, returnCursor)

    def test__getTemplateFile_create_the_file_without_template(self):
    	fileName = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
        cursors = [(0, 0)]

        cats = self._getrInstanceWithMockedDependencies()
        cats.templateFileCreator.files = {
    		fileName: ([(11, 15)], False)
    	}
        resultFileDir, resultCursor = cats._getTemplateFile(fileName)
        resultFileCreated = cats.fileManipulator.isfile(fileName)

        self.assertEqual(fileName, resultFileDir)
        self.assertEqual(cursors, resultCursor)
        self.assertEqual(True, resultFileCreated)

    def test__getTemplateFile_file_exists(self):
    	fileName = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
        cursors = [(0, 0)]

        cats = self._getrInstanceWithMockedDependencies()
        cats.fileManipulator.createFile(fileName)
        returnFileDir, returnCursor = cats._getTemplateFile(fileName)

        self.assertEqual(fileName, returnFileDir)
        self.assertEqual(cursors, returnCursor)

    def test__getTemplateFile_fileName_is_None(self):
    	fileName = None
        cursors = None

        cats = self._getrInstanceWithMockedDependencies()
        returnFileDir, returnCursor = cats._getTemplateFile(fileName)

        self.assertEqual(fileName, returnFileDir)
        self.assertEqual(cursors, returnCursor)

###############################################################
#   TESTING _getCorrespondingTemplateFilePath, called in on_done  #
###############################################################
    def test__getCorrespondingTemplateFilePath_class_file_provided_test_file_createion_disabled(self):
    	fileName = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
    	settings = MockSettings()
    	settings.set("create_tests_for_source_files", False)
    	settings.set("create_source_for_test_files", True)
    	cats = self._getrInstanceWithMockedDependencies()
    	cats.settings = settings
    	cats.mirroredDirectory.setMockKind(fileName, "class")
    	result = cats._getCorrespondingTemplateFilePath(fileName)
    	self.assertEqual(None, result)

    def test__getCorrespondingTemplateFilePath_test_file_provided_class_file_createion_disabled(self):
    	fileName = os.path.join(os.sep, "MyProject", "library", "aaeTest", "mvc", "ControllerTest.php")
    	settings = MockSettings()
    	settings.set("create_tests_for_source_files", True)
    	settings.set("create_source_for_test_files", False)
    	cats = self._getrInstanceWithMockedDependencies()
    	cats.settings = settings
    	cats.mirroredDirectory.setMockKind(fileName, "test")
    	result = cats._getCorrespondingTemplateFilePath(fileName)
    	self.assertEqual(None, result)

    def test__getCorrespondingTemplateFilePath_class_file_provided_creating_test_file(self):
    	fileName = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
    	correspondingFileName = os.path.join(os.sep, "MyProject", "library", "aaeTest", "mvc", "ControllerTest.php")
    	cats = self._getrInstanceWithMockedDependencies()
    	cats.mirroredDirectory.setMockKind(fileName, "class")
    	cats.mirroredDirectory.setMockOriginalFileName(correspondingFileName)
    	
    	result = cats._getCorrespondingTemplateFilePath(fileName)
    	self.assertEqual(correspondingFileName, result)

    def test__getCorrespondingTemplateFilePath_test_file_provided_creating_class_file(self):
    	fileName = os.path.join(os.sep, "MyProject", "library", "aaeTest", "mvc", "ControllerTest.php")
    	correspondingFileName = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
    	cats = self._getrInstanceWithMockedDependencies()
    	cats.mirroredDirectory.setMockKind(fileName, "test")
    	cats.mirroredDirectory.setMockOriginalFileName(correspondingFileName)
    	
    	result = cats._getCorrespondingTemplateFilePath(fileName)
    	self.assertEqual(correspondingFileName, result)

if __name__ == '__main__':
    unittest.main()