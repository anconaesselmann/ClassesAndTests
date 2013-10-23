import sublime
import sublime_plugin

from src.OutputPanel import OutputPanel
from src.MultipleCommandExecutionThread import MultipleCommandExecutionThread
from src.LiveUnitTest import LiveUnitTest

PACKAGE_NAME = "ClassesAndTests"
PACKAGE_VERSION = "0.2.0"

settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')

INTERVAL_BETWEEN_CONTINUOUS_UNIT_TESTS = settings.get("interval_between_continuous_unit_tests")

continuousUnitTestingThread = None


class ContinuousUnitTestingCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.outputPanel = OutputPanel(self.view.window(), "php_unit_output_panel", PACKAGE_NAME)
        self.liveUnitTest = LiveUnitTest(settings.get("php_unit_binary_dir"))

        self.initCommandThread()
        self.liveUnitTest.updateTempFiles(self.view)
        self.outputProgramStart()
        self.runTests()

    def runTests(self):
        view = sublime.active_window().active_view()
        self.liveUnitTest.updateTempFiles(view)
        self.updateCommandThread()
        self.handleCommandThread()

    def initCommandThread(self):
        global continuousUnitTestingThread
        if continuousUnitTestingThread is None:
            continuousUnitTestingThread = MultipleCommandExecutionThread()
            print "Starting continuousUnitTestingThread"
            continuousUnitTestingThread.start()

    def updateCommandThread(self):
        global continuousUnitTestingThread
        continuousUnitTestingThread.setCommand(self.liveUnitTest.getCommand()) # TODO: used to be command string, now is argument!!!
        continuousUnitTestingThread.setArgument(self.liveUnitTest.getArgument())

    def outputProgramStart(self):
        if settings.get("show_executed_command") == True:
            credits = PACKAGE_NAME + " " + PACKAGE_VERSION + " by Axel Ancona Esselmann"
            import datetime
            ts = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
            self.outputPanel.printToPanel(credits + "\n" + "\nExecuting on " + ts + ":\n$ " + self.liveUnitTest.getCommand() + " " + self.liveUnitTest.getArgument() + "\n\nResult:\n")

    def handleCommandThread(self):
        global continuousUnitTestingThread
        if continuousUnitTestingThread.is_alive():
            if not continuousUnitTestingThread.hasRun():
                sublime.set_timeout(lambda: self.handleCommandThread(), 100)
            else:
                viewPosition = self.outputPanel.getViewPosition()
                #viewPosition = (0, 100)
                #print "viewPosition: " + str(viewPosition)
                self.outputPanel.clear()
                #self.outputPanel.printToPanel("Tests for " + self.liveUnitTest.activeFile.getFileName() + ": ")
                self.outputPanel.printToPanel("Tests for " + self.liveUnitTest.activeFile.getFileName() + ": "+ str(continuousUnitTestingThread.getResult()))
                #print "view positint is loading: " + str(self.outputPanel.outputView.is_loading())
                self.outputPanel.setViewPosition(viewPosition)
                continuousUnitTestingThread.reset()
                if self.outputPanel.isVisible():
                    sublime.set_timeout(lambda: self.runTests(), INTERVAL_BETWEEN_CONTINUOUS_UNIT_TESTS)