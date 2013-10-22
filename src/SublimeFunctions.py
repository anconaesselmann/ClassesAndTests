import sublime
import sublime_plugin

class SublimeFunctions():
    @staticmethod
    def getViewContent(view):
        return view.substr(sublime.Region(0, view.size()))