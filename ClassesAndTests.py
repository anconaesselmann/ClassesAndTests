import sublime
import sys

VERSION = int(sublime.version())

reloader = "classes_and_tests.src.reloader"


if VERSION > 3000:
	reloader = 'ClassesAndTests.' + reloader
	from imp import reload


# Make sure all dependencies are reloaded on upgrade
if reloader in sys.modules:
	reload(sys.modules[reloader])

if VERSION > 3000:
	from .classes_and_tests import reloader
	from .classes_and_tests.ClassesAndTests import *
	from .classes_and_tests.ToggleSourceTest import *
	from .classes_and_tests.RunUnitTests import *
	from .classes_and_tests.CreateMissingFunctions import *
	from .classes_and_tests.ContinuousUnitTesting import *
	from .classes_and_tests.ClassesAndTests import *
else:

	from classes_and_tests.src import reloader
	from classes_and_tests.ClassesAndTests import *
	from classes_and_tests.ToggleSourceTest import *
	from classes_and_tests.RunUnitTests import *
	from classes_and_tests.CreateMissingFunctions import *
	from classes_and_tests.ContinuousUnitTesting import *
	from classes_and_tests.ClassesAndTests import *
	from classes_and_tests.SyncronizeClassAndTestTabs import *
