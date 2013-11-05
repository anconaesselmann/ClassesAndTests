import unittest
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..", "..")))

from classes_and_tests.src.FileManipulator import FileManipulator

class FileManipulatorTest(unittest.TestCase):
	def test___init__(self):
		obj = FileManipulator()



if __name__ == '__main__':
    unittest.main()