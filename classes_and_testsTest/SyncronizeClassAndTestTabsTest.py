import unittest
import os
import time
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from classes_and_tests.SyncronizeClassAndTestTabs import *
from classes_and_tests.src.mocking.sublime import *

class SyncronizeClassAndTestTabsTest(unittest.TestCase):
	def test___init__(self):
		obj = SyncronizeClassAndTestTabsListener()

	def helper_getInstance(self):
		settings = MockSettings()
		settings.set("tab_syncronization", True)
		settings.set("seperate_tests_and_sources_by_split_view", True)
		
		listener = SyncronizeClassAndTestTabsListener()
		listener.settings = settings
		
		return listener

	def test__openingIsEnabled(self):
		listener = self.helper_getInstance()
		result = listener._openingIsEnabled()
		self.assertEqual(True, result)

	def test__openingIsEnabled_no_tab_sync(self):
		settings = MockSettings()
		settings.set("tab_syncronization", False)
		settings.set("seperate_tests_and_sources_by_split_view", True)
		
		listener = SyncronizeClassAndTestTabsListener()
		listener.settings = settings
		result = listener._openingIsEnabled()
		self.assertEqual(False, result)

	def test__openingIsEnabled_no_split_view_seperation(self):
		settings = MockSettings()
		settings.set("tab_syncronization", True)
		settings.set("seperate_tests_and_sources_by_split_view", False)
		
		listener = SyncronizeClassAndTestTabsListener()
		listener.settings = settings
		result = listener._openingIsEnabled()
		self.assertEqual(False, result)

	####

	def test__getActiveViewFileName(self):
		fileName = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
		view = MockSublimeView(fileName)
		listener = self.helper_getInstance()
		result = listener._getActiveViewFileName(view)
		self.assertEqual(fileName, result)

	def test__getActiveViewFileName_no_fleName(self):
		view = MockSublimeView(None)
		listener = self.helper_getInstance()
		result = listener._getActiveViewFileName(view)
		self.assertEqual(None, result)

	def test__fileIsHot_file_is_hot(self):
		fileName = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
		syncHelper = SyncHelper()
		syncHelper.setHotFile(fileName)
		listener = self.helper_getInstance()
		listener.syncHelper = syncHelper
		result = listener._fileIsHot(fileName)
		self.assertEqual(True, result)

	def test__fileIsHot_file_is_not_hot(self):
		fileName = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
		syncHelper = SyncHelper()
		listener = self.helper_getInstance()
		listener.syncHelper = syncHelper
		result = listener._fileIsHot(fileName)
		self.assertEqual(False, result)

	def test__setHotFile(self):
		fileName = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
		syncHelper = SyncHelper()
		listener = self.helper_getInstance()
		listener.syncHelper = syncHelper
		resultIsNotHot = listener._fileIsHot(fileName)
		listener._setHotFile(fileName)
		resultIsHot = listener._fileIsHot(fileName)
		self.assertEqual(False, resultIsNotHot)
		self.assertEqual(True, resultIsHot)


class SyncHelperTest(unittest.TestCase):
	def test___init__(self):
		obj = SyncHelper()

	def test_fileIsHot_file_is_not_hot(self):
		aPath = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
		sync = SyncHelper()
		result = sync.fileIsHot(aPath)
		self.assertEqual(False, result)

	def test_fileIsHot_file_is_hot(self):
		aPath = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
		sync = SyncHelper()
		sync.hotFiles[aPath] = time.clock()
		result = sync.fileIsHot(aPath)
		self.assertEqual(True, result)

	def test_setHotFile(self):
		aPath = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
		sync = SyncHelper()
		sync.setHotFile(aPath)
		result = sync.fileIsHot(aPath)
		self.assertEqual(True, result)

	def test_coolFile(self):
		aPath = os.path.join(os.sep, "MyProject", "library", "aae", "mvc", "Controller.php")
		sync = SyncHelper()
		sync.setHotFile(aPath)
		resultSet = sync.fileIsHot(aPath)
		sync.coolFile(aPath)
		resultUnset = sync.fileIsHot(aPath)

		self.assertEqual(True, resultSet)
		self.assertEqual(False, resultUnset)

if __name__ == '__main__':
    unittest.main()