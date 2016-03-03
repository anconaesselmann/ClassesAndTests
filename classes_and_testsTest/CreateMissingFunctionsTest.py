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
    		float   = "parameter3",
            dbtc    = FileSystem.getFileContentFromTestDataFile("TestDataPhpDatabaseTestCase.php")
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

    def test__isPhpDbTestCase(self):
        fileDir = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "TestDataPhpDatabaseTestCase.php")
        data    = self._dataProvider_getParameterType_python()["dbtc"]

        obj = self._getInstance()
        obj.fileSystem.createFile(fileDir, data)

        # When _isPhpDbTestCase is called
        result = obj._isPhpDbTestCase(fileDir)

        # Then
        self.assertEqual(True, result)

    # TODO: this one doesn't really test anything....
    def test__createDbTestCaseFilesIfNotExist_do_not_exist(self):
        fileDir = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "MyPersistingClassTest.php")
        data    = self._dataProvider_getParameterType_python()["dbtc"]

        obj = self._getInstance()
        obj.fileSystem.createFile(fileDir, data)

        # When _isPhpDbTestCase is called
        result = obj._createDbTestCaseFilesIfNotExist(fileDir)

        # Then
        # self.assertEqual(True, result)

    def test__getFunctionName_sql_procedure(self):
        data = """aae\db\StorageAPIException: Database Error with message:
        SQLSTATE[42000]: Syntax error or access violation: 1305 PROCEDURE tests.doFo16_times does not exist"""
        obj = self._getInstance()

        # When _getFunctionName is called
        functionName, functionType = obj._getFunctionName(data)

        # Then
        self.assertEqual("doFo16_times", functionName)
        self.assertEqual("sqlPro", functionType)

    def test__getFunctionName_sql_function(self):
        data = """aae\db\StorageAPIException: Database Error with message:
SQLSTATE[42000]: Syntax error or access violation: 1305 FUNCTION tests.doFo16_times does not exist"""
        obj = self._getInstance()

        # When _getFunctionName is called
        functionName, functionType = obj._getFunctionName(data)

        # Then
        self.assertEqual("doFo16_times", functionName)
        self.assertEqual("sqlFunc", functionType)

    def test__getParameterNamesFromString(self):
        data = """public function fu() {
            $this->_db->doFo16_times(    $something,  $some34_thingElse );
            return;
        }"""
        functionName = "doFo16_times";
        obj = self._getInstance()

        # When _getParameterNamesFromString is called
        result = obj._getParameterNamesFromString(data, functionName)

        # Then
        self.assertEqual(["something", "some34_thingElse"], result)

    def test__createFunctionBody(self):
        functionName = "doFo16_times"
        parameterList = ["something", "some34_thingElse"]
        expected = """
CREATE FUNCTION doFo16_times (something INT UNSIGNED, some34_thingElse INT UNSIGNED)
    RETURNS INT UNSIGNED
    BEGIN

        RETURN something;
    END //
"""

        obj = self._getInstance()

        # When _createFunctionBody is called
        result = obj._createFunctionBody(functionName, parameterList)

        # Then
        self.assertEqual(expected, result)

    def test__replaceDelimiter(self):
        data = """Some other stuff

DELIMITER ;
possibly other stuff
"""
        expected = """Some other stuff


newStuff

DELIMITER ;
possibly other stuff
"""
        obj = self._getInstance()

        # When _replaceDelimiter is called
        result = obj._replaceDelimiter(data, "newStuff")

        # Then
        self.assertEqual(expected, result)


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