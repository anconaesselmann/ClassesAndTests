import sublime
import sublime_plugin

class OutputPanelClearCommand(sublime_plugin.TextCommand):
    def run(self, edit, string=''):
        self.view.set_read_only(False)
        self.view.erase(edit, sublime.Region(0, self.view.size()))
        self.view.set_read_only(True)