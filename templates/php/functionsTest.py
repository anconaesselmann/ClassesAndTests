import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))
    sys.path.append(path.abspath(path.join(__file__, "..", "..", "..", "classes_and_tests")))


from php.functions import *
from src.mocking.MockFileSystem import MockFileSystem

class PhpFunctionsTest(unittest.TestCase):

    def test_get_doc_block_tag(self):
        settings = "{\"author\": \"Axel\"}"
        args = {"settings" : settings}
        expected = "@author Axel"
        fc = FunctionCollection()
        result = fc.get_doc_block_tag(args)
        self.assertEqual(expected, result)

    def test_get_doc_block_tag_with_empty_value(self):
        settings = "{\"author\": None}"
        args = {"settings" : settings}
        expected = None
        fc = FunctionCollection()
        result = fc.get_doc_block_tag(args)
        self.assertEqual(expected, result)

    def test_get_class_name(self):
        args = {"dir" : path.join("Folder1", "Folder2", "FileName.php")}
        expected = "FileName"
        fc = FunctionCollection()
        result = fc.get_class_name(args)
        self.assertEqual(expected, result)


    def test_get_py_package_name(self):
    	args = {"dir" : path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")}
        expected = path.join("aae\\mvc")
        mockFileSystem = MockFileSystem()
        mockFileSystem.createFile(path.join(os.sep, "MyProject", "libraryTest", "SomeFileTest.php"))
        fc = FunctionCollection()
        fc.fileSystem = mockFileSystem
        result = fc.get_php_namespace(args)

        self.assertEqual(expected, result)









    """def test_get_relative_autoloader_path(self):
        settings = "{\"php_autoloader_dir\": \"relative/path/to/Autoloader.php\"}"
        args = {"settings" : settings}
        expected = "require_once strstr(__FILE__, 'Test', true).'/relative/path/to/Autoloader.php';"
        result = FunctionCollection.get_php_autoloader(args)
        self.assertEqual(expected, result)

    def test_get_absolute_autoloader_path(self):
        settings = "{\"php_autoloader_dir\": \"/absolute/path/to/Autoloader.php\"}"
        args = {"settings" : settings}
        expected = "require_once \"/absolute/path/to/Autoloader.php\";"
        result = FunctionCollection.get_php_autoloader(args)
        self.assertEqual(expected, result)


    def test_getautoloader_path_with_no_value(self):
        settings = "{\"php_autoloader_dir\": None}"
        args = {"settings" : settings}
        expected = None
        result = FunctionCollection.get_php_autoloader(args)
        self.assertEqual(expected, result)


    def test_get_php_namespace(self):
        settings = "{\"base_dir\": \"/MyProject/library\"}"
        args = {"settings" : settings, "dir": "/MyProject/library/aae/mvc/Controller.php"}
        expected = "aae\\mvc"
        result = FunctionCollection.get_php_namespace(args)
        self.assertEqual(expected, result)"""


if __name__ == '__main__':
    unittest.main()