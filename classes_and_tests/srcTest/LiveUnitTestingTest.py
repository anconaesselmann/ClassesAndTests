import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from src.LiveUnitTesting import LiveUnitTesting
from src.mocking.MockFileSystem import MockFileSystem
from src.mocking.sublime import MockSublimeView

class LiveUnitTestingTest(unittest.TestCase):
    def _getInstance(self):
        classFile = path.join(os.sep, "MyProject1", "library", "aae", "mvc", "Controller.php")
        testFile = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.php")
        mockFileSystem = MockFileSystem()
        mockFileSystem.createFolder(testFile)
        mockFileSystem.createFolder(classFile)

        commandFolders = dict()
        commandFolders["php"] = classFile = path.join(os.sep, "some", "folder")
        commandFolders["py"] = classFile = path.join(os.sep, "some", "other", "folder")

        lut = LiveUnitTesting(commandFolders)
        lut.fileSystem = mockFileSystem

        return lut

    def test___init__(self):
        lut = self._getInstance()

    def test__getTempFileDir_from_class_file(self):
        classFile = path.join(os.sep, "MyProject1", "library", "aae", "mvc", "Controller.php")
        expected = path.join(os.sep, "MyProject1", "library", "aae", "mvc", "____liveUnitTesting_Controller.php")
        
        mockCurrentView = MockSublimeView(classFile)
        lut = self._getInstance()
        lut._setActiveFile(mockCurrentView)

        tempFileDir = lut._getTempFileDir()
        self.assertEqual(expected, tempFileDir)

    def test__getTempFileDir_from_test_file(self):
        testFile = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.php")
        expected = path.join(os.sep, "MyProject1", "library", "aae", "mvc", "____liveUnitTesting_Controller.php")
        
        mockCurrentView = MockSublimeView(testFile)
        lut = self._getInstance()
        lut._setActiveFile(mockCurrentView)
        
        tempFileDir = lut._getTempFileDir()
        self.assertEqual(expected, tempFileDir)

    def test__getTempTestFileDir_from_class_file(self):
        classFile = path.join(os.sep, "MyProject1", "library", "aae", "mvc", "Controller.php")
        expected = path.join(os.sep, "MyProject1", "library", "aae", "mvc", "____liveUnitTesting_ControllerTest.php")
        
        mockCurrentView = MockSublimeView(classFile)
        lut = self._getInstance()
        lut._setActiveFile(mockCurrentView)

        tempFileDir = lut._getTempTestFileDir()
        self.assertEqual(expected, tempFileDir)

    def test__getTempTestFileDir_from_test_file(self):
        testFile = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.php")
        expected = path.join(os.sep, "MyProject1", "library", "aae", "mvc", "____liveUnitTesting_ControllerTest.php")
        
        mockCurrentView = MockSublimeView(testFile)
        lut = self._getInstance()
        lut._setActiveFile(mockCurrentView)
        
        tempFileDir = lut._getTempTestFileDir()
        self.assertEqual(expected, tempFileDir)
        
if __name__ == '__main__':
    unittest.main()