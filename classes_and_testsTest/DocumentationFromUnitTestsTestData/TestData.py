        def test_thisIsAFunction_first_test(self):
            # Given: these special conditions
            obj = aClass()
            parameter1 = "aString"
            parameter2 = "anotherString"

            # When: this specific thing happens
            result = obj.thisIsAFunction(parameter1, parameter2)
            
            # Then: this thing happens
            expected = "expected String"
            self.assertEqual(expected, result)

        def test_thisIsAFunction_testing_this_other_thing(self):
            /** Given: this other circumstance,
             * and when the thing can't be controlled
             */
            obj = aClass()

            /** When: thisIsAFunction is called,
             * but the main thing was not initialized
             */
            result = obj.thisIsAFunction()
            
            /** Then: we are in a pickle, because
             * we have no idea if this other thing happened
             */
            expected = False
            self.assertEqual(expected, result)

        def test_thisIsAFunction_third_test (self):
            # Given: other one line conditions
            obj = aClass()
            parameter1 = "aString"
            parameter2 = "anotherString"

            # When: this setting is not set
            result = obj.thisIsAFunction(parameter1, parameter2)
            
            # Then: this other thing happens
            expected = "expected String"
            self.assertEqual(expected, result)

        public function test_thisIsAFunction_php_fct($parameter1) {
            // Given: One Line php comment
            $obj = aClass();
            $parameter1 = "aString";
            $parameter2 = "anotherString";

            // When: php second comment
            $result = $obj->thisIsAFunction($parameter1, $parameter2);
            
            // Then: php thired comment
            $expected = "expected String";
            $this->assertEqual($expected, $result);
        }