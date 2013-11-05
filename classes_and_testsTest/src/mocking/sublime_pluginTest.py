import unittest
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..", "..", "..")))

import classes_and_tests.src.mocking.sublime_plugin

class WindowCommandTest(unittest.TestCase):
	def test___init__(self):
		obj = WindowCommand()


if __name__ == '__main__':
    unittest.main()