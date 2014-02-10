class DataClassFile():
    def functionWithNoDocumentation1(self, parameter1):
        return False

    def functionWithNoDocumentation2(self, parameter1, parameter2):
        """ Function without any tests
        """
        return False

    def functionWithNoDocumentation3(self, parameter1, parameter2):
        """
        Function with a test but without comments
        """
        return False

    def functionName6(self, parameter1):
        """ One Function (takes a parameter) with one test function
        (with multi line comments) where outdated documentation
        exists. Class file has three functions without documentation
        
        ************************************************************
        ####UnitTest Specifications
        - Given: Old specifications Given: line
          When : Old specifications When: line
          Then : Old specifications Then: line
        
             `test_functionName6_test_case_6()`
        ************************************************************
        
        
        ************************************************************
        
        @param  string parameter1 a String
        @return string             a String
        """
        say = "say"
        fu = "fu"
        return say + " " + fu

    def functionWithNoDocumentation4(parameter1, parameter2):
        return False