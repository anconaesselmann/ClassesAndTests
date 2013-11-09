import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..", "..")))

from src.mocking.MockFileSystem import *

class MockFileSystemTest(unittest.TestCase):
     
    def test___init__(self):
        obj = MockFileSystem()

    def test__createFolderNonRecursive_insert_one_folder(self):
    	aDict = {}
    	aFolder = "Folder1"
    	expected = {"Folder1": {}}
    	mfs = MockFileSystem()
    	created = mfs._createFolderNonRecursive(aDict, aFolder)
    	self.assertEqual(True, created)
    	self.assertEqual(expected, aDict)

    def test__createFolderNonRecursive_insert_two_folders_horizontally(self):
    	aDict = {}
    	aFolder1 = "Folder1"
    	aFolder2 = "Folder2"
    	expected = {"Folder1": {}, "Folder2": {}}
    	mfs = MockFileSystem()
    	created1 = mfs._createFolderNonRecursive(aDict, aFolder1)
    	created2 = mfs._createFolderNonRecursive(aDict, aFolder2)
    	self.assertEqual(True, created1)
    	self.assertEqual(True, created2)
    	self.assertEqual(expected, aDict)

    def test__createFolderNonRecursive_insert_fail(self):
    	aDict = {}
    	aFolder = "Folder1"
    	expected = {"Folder1": {}}
    	mfs = MockFileSystem()
    	created1 = mfs._createFolderNonRecursive(aDict, aFolder)
    	created2 = mfs._createFolderNonRecursive(aDict, aFolder)
    	self.assertEqual(True, created1)
    	self.assertEqual(False, created2)
    	self.assertEqual(expected, aDict)

    def test_isDir_root(self):
        aFolder = os.sep
        mfs = MockFileSystem()
        result = mfs.isdir(os.sep)   
        self.assertEqual(True, result)    
    
    def test_isDir_one_level(self):
        aFolder = path.join(os.sep, "Folder1")
        mfs = MockFileSystem()
        mfs.root = {os.sep: {"Folder1": {}}}
        result = mfs.isdir(aFolder)
        self.assertEqual(True, result) 

    def test_isDir_multiple_levels(self):
        print("")
        aFolder = path.join(os.sep, "Folder1", "Folder2", "folder3", "folder4")
        mfs = MockFileSystem()
        mfs.root = {os.sep: {"Folder1": {"Folder2": {"folder3": {"folder4": {}}}}}}
        result = mfs.isdir(aFolder)
        self.assertEqual(True, result) 

    def test_isdir_file_provided(self):
    	aFileName = path.join(os.sep, "Folder1", "Folder2", "AFile.txt")
    	mfs = MockFileSystem()
    	mfs.createFile(aFileName, "")

    	result = mfs.isdir(aFileName)

    	self.assertEqual(False, result)
    
    def test_createFolder_one_branch(self):
        mfs = MockFileSystem()
        aFolder = path.join(os.sep, "Folder1", "Folder2", "Folder3")
        created = mfs.createFolder(aFolder)
        result = mfs.isdir(aFolder)
        self.assertEqual(True, created)    
        self.assertEqual(True, result)

    def test_createFolder_folder_exists(self):
        mfs = MockFileSystem()
        aFolder = path.join(os.sep, "Folder1", "Folder2", "Folder3")
        created1 = mfs.createFolder(aFolder)
        result1 = mfs.isdir(aFolder)
        created2 = mfs.createFolder(aFolder)
        self.assertEqual(True, created1)    
        self.assertEqual(True, result1)
        self.assertEqual(False, created2)

    
    def test_createFolder_multiple_branches(self):
        mfs = MockFileSystem()

        path1 = path.join(os.sep, "a", "aa")
        path2 = path.join(os.sep, "a", "ab")
        path3 = path.join(os.sep, "a", "ac", "aca")
        path4 = path.join(os.sep, "a", "ac", "acb", "acba")
        path5 = path.join(os.sep, "b", "ba")
        path6 = path.join(os.sep, "c", "ca", "caa")
        path7 = path.join(os.sep, "c", "ca", "cab")
        path8 = path.join(os.sep, "c", "cb", "cba")
        path9 = path.join(os.sep, "c", "cb", "cbb")

        path10 = path.join(os.sep, "a")
        path11 = path.join(os.sep, "a", "ac")
        path12 = path.join(os.sep, "a", "ac", "acb")
        path13 = path.join(os.sep, "b")
        path14 = path.join(os.sep, "c")
        path15 = path.join(os.sep, "c", "ca")
        path16 = path.join(os.sep, "c", "cb")

        created1 = mfs.createFolder(path1)
        created2 = mfs.createFolder(path2)
        created3 = mfs.createFolder(path3)
        created4 = mfs.createFolder(path4)
        created5 = mfs.createFolder(path5)
        created6 = mfs.createFolder(path6)
        created7 = mfs.createFolder(path7)
        created8 = mfs.createFolder(path8)
        created9 = mfs.createFolder(path9)

        self.assertEqual(True, created1)    
        self.assertEqual(True, created2)    
        self.assertEqual(True, created3)    
        self.assertEqual(True, created4)    
        self.assertEqual(True, created5)    
        self.assertEqual(True, created6)    
        self.assertEqual(True, created7)    
        self.assertEqual(True, created8)    
        self.assertEqual(True, created9)    

        exists1 = mfs.isdir(path1)
        exists2 = mfs.isdir(path2)
        exists3 = mfs.isdir(path3)
        exists4 = mfs.isdir(path4)
        exists5 = mfs.isdir(path5)
        exists6 = mfs.isdir(path6)
        exists7 = mfs.isdir(path7)
        exists8 = mfs.isdir(path8)
        exists9 = mfs.isdir(path9)
        exists10 = mfs.isdir(path10)
        exists11 = mfs.isdir(path11)
        exists12 = mfs.isdir(path12)
        exists13 = mfs.isdir(path13)
        exists14 = mfs.isdir(path14)
        exists15 = mfs.isdir(path15)
        exists16 = mfs.isdir(path16)

        self.assertEqual(True, exists1)
        self.assertEqual(True, exists2)
        self.assertEqual(True, exists3)
        self.assertEqual(True, exists4)
        self.assertEqual(True, exists5)
        self.assertEqual(True, exists6)
        self.assertEqual(True, exists7)
        self.assertEqual(True, exists8)
        self.assertEqual(True, exists9)
        self.assertEqual(True, exists10)
        self.assertEqual(True, exists11)
        self.assertEqual(True, exists12)
        self.assertEqual(True, exists13)
        self.assertEqual(True, exists14)
        self.assertEqual(True, exists15)
        self.assertEqual(True, exists16)
    
    def test_folder_is_absolute(self):
    	aPath = path.join("Folder1", "Folder2", "Folder3")
    	mfs = MockFileSystem()
    	result = mfs.createFolder(aPath)
    	self.assertEqual(False, result)

    def test_createFile_atRoot(self):
    	aFileName = path.join(os.sep, "AFile.txt")
    	mfs = MockFileSystem()
    	result = mfs.createFile(aFileName, "")
    	self.assertEqual(True, result)

    def test_createFile_atRoot_file_exists(self):
    	aFileName = path.join(os.sep, "AFile.txt")
    	mfs = MockFileSystem()
    	result1 = mfs.createFile(aFileName, "")
    	result2 = mfs.createFile(aFileName, "")
    	self.assertEqual(True, result1)
    	self.assertEqual(False, result2)

    def test_createFile_not_at_root(self):
    	aFileName = path.join(os.sep, "Folder1", "Folder2", "AFile.txt")
    	mfs = MockFileSystem()
    	result = mfs.createFile(aFileName, "")
    	self.assertEqual(True, result)

    def test_isfile_file_provided(self):
    	aFileName = path.join(os.sep, "Folder1", "Folder2", "AFile.txt")
    	mfs = MockFileSystem()
    	mfs.createFile(aFileName, "")

    	result = mfs.isfile(aFileName)

    	self.assertEqual(True, result)

    def test_isfile_folder_provided(self):
    	aFolderName = path.join(os.sep, "Folder1", "Folder2", "Folder3")
    	mfs = MockFileSystem()
    	mfs.createFolder(aFolderName)

    	result = mfs.isfile(aFolderName)

    	self.assertEqual(False, result)

    def test_getFileContent(self):
    	aFileName = path.join(os.sep, "Folder1", "Folder2", "AFile.txt")
    	fileContent = "File content"
    	mfs = MockFileSystem()
    	mfs.createFile(aFileName, fileContent)

    	result = mfs.getFileContent(aFileName)

    	self.assertEqual(fileContent, result)    	

if __name__ == '__main__':
    unittest.main()