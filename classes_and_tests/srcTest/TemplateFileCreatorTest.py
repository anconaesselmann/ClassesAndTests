import unittest
import os
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.abspath(path.join(__file__, "..", "..")))

from src.MirroredDirectory import MirroredDirectory
from src.TemplateFileCreator import TemplateFileCreator
from src.mocking.MockFileManipulator import MockFileManipulator
from src.mocking.sublime import MockSettings

class UnitTestHelpers:

    @staticmethod
    def dictIsEqual(expected, result, printErrors=True, returnErrors=False):
        isEqual = True
        errors = dict()
        try:
            for expKey, expVal in expected.iteritems():
                if result[expKey] != expected[expKey]:
                    isEqual = False
                    errors[expKey] = "expected[" + expKey + "] == " + expected[expKey] + " != " + "result[" + expKey + "] == " + result[expKey]
            for resKey, resVal in result.iteritems():
                if result[resKey] != expected[resKey]:
                    isEqual = False
                    errors[expKey] = "expected[" + expKey + "] != " + "result[" + expKey + "]"
        except Exception, e:
            errors["missingKey"] = "Keys are not equal"
            isEqual = False

        if isEqual is False:
            if returnErrors is True:
                isEqual = errors
            if printErrors is True:
                for e, message in errors.iteritems():
                   print(message)

        return isEqual


class MockPHPFunctionCollectionObject(object):
    def get_php_namespace(self, args):
        expected = {'command': 'get_php_namespace',
                    'dir': '/MyProject1/library/aae/mvc/Controller.php',
                    'name': 'namespace',
                    'settings': "{'base_path': '/MyProject1/library'}"}
        if UnitTestHelpers.dictIsEqual(expected, args):
            return "aae\\mvc"
        else:
            return "ERROR"

    def get_class_name(self, args):
        expected = {'command': 'get_class_name',
                    'dir': '/MyProject1/library/aae/mvc/Controller.php',
                    'name': 'class_name',
                    'settings': '{}'}
        if UnitTestHelpers.dictIsEqual(expected, args):
            return "MockedClassSuccess"
        else:
            return "ERROR"

    def get_doc_block_tag(self, args):
        if args["name"] == "author":
            expected = {'command': 'get_doc_block_tag',
                        'dir': '/MyProject1/library/aae/mvc/Controller.php',
                        'name': 'author',
                        'settings': "{'author': 'Axel'}"}
            if UnitTestHelpers.dictIsEqual(expected, args):
                return "@author Axel"
            else:
                return "ERROR"
        elif args["name"] == "license":
            expected = {'command': 'get_doc_block_tag',
                        'dir': '/MyProject1/library/aae/mvc/Controller.php',
                        'name': 'license',
                        'settings': "{'license': None}"}
            if UnitTestHelpers.dictIsEqual(expected, args):
                return None
            else:
                return "ERROR"
        else:
            return None

class MockImporter:
	def __init__(self):
		self._mockObjects = dict()

	def setObjectInstance(self, functionFileDir, ClassName, functionCollectionObject):
		self._mockObjects[functionFileDir + " " + ClassName] = functionCollectionObject

	def getObjectInstance(self, functionFileDir, ClassName):
		return self._mockObjects[functionFileDir + " " + ClassName]

class TemplateFileCreatorTest(unittest.TestCase):
    def _getSettings(self):
        settings = MockSettings()
        settings.set("author", "Axel")
        settings.set("base_path", "/MyProject1/library")
        settings.set("license", None)

        return settings

    def test_UnitTestHelpers_dictIsEqual_dicts_are_equal(self):
        dict1 = {"a": None, "b": "works", "c": "Cam"}
        dict2 = {"a": None, "b": "works", "c": "Cam"}
        result = UnitTestHelpers.dictIsEqual(dict1, dict2, False)
        self.assertEqual(True, result)

    def test_UnitTestHelpers_dictIsEqual_dicts_are_equal_length_but_not_equal(self):
        dict1 = {"a": None, "b": "works", "c": "Cam"}
        dict2 = {"a": None, "b": "works", "c": "Cam1"}
        result = UnitTestHelpers.dictIsEqual(dict1, dict2, False)
        self.assertEqual(False, result)


    def test_UnitTestHelpers_dictIsEqual_dicts_are_not_equal_length_and_not_equal(self):
        dict1 = {"a": None, "b": "works", "c": "Cam"}
        dict2 = {"a": None, "b": "works", "c": "Cam", "d": "other value"}
        result = UnitTestHelpers.dictIsEqual(dict1, dict2, False)
        self.assertEqual(False, result)


    def test___init__(self):
        aPath = "/test.txt"
        obj = TemplateFileCreator(aPath)

    def test_getArgsDictFromVarContent_could_not_be_evaluated_exception(self):
        aPath = "/MyProject1/library/aae/mvc/Controller.php"
        basePath = "/MyProject1/library"
        variableContent = None

        fc = TemplateFileCreator(aPath)
        self.assertRaises(TypeError, lambda: fc.getArgsDictFromVarContent(variableContent))

    def test_getArgsDictFromVarContent(self):
        aPath = "/MyProject1/library/aae/mvc/Controller.php"
        basePath = "/MyProject1/library"
        variableContent = "[\n    {\n        \"variable\": \"namespace\",\n        \"command\": \"get_php_namespace\",\n        \"fromSettings\": [\"base_path\"]\n    },\n    {\n        \"variable\": \"class_name\",\n        \"command\": \"get_class_name\"\n    },\n    {\n        \"variable\": \"author\",\n        \"command\": \"get_doc_block_tag\",\n        \"fromSettings\": [\"author\"]\n    },\n    {\n        \"variable\": \"license\",\n        \"command\": \"get_doc_block_tag\",\n        \"fromSettings\": [\"license\"]\n    }\n]"
        expected = {'author': {'command': 'get_doc_block_tag',
                               'dir': '/MyProject1/library/aae/mvc/Controller.php',
                               'name': 'author',
                               'settings': "{'author': 'Axel'}"},
                    'class_name': {'command': 'get_class_name',
                                   'dir': '/MyProject1/library/aae/mvc/Controller.php',
                                   'name': 'class_name',
                                   'settings': '{}'},
                    'license': {'command': 'get_doc_block_tag',
                                'dir': '/MyProject1/library/aae/mvc/Controller.php',
                                'name': 'license',
                                'settings': "{'license': None}"},
                    'namespace': {'command': 'get_php_namespace',
                                  'dir': '/MyProject1/library/aae/mvc/Controller.php',
                                  'name': 'namespace',
                                  'settings': "{'base_path': '/MyProject1/library'}"}}
        self.maxDiff = None
        fc = TemplateFileCreator(aPath)
        fc.setBasePath(basePath)
        fc.setSettings(self._getSettings())
        result = fc.getArgsDictFromVarContent(variableContent)

        self.assertEqual(result, expected)

    def test_getCursorsFromContent_one_cursor(self):
        aPath = "/MyProject1/library/aae/mvc/Controller.php"
        templateContent = "<?php\n/**\n *\n */\nnamespace /* @namespace */ {\n    /**\n     * /* @author */\n     * /* @license */\n     * @package /* @namespace */\n     */\n    class /* @class_name */ {\n        Before/* @cursor */After\n    }\n}"
        expected = [(11, 14)]
        fc = TemplateFileCreator(aPath)

        result = fc.getCursorsFromContent(templateContent)
        self.assertEqual(expected, result)


    def test_getCursorsFromContent_multiple_cursors(self):
        aPath = "/MyProject1/library/aae/mvc/Controller.php"
        templateContent = "/* @cursor */<?php\n/**\n *\n */\nnamespace /* @namespace */ {\n    /**\n     * /* @author */\n/* @cursor */     * /* @license */\n    /* @cursor */ * @package /* @namespace */\n     */\n    class /* @class_name */ {\n        /* @cursor */\n    }\n}/* @cursor */"
        expected = [(0, 0), (7, 0), (8, 4), (11, 8), (13, 1)]
        fc = TemplateFileCreator(aPath)

        result = fc.getCursorsFromContent(templateContent)
        self.assertEqual(expected, result)

    def test_getCursorsFromContent_multiple_cursors_in_same_line(self):
        aPath = "/MyProject1/library/aae/mvc/Controller.php"
        templateContent = "<?php\n/**\n *\n */\nnamespace /* @namespace */ {\n    /**\n     * /* @author */\n     * /* @license */\n     * @package /* @namespace */\n     */\n    class /* @class_name */ {\n/* @cursor */123456789/* @cursor */\n    }\n}"
        expected = [(11, 0), (11, 9)]
        fc = TemplateFileCreator(aPath)

        result = fc.getCursorsFromContent(templateContent)
        self.assertEqual(expected, result)

    def test_getCursorsFromContent_no_cursors(self):
        aPath = "/MyProject1/library/aae/mvc/Controller.php"
        templateContent = "<?php\n/**\n *\n */\nnamespace /* @namespace */ {\n    /**\n     * /* @author */\n     * /* @license */\n     * @package /* @namespace */\n     */\n    class /* @class_name */ {\n        \n    }\n}"
        expected = []
        fc = TemplateFileCreator(aPath)

        result = fc.getCursorsFromContent(templateContent)
        self.assertEqual(expected, result)

    def test_getReplacements_no_class_instance_exception(self):
        aPath = "/MyProject1/library/aae/mvc/Controller.php"
        functionCollectionObject = None
        args = {}

        fc = TemplateFileCreator(aPath)
        self.assertRaises(Exception, lambda: fc.getReplacements(args, functionCollectionObject))

    def test_getReplacements(self):
        aPath = "/MyProject1/library/aae/mvc/Controller.php"
        basePath = "/MyProject1/library"
        args = {'author': {'command': 'get_doc_block_tag',
                           'dir': '/MyProject1/library/aae/mvc/Controller.php',
                           'name': 'author',
                           'settings': "{'author': 'Axel'}"},
                'class_name': {'command': 'get_class_name',
                               'dir': '/MyProject1/library/aae/mvc/Controller.php',
                               'name': 'class_name',
                               'settings': '{}'},
                'license': {'command': 'get_doc_block_tag',
                            'dir': '/MyProject1/library/aae/mvc/Controller.php',
                            'name': 'license',
                            'settings': "{'license': None}"},
                'namespace': {'command': 'get_php_namespace',
                              'dir': '/MyProject1/library/aae/mvc/Controller.php',
                              'name': 'namespace',
                              'settings': "{'base_path': '/MyProject1/library'}"}}
        functionCollectionObject = MockPHPFunctionCollectionObject()
        expected = {'/* @author */': '@author Axel',
                    '/* @class_name */': 'MockedClassSuccess',
                    '/* @license */': None,
                    '/* @namespace */': 'aae\\mvc'}

        fc = TemplateFileCreator(aPath)
        fc.setBasePath(basePath)
        fc.setSettings(self._getSettings())

        result = fc.getReplacements(args, functionCollectionObject)
        self.assertEqual(result, expected)

    def test_getReplacedContent_for_php_class(self):
        aPath = "/MyProject1/library/aae/mvc/Controller.php"
        basePath = "/MyProject1/library"
        templateContent = "<?php\n/**\n *\n */\nnamespace /* @namespace */ {\n    /**\n     * /* @author */\n     * /* @license */\n     * @package /* @namespace */\n     */\n    class /* @class_name */ {\n        /* @cursor */\n    }\n}"
        variableContent = "[\n    {\n        \"variable\": \"namespace\",\n        \"command\": \"get_php_namespace\",\n        \"fromSettings\": [\"base_path\"]\n    },\n    {\n        \"variable\": \"class_name\",\n        \"command\": \"get_class_name\"\n    },\n    {\n        \"variable\": \"author\",\n        \"command\": \"get_doc_block_tag\",\n        \"fromSettings\": [\"author\"]\n    },\n    {\n        \"variable\": \"license\",\n        \"command\": \"get_doc_block_tag\",\n        \"fromSettings\": [\"license\"]\n    }\n]"
        functionCollectionObject = MockPHPFunctionCollectionObject()

        expected = "<?php\n/**\n *\n */\nnamespace aae\mvc {\n    /**\n     * @author Axel\n     * @package aae\mvc\n     */\n    class MockedClassSuccess {\n        \n    }\n}"
        expectedCursorPos = [(10, 8)]
        fc = TemplateFileCreator(aPath)
        fc.setBasePath(basePath)
        fc.setSettings(self._getSettings())
        result = fc.getReplacementContent(templateContent, variableContent, functionCollectionObject)
        resultCursorPos = fc.getCursors()
        self.assertEqual(result, expected)
        self.assertEqual(expectedCursorPos, resultCursorPos)

    def test_set_and_getTemplateDir(self):
        aPath = "/MyProject1/library/aae/mvc/Controller.php"
        fc = TemplateFileCreator(aPath)
        templateDir = path.join("Path", "to", "Templates")

        fc.setTemplateDir(templateDir)
        result = fc.getTemplateDir()
        self.assertEqual(templateDir, result)

    def test_classifyKind(self):
    	aPath = "/MyProject1/library/aae/mvc/Controller.php"
        fc = TemplateFileCreator(aPath)
        expectedKind = "class"
        result = fc.classifyKind()
        self.assertEqual(expectedKind, result)

    def test_createFromTemplate(self):
        aPath = "/MyProject1/library/aae/mvc/Controller.php"
        basePath = "/MyProject1/library"
        templateDir = "/Users/axelesselmann/Documents/Dropbox/python/sublimePackages/ClassesAndTests/templates"
        templateFileDir = os.path.join(templateDir, "php", "class.template")
        variableFileDir = os.path.join(templateDir, "php", "class.variables")
        functionFileDir = os.path.join(templateDir, "php", "functions.py")
        templateContent = "<?php\n/**\n *\n */\nnamespace /* @namespace */ {\n    /**\n     * /* @author */\n     * /* @license */\n     * @package /* @namespace */\n     */\n    class /* @class_name */ {\n        /* @cursor */\n    }\n}"
        variableContent = "[\n    {\n        \"variable\": \"namespace\",\n        \"command\": \"get_php_namespace\",\n        \"fromSettings\": [\"base_path\"]\n    },\n    {\n        \"variable\": \"class_name\",\n        \"command\": \"get_class_name\"\n    },\n    {\n        \"variable\": \"author\",\n        \"command\": \"get_doc_block_tag\",\n        \"fromSettings\": [\"author\"]\n    },\n    {\n        \"variable\": \"license\",\n        \"command\": \"get_doc_block_tag\",\n        \"fromSettings\": [\"license\"]\n    }\n]"
        functionCollectionObject = MockPHPFunctionCollectionObject
        #print("\n" + templateFileDir)
        fc = TemplateFileCreator(aPath)
        fc.setBasePath(basePath)
        fc.setSettings(self._getSettings())
        fc.setTemplateDir(templateDir)
        fc.fileManipulator = MockFileManipulator()
        fc.fileManipulator.createFile(templateFileDir, templateContent)
        fc.fileManipulator.createFile(variableFileDir, variableContent)
        fc.importer = MockImporter()
        fc.importer.setObjectInstance(functionFileDir, "FunctionCollection", functionCollectionObject)
        result = fc.createFromTemplate()

        self.assertEqual(True, result)

    def test_determine_kind_with_default_extension(self):
        aPath = "/MyProject1/library/aae/mvc/Controller"
        defaultFileExtension = "php"
        expectedKind = "class"

        fc = TemplateFileCreator(aPath)
        fc.setDefaultExtension(defaultFileExtension)

        result = fc.classifyKind()

        self.assertEqual(expectedKind, result)

    def test_setKind(self):
        aPath = "/MyProject1/library/aae/mvc/Controller.php"
        expectedPath = "/MyProject1/library/aae/mvc/ControllerTest.php"
        fc = TemplateFileCreator(aPath)
        fc._fileComponents.fileManipulator = MockFileManipulator()
        fc.setKind(MirroredDirectory.KIND_IS_TEST)
        result = fc.getFileName()

        self.assertEqual(expectedPath, result)

    def test_setDefaultExtension(self):
        aPath = "/MyProject1/library/aae/mvc/Controller"
        defaultFileExtension = "php"
        expected = "/MyProject1/library/aae/mvc/Controller.php"
        fc = TemplateFileCreator(aPath)
        fc.setDefaultExtension(defaultFileExtension)

        result = fc.getFileName()

        self.assertEqual(expected, result)

    def test_setDefaultExtension_call_set_after_setting_default_file_extension(self):
        aPath = "/Some/Thing/Completely/different.php"
        anotherPath = "/MyProject1/library/aae/mvc/Controller"

        defaultFileExtension = "php"
        expected = "/MyProject1/library/aae/mvc/Controller.php"
        fc = TemplateFileCreator(aPath)
        fc.setDefaultExtension(defaultFileExtension)

        fc.set(anotherPath)

        result = fc.getFileName()

        self.assertEqual(expected, result)



if __name__ == '__main__':
    unittest.main()