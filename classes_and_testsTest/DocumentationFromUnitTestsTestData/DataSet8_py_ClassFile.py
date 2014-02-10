class DocumentationFromUnitTestsCommand(sublime_plugin.TextCommand):
    def _getMethodNames(self, fileContent, fileExtension):
        """ finds all method names int string "fileContent"
        
        @param str fileContent The content of a class file
        @returns: A list of method names
        """
        return True
    
    def _findDockBlock(self, extension, classFileContent, functionName):
        """ Returns funcitonName's docBlock
    
        @param str classFileContent The content of a class file
        @param str functionName the name of a function
    
        returns: the position and length of the documentation block in classFileContent
        """
        return True