import unittest

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from src.Std import Std
from os import path, sep

data = [
            (["folder"], "folder"),
            (["folder", "folder2", "folder3"], "folder" + sep + "folder2" + sep + "folder3"),
            ([sep, "folder2", "folder3"], sep + "folder2" + sep + "folder3")
        ]

class StdTest(unittest.TestCase):
    def test___init__(self):
        obj = Std()

    def test_dirExplode(self):
        global data
        obj = Std()

        for expected, inputValue in data:
            result = obj.dirExplode(inputValue)
            self.assertEqual(expected, result)

    def test_dirImplode(self):
        global data
        obj = Std()

        for inputValue, expected in data:
            result = obj.dirImplode(inputValue)
            self.assertEqual(expected, result)

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

    def test_getSettingNameValuePair(self):
        settings = "{\"author\": \"Axel\"}"
        expected = ("author", "Axel")
        result1, result2 = Std.getSettingNameValuePair(settings)
        self.assertEqual(expected, (result1, result2))

if __name__ == '__main__':
    unittest.main()