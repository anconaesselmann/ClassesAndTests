import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))
    sys.path.append(path.abspath(path.join(__file__, "..", "..", "..", "classes_and_tests")))


from py.functions import *
from src.mocking.MockFileManipulator import MockFileManipulator


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
        expected = path.join("library.aae.mvc.Controller")
        mockFileManipulator = MockFileManipulator()
        mockFileManipulator.createFile(path.join(os.sep, "MyProject", "libraryTest", "SomeFileTest.php"))
        fc = FunctionCollection()
        fc.fileManipulator = mockFileManipulator
        result = fc.get_py_package_name(args)

        self.assertEqual(expected, result)

    def test_get_project_folder(self):
        settings = "{\"base_dir\": \"/MyProject/library/\"}"
        args = {"settings" : settings, "dir": "/MyProject/library/aae/mvc/Controller.php"}
        expected = ", \"..\", \"..\", \"..\""
        fc = FunctionCollection()
        result = fc.get_project_folder(args)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()