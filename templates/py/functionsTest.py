import unittest
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))
    sys.path.append(path.abspath(path.join(__file__, "..", "..", "..", "classes_and_tests")))


from py.functions import *

class PhpFunctionsTest(unittest.TestCase):
	def test_get_project_folder(self):
		settings = "{\"base_dir\": \"/MyProject/library/\"}"
		args = {"settings" : settings, "dir": "/MyProject/library/aae/mvc/Controller.php"}
		expected = ", \"..\", \"..\", \"..\""
		result = get_project_folder(args)
		self.assertEqual(expected, result)

	def test_get_py_package_name(self):
		settings = "{\"base_dir\": \"/MyProject/library/\"}"
		args = {"settings" : settings, "dir": "/MyProject/library/aae/mvc/Controller.php"}
		expected = "library.aae.mvc.Controller"
		result = get_py_package_name(args)
		self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()