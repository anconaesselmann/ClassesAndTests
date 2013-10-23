import re
import sublime
import sublime_plugin

from src.CommandExecutionThread import CommandExecutionThread
from src.LiveUnitTest import LiveUnitTest

PACKAGE_NAME = "ClassesAndTests"
PACKAGE_VERSION = "0.2.0"

DEBUG = True

settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')

class CreateMissingFunctionsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.classView = self.view # possibly try to find the classes view
        self.edit = edit

        self._runUnitTest()

    def _runUnitTest(self):
        if DEBUG:
            print("Running tests to determine if all functions have been declared:")
        classView = self.classView
        liveUnitTest = LiveUnitTest(settings.get("php_unit_binary_dir"))
        liveUnitTest.updateTempFiles(classView)
        command = liveUnitTest.getCommand()
        argument = liveUnitTest.getArgument()

        thread = CommandExecutionThread(command, argument)
        thread.start()
        self._handleCommandThread(thread)

    def _handleCommandThread(self, thread):
        if thread.is_alive():
            sublime.set_timeout(lambda: self._handleCommandThread(thread), 100)
        else:
            functionName = self._getFunctionName(thread.result)
            if functionName is not None:
                self._insertFunction(functionName)
            else:
                if DEBUG:
                    print("No functions have to be declared.")

    def _getFunctionName(self, testResult):
        matches = re.findall("(?<=Fatal\\serror:)(?:[\\s\\w\\\\]+undefined\\smethod)(?:[\\s\\w\\\\]+::)([\\w]+)(?=\\(\\))", testResult)
        if len(matches) > 0:
            result = matches[0]
        else:
            result = None
        return result

    def _insertFunction(self, functionName):
        classView = self.classView

        region = classView.find("\\}[^\\}]*\\}[^\\}]*\\z", 0)
        if region is not None:
            #print classView.substr(region)
            insertionPoint = region.begin()
            indentation = classView.substr(classView.line(insertionPoint))[:-1] # fails when some idiot does some wacky formatting that puts code on the same line before or after the closing bracket of a class
            classView.insert(self.edit, insertionPoint, self._getFunctionBody(functionName, indentation))


            sublime.set_timeout(lambda: self._runUnitTest(), 100)
        else:
            print("File is not formatted correctly. A class{} needs to be inside a namespace{}")

    def _getFunctionBody(self, functionName, indent):
        if DEBUG:
            print("Creating function \"" + functionName + "()\"")
        indent2 = indent + indent
        indent3 = indent2 + indent

        out =  "\n"
        out += indent2 + "public function " + functionName + "() {\n"
        out += indent3 + "return ;\n"
        out += indent2 + "}\n"
        out += indent

        return out