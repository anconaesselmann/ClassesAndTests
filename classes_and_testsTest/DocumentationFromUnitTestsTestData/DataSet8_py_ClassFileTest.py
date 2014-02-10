class DocumentationFromUnitTests(unittest.TestCase):

    def test__getMethodNames_php_class_file(self):
        # Given: The file content of a php class file
        obj           = DocumentationFromUnitTestsCommand()
    
        # When: The class file has at least one function
        result = obj._getMethodNames(fileContent, fileExtension)
        
        # Then: A list with the names of all functions in fileContent is returned
        self.assertEqual(expected, result)

    def test__getMethodNames_py_class_file(self):
        # Given: The file content of a python class file
        obj           = DocumentationFromUnitTestsCommand()
    
        # When: The class file has at least one function
        result = obj._getMethodNames(fileContent, fileExtension)
        
        # Then: A list with the names of all functions in fileContent is returned
        self.assertEqual(expected, result)
        
    def test__findDockBlock(self, extension, classFileContent, functionName, expected):
        # Given: line1
        obj = DocumentationFromUnitTestsCommand()
        
        # When: line2
        result = obj._findDockBlock(extension, classFileContent, functionName)
        
        # Then: line3
        self.assertEqual(expected, result)