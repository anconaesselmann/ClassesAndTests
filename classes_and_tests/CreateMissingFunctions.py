DEBUG = False
UNIT_TEST_DEBUG = False

import re
import os
import string
from os import path

PACKAGE_NAME = "ClassesAndTests"

def plugin_loaded():
    global settings
    settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')
    global PACKAGE_DIR
    global TEMPLATES_DIR
    PACKAGE_DIR = os.path.join(sublime.packages_path(), PACKAGE_NAME)
    TEMPLATES_DIR = os.path.join(PACKAGE_DIR, "templates")

try:
    import sublime
    import sublime_plugin
except ImportError:
    try:
        from  src.mocking.sublime import sublime
        from  src.mocking         import sublime_plugin
    except ImportError:
        from .src.mocking.sublime import sublime
        from .src.mocking         import sublime_plugin
    if UNIT_TEST_DEBUG:
        DEBUG = True
        print("CreateMissingFunctions: sublime and sublime_plugin not imported in " + __file__)
    else:
        DEBUG = False

try:
    from  src.CommandExecutionThread import CommandExecutionThread
    from  src.LiveUnitTesting        import LiveUnitTesting
    from  src.UnitTestFunctions      import UnitTestFunctions
    from  src.FileComponents         import FileComponents
    from  src.Std                    import Std
    from  src.FileSystem             import FileSystem
    from  src.MirroredDirectory      import MirroredDirectory
except ImportError:
    from .src.CommandExecutionThread import CommandExecutionThread
    from .src.LiveUnitTesting        import LiveUnitTesting
    from .src.UnitTestFunctions      import UnitTestFunctions
    from .src.FileComponents         import FileComponents
    from .src.Std                    import Std
    from .src.FileSystem             import FileSystem
    from .src.MirroredDirectory      import MirroredDirectory
    def plugin_loaded():
        global settings
        settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')
        global PACKAGE_DIR
        global TEMPLATES_DIR
        PACKAGE_DIR = os.path.join(sublime.packages_path(), PACKAGE_NAME)
        TEMPLATES_DIR = os.path.join(PACKAGE_DIR, "templates")
else:
    plugin_loaded()

class CreateMissingFunctionsCommand(sublime_plugin.TextCommand):
    def initializeDependencies(self):
        if not hasattr(self, "fileSystem"):
            self.fileSystem = FileSystem()

    def run(self, edit):
        self.initializeDependencies()
        window = self.view.window()
        if window is None:
            return
        self.classView = UnitTestFunctions.getClassView(window, self.view)
        self.edit = edit

        self._runUnitTest()

    def _runUnitTest(self):
        if DEBUG: print("Running tests to determine if all functions have been declared:")
        classView    = self.classView
        liveUnitTest = LiveUnitTesting(UnitTestFunctions.getCommandFolders(settings))
        liveUnitTest.updateTempFiles(classView)
        command      = liveUnitTest.getCommand()
        argument     = liveUnitTest.getArgument()

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
                if DEBUG: print("No functions have to be declared.")

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

            classFileName = self.classView.file_name()

            md = MirroredDirectory()
            md.fileSystem = self.fileSystem
            md.set(classFileName)

            testFileName = md.getTestFileName()
            parameters = self._getParameterNames(functionName, testFileName)
            insertionString = self._getFunctionBody(classFileName, functionName, indentation, parameters)

            self.classView.sel().clear()
            self.classView.sel().add(sublime.Region(insertionPoint))
            self.classView.run_command("insert_snippet", {"contents": insertionString })
            if self.view != self.classView:
                sublime.active_window().run_command("toggle_sources_tests")
            extension = FileComponents(classView.file_name()).getExtension()
            if extension != "py":
                # for some odd reason in .py scripts this would create multiple functions with
                # the same name.... I might have to hook into the on_change event
                sublime.set_timeout(lambda: self._runUnitTest(), 200)

            # if db test case in php, create templates for db setup
            if self._isPhpDbTestCase(testFileName):
                self._createDbTestCaseFilesIfNotExist(testFileName)

        else:
            print("File is not formatted correctly. A class{} needs to be inside a namespace{}")

    def _isPhpDbTestCase(self, testFileDir):
        result = None
        fileContent = self.fileSystem.getFileContent(testFileDir)
        pyMatches = re.findall("DbTestCase?\s{", fileContent)
        if len(pyMatches) > 0: return True
        return False

    def _createDbTestCaseFilesIfNotExist(self, testFile):
        md = MirroredDirectory()
        md.fileSystem = self.fileSystem
        md.set(testFile)

        classFile = md.getFileName()

        # RunkeeperTestData
        print("\n\n\n" + testFile)
        print(classFile + "\n\n\n")


        testDataDir = path.join(FileComponents(testFile).getDir(), FileComponents(testFile).getFile() + "Data")
        classDataDir = path.join(FileComponents(classFile).getDir(), FileComponents(classFile).getFile() + "Data")

        print(testDataDir)
        print(classDataDir)

        if self.fileSystem.isdir(classDataDir) == False:
            self.fileSystem.createFolder(testDataDir)
            self.fileSystem.createFolder(classDataDir)
            testSetupDir          = path.join(testDataDir,      "setup.sql")
            testSetupContent      = self._templateContentGetter("setup.sql")
            classSetupDir         = path.join(classDataDir,     "setup.json")
            classSetupContent     = self._templateContentGetter("setup.json")
            classFunctionsDir     = path.join(classDataDir,     "functions.sql")
            classFunctionsContent = self._templateContentGetter("functions.sql")
            classTablesDir        = path.join(classDataDir,     "tables.sql")
            classTablesContent    = self._templateContentGetter("tables.sql")
            print(testSetupDir)
            print(testSetupContent)
            print(classSetupDir)
            print(classSetupContent)
            print(classFunctionsDir)
            print(classFunctionsContent)
            print(classTablesDir)
            print(classTablesContent)
            self.fileSystem.createFile(testSetupDir,      testSetupContent)
            self.fileSystem.createFile(classSetupDir,     classSetupContent)
            self.fileSystem.createFile(classFunctionsDir, classFunctionsContent)
            self.fileSystem.createFile(classTablesDir,    classTablesContent)
            return True

        return False

    def _templateContentGetter(self, name):
        templatePath    = os.path.join(TEMPLATES_DIR, "php", "dbTestCase", name)
        templateContent = self.fileSystem.getFileContent(templatePath)
        return templateContent

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

    def _getFunctionBody(self, fileName, functionName, indent, parameters=[]):
        md = MirroredDirectory()
        md.fileSystem = self.fileSystem
        md.set(fileName)

        testFileName = md.getTestFileName()

        extension = FileComponents(fileName).getExtension()
        if len(parameters) > 0:
            parameterString = ', '.join(parameters)
        else:
            parameterString = ""
        out = ""
        tabCounter = 2
        if extension == "php":
            parameterString = parameterString.replace("$", "\$")
            if DEBUG: print("Creating php function \"" + functionName + "()\"")
            indent2 = indent + indent
            if parameterString != "":
                parameterDescriptionString = ""
                for parameter in parameters:
                    # TODO: parameter type detection for php types
                    #print("parameter: " + parameter)
                    parameterType = self._getParameterType(testFileName, functionName, parameter)
                    parameterDescriptionString += indent + " * @param " + parameterType + " " + parameter + "${" + str(tabCounter) + ":__parameterDescription__}\n"
                    tabCounter += 1
            else:
                parameterDescriptionString = ""
            out += "\n"
            out += indent + "/**\n"
            out += indent + " * ${1:__functionDescription__}\n"
            out += parameterDescriptionString
            out += indent + " */\n"
            out += indent + "public function " + functionName + "(" + parameterString + ") \{\n"
            out += indent2+    "${" + str(tabCounter) + "://FunctionBody};\n"
            tabCounter += 1
            out += indent2+    "return${" + str(tabCounter) + ":};\n"
            tabCounter += 1
            out += indent + "\}${" + str(tabCounter) + ":}\n"
        elif extension == "py":
            if DEBUG: print("Creating py function \"" + functionName + "()\"")
            indent = "    " # ignoring the indentation passed with indent
            indent2 = indent + indent
            if parameterString != "":
                parameterString = ', ' + parameterString

                parameterDescriptionString = "\n"
                for parameter in parameters:
                    parameterType = self._getParameterType(testFileName, functionName, parameter)
                    parameterDescriptionString += indent + "@param " + parameterType + " " + parameter + " ${" + str(tabCounter) + ":__parameterDescription__}\n"
                    tabCounter += 1
            else:
                parameterDescriptionString = ""
            out += "\n"
            out +=  "def " + functionName + "(self" + parameterString + "):\n"
            out += indent +     "\"\"\" ${1:__functionDescription__}\n"
            out += parameterDescriptionString
            out += "\n"
            out += indent +     "returns: ${" + str(tabCounter) + ":__returnTypeDescription__}\n"
            tabCounter += 1
            out += indent +     "\"\"\"\n"
            out += indent +    "${" + str(tabCounter) + ":# FunctionBody}\n"
            tabCounter += 1
            out += indent +    "return${" + str(tabCounter) + ":}\n"
        else:
            out = None

        return out

    def _getParameterNames(self, functionName, fileDir):
        fileName, extension = os.path.splitext(fileDir)
        if extension == ".py":
            testFileContent = self.fileSystem.getFileContent(fileDir)
            regexString = "(?<=\\." + functionName + "\\()[^\\)]+"

            match = re.search(regexString, testFileContent)
            if match:
                rawParameterString = match.group()
                parameterString = re.sub('\\s', '', rawParameterString)
                parameters = str.split(parameterString, ',')
                return parameters
            else:
                return []
        elif extension == ".php":
            testFileContent = self.fileSystem.getFileContent(fileDir)
            regexString = "(?<=->" + functionName + "\\()[^\\)]+"
            match = re.search(regexString, testFileContent)
            if match:
                rawParameterString = match.group()
                parameterString = re.sub('\\s', '', rawParameterString)
                parameters = str.split(parameterString, ',')
                return parameters
            else:
                return []
        return

    def _getParameterType(self, fileDir, functionName, parameterName):
        """ Goes through a test file and determines the parameter type of
        parameter "parameterName" of the function "functionName"

        @param str fileDir The path to a test file
        @param str functionName The function name who's parameter is being typed
        @param str parameterName The parameter to be typed

        returns: str The parameter type
        """
        parameterName = re.escape(parameterName)
        fileData = self.fileSystem.getFileContent(fileDir)
        temp, extension = os.path.splitext(fileDir)

        regexString = '(?:test_' + functionName + ')(?:.+)(?:' + parameterName + '\s*=\s*)([^\n|^\r|^;]+)'
        parameterValues = re.findall(regexString, fileData, re.S)
        try:
            evaluatedParameterValue = eval(parameterValues[0])
            parameterValueTypeString = type(evaluatedParameterValue).__name__
        except Exception:
            parameterValueTypeString = "__type__"

        return parameterValueTypeString

