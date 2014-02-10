class SomeClassNameTest:
    def test_aMemberFunctionWithParameters(self):
        """ This is the first documentation block.
        """
        expected = True
        obj = SomeClassName()
        parameter1 = "aString"
        parameter2 = 69
        parameter3 = 0.5
        parameter4 = False
        result = obj.aMemberFunctionWithParameters(parameter1, parameter2, parameter3, parameter4)

        self.assertEqual(expected, result)

    
    def test_aMemberFunctionWithParameters_second_test (self):
        """ This is the second documentation block.
Sentence two.
        """
        pass
    
    def test_aMemberFunctionWithParameters_third_test(self):
        """ This is the third documentation block.
		Sentence two.
		Sentence three
        """
        pass
    
        @staticmethod
        def test_aMemberFunctionWithParameters_fourth_test() :
            """ This is the fourth documentation block.
            """ 
            pass
        
    def test_aMemberFunctionWithoutParameters(self):
        obj = SomeClassName()
        result = obj.aMemberFunctionWithoutParameters()