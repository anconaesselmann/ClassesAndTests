import os
import sublime
import sublime_plugin

PACKAGE_NAME = "ClassesAndTests"
PACKAGE_VERSION = "0.2.0"

def plugin_loaded():
    global settings
    global PACKAGE_DIR
    global TEMPLATES_DIR
    settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')
    PACKAGE_DIR = os.path.join(sublime.packages_path(), PACKAGE_NAME)
    TEMPLATES_DIR = os.path.join(PACKAGE_DIR, "templates")

try:
    from src.MirroredDirectory import MirroredDirectory
    from src.OutputPanel import OutputPanel
    from src.CommandExecutionThread import CommandExecutionThread
    from src.UnitTestFunctions import UnitTestFunctions
except ImportError:
    from .src.MirroredDirectory import MirroredDirectory
    from .src.OutputPanel import OutputPanel
    from .src.CommandExecutionThread import CommandExecutionThread
    from .src.UnitTestFunctions import UnitTestFunctions
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
        elif extension == "js":
            command = UnitTestFunctions.getCommand(extension)
        else:
            print("File extension not supported for running unit tests. Currently only 'php', 'py' and 'js' are allowed")
            return

        self.runTests(command, testsPath)

    def runTests(self, command, testsPath):
        testsPathString = "\"" +  testsPath + "\""
        self.outputPanel = self.getOutputPanel(command + " " + testsPathString)
        thread = CommandExecutionThread(command, testsPath)
        thread.start()
        self.handleCommandThread(thread)

    def getPyCommand(self):
        commandFolders = UnitTestFunctions.getCommandFolders(settings)
        return os.path.join(commandFolders["py"], "python")

    #def getCommand(self, extension):
    #    extTemplateDir = os.path.join(TEMPLATES_DIR, extension)
    #    if os.path.exists(extTemplateDir):
    #        return os.path.join(extTemplateDir, "testRunner");
    #   else:
    #       return None

    def getPhpCommand(self):
        commandFolders = UnitTestFunctions.getCommandFolders(settings)
        return os.path.join(commandFolders["php"], "phpunit")

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
                self.outputPanel.printToPanel( "A problem occured executing the unit tests. Make sure you supplied the correct path to the unit testing program." )