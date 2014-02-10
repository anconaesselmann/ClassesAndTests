class DocumentationFromUnitTestsCommand(sublime_plugin.TextCommand):
    def _getMethodNames(self, fileContent, fileExtension):
        """ finds all method names int string "fileContent"
        
        
        ************************************************************
        ####UnitTest Specifications
        
        
        - Given: The file content of a php class file
          When : The class file has at least one function
          Then : A list with the names of all functions in fileContent is returned
        
             `test__getMethodNames_php_class_file()`
        
        - Given: The file content of a python class file
          When : The class file has at least one function
          Then : A list with the names of all functions in fileContent is returned
        
             `test__getMethodNames_py_class_file()`
        
        
        ************************************************************
        @param str fileContent The content of a class file
        @returns: A list of method names
        """
        return True
    
    def _findDockBlock(self, extension, classFileContent, functionName):
        """ Returns funcitonName's docBlock
        
        
        ************************************************************
        ####UnitTest Specifications
        
        
        - Given: line1
          When : line2
          Then : line3
        
             `test__findDockBlock()`
        
        
        ************************************************************
        @param str classFileContent The content of a class file
        @param str functionName the name of a function
    
        returns: the position and length of the documentation block in classFileContent
        """
        return True