import unittest
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from src.FileCreator import FileCreator

data = [ # input data          ,extension
    ("/A/path/To/a/file.txt"                                  , ".txt" , "file"),
    ("A/path/To/a/File.py"                                    , ".py"  , "File"),
    ("/A/path/To/a/file"                                      , ""     , None),
    ("A/path/To/a/file"                                       , ""     , None),
    ("/AClass.php"                                            , ".php" , "AClass"),
    ("Main.html"                                              , ".html", "Main"),
    (".csv"                                                   , ""     , None),
    (""                                                       , ""     , None),
    ("/"                                                      , ""     , None),
    ("/MyProject/library/scrTest/aae/MyClassTest.php"         , ".php" , "MyClass")
]

class FileCreatorTest(unittest.TestCase):
	def test___init__(self):
		aPath = "/test.txt"
		obj = FileCreator(aPath)

	def test_getFileExtension(self):
		global data
		for inputValue, extension, className in data:
			result = FileCreator.getFileExtension(inputValue)
			self.assertEqual(extension, result)
		pass

	def test_getClassName(self):
		global data
		for inputValue, extension, className in data:
			fc = FileCreator(inputValue)
			result = fc.getClassName()
			self.assertEqual(className, result)
		pass


if __name__ == '__main__':
    unittest.main()