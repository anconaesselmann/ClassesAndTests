class DataClassFileTests():
    def test_functionName1_test_case_2(self):
        # Given: In the test function single line comments starting with given, when, then
        obj = new aClass()
        expected = "Some result"
        parameter1 = False
    
        # When: one parameter is passed
        result = obj.functionName1(parameter1)
        
        # Then: the documentation should be added before the parameter description.
        this->assertEquals(expected, result)