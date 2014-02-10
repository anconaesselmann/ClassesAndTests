class DataClassFile():
    def functionName1(self, parameter1):
        """ One Function (takes a parameter) with one test function
        (with single line comments) where outdated documentation
        exists.
        
        ************************************************************
        ####UnitTest Specifications
        
        
        - Given: The class file has outdated documentation
          When : Documentation is updated
          Then : The old documentation is replaced by text from the test file
        
             `test_functionName1_test_case_3()`
        
        
        ************************************************************
        
        @param  string $parameter1 a String
        @return string             a String
        """
        say = "say"
        fu = "fu"
        return say + " " + fu