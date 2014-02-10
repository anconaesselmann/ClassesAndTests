class DataClassFileTests():
    def test_functionName7_test_case_6(self):
        """
        Given: Multi Line comment.
        This is line two of the Given: comment
        This is line three
        """
        obj = new aClass()
        expected = "Some result"
        parameter1 = False
    
        """
        When: First line second comment.
        		 Second line first comment.
        """
        result = obj.functionName7(parameter1)
        
        """
        Then: Last comment first line.
        Last comment second line.
        Last comment third line.
        Last comment last line.
        """
        this->assertEquals(expected, result)

class DataClassFileTests():
    def test_functionName7_alternate_format_1(self):
        """Given: Second Test function.
        Line Two.
        Line three"""
        obj = new aClass()
        expected = "Some result"
        parameter1 = False
    
        """When: Second Test Function.
        		 Second comment."""
        result = obj.functionName7(parameter1)
        
        """Then: Second Test Function.
        Third comment.
        Last Line"""
        this->assertEquals(expected, result)

class DataClassFileTests():
    def test_functionName8_only_function(self):
        """
        Given: line 1
        line 2
        line 3
        """
        obj = new aClass()
        expected = "Some result"
        parameter1 = False
    
        """
        When: a line
        """
        result = obj.functionName8(parameter1)
        
        """
        Then: another line.
        """
        this->assertEquals(expected, result)