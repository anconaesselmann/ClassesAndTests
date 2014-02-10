<?php
namespace DocumentationFromUnitTestsTestData {
	require_once strstr(__FILE__, 'Test', true).'/aae/std/AutoLoader.php';
	class DataClassFileTest extends \PHPUnit_Framework_TestCase {
		public function test_functionName1_test_case_2() {
			// Given: In the test function single line comments starting with given, when, then
			$obj = new aClass();
			$expected = "Some result";
			$parameter1 = False
		
			// When: one parameter is passed
			$result = $obj->functionName1($parameter1);
			
			// Then: the documentation should be added before the parameter description.
			$this->assertEquals($expected, $result);
		}
	}
}