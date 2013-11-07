import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..", "..")))

from src.mocking.MockFileManipulator import MockFileManipulator

class MockFileManipulatorTest(unittest.TestCase):
	def test___init__(self):
		obj = MockFileManipulator()

	def test_mocked_getFileContent(self):
		fileDir = "/Some/File.txt"
		content = "Content of a file."
		mfm = MockFileManipulator()
		mfm.addGetFileContentMock(fileDir, content)
		result = mfm.getFileContent(fileDir)

		self.assertEqual(content, result)

	def test_mocked_getFileContent_multiple_dirs(self):
		fileDir1 = "/Some/Folder/With/a_file.txt"
		content1 = "Content of a a_file."
		fileDir2 = "/Some/File.php"
		content2 = "php content."
		fileDir3 = "/Some/File.txt"
		content3 = "Content of a file."
		mfm = MockFileManipulator()
		mfm.addGetFileContentMock(fileDir1, content1)
		result1 = mfm.getFileContent(fileDir1)
		mfm.addGetFileContentMock(fileDir3, content3)
		result3 = mfm.getFileContent(fileDir3)
		mfm.addGetFileContentMock(fileDir2, content2)
		result2 = mfm.getFileContent(fileDir2)

		self.assertEqual(content1, result1)
		self.assertEqual(content2, result2)
		self.assertEqual(content3, result3)

	def test_mocked_createFile(self):
		fileDir = "/Some/Folder/With/a_file.txt"
		content = "Content of a a_file."

		mfm = MockFileManipulator()
		mfm.createFile(fileDir, content)

		result = mfm.getCreatedFile(fileDir)

		self.assertEqual(content, result)

	def test_mocked_createFile_file_was_not_created(self):
		fileDir = "/Some/Folder/With/a_file.txt"
		mfm = MockFileManipulator()
		result = mfm.getCreatedFile(fileDir)
		self.assertEqual(False, result)

	def test_get_content_of_nonexisting_file(self):
		fileDir = "/Some/Folder/With/a_file.txt"
		mfm = MockFileManipulator()
		self.assertRaises(Exception, lambda: mfm.getFileContent(fileDir))


	def test_get_content_of_created_file(self):
		fileDir = "/Some/File.txt"
		content = "Content of a file."
		mfm = MockFileManipulator()
		mfm.createFile(fileDir, content)
		result = mfm.getFileContent(fileDir)

		self.assertEqual(content, result)

	def test_new_file_would_overwrite_old_file(self):
		fileDir = "/Some/File.txt"
		content = "Content of a file."
		mfm = MockFileManipulator()
		mfm.addGetFileContentMock(fileDir, content)

		result = mfm.createFile(fileDir, content)
		self.assertEqual(False, result)

	def test_isdir_file_given(self):
		aDir = os.path.join("A", "mocked", "directory.txt")
		mfm = MockFileManipulator()
		result = mfm.isdir(aDir)
		self.assertEqual(False, result)

	def test_isdir_does_not_exist(self):
		aDir = os.path.join("A", "mocked", "directory")
		mfm = MockFileManipulator()
		result = mfm.isdir(aDir)
		self.assertEqual(False, result)

	def test_isdir_file_created(self):
		fileName = os.path.join("A", "mocked", "directory", "fileName.txt")
		aDir = os.path.join("A", "mocked", "directory")
		mfm = MockFileManipulator()
		mfm.createFile(fileName, "")
		result = mfm.isdir(aDir)
		self.assertEqual(True, result)

	def test_isfile(self):
		fileName = os.path.join("A", "mocked", "directory", "fileName.txt")
		mfm = MockFileManipulator()
		mfm.createFile(fileName, "")
		result = mfm.isfile(fileName)
		self.assertEqual(True, result)

	def test_isfile(self):
		fileName = os.path.join("A", "mocked", "directory", "fileName.txt")
		wrongFileName = os.path.join("A", "mocked", "directory", "fileName1.txt")
		mfm = MockFileManipulator()
		mfm.createFile(fileName, "")
		result = mfm.isfile(wrongFileName)
		self.assertEqual(False, result)

if __name__ == '__main__':
    unittest.main()