DEBUG = False
UNIT_TEST_DEBUG = False

import os
import fileinput

try:
    import sublime
    import sublime_plugin
except ImportError:
    try:
        from src.mocking.sublime import sublime
        from src.mocking import sublime_plugin
    except ImportError:
        from .src.mocking.sublime import sublime
        from .src.mocking import sublime_plugin
    if UNIT_TEST_DEBUG: 
        DEBUG = True
        print("LiveUnitTesting: sublime and sublime_plugin not imported in " + __file__)
    else:
        DEBUG = False

class SublimeFunctions():
    @staticmethod
    def getViewContent(view):
        return view.substr(sublime.Region(0, view.size()))