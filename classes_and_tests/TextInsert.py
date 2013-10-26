import sublime
import sublime_plugin

class TextInsertCommand(sublime_plugin.TextCommand):
    def run(self, edit, insertionPoint, string=''):
        self.view.insert(edit, insertionPoint, string)