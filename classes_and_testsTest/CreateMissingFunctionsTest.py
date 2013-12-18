import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from classes_and_tests.CreateMissingFunctions import CreateMissingFunctionsCommand
from classes_and_tests.src.mocking.MockFileSystem import MockFileSystem

class CreateMissingFunctionsTest(unittest.TestCase):
    def _getInstance(self):
        pyClassFile = path.join(os.sep, "MyProject1", "library", "aae", "mvc", "Controller.py")
        phpClassFile = path.join(os.sep, "MyProject1", "library", "aae", "mvc", "Controller.php")
        pyTestFile = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.py")
        phpTestFile = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.php")


        pyTestFileContent = "class SomeClassNameTest:\n    def test_aMemberFunctionWithParameters(self):\n    	parameter1 = \"aString\"\n    	parameter2 = 69\n        obj = SomeClassName()\n        result = obj.aMemberFunctionWithParameters(parameter1, parameter2)\n    def test_aMemberFunctionWithoutParameters(self):\n        obj = SomeClassName()\n        result = obj.aMemberFunctionWithoutParameters()"
        phpTestFileContent = "<?php\nclass SomeClassNameTest {\n	public function test_aMemberFunctionWithParameters() {\n		$parameter1 = \"aString\"\n		$parameter2 = 69\n		$obj = new SomeClassName();\n		$obj->aMemberFunctionWithParameters(parameter1, parameter2);\n	}\n	public function test_aMemberFunctionWithoutParameters() {\n		$obj = new SomeClassName();\n		$obj->aMemberFunctionWithoutParameters();\n	}\n}"
        
        obj = CreateMissingFunctionsCommand()
        obj.fileSystem = MockFileSystem()
        obj.fileSystem.createFile(pyClassFile)
        obj.fileSystem.createFile(phpClassFile)
        obj.fileSystem.createFile(pyTestFile, pyTestFileContent)
        obj.fileSystem.createFile(phpTestFile, phpTestFileContent)

        return obj


    def test_getParameterNames_python_function_has_parameters(self):
        functionName = "aMemberFunctionWithParameters"
        fileDir = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.py")
        expected = ["parameter1", "parameter2"]
        obj = self._getInstance()

        parameterNames = obj._getParameterNames(functionName, fileDir)

        self.assertEqual(expected, parameterNames)

    def test_getParameterNames_python_function_doesnt_have_parameters(self):
    	functionName = "aMemberFunctionWithoutParameters"
    	fileDir = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.py")
    	expected = []
        obj = self._getInstance()

        parameterNames = obj._getParameterNames(functionName, fileDir)

        self.assertEqual(expected, parameterNames)


    def test_getParameterNames_php_function_has_parameters(self):
    	functionName = "aMemberFunctionWithParameters"
    	fileDir = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.php")
    	expected = ["parameter1", "parameter2"]
        obj = self._getInstance()

        parameterNames = obj._getParameterNames(functionName, fileDir)

        self.assertEqual(expected, parameterNames)

    def test_getParameterNames_php_function_doesnt_have_parameters(self):
    	functionName = "aMemberFunctionWithoutParameters"
    	fileDir = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.php")
    	expected = []
        obj = self._getInstance()

        parameterNames = obj._getParameterNames(functionName, fileDir)

        self.assertEqual(expected, parameterNames)

    def test__getFunctionBody_py_function_has_parameters(self):
    	expected = "\ndef aMemberFunctionWithParameters(self, parameter1, parameter2):\n    \"\"\" ${1:__functionDescription__}\n\n    @param str parameter1 ${2:__parameterDescription__}\n    @param int parameter2 ${3:__parameterDescription__}\n\n    returns: ${4:__returnTypeDescription__}\n    \"\"\"\n    ${5:# FunctionBody};\n    return${6:}\n"
    	obj = self._getInstance()
    	fileName = path.join(os.sep, "MyProject1", "library", "aae", "mvc", "Controller.py")
    	functionName = "aMemberFunctionWithParameters"
    	indent = "    "
    	parameters = ["parameter1", "parameter2"]

    	functionBody = obj._getFunctionBody(fileName, functionName, indent, parameters)

    	self.assertEqual(expected, functionBody)

    def test__getFunctionBody_php_function_has_parameters(self):
    	expected = "\n\t/**\n\t * ${1:__functionDescription__}\n\t * @param str $parameter1${2:__parameterDescription__}\n\t * @param int $parameter2${3:__parameterDescription__}\n\t */\n\tpublic function aMemberFunctionWithParameters(\\$parameter1\\,\\ \\$parameter2) {\n\t\t${4://FunctionBody};\n\t\treturn${5:};\n\t}${6:}\n"
    	obj = self._getInstance()
    	fileName = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest.php")
    	functionName = "aMemberFunctionWithParameters"
    	indent = "\t"
    	parameters = ["$parameter1", "$parameter2"]

    	functionBody = obj._getFunctionBody(fileName, functionName, indent, parameters)

    	self.assertEqual(expected, functionBody)

    def _dataProvider_getParameterType_python(self):
    	return dict(
    		dataPy = "class SomeClassNameTest:\n	def test_aFunctionName(self):\n		expected = True\n		obj = SomeClassName()\n		parameter1 = \"aString\"\n		parameter2 = 69\n		parameter3 = 0.5\n		parameter4 = 51924361L\n		parameter5 = 3.14j\n		parameter6 = False\n		parameter7 = dict(value1 = 1, value2 = 2)\n		parameter8 = [1, 2, 3]\n		parameter9 = (1, 2)\n		result = obj.aFunctionName(parameter1, parameter2, parameter3, parameter4, parameter5)\n\n        self.assertEqual(expected, result)",
    		dataPhp = "<?php\nclass SomeClassNameTest {\n	public function test_aFunctionName() {\n		$expected = true;\n		$obj = new SomeClassName();\n		$parameter1 = \"aString\";\n		$parameter2 = 69;\n		$parameter3 = 0.5;\n		$parameter6 = false;\n		$result = $obj->aFunctionName($parameter1, $parameter2, $parameter3, $parameter6);\n\n		$this->assertEquals($expected, $result);\n	}\n}",
    		string = "parameter1",
    		integer = "parameter2",
    		float = "parameter3"
    	)
    def test__getParameterType_Determine_the_type_of_a_parameter_of_a_python_function(self):
    	fileDir = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest1.py")
    	functionName = "aFunctionName"
    	data = self._dataProvider_getParameterType_python()["dataPy"]

    	obj = self._getInstance()
    	obj.fileSystem.createFile(fileDir, data)

    	parameterName = self._dataProvider_getParameterType_python()["string"]
    	stringResult = obj._getParameterType(fileDir, functionName, parameterName)
		
    	parameterName = self._dataProvider_getParameterType_python()["integer"]
    	intResult = obj._getParameterType(fileDir, functionName, parameterName)

    	parameterName = self._dataProvider_getParameterType_python()["float"]
    	floatResult = obj._getParameterType(fileDir, functionName, parameterName)

    	self.assertEqual("str", stringResult)
    	self.assertEqual("int", intResult)
    	self.assertEqual("float", floatResult)

    def test__getParameterType_Determine_the_type_of_a_parameter_of_a_php_function(self):
    	fileDir = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest1.php")
    	functionName = "aFunctionName"
    	data = self._dataProvider_getParameterType_python()["dataPhp"]

    	obj = self._getInstance()
    	obj.fileSystem.createFile(fileDir, data)

    	parameterName = self._dataProvider_getParameterType_python()["string"]
    	stringResult = obj._getParameterType(fileDir, functionName, parameterName)
		
    	parameterName = self._dataProvider_getParameterType_python()["integer"]
    	intResult = obj._getParameterType(fileDir, functionName, parameterName)

    	parameterName = self._dataProvider_getParameterType_python()["float"]
    	floatResult = obj._getParameterType(fileDir, functionName, parameterName)

    	self.assertEqual("str", stringResult)
    	self.assertEqual("int", intResult)
    	self.assertEqual("float", floatResult)

    def test__getParameterType_Return_type_when_parameter_can_not_be_determined(self):
    	fileDir = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest1.py")
    	functionName = "aFunctionName"
    	data = self._dataProvider_getParameterType_python()["dataPy"]

    	obj = self._getInstance()
    	obj.fileSystem.createFile(fileDir, data)

    	parameterName = "doesNotExist"
    	result = obj._getParameterType(fileDir, functionName, parameterName)

    	self.assertEqual("__type__", result)

    """def test__getParameterType_Determine_the_type_of_a_parameter_of_a_php_function(self):
    	fileDir = path.join(os.sep, "MyProject1", "library", "aaeTest", "mvc", "ControllerTest1.php")
    	functionName = "set"
    	data = "<?php\nnamespace aae\resources {\n	require_once strstr(__FILE__, 'Test', true).'/aae/std/AutoLoader.php';\n	class LanguageTest extends \PHPUnit_Framework_TestCase {\n		public function test___construct() {\n			$obj = new Language();\n		}\n\n		public function test_set() {\n			$l = new Language();\n			$languageString = \"eng\";\n			$l->fileSystem = $this->getMock('aae\resources\FileSystem');\n			$l->set($languageString);\n		}\n	}\n}"

    	obj = self._getInstance()
    	obj.fileSystem.createFile(fileDir, data)

    	parameterName = "$languageString"
    	stringResult = obj._getParameterType(fileDir, functionName, parameterName)
		
    	
    	self.assertEqual("str", stringResult)"""



if __name__ == '__main__':
    unittest.main()