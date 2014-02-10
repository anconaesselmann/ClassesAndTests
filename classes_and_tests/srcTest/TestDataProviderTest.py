import unittest
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from src.TestDataProvider import TestDataProvider

class TestDataProviderTest(unittest.TestCase):
	def test___init__(self):
		obj = TestDataProvider()

	def test_stringToPath(self):
	    """ A path string with unknown path separators is converted
	    to a valid path name for the current operating system
	    """
	    # Setup
	    obj = aClass()
	    expected = EXPECTED_TEST_RESULT
	    separator = "/"
	
	    # Testing
	    result = obj.stringToPath(pathName, separator)
	    
	    # Verification
	    self.assertEqual(expected, result)
	
	

if __name__ == '__main__':
    unittest.main()