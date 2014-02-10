class DataClassFileTests():
    def test_functionName6_test_case_6(self):
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
        result = obj.functionName6(parameter1)
        
        """
        Then: Last comment first line.
        Last comment second line.
        Last comment third line.
        Last comment last line.
        """
        this->assertEquals(expected, result)

    def test_functionWithNoDocumentation3_no_comments(self):
        obj = new aClass()
        expected = "Some result"
        parameter1 = False
        result = obj.functionWithNoDocumentation3(parameter1)
        this->assertEquals(expected, result)