import sublime
import sublime_plugin

class OutputPanelInsertCommand(sublime_plugin.TextCommand):
    def run(self, edit, string=''):
        self.view.set_read_only(False)
        self.view.insert(edit, self.view.size(), string)
        self.view.set_read_only(True)