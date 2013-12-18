import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from src.mocking.MockFileSystem import MockFileSystem
from src.FileSystem import FileSystem


class FileSystemTest(unittest.TestCase):
    def test___init__(self):
        obj = FileSystem()

    def test_getFileContentFromTestDataFile_regular_test_file(self):
        fs = FileSystem()
        executingFileName = os.path.join(os.sep, "Some", "Folder", "AClassTest.php")
        expected = '/Some/Folder/AClassTestData/test.php'

        result = fs._getTestDataFileName(executingFileName, "test.php")
        self.assertEqual(expected, result)

    def test_getFileContentFromTestDataFile_live_unit_test_file(self):
        fs = FileSystem()
        executingFileName = os.path.join(os.sep, "Some", "Folder", "___liveUnitTesting_AClassTest.php")
        expected = '/Some/Folder/AClassTestData/test.php'

        result = fs._getTestDataFileName(executingFileName, "test.php")
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()