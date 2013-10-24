import sublime
import sublime_plugin
from os import path

from src.OutputPanel import OutputPanel
from src.MultipleCommandExecutionThread import MultipleCommandExecutionThread
from src.LiveUnitTesting import LiveUnitTesting
from src.UnitTestFunctions import UnitTestFunctions
from src.MirroredDirectory import MirroredDirectory

PACKAGE_NAME = "ClassesAndTests"
PACKAGE_VERSION = "0.2.0"

settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')

INTERVAL_BETWEEN_CONTINUOUS_UNIT_TESTS = settings.get("interval_between_continuous_unit_tests")

continuousUnitTestingThread = None


class ContinuousUnitTestingCommand(sublime_plugin.WindowCommand):
    """def test(self):

        windows = sublime.windows()
        for window in windows:
            windowId = window.id()
            activeView = window.active_view()
            num_groups = window.num_groups()
            print windowId
            print activeView
            print num_groups
            views = window.views()
            for view in views:
                file_name = view.file_name()
                print file_name
                if file_name == "/MyProject/libraryTest/python/a/b/c/PythonClass14Test.py":
                    #window.focus_view(view)
                    pass
    """

    def run(self):
        #self.test()
        view = self.window.active_view()
        self.outputPanel = OutputPanel(self.window, "php_unit_output_panel", PACKAGE_NAME)
        if not UnitTestFunctions.classHasTest(view):
            self.outputPanel.printToPanel("No Class-Test file pair exists.")
            return
        UnitTestFunctions.bringViewsToFront(self.window, view)

        self.liveUnitTest = LiveUnitTesting(UnitTestFunctions.getCommandFolders(settings))

        self.initCommandThread()
        self.liveUnitTest.updateTempFiles(self.window.active_view())
        self.outputProgramStart()
        self.runTests(view)



    def _getClassView(self, view):
        classView = None
        classFileName = MirroredDirectory(view.file_name()).getFileName()
        if view.file_name == classFileName:
            classView = view
        else:
            for tempView in self.window.views():
                file_name = tempView.file_name()
                if file_name == classFileName:
                    classView = tempView
                    break
        return classView

    def _getClassAndTestView(self):
        md = MirroredDirectory(self.window.active_view().file_name())

    def runTests(self, classView):
        if classView is not None:
            self.liveUnitTest.updateTempFiles(classView)
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
        if continuousUnitTestingThread is not None and continuousUnitTestingThread.is_alive():
            if not continuousUnitTestingThread.hasRun():
                sublime.set_timeout(lambda: self.handleCommandThread(), 100)
            else:
                viewPosition = self.outputPanel.getViewPosition()
                #viewPosition = (0, 100)
                #print "viewPosition: " + str(viewPosition)
                self.outputPanel.clear()
                #self.outputPanel.printToPanel("Tests for " + self.liveUnitTest.getActiveFile().getFileName() + ": ")
                self.outputPanel.printToPanel("Tests for " + self.liveUnitTest.getActiveFile().getFileName() + ": "+ str(continuousUnitTestingThread.getResult()))
                #print "view positint is loading: " + str(self.outputPanel.outputView.is_loading())
                self.outputPanel.setViewPosition(viewPosition)
                continuousUnitTestingThread.reset()
                if self.outputPanel.isVisible():
                    classView = self._getClassView(self.window.active_view())
                    sublime.set_timeout(lambda: self.runTests(classView), INTERVAL_BETWEEN_CONTINUOUS_UNIT_TESTS)