import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from classes_and_tests.DocumentationFromUnitTests import DocumentationFromUnitTestsCommand
from classes_and_tests.src.mocking.MockFileSystem import MockFileSystem
from classes_and_tests.src.FileSystem import FileSystem
from classes_and_tests.src.Testing import *

class DocumentationFromUnitTests(unittest.TestCase):

    def test__getMethodNames_php_class_file(self):
        # Given: The file content of a php class file
        obj           = DocumentationFromUnitTestsCommand()
        fileContent   = FileSystem.getFileContentFromTestDataFile("ClassFile.php")
        fileExtension = ".php"
        expected      = ["function1", "_function2", "function3", "function4"]
    
        # When: The class file has at least one function
        result = obj._getMethodNames(fileContent, fileExtension)
        
        # Then: A list with the names of all functions in fileContent is returned
        self.assertEqual(expected, result)

    def test__getMethodNames_py_class_file(self):
        # Given: The file content of a python class file
        obj           = DocumentationFromUnitTestsCommand()
        fileContent   = FileSystem.getFileContentFromTestDataFile("ClassFile.py")
        fileExtension = ".py"
        expected      = ["function1", "_function2", "function3", "function4"]
    
        # When: The class file has at least one function
        result = obj._getMethodNames(fileContent, fileExtension)
        
        # Then: A list with the names of all functions in fileContent is returned
        self.assertEqual(expected, result)
        
# TODO: create much more test data
    def dataProvider__findDockBlock(self):
        return [
            [ # data set 1
                ".php",
                FileSystem.getFileContentFromTestDataFile("ClassFile.php"),
                "_function2",
                (205, 287)
            ],
            [ # data set 2
                ".py",
                FileSystem.getFileContentFromTestDataFile("ClassFile.py"),
                "_function2",
                (210, 283)
            ],
        ]

    @dataProvider(dataProvider__findDockBlock)
    def test__findDockBlock(self, extension, classFileContent, functionName, expected):
        # Given: 
        obj = DocumentationFromUnitTestsCommand()
        
        # When: 
        result = obj._findDockBlock(extension, classFileContent, functionName)
        
        # Then: 
        self.assertEqual(expected, result)


    def dataProvider__insertAutomaticDockBlock(self):
        return [
            [ # data set 1
                FileSystem.getFileContentFromTestDataFile("data_insertAutomaticDockBlock1.php"), 
                "\nThis is the new text\nThis is line two\n", 
                FileSystem.getFileContentFromTestDataFile("expected_insertAutomaticDockBlock1.php")
            ],
            [ # data set 2
                FileSystem.getFileContentFromTestDataFile("data_insertAutomaticDockBlock2.php"), 
                "\nThis is the new text\nThis is line two\n", 
                FileSystem.getFileContentFromTestDataFile("expected_insertAutomaticDockBlock1.php")
            ],
            [ # data set 3
                FileSystem.getFileContentFromTestDataFile("data_insertAutomaticDockBlock3.php"), 
                "\nThis is the new text\nThis is line two\n", 
                FileSystem.getFileContentFromTestDataFile("expected_insertAutomaticDockBlock3.php")
            ],
            [ # data set 4
                FileSystem.getFileContentFromTestDataFile("data_insertAutomaticDockBlock1.py"), 
                "\nThis is the new text\nThis is line two\n", 
                FileSystem.getFileContentFromTestDataFile("expected_insertAutomaticDockBlock1.py")
            ],
            [ # data set 5
                FileSystem.getFileContentFromTestDataFile("data_insertAutomaticDockBlock2.py"), 
                "\nThis is the new text\nThis is line two\n", 
                FileSystem.getFileContentFromTestDataFile("expected_insertAutomaticDockBlock1.py")
            ],
            [ # data set 6
                FileSystem.getFileContentFromTestDataFile("data_insertAutomaticDockBlock3.py"), 
                "\nThis is the new text\nThis is line two\n", 
                FileSystem.getFileContentFromTestDataFile("expected_insertAutomaticDockBlock3.py")
            ],
        ]

    @dataProvider(dataProvider__insertAutomaticDockBlock)
    def test__insertAutomaticDockBlock(self, dockBlockString, replacementStr, expected):
        # Given a dockBlockString documenting a function with automatically generated documentation block
        obj = DocumentationFromUnitTestsCommand()

        # When the replacement string is a nonempty string
        result = obj._insertAutomaticDockBlock(dockBlockString, replacementStr)
        
        # Then a dockBlock with the replacementStr replacing the old content is returned
        self.assertEqual(expected, result)
        

    def test_prependEachLine(self):
        """ Prepends lineStart to each line in the string
        """
        # Given a string containing line breaks
        obj       = DocumentationFromUnitTestsCommand()
        lineStart = r"""		 * """
        string    = "Line One\nLine Two\nLine Three"
        expected  = r"""Line One
		 * Line Two
		 * Line Three"""

        # When prependEachLine() is called
        result = obj.prependEachLine(lineStart, string)
        
        # Then the returned string has lines that each begins with lineStart
        self.assertEqual(expected, result)

    def dataProvider_getTestFunctionDocumentation(self):
        return [
            [".py", FileSystem.getFileContentFromTestDataFile("TestData.py"), "thisIsAFunction", "test_thisIsAFunction_first_test"],
            [".py", FileSystem.getFileContentFromTestDataFile("TestData.py"), "thisIsAFunction", "test_thisIsAFunction_testing_this_other_thing"],
            [".py", FileSystem.getFileContentFromTestDataFile("TestData.py"), "thisIsAFunction", "test_thisIsAFunction_third_test"],
            [".php", FileSystem.getFileContentFromTestDataFile("TestData.py"), "thisIsAFunction", "test_thisIsAFunction_php_fct"],
        ]

    @dataProvider(dataProvider_getTestFunctionDocumentation)
    def test__getTestFunctionDocumentation_python(self, extension, inputString, functionName, testFunctionName):
        # Given the content of a test file and a class function name
        obj = DocumentationFromUnitTestsCommand()
        
        # When _getTestFunctionDocumentation is called
        result = obj._getTestFunctionDocumentation(extension, inputString, functionName)
        
        # Then a dictionary with "Given", "When", and "Then" keys is returned
        commentDict = eval(FileSystem.getFileContentFromTestDataFile("result_test__getTestFunctionDocumentation.json"))[functionName][testFunctionName]
        resultDict  = result[testFunctionName]
        self.assertEqual(commentDict["given"], resultDict["given"])
        self.assertEqual(commentDict["when"],  resultDict["when"])
        self.assertEqual(commentDict["then"],  resultDict["then"])

    def test_leftStripEachLine(self):
        # Given textString has multiple lines that start with lineStart
        obj        = DocumentationFromUnitTestsCommand()
        lineStart  = r"* "
        textString = r"""Line One
         * Line Two         * 
         * Line Three"""
    
        # When leftStripEachLine is called
        result = obj.leftStripEachLine(lineStart, textString)
        
        # Then the return string has line starts without the string lineStart
        expected = "Line One\n         Line Two         * \n         Line Three"
        self.assertEqual(expected, result)

    def dataProvider_extractAndInsertDocumentation_php(self):
        return [
            [ # data set 1
                ".php",
                FileSystem.getFileContentFromTestDataFile("DataSet1_php_ClassFile.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet1_php_ClassFileTest.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet1_php_Result.php")
            ],
            [ # data set 2
                ".php", 
                FileSystem.getFileContentFromTestDataFile("DataSet2_php_ClassFile.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet2_php_ClassFileTest.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet2_php_Result.php")
            ],
            [ # data set 3
                ".php", 
                FileSystem.getFileContentFromTestDataFile("DataSet3_php_ClassFile.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet3_php_ClassFileTest.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet3_php_Result.php")
            ],
            [ # data set 4
                ".php", 
                FileSystem.getFileContentFromTestDataFile("DataSet4_php_ClassFile.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet4_php_ClassFileTest.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet4_php_Result.php")
            ],
            [ # data set 5
                ".php", 
                FileSystem.getFileContentFromTestDataFile("DataSet5_php_ClassFile.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet5_php_ClassFileTest.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet5_php_Result.php")
            ],
            [ # data set 6
                ".php", 
                FileSystem.getFileContentFromTestDataFile("DataSet6_php_ClassFile.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet6_php_ClassFileTest.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet6_php_Result.php")
            ],
            [ # data set 7
                ".php", 
                FileSystem.getFileContentFromTestDataFile("DataSet7_php_ClassFile.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet7_php_ClassFileTest.php"),
                FileSystem.getFileContentFromTestDataFile("DataSet7_php_Result.php")
            ],
        ]

    @dataProvider(dataProvider_extractAndInsertDocumentation_php)
    def test_extractAndInsertDocumentation_php(self, extension, classFileContent, testFileContent, expected):
        # Given the contents of a php class and test file
        obj = DocumentationFromUnitTestsCommand()
    
        # When the test file has Given, When, Then documentation blocks
        result = obj.extractAndInsertDocumentation(extension, classFileContent, testFileContent)
        
        # Then the test file documentation is extracted and inserted into the class file
        self.assertEqual(expected, result)

    def dataProvider_extractAndInsertDocumentation_py(self):
        return [
            [ # data set 1
                ".py",
                FileSystem.getFileContentFromTestDataFile("DataSet1_py_ClassFile.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet1_py_ClassFileTest.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet1_py_Result.py")
            ],
            [ # data set 2
                ".py", 
                FileSystem.getFileContentFromTestDataFile("DataSet2_py_ClassFile.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet2_py_ClassFileTest.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet2_py_Result.py")
            ],
            [ # data set 3
                ".py", 
                FileSystem.getFileContentFromTestDataFile("DataSet3_py_ClassFile.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet3_py_ClassFileTest.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet3_py_Result.py")
            ],
            [ # data set 4
                ".py", 
                FileSystem.getFileContentFromTestDataFile("DataSet4_py_ClassFile.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet4_py_ClassFileTest.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet4_py_Result.py")
            ],
            [ # data set 5
                ".py", 
                FileSystem.getFileContentFromTestDataFile("DataSet5_py_ClassFile.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet5_py_ClassFileTest.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet5_py_Result.py")
            ],
            [ # data set 6
                ".py", 
                FileSystem.getFileContentFromTestDataFile("DataSet6_py_ClassFile.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet6_py_ClassFileTest.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet6_py_Result.py")
            ],
            [ # data set 7
                ".py", 
                FileSystem.getFileContentFromTestDataFile("DataSet7_py_ClassFile.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet7_py_ClassFileTest.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet7_py_Result.py")
            ],
            #[ # data set 8
            #    ".py", 
            #    FileSystem.getFileContentFromTestDataFile("DataSet8_py_ClassFile.py"),
            #    FileSystem.getFileContentFromTestDataFile("DataSet8_py_ClassFileTest.py"),
            #    FileSystem.getFileContentFromTestDataFile("DataSet8_py_Result.py")
            #],
        ]

    @dataProvider(dataProvider_extractAndInsertDocumentation_py)
    def test_extractAndInsertDocumentation_py(self, extension, classFileContent, testFileContent, expected):
        # Given the contents of a python class and test file
        obj = DocumentationFromUnitTestsCommand()
    
        # When the test file has Given, When, Then documentation blocks
        result = obj.extractAndInsertDocumentation(extension, classFileContent, testFileContent)
        
        # Then the test file documentation is extracted and inserted into the class file
        self.assertEqual(expected, result)

    '''def test_temp(self):
        # Given 
        obj = DocumentationFromUnitTestsCommand()
    
        # When 
        result = obj.temp()
        
        # Then 
        expected = True
        self.assertEqual(expected, result)'''
    
    """def dataProvider__getLineStart(self):
        return [
            [ # data set 1
                ".py",
                FileSystem.getFileContentFromTestDataFile("DataSet1_py_ClassFile.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet1_py_ClassFileTest.py"),
                FileSystem.getFileContentFromTestDataFile("DataSet1_py_Result.py")
            ],
        ]

    @dataProvider(dataProvider__getLineStart)
    def test__getLineStart(self, commentBlock):
        # Given A string containing a comment block
        obj = aClass()
    
        # When _getLineStart is called
        result = obj._getLineStart(commentBlock)
        
        # Then a string containing the beginning of comment block lines gets returned
        expected = EXPECTED_TEST_RESULT
        self.assertEqual(expected, result)"""

    
    

if __name__ == '__main__':
    unittest.main()