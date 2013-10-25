import sublime
import sublime_plugin
import os

def do_when(conditional, callback, *args, **kwargs):
    if conditional():
        return callback(*args, **kwargs)
    sublime.set_timeout(functools.partial(do_when, conditional, callback, *args, **kwargs), 50)
    

class OutputPanel():
    def __init__(self, window, panelName, packageName):
        settings = sublime.load_settings(packageName + '.sublime-settings')
        self.window = window
        self.panelName = panelName
        if not hasattr(self, 'outputView'):
            colorTheme = settings.get("color_theme")
            packageDir = os.path.join(sublime.packages_path(), packageName)
            tmThemeDir = os.path.join("Packages", packageName, "colorThemes", packageName + "_" + colorTheme + ".tmTheme")
            tmLanguageDir = os.path.join("Packages", packageName, "colorThemes", packageName + ".tmLanguage")
            self.outputView = self.window.get_output_panel(panelName)
            self.outputView.settings().set(panelName, True)
            self.outputView.set_syntax_file(tmLanguageDir)
            self.outputView.settings().set("color_scheme", tmThemeDir)
            self.outputView.settings().set("font_size", settings.get("output_font_size"))
            self.outputView.settings().set("line_numbers", False)
        self.window.run_command("show_panel", {"panel": "output." + panelName})

    def printToPanel(self, text):
        try:
            #sublime2
            self.outputView.set_read_only(False)
            edit = self.outputView.begin_edit()
            self.outputView.insert(edit, self.outputView.size(), text)
            self.outputView.end_edit(edit)
            self.outputView.set_read_only(True)
        except Exception:
            #sublime3
            self.outputView.run_command('output_panel_insert', {'string': text})

    def clear(self):
        try:
            #sublime2
            self.outputView.set_read_only(False)
            edit = self.outputView.begin_edit()
            self.outputView.erase(edit, sublime.Region(0, self.outputView.size()))
            self.outputView.end_edit(edit)
            self.outputView.set_read_only(True)
        except Exception:
            #sublime3
            self.outputView.run_command('output_panel_clear', {'string': ""})

    def isVisible(self):
        return bool(self.outputView.window())

    def getViewPosition(self):
        #return [self.outputView.visible_region(), self.outputView.viewport_position(), self.outputView.viewport_extent()]
        viewPosition = self.outputView.viewport_position()
        #print viewPosition
        return viewPosition
    #Not working correctly!!!!!!!!!
    def setViewPosition(self, position):
        #do_when(lambda: not self.outputView.is_loading(), lambda: self.outputView.set_viewport_position(position, False))


        #print "setting view to: " + str(position)


        #textPos = self.outputView.layout_to_text(position)
        #self.outputView.set_viewport_position(textPos, False)

        #sublime.set_timeout(self.setViewport(position), 0)
        self.outputView.set_viewport_position(position, False)
        #self.outputView.set_viewport_position(position)

        #
    """def setViewport(self, position):
        print "before set_viewport_position"
        if self.outputView is None:
            print "waiting"
            sublime.set_timeout(self.setViewport(position), 0)
            return
        self.outputView.set_viewport_position(position, False)
        print "after set_viewport_position"""

