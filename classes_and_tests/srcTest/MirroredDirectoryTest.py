import unittest
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, ".."/* @project_folder */)))

from /* @package_name */ import /* @class_name */

class /* @class_name */Test(unittest.TestCase):
	def test___init__(self):
		obj = /* @class_name */()

	/* @cursor */

if __name__ == '__main__':
    unittest.main()