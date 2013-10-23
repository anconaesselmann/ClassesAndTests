import os
import sublime
import sublime_plugin

from src.MirroredDirectory import MirroredDirectory
from src.OutputPanel import OutputPanel
from src.CommandExecutionThread import CommandExecutionThread

PACKAGE_NAME = "ClassesAndTests"
PACKAGE_VERSION = "0.2.0"

settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')


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
        self.outputPanel = self.getOutputPanel(command + " " +  testsPath)
        thread = CommandExecutionThread(command, testsPath)
        thread.start()
        self.handleCommandThread(thread)

    def getPyCommand(self):
        pythonDir = os.path.normpath("/usr/bin") # TODO: get from settings
        return os.path.join(pythonDir, "python")

    def getPhpCommand(self):
        phpUnitDir = os.path.normpath(settings.get("php_unit_binary_dir"))
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
            self.outputPanel.printToPanel( thread.result )