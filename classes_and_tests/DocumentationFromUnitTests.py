"""
@author Axel Ancona Esselmann
"""
DEBUG = True
UNIT_TEST_DEBUG = False
PACKAGE_NAME = "ClassesAndTests"

import re
import os
from os import path
import sys
if sys.version_info < (3, ):
    from src.orderedDict import OrderedDict
else:
    from collections import OrderedDict

def plugin_loaded():
    global settings
    settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')

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
        print("DocumentationFromUnitTestsCommand: sublime and sublime_plugin not imported in " + __file__)
    else:
        DEBUG = False

try:
    from  src.Std                    import Std
    from  src.FileSystem             import FileSystem
    from  src.MirroredDirectory      import MirroredDirectory
    from  src.SublimeFunctions       import SublimeFunctions
    from  src.UnitTestFunctions      import UnitTestFunctions
except ImportError:
    from .src.Std                    import Std
    from .src.FileSystem             import FileSystem
    from .src.MirroredDirectory      import MirroredDirectory
    from .src.SublimeFunctions       import SublimeFunctions
    from .src.UnitTestFunctions      import UnitTestFunctions
    def plugin_loaded():
        global settings
        settings = sublime.load_settings(PACKAGE_NAME+ '.sublime-settings')
else:
    plugin_loaded()

class DocumentationFromUnitTestsCommand(sublime_plugin.TextCommand):
    def initializeDependencies(self):
        if not hasattr(self, "fileSystem"):
            self.fileSystem = FileSystem()

    def run(self, edit):
        if DEBUG: print("DocumentationFromUnitTestsCommand called")
        self.initializeDependencies()

        classFileName = self.view.file_name()

        md = MirroredDirectory()
        md.fileSystem = self.fileSystem
        md.set(classFileName)
        testFileName  = md.getTestFileName()

        window = self.view.window()
        if window is None:
            return
        classView = UnitTestFunctions.getClassView(window, self.view)

        temp, extension = os.path.splitext(classFileName)

        testFileContent = self.fileSystem.getFileContent(testFileName)
        classFileContent = SublimeFunctions.getViewContent(classView)
        
        newClassFileContent = self.extractAndInsertDocumentation(extension, classFileContent, testFileContent)

        region = sublime.Region(0, classView.size())
        #text = classView.substr(region)
        classView.replace(edit, region, newClassFileContent)
    
    def extractAndInsertDocumentation(self, extension, classFileContent, testFileContent):
        """ Given the content of a class and test file and their file extension, 
        Given, When, Then documentation blocks from the test file are inserted 
        into the function's description in the class file.
    
        ************************************************************
        ####UnitTest Specifications
        
        
        - Given: the contents of a php class and test file
          When : the test file has Given, When, Then documentation blocks
          Then : the test file documentation is extracted and inserted into the class file
        
             `test_extractAndInsertDocumentation_php()`
        
        - Given: the contents of a python class and test file
          When : the test file has Given, When, Then documentation blocks
          Then : the test file documentation is extracted and inserted into the class file
        
             `test_extractAndInsertDocumentation_py()`
        
        
        ************************************************************
        
        @param str extension the file extension for the language used (.php or .py)
        @param str classFileContent A string with the content of a class file
        @param str testFileContent A string with the content of a test file
    
        returns: a string with the test file contents and the tests' documentation

        """
        functions = self._getMethodNames(classFileContent, extension)
        for funct in functions:
            functionDocumentation = self._getTestFunctionDocumentation(extension, testFileContent, funct)
            if len(functionDocumentation) > 0:
                DocBlockInsertString = "\n\n"
                for testFunctionName, testFunctionDoc in Std.getIterItems(functionDocumentation):
                    DocBlockInsertString += "- Given: " + testFunctionDoc["given"] + "\n"
                    DocBlockInsertString += "  When : " + testFunctionDoc["when"] + "\n"
                    DocBlockInsertString += "  Then : " + testFunctionDoc["then"] + "\n\n"
                    DocBlockInsertString += "     `" + testFunctionName + "()`\n\n"
                #if extension == ".py":
                    #print ("\nBEGIN")
                    #print functionDocumentation
                    #for testFunctionName, testFunctionDoc in Std.getIterItems(functionDocumentation):
                        #print(testFunctionName)
                        #print(testFunctionDoc)
                        #pass
                originalDocBlockSpan = self._findDockBlock(extension, classFileContent, funct)
                if originalDocBlockSpan == False:
#TODO: exit gracefully and create test
                    print("function does not have docBlock, even though the test does.")
                startPos, endPos = originalDocBlockSpan
                originalDocBlock = classFileContent[startPos: endPos]
                newDockBlock = self._insertAutomaticDockBlock(originalDocBlock, DocBlockInsertString)
                classFileContent = classFileContent[:startPos] + newDockBlock + classFileContent[endPos:]
                #if funct == "functionName8" and extension == ".py":
                    #print("\nBEGIN")
                    #print functionDocumentation
                    #print(DocBlockInsertString)
                    #print("startPos: " + str(startPos) + "\nendPos: " + str(endPos) + "\nStrLen: " + str(len(classFileContent)))
                    #print originalDocBlock
                    #print "newDockBlock"
                    #print newDockBlock
                    #print classFileContent
                
        return classFileContent

    def _getMethodNames(self, fileContent, fileExtension):
        """ finds all method names int string "fileContent"
        
        @param str fileContent The content of a class file
        @returns: A list of method names
        """
        if fileExtension == ".php":
            compiledExpression = re.compile(r"""
                # Non-capturing group matching the end of a documentation block
                (?:\*/)
                # Non-capturing group matching anything between the end of the documentation block
                # and the beginning of the function's name
                (?:.*?)

                # Non-capturing group finding the start of a function
                (?:[\s]?function[\s]+)
                # Capture group for the function name
                (\w+)
                # Function names end with whitespace or an open parentheses
                (?=[\s\(])
                """, re.X|re.S)
            methods = re.findall(compiledExpression, fileContent)
        elif fileExtension == ".py":
            compiledExpression = re.compile(r"""
                # Non-capturing group finding the start of a function
                (?:[\s]?def[\s]+)
                # Capture group for the function name
                (\w+)
                # Function names end with whitespace or an open parentheses
                (?=[\s\(])
                """, re.X|re.S)
            methods = re.findall(compiledExpression, fileContent)
        return methods
    
    def _insertAutomaticDockBlock(self, docBlockString, replacementStr):
        """ Replaces an automatically generated dock-block inside a regular dock-block
    
        @param str docBlockString A dock-block with automatically generated documentation
        @param str replacementStr A string with content
    
        returns: A dock block that has the replacementStr inserted
        """
        result = docBlockString
        compiledExpressionReplaceBlock = re.compile(r"""
            (?P<oldContent>
                (?:\*{60}\n)
                (?P<lineStart>.*?)
                (?:\#\#\#)
                (?:.+)
                (?:\*{60})
            )
            """, re.X|re.S)
        reResult = re.search(compiledExpressionReplaceBlock, docBlockString)
        compiledExpressionNoBlock = re.compile(r"""
            #(?P<oldContent>
                (?P<lineStart>[^\n^\r]*?)
                (?:\w+)
                (?:.*?)
                (?P<insertionPoint>[\n\r])
                (?:(?P=lineStart)@\w+)
            #)
            """, re.X|re.S)
        compiledExpressionNoBlockNoParameters = re.compile(r"""
            (?P<beforeLineStart>
                (?:["]{3}|/\*\*)
                (?:[^\n^\r]*?)
                (?:[\n\r])
            )
            (?P<lineStart>[^\w^@^\n^\r]*)
            (?P<beforeInsertionPoint>
                (?:[^\w^@^\n^\r]*?)
                (?:.*?)
            )
            (?P<insertionPoint>[\n\r])
            (?P<afterInsertionPoint>
                (?:
                    (?:[^\n^\r]*?@.*|[\n\r]\s*?)
                    (?:["]{3}|\*/)
                )
                |
                (?:\s*?["]{3}|\s*?\*/)
            )



                #(?:/\*\*|\"\"\")
                #(?:.*)
                #(?:[\n\r])
                #(?P<lineStart>[^\n^\r]*?)
                #(\w+.*?) # TODO: make sure empty lines also work
                #(?P<insertionPoint>[\n\r])
                #(?:\s*?\*/|\s*?\"\"\")
            """, re.S|re.X)

        if reResult is None:
            reResult = re.search(compiledExpressionNoBlock, docBlockString)
            if reResult is None:
                reResult = re.search(compiledExpressionNoBlockNoParameters, docBlockString)
                lineStart = reResult.group("lineStart")
                finalReplacementString = "\n" + lineStart + self._getFormatedAutomaticDockBlock(lineStart, replacementStr, docBlockString)
            else:
                lineStart = reResult.group("lineStart")
                finalReplacementString = self._getFormatedAutomaticDockBlock(lineStart, replacementStr, docBlockString) + "\n" +lineStart
            
            temp, matchSpan = reResult.span("insertionPoint")
            result = docBlockString[:matchSpan] + reResult.group("lineStart") + finalReplacementString + "\n" + docBlockString[matchSpan:]
        else:
            finalReplacementString = self._getFormatedAutomaticDockBlock(reResult.group("lineStart"), replacementStr, docBlockString)
            result = re.sub(compiledExpressionReplaceBlock, finalReplacementString, docBlockString)
        return result

    def _getFormatedAutomaticDockBlock(self, lineStart, replacementStr, dockBlockString):
        #print "'" + lineStart.strip() + "'"
        finalReplacementString  = "************************************************************\n"
        finalReplacementString += lineStart+ "####UnitTest Specifications\n"
        finalReplacementString += lineStart
        finalReplacementString += self.prependEachLine(
                lineStart,
                replacementStr)
        finalReplacementString += "\n" + lineStart + "************************************************************"
        return finalReplacementString
    
    def prependEachLine(self, lineStart, string):
        """ Prepends lineStart to each line in the string
    
    
        ************************************************************
        ####UnitTest Specifications
        
        
        - Given: a string containing line breaks
          When : prependEachLine() is called
          Then : the returned string has lines that each begins with lineStart
        
             `test_prependEachLine()`
        
        
        ************************************************************
        @param str lineStart string that gets prepended to each line
        @param str string the original string
    
        returns: a multi-line string with lineStart prepended to each line
        """
        compiledExpression = re.compile(r"""
            (\n)
            """, re.X|re.S)
        result = re.sub(compiledExpression, "\n" + lineStart, string)
        return result
    
    def _getTestFunctionDocumentation(self, extension, inputString, functionName):
        """ extracts test function documentation
    
        @param str inputString the content of a test file
        @param str functionName the name of the test function for which documentation is to be extracted
    
        returns: a dictionary with "given", "when", and "then" keys
        """
        result = OrderedDict()
        compiledExpressionFunctionContentPY = re.compile(r"""
                (?:\s*?def\s*)
                (?P<functionName>test_""" + functionName + """.*?)
                (?:\s?\(.*?\)\s*?:\s*)
                (?P<functionContent>
                    (?:.*?)
                )
                (?=\s*?def[\s\w\d]*\(.*?\)\w*?:|$)
            """, re.X|re.S)
        compiledExpressionFunctionContentPHP = re.compile(r"""
                (?:\s*?function\s*)
                (?P<functionName>test_""" + functionName + """.*?)
                (?:\s?\(.*?\)\s*?\{\s*)
                (?P<functionContent>
                    (?:.*?)
                )
                (?=\s*?\})
            """, re.X|re.S)
        compiledExpressionSingleLineComments = re.compile(r"""
            (?P<commentType>\#|//)
            (?:\sGiven:?\s)
            (?P<given>[^\n^\r]*)
            (?:.*?)
            (?:\#|//)
            (?:\sWhen:?\s)
            (?P<when>[^\n^\r]*)
            (?:.*?)
            (?:\#|//)
            (?:\sThen:?\s)
            (?P<then>[^\n^\r]*)
            (?:.*?)
            """, re.X|re.S)
        compiledExpressionMultiLineComments = re.compile(r"""
            (?P<commentType>\"\"\"|/\*\*)
            (?:\s*?\*?\s*?Given:?\s)
            (?P<given>.*?)
            (?:\s*?\"\"\"|\s*?\*/)
            (?:.*?)
            (?:\"\"\"|/\*\*)
            (?:\s*?\*?\s*?When:?\s)
            (?P<when>.*?)
            (?:\s*?\"\"\"|\s*?\*/)
            (?:.*?)
            (?:\"\"\"|/\*\*)
            (?:\s*?\*?\s*?Then:?\s)
            (?P<then>.*?)
            (?:\s*?\"\"\"|\s*?\*/)
            (?:.*?)
            """, re.X|re.S)
        if extension == ".py":
            reResultFunctionContent = re.findall(compiledExpressionFunctionContentPY, inputString)
        elif extension == ".php":
            reResultFunctionContent = re.findall(compiledExpressionFunctionContentPHP, inputString)
        else:
            return False
        if reResultFunctionContent is not None:
            for functionName, functionContent in reResultFunctionContent:
                reResultComments = re.search(compiledExpressionSingleLineComments, functionContent)
                if reResultComments is None:
                    reResultComments = re.search(compiledExpressionMultiLineComments, functionContent)
                if reResultComments is not None:
                    comments = dict()
                    commentType = reResultComments.group("commentType")
                    replacementStr = ""
                    if commentType == "/**":
                        replacementStr = "* "
                    comments["given"]    = self.leftStripEachLine(replacementStr, reResultComments.group("given"))
                    comments["when"]     = self.leftStripEachLine(replacementStr, reResultComments.group("when"))
                    comments["then"]     = self.leftStripEachLine(replacementStr, reResultComments.group("then"))
                    result[functionName] = comments
        return result
    
    def leftStripEachLine(self, lineStart, textString):
        """ Removes white space and lineStart from the beginning of each line in textString
    
    
        ************************************************************
        ####UnitTest Specifications
        
        
        - Given: textString has multiple lines that start with lineStart
          When : leftStripEachLine is called
          Then : the return string has line starts without the string lineStart
        
             `test_leftStripEachLine()`
        
        
        ************************************************************
        @param str lineStart the character to be removed from the beginning of each line
        @param str textString A string with multiple lines
    
        returns: a string with lineStart removed from the beginning of each line
        """
        compiledExpression = re.compile(r"""
            (\n\s*""" + re.escape(lineStart) + """\s*)
        """, re.X|re.S)
        reResult = re.sub(compiledExpression, "\n         ", textString)
        return reResult
    
    def _findDockBlock(self, extension, classFileContent, functionName):
        """ Returns funcitonName's docBlock
    
        @param str classFileContent The content of a class file
        @param str functionName the name of a function
    
        returns: the position and length of the documentation block in classFileContent
        """
        docBlockSpan = False

        if extension == ".php":
            compiledExpression = re.compile(r"""
                (?P<docBlock>
                    (/\*\*)
                    ([^\{^\}]*?)
                    (\*/)
                )
                (?:[\w\s]*?)
                (?:""" + functionName + """)
                (?=\s?\(.*?\)\s*?\{\s*)
                """, re.X|re.S) # Verbose and multi-line flags
            rawDocumentation = re.search(compiledExpression, classFileContent)
        elif extension == ".py":
            compiledExpression = re.compile(r"""
                (?:""" + functionName + """)
                (?=\s?\(.*?\)\s*?\:\s*)
                (?:.*?)
                (?P<docBlock>
                    (\"\"\")
                    (.*?)
                    (\"\"\")
                )
                """, re.X|re.S) # Verbose and multi-line flags
            rawDocumentation = re.search(compiledExpression, classFileContent)
        if rawDocumentation is not None:
            docBlockSpan = rawDocumentation.span("docBlock")
        return docBlockSpan
    
    def temp(self):
        data = []
        data.append(r'''""" Second function (no parameters) with one test function
        
        
        ************************************************************
        ####UnitTest Specifications
        
        
        - Given: 
          When : 
          Then : 
        
             `test_temp()`
        
        
        ************************************************************
        @param  string parameter1 a String
        @return string             a String
        """
        ''')
        data.append(r'''""" Second function (no parameters) with one test function
        Second Row
        Row 3
        Row 4
        @param  string parameter1 a String
        @return string             a String
        """
        ''')
        data.append(r'''""" Second function (no parameters) with one test function
        Line Two
        Line Three
        """
        ''')



        data.append(r'''/** Second function (no parameters) with one test function
         *
         * @param  string parameter1 a String
         * @return string             a String
         */
        ''')
        data.append(r'''/** Second function (no parameters) with one test function
         * Second Row
         * Row 3
         * Row 4
         * @param  string parameter1 a String
         * @return string             a String
         */
        ''')
        data.append(r'''/** Second function (no parameters) with one test function
         * Line Two
         * Line Three
         */
        ''')
        #data.append(r'''""" Second function (no parameters) with one test function
        #"""
        #''')
        #data.append(r'''""" Second function (no parameters) with one test function
        #@param  string parameter1 a String
        #@return string             a String
        #"""
        #''')
        regEx = re.compile(r"""
            (?P<beforeLineStart>
                (?:["]{3}|/\*\*)
                (?:[^\n^\r]*?)
                (?:[\n\r])
            )
            (?P<lineStart>[^\w^@^\n^\r]*)
            (?P<beforeInsertionPoint>
                (?:[^\w^@^\n^\r]*?)
                (?:.*?)
            )
            (?P<insertionPoint>[\n\r])
            (?P<afterInsertionPoint>
                (?:
                    (?:[^\n^\r]*?@.*|[\n\r]\s*?)
                    (?:["]{3}|\*/)
                )
                |
                (?:\s*?["]{3}|\s*?\*/)
            )
            
        """, re.S|re.X)
        print("\n")
        for d in data:
            result = re.search(regEx, d)
            print ("beforeLineStart: \n'" + result.group("beforeLineStart") + "'")
            print ("linestart: \n'" + result.group("lineStart") + "'")
            #print ("beforeInsertionPoint: \n'" + result.group("beforeInsertionPoint") + "'")
            print ("insertionPoint: \n'" + result.group("insertionPoint") + "'")
            print ("afterInsertionPoint: \n'" + result.group("afterInsertionPoint") + "'")
            print ("\n")
        
        return True
    