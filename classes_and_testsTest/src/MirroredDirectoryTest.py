import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..", "..")))

from classes_and_tests.src.MirroredDirectory import MirroredDirectory
from classes_and_tests.src.mocking.MockFileManipulator import MockFileManipulator

class MirroredDirectoryTest(unittest.TestCase):
    
    def test___init__(self):
        aPath = os.path.join("a", "path", "to", "a", "file.php")
        obj = MirroredDirectory(aPath)

    def test__getExistingFileDir_no_test_folder_present(self):
        aFileName = os.path.join("a", "path", "to", "a", "file.php")
        aPath = os.path.join("a", "path", "to", "a")
        mockFileManipulator = MockFileManipulator()
        mockFileManipulator.createFile(aFileName, "")
        md = MirroredDirectory(aFileName)
        md.fileManipulator = mockFileManipulator
        result = md._getExistingFileDir("")
        self.assertEqual(aPath, result)
    
    def test__getExistingFileDir_get_test_file(self):
        aFileName = os.path.join("a", "path", "to", "a", "file.php")
        aTestFileName = os.path.join("a", "pathTest", "to", "a", "file.php")
        aPath = os.path.join("a", "pathTest", "to", "a")
        mockFileManipulator = MockFileManipulator()
        mockFileManipulator.createFile(aFileName, "")
        mockFileManipulator.createFile(aTestFileName, "")
        md = MirroredDirectory(aFileName)
        md.fileManipulator = mockFileManipulator
        result = md._getExistingFileDir("Test")
        self.assertEqual(aPath, result)
       
    #horribly messy, since my mock file createor is absolutely DUMB!!!
    def test__getExistingFileDir_get_test_file_multiple_test_folders(self):
        aFileName = os.path.join("a", "path", "to", "a", "file.php")
        aTestFileName1 = os.path.join("a", "path", "toTest", "a", "file.php")
        aTestFileName2 = os.path.join("a", "pathTest", "to", "a", "file.php")
        aPath = os.path.join("a", "path", "toTest", "a")
        mockFileManipulator = MockFileManipulator()
        mockFileManipulator.createFile(aFileName, "")
        mockFileManipulator.createFile(aTestFileName1, "")
        mockFileManipulator.createFile(aTestFileName2, "")
        md = MirroredDirectory(aFileName)
        md.fileManipulator = mockFileManipulator
        result = md._getExistingFileDir("Test")
        self.assertEqual(aPath, result)
    
    def test_getToggledFileName_class_to_test(self):
        aFileName = os.path.join("a", "path", "to", "a", "file.php")
        aTestFileName = os.path.join("a", "pathTest", "to", "a", "fileTest.php")
        mockFileManipulator = MockFileManipulator()
        mockFileManipulator.createFile(aFileName, "")
        mockFileManipulator.createFile(aTestFileName, "")
        md = MirroredDirectory(aFileName)
        md.fileManipulator = mockFileManipulator

        result = md.getToggledFileName();

        self.assertEqual(aTestFileName, result)
    
    def test_getToggledFileName_test_to_class(self):
        aFileName = os.path.join("a", "path", "to", "a", "file.php")
        aTestFileName = os.path.join("a", "pathTest", "to", "a", "fileTest.php")
        mockFileManipulator = MockFileManipulator()
        mockFileManipulator.createFile(aFileName, "")
        mockFileManipulator.createFile(aTestFileName, "")
        md = MirroredDirectory(aTestFileName)
        md.fileManipulator = mockFileManipulator

        result = md.getToggledFileName();

        self.assertEqual(aFileName, result)

    def test_find_base_path(self):
        aFileName = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
        testDir = os.path.join(os.sep, "MyProject", "libraryTest")

        expectedBasePath = os.path.join(os.sep, "MyProject", "library")
        expectedRelativePath = os.path.join("aae", "mvc")

        mockFileManipulator = MockFileManipulator()
        mockFileManipulator.createFile(os.path.join(testDir, "someFileTest.php"), "") #TODO: replace once directories can be mocked

        md = MirroredDirectory(aFileName)
        md.fileManipulator = mockFileManipulator

        md._discoverBasePath()

        resultBasePath = md.getBasePath()
        resultRelativePath = md.getRelativePath()

        self.assertEqual(expectedBasePath, resultBasePath)
        self.assertEqual(expectedRelativePath, resultRelativePath)

    def test__discoverBasePath_with_relative_path_provided(self):
        aFileName = os.path.join("MyProject", "library", "aae", "mvc", "Controller.php")
        testDir = os.path.join("MyProject", "libraryTest")

        expectedRelativePath = os.path.join("MyProject", "library", "aae", "mvc")
        expectedBasePath = None

        mockFileManipulator = MockFileManipulator()
        mockFileManipulator.createFile(os.path.join(testDir, "someFileTest.php"), "") #TODO: replace once directories can be mocked

        md = MirroredDirectory(aFileName)
        md.fileManipulator = mockFileManipulator

        md._discoverBasePath()

        resultBasePath = md.getBasePath()
        resultRelativePath = md.getRelativePath()

        self.assertEqual(expectedBasePath, resultBasePath)
        self.assertEqual(expectedRelativePath, resultRelativePath)

    def test_getFileDir_with_empty_dir(self):
        aFileName = ""
        md = MirroredDirectory(aFileName)
        result = md.getFileDir()

        self.assertEqual(None, result)

    def test_getFileName_with_empty_dir(self):
        aFileName = ""
        md = MirroredDirectory(aFileName)
        result = md.getFileName()

        self.assertEqual(None, result)

    def test_getTestFileName_with_empty_dir(self):
        aFileName = ""
        md = MirroredDirectory(aFileName)
        result = md.getTestFileName()

        self.assertEqual(None, result)

    def test_getTestFileName_from_class_file_with_test_folder(self):
        expectedPath = "/MyProject/library/aaeTest/mvc/ControllerTest.php"
        md = self._getInstance()
        result = md.getTestFileName()
        self.assertEqual(expectedPath, result)

    def test_getOriginalFileName(self):
        aFileName = os.path.join("MyProject", "library", "aae", "mvc", "Controller.php")

        md = MirroredDirectory(aFileName)
        result = md.getOriginalFileName()

        self.assertEqual(aFileName, result)

    def test_setKind(self):
        aPath = "/MyProject/library/aae/mvc/Controller.php"
        testDir = "/MyProject/library/aaeTest"
        expectedPath = "/MyProject/library/aaeTest/mvc/ControllerTest.php"
        mockFileManipulator = MockFileManipulator()
        mockFileManipulator.createFile(os.path.join(testDir, "someFileTest.php"), "") #TODO: replace once directories can be mocked

        md = MirroredDirectory(aPath)
        md.fileManipulator = mockFileManipulator
        md.setKind(MirroredDirectory.KIND_IS_TEST)
        result = md.getOriginalFileName()
        resultKind = md.getKind()

        self.assertEqual(expectedPath, result)
        self.assertEqual(MirroredDirectory.KIND_IS_TEST, resultKind)
    
    def test_setKind_retain_base_path(self):
        aPath = "/MyProject/library/aae/mvc/Controller.php"
        testDir = "/MyProject/library/aaeTest" 
        basePath = "/MyProject/library"
        expectedPath = "/MyProject/library/aaeTest/mvc/ControllerTest.php"
        mockFileManipulator = MockFileManipulator()
        mockFileManipulator.createFile(os.path.join(testDir, "someFileTest.php"), "") #TODO: replace once directories can be mocked

        md = MirroredDirectory(aPath)
        md.fileManipulator = mockFileManipulator
        md.setBasePath(basePath)
        md.setKind(MirroredDirectory.KIND_IS_TEST)
        result = md.getOriginalFileName()
        resultBasePath = md.getBasePath()

        self.assertEqual(expectedPath, result)
        self.assertEqual(basePath, resultBasePath)

    def _getInstance(self):
        aPath = "/MyProject/library/aae/mvc/Controller.php"
        testDir = "/MyProject/library/aaeTest"
        mockFileManipulator = MockFileManipulator()
        mockFileManipulator.createFile(os.path.join(testDir, "someFileTest.php"), "") #TODO: replace once directories can be mocked

        md = MirroredDirectory(aPath)
        md.fileManipulator = mockFileManipulator

        return md

    def test_getBasePath_no_base_path_set_but_has_test_folder(self):
        expected = os.path.join(os.sep, "MyProject", "library", "aae")
        md = self._getInstance()

        result = md.getBasePath()

        self.assertEqual(expected, result)
        
    def test_getRelativeFileName(self):
        expected = os.path.join("mvc", "Controller.php")
        md = self._getInstance()

        result = md.getRelativeFileName()

        self.assertEqual(expected, result)

    def test_setDefaultExtension(self):
        aPath = "/MyProject/library/aae/mvc/Controller"
        defaultFileExtension = "php"
        expected = "/MyProject/library/aae/mvc/Controller.php"
        md = self._getInstance()
        md.setDefaultExtension(defaultFileExtension)

        result = md.getOriginalFileName()

        self.assertEqual(expected, result)

    def test_setDefaultExtension_call_set_after_setting_default_file_extension(self):
        aPath = "/Some/Thing/Completely/different.php"
        anotherPath = "/MyProject/library/aae/mvc/Controller"
        
        defaultFileExtension = "php"
        expected = "/MyProject/library/aae/mvc/Controller.php"
        md = MirroredDirectory(aPath)
        md.setDefaultExtension(defaultFileExtension)

        md.set(anotherPath)

        result = md.getOriginalFileName()

        self.assertEqual(expected, result)
    
if __name__ == '__main__':
    unittest.main()