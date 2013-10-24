import re
import sublime
import sublime_plugin

from src.CommandExecutionThread import CommandExecutionThread
from src.LiveUnitTesting import LiveUnitTesting
from src.UnitTestFunctions import UnitTestFunctions
from src.FileComponents import FileComponents
from src.Std import Std

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
        liveUnitTest = LiveUnitTesting(UnitTestFunctions.getCommandFolders(settings))
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
        result = None
        phpMatches = re.findall("(?<=Fatal\\serror:)(?:[\\s\\w\\\\]+undefined\\smethod)(?:[\\s\\w\\\\]+::)([\\w]+)(?=\\(\\))", testResult)
        if len(phpMatches) > 0:
            return phpMatches[0]
        pyMatches = re.findall("(?<=AttributeError:)(?:[\\s\\w]+')(\\w+)(?=')", testResult)
        if len(pyMatches) > 0:
            return pyMatches[0]

        return result

    def _insertFunction(self, functionName):
        classView = self.classView
        insertionPoint = self._getInsertPoint(classView)
        if insertionPoint is not None:
            indentation = Std.getLineIndentAsWhitespace(classView.substr(classView.line(insertionPoint)))
            classView.insert(self.edit, insertionPoint, self._getFunctionBody(self.classView.file_name(), functionName, indentation))
            extension = FileComponents(view.file_name()).getExtension()
            if extension is not "py": # for some odd reason in .py scripts this would create multiple functions with the same name....
                sublime.set_timeout(lambda: self._runUnitTest(), 200)
        else:
            print("File is not formatted correctly. A class{} needs to be inside a namespace{}")

    def _getInsertPoint(self, view):
        extension = FileComponents(view.file_name()).getExtension()
        insertionPoint = None
        if extension == "php":
            region = view.find("\\}[^\\}]*\\}[^\\}]*\\z", 0)
            if region is not None:
                insertionPoint = region.begin()
        elif extension == "py":
            region = view.line(view.size())
            if region is not None:
                insertionPoint = region.end()

        return insertionPoint

    def _getFunctionBody(self, fileName, functionName, indent):
        extension = FileComponents(fileName).getExtension()
        out = ""
        if extension == "php":
            if DEBUG:
                print("Creating php function \"" + functionName + "()\"")
            indent2 = indent + indent
            indent3 = indent2 + indent

            out +=  "\n"
            out += indent2 + "public function " + functionName + "() {\n"
            out += indent3 + "return ;\n"
            out += indent2 + "}\n"
            out += indent
        elif extension == "py":
            if DEBUG:
                print("Creating py function \"" + functionName + "()\"")
            indent = "    " # ignoring the indentation passed with indent
            indent2 = indent + indent
            indent3 = indent2 + indent

            out +=  "\n"
            out += indent + "def " + functionName + "(self):\n"
            out += indent2 + "return\n"
            out += indent
        else:
            out = None

        return out



