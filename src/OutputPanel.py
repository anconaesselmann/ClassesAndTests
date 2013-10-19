import sublime
import sublime_plugin
import os

class OutputPanel():
    def run(self):
        pass
    def __init__(self, window, panelName, packageName):
        settings = sublime.load_settings(packageName + '.sublime-settings')
        self.window = window
        self.panelName = panelName
        if not hasattr(self, 'outputView'):
            colorTheme = settings.get("color_theme")
            packageDir = os.path.join(sublime.packages_path(), packageName)
            tmThemeDir = os.path.join(packageDir, "colorThemes", packageName + "_" + colorTheme + ".tmTheme")
            tmLanguageDir = os.path.join(packageDir, "colorThemes", packageName + ".tmLanguage")

            self.outputView = self.window.get_output_panel(panelName)
            self.outputView.settings().set(panelName, True)
            self.outputView.set_syntax_file(tmLanguageDir)
            self.outputView.settings().set("color_scheme", tmThemeDir)
            self.outputView.settings().set("font_size", settings.get("output_font_size"))
            self.outputView.settings().set("line_numbers", False)
        self.window.run_command("show_panel", {"panel": "output." + panelName})

    def printToPanel(self, text):
        self.outputView.set_read_only(False)
        edit = self.outputView.begin_edit()
        self.outputView.insert(edit, self.outputView.size(), text)
        self.outputView.end_edit(edit)
        self.outputView.set_read_only(True)