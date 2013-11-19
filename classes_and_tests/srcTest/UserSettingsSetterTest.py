import unittest
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from src.UserSettingsSetter import UserSettingsSetter

class UserSettingsSetterTest(unittest.TestCase):
	def test___init__(self):
		obj = UserSettingsSetter()

if __name__ == '__main__':
    unittest.main()