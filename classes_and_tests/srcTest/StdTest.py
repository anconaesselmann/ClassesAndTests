import unittest

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from src.Std import Std

class StdTest(unittest.TestCase):
	def test___init__(self):
		obj = Std()

	def test_getLineIndentAsWhitespace(self):
		obj = Std()

		data = [
			(" ", " "),
			("\t", "\t"),
			("    pass", "    "),
			("    pass    ", "    "),
			("\tpass\t", "\t")]

		for inputValue, expected in data:
			result = obj.getLineIndentAsWhitespace(inputValue)
			self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()