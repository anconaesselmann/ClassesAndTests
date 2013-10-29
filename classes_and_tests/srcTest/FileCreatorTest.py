import unittest
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from src.FileCreator import FileCreator


class FileCreatorTest(unittest.TestCase):
	def test___init__(self):
		aPath = "/test.txt"
		obj = FileCreator(aPath)



if __name__ == '__main__':
    unittest.main()