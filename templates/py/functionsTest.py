import unittest
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))
    sys.path.append(path.abspath(path.join(__file__, "..", "..", "..", "classes_and_tests")))


from py.functions import *

class PhpFunctionsTest(unittest.TestCase):
    def test_get_doc_block_tag(self):
        settings = "{\"author\": \"Axel\"}"
        args = {"settings" : settings}
        expected = "@author Axel"
        result = FunctionCollection.get_doc_block_tag(args)
        self.assertEqual(expected, result)

    def test_get_doc_block_tag_with_empty_value(self):
        settings = "{\"author\": None}"
        args = {"settings" : settings}
        expected = None
        result = FunctionCollection.get_doc_block_tag(args)
        self.assertEqual(expected, result)

    def test_get_class_name(self):
        args = {"dir" : path.join("Folder1", "Folder2", "FileName.php")}
        expected = "FileName"
        result = FunctionCollection.get_class_name(args)
        self.assertEqual(expected, result)

    def test_getSettingNameValuePair(self):
        settings = "{\"author\": \"Axel\"}"
        expected = ("author", "Axel")
        result1, result2 = FunctionCollection.getSettingNameValuePair(settings)
        self.assertEqual(expected, (result1, result2))









    def test_get_project_folder(self):
        settings = "{\"base_dir\": \"/MyProject/library/\"}"
        args = {"settings" : settings, "dir": "/MyProject/library/aae/mvc/Controller.php"}
        expected = ", \"..\", \"..\", \"..\""
        result = FunctionCollection.get_project_folder(args)
        self.assertEqual(expected, result)

    def test_get_py_package_name(self):
        settings = "{\"base_dir\": \"/MyProject/library/\"}"
        args = {"settings" : settings, "dir": "/MyProject/library/aae/mvc/Controller.php"}
        expected = "library.aae.mvc.Controller"
        result = FunctionCollection.get_py_package_name(args)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()