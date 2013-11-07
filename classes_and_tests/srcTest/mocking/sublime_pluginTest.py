import unittest
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..", "..")))

from src.mocking.sublime_plugin import *

class WindowCommandTest(unittest.TestCase):
	def test___init__(self):
		obj = WindowCommand()

class TextCommandTest(unittest.TestCase):
	def test___init__(self):
		obj = TextCommand()


if __name__ == '__main__':
    unittest.main()