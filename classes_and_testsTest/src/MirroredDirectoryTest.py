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

	def test__getExistingFileDir_no_change(self):
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
		aTestFileName1 = os.path.join("a", "pathTest", "toTest", "aTest", "file.php")
		aTestFileName2 = os.path.join("a", "pathTest", "toTest", "a", "file.php")
		aTestFileName3 = os.path.join("a", "pathTest", "to", "a", "file.php")
		aTestFileName4 = os.path.join("a", "path", "toTest", "a", "file.php")
		aTestFileName5 = os.path.join("a", "path", "to", "aTest", "file.php")
		aPath = os.path.join("a", "path", "to", "aTest")
		mockFileManipulator = MockFileManipulator()
		mockFileManipulator.createFile(aFileName, "")
		mockFileManipulator.createFile(aTestFileName1, "")
		mockFileManipulator.createFile(aTestFileName2, "")
		mockFileManipulator.createFile(aTestFileName3, "")
		mockFileManipulator.createFile(aTestFileName4, "")
		mockFileManipulator.createFile(aTestFileName5, "")
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


if __name__ == '__main__':
    unittest.main()