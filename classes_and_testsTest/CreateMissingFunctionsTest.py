import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from classes_and_tests.CreateMissingFunctions import CreateMissingFunctionsCommand
from classes_and_tests.src.mocking.MockFileSystem import MockFileSystem
from classes_and_tests.src.FileSystem import FileSystem

class CreateMissingFunctionsTest(unittest.TestCase):
    def _getInstance(self):
        pyClassFile  = path.join(os.sep, "MyProject1", "library", "aae", 	 "mvc", "Controller.py")
        phpClassFile = path.join(os.sep, "MyProject1", "library", "aae", 	 "mvc", "Controller.php")
        pyTestFile   = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.py")
        phpTestFile  = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.php")

        pyTestFileContent  = FileSystem.getFileContentFromTestDataFile("TestData.py")
        phpTestFileContent = FileSystem.getFileContentFromTestDataFile("TestData.php")
        
        obj = CreateMissingFunctionsCommand()
        obj.fileSystem = MockFileSystem()
        obj.fileSystem.createFile(pyClassFile)
        obj.fileSystem.createFile(phpClassFile)
        obj.fileSystem.createFile(pyTestFile, pyTestFileContent)
        obj.fileSystem.createFile(phpTestFile, phpTestFileContent)

        return obj


    def test_getParameterNames_python_function_has_parameters(self):
        functionName = "aMemberFunctionWithParameters"
        fileDir 	 = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.py")
        expected	 = ["parameter1", "parameter2", "parameter3", "parameter4"]
        obj 		 = self._getInstance()

        parameterNames = obj._getParameterNames(functionName, fileDir)

        self.assertEqual(expected, parameterNames)

    def test_getParameterNames_python_function_doesnt_have_parameters(self):
    	functionName = "aMemberFunctionWithoutParameters"
    	fileDir  	 = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.py")
    	expected 	 = []
        obj 		 = self._getInstance()

        parameterNames = obj._getParameterNames(functionName, fileDir)

        self.assertEqual(expected, parameterNames)


    def test_getParameterNames_php_function_has_parameters(self):
    	functionName = "aMemberFunctionWithParameters"
    	fileDir  	 = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.php")
    	expected 	 = ["parameter1", "parameter2", "parameter3", "parameter4"]
        obj 		 = self._getInstance()

        parameterNames = obj._getParameterNames(functionName, fileDir)

        self.assertEqual(expected, parameterNames)

    def test_getParameterNames_php_function_doesnt_have_parameters(self):
    	functionName = "aMemberFunctionWithoutParameters"
    	fileDir  	 = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.php")
    	expected 	 = []
        obj 		 = self._getInstance()

        parameterNames = obj._getParameterNames(functionName, fileDir)

        self.assertEqual(expected, parameterNames)

    def test__getFunctionBody_py_function_has_parameters(self):
    	expected 	 = FileSystem.getFileContentFromTestDataFile("ExpectedResultSnippetMemberFunctionWithParameters.py")
    	obj 	 	 = self._getInstance()
    	fileName 	 = path.join(os.sep, "MyProject1", "library", "aae", "mvc", "Controller.py")
    	functionName = "aMemberFunctionWithParameters"
    	indent 	 	 = "    "
    	parameters 	 = ["parameter1", "parameter2"]

    	functionBody = obj._getFunctionBody(fileName, functionName, indent, parameters)

    	self.assertEqual(expected, functionBody)

    def test__getFunctionBody_php_function_has_parameters(self):
    	expected 	 = FileSystem.getFileContentFromTestDataFile("ExpectedResultSnippetMemberFunctionWithParameters.php")
    	obj 		 = self._getInstance()
    	fileName 	 = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.php")
    	functionName = "aMemberFunctionWithParameters"
    	indent 		 = "\t"
    	parameters 	 = ["$parameter1", "$parameter2"]

    	functionBody = obj._getFunctionBody(fileName, functionName, indent, parameters)

    	self.assertEqual(expected, functionBody)

    def _dataProvider_getParameterType_python(self):
    	return dict(
    		dataPy  = FileSystem.getFileContentFromTestDataFile("TestData.py"),
        	dataPhp = FileSystem.getFileContentFromTestDataFile("TestData.php"),
    		string  = "parameter1",
    		integer = "parameter2",
    		float   = "parameter3"
    	)
    def test__getParameterType_Determine_the_type_of_a_parameter_of_a_python_function(self):
    	fileDir 	 = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest1.py")
    	functionName = "aMemberFunctionWithParameters"
    	data 		 = self._dataProvider_getParameterType_python()["dataPy"]

    	obj = self._getInstance()
    	obj.fileSystem.createFile(fileDir, data)

    	parameterName = self._dataProvider_getParameterType_python()["string"]
    	stringResult  = obj._getParameterType(fileDir, functionName, parameterName)
		
    	parameterName = self._dataProvider_getParameterType_python()["integer"]
    	intResult     = obj._getParameterType(fileDir, functionName, parameterName)

    	parameterName = self._dataProvider_getParameterType_python()["float"]
    	floatResult   = obj._getParameterType(fileDir, functionName, parameterName)

    	self.assertEqual("str", stringResult)
    	self.assertEqual("int", intResult)
    	self.assertEqual("float", floatResult)

    def test__getParameterType_Determine_the_type_of_a_parameter_of_a_php_function(self):
    	fileDir 	 = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest1.php")
    	functionName = "aMemberFunctionWithParameters"
    	data 		 = self._dataProvider_getParameterType_python()["dataPhp"]

    	obj = self._getInstance()
    	obj.fileSystem.createFile(fileDir, data)

    	parameterName = self._dataProvider_getParameterType_python()["string"]
    	stringResult  = obj._getParameterType(fileDir, functionName, parameterName)
		
    	parameterName = self._dataProvider_getParameterType_python()["integer"]
    	intResult 	  = obj._getParameterType(fileDir, functionName, parameterName)

    	parameterName = self._dataProvider_getParameterType_python()["float"]
    	floatResult   = obj._getParameterType(fileDir, functionName, parameterName)

    	self.assertEqual("str", stringResult)
    	self.assertEqual("int", intResult)
    	self.assertEqual("float", floatResult)

    def test__getParameterType_Return_type_when_parameter_can_not_be_determined(self):
    	fileDir 	 = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest1.py")
    	functionName = "aFunctionName"
    	data 		 = self._dataProvider_getParameterType_python()["dataPy"]

    	obj = self._getInstance()
    	obj.fileSystem.createFile(fileDir, data)

    	parameterName = "doesNotExist"
    	result = obj._getParameterType(fileDir, functionName, parameterName)

    	self.assertEqual("__type__", result)
    
    

if __name__ == '__main__':
    unittest.main()