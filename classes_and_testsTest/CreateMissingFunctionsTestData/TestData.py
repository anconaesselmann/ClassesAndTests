class SomeClassNameTest:
    def test_aMemberFunctionWithParameters(self):
    	expected = True
    	obj = SomeClassName()
        parameter1 = "aString"
    	parameter2 = 69
		parameter3 = 0.5
		parameter4 = False
        result = obj.aMemberFunctionWithParameters(parameter1, parameter2, parameter3, parameter4)

        self.assertEqual(expected, result)
        
    def test_aMemberFunctionWithoutParameters(self):
        obj = SomeClassName()
        result = obj.aMemberFunctionWithoutParameters()