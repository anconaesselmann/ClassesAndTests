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



if __name__ == '__main__':
    unittest.main()