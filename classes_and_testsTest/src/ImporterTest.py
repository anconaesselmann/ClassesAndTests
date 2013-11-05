import unittest
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..", "..")))

from classes_and_tests.src.Importer import Importer

class ImporterTest(unittest.TestCase):
	def test___init__(self):
		obj = Importer()


if __name__ == '__main__':
    unittest.main()