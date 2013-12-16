import os
import sublime
import sublime_plugin

PACKAGE_NAME = "ClassesAndTests"
PACKAGE_VERSION = "0.2.0"

def plugin_loaded():
    global settings
    settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')

try:
    from src.MirroredDirectory import MirroredDirectory
    from src.OutputPanel import OutputPanel
    from src.CommandExecutionThread import CommandExecutionThread
except ImportError:
    from .src.MirroredDirectory import MirroredDirectory
    from .src.OutputPanel import OutputPanel
    from .src.CommandExecutionThread import CommandExecutionThread
    def plugin_loaded():
        global settings
        settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')
else:
    plugin_loaded()


class RunUnitTestsCommand(sublime_plugin.WindowCommand):
    def run(self, run_test_suite = False):
        if run_test_suite == False:
            view = self.window.active_view() # ????
            fileName = view.file_name()
            if fileName is not None:
                md = MirroredDirectory(fileName)
                testsPath = md.getTestFileName()
                extension = md.getExtension()
            else :
                print("Tests can only be run on files that have been saved.")
                return
        elif run_test_suite == True:
            testsPath = os.path.normpath(settings.get("current_php_test_suite_dir"))
            extension = "php" # TODO: this is temporary...
        else:
            testsPath = run_test_suite
            extension = "php" # TODO: this is temporary...

        if extension == "php":
            command = self.getPhpCommand()
        elif extension == "py":
            command = self.getPyCommand()
        else:
            print("File extension not supported for running unit tests. Currently only 'php' and 'py' are allowed")
            return

        self.runTests(command, testsPath)

    def runTests(self, command, testsPath):
        testsPathString = "\"" +  testsPath + "\""
        self.outputPanel = self.getOutputPanel(command + " " + testsPathString)
        thread = CommandExecutionThread(command, testsPath)
        thread.start()
        self.handleCommandThread(thread)

    def getPyCommand(self):
        pythonDir = settings.get("python_dir")
        if pythonDir is not None:
            pythonDir = os.path.normpath(pythonDir)
        else:
            pythonDir = ""
        pythonDir = os.path.join(pythonDir, "python")
        return pythonDir

    def getPhpCommand(self):
        phpUnitDir = os.path.normpath(settings.get("php_unit_binary_dir"))
        if phpUnitDir[-7:] == "phpunit":
            phpUnitDir = phpUnitDir[:-7]
        return os.path.join(phpUnitDir, "phpunit")

    def getOutputPanel(self, commandString):
        outputPanel = OutputPanel(self.window, "php_unit_output_panel", PACKAGE_NAME)
        if settings.get("show_executed_command") == True:
            credits = PACKAGE_NAME + " " + PACKAGE_VERSION + " by Axel Ancona Esselmann"
            import datetime
            ts = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
            outputPanel.printToPanel(credits + "\n" + "\nExecuting on " + ts + ":\n$ " + commandString + "\n\nResult:\n")
        return outputPanel

    def handleCommandThread(self, thread):
        if thread.is_alive():
            sublime.set_timeout(lambda: self.handleCommandThread(thread), 100)
        else:
            if thread.result != False:
                self.outputPanel.printToPanel( thread.result )
            else:
                self.outputPanel.printToPanel( "A problem occured executing the unit tests. Make sure you supplied the correct path the unit testing program." )