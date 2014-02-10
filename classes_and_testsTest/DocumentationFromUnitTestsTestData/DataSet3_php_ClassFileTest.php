<?php
namespace DocumentationFromUnitTestsTestData {
	require_once strstr(__FILE__, 'Test', true).'/aae/std/AutoLoader.php';
	class DataClassFileTest extends \PHPUnit_Framework_TestCase {
		public function test_functionName1_test_case_3() {
			// Given: The class file has outdated documentation
			$obj = new aClass();
			$expected = "Some result";
			$parameter1 = False
		
			// When: Documentation is updated
			$result = $obj->functionName1($parameter1);
			
			// Then: The old documentation is replaced by text from the test file
			$this->assertEquals($expected, $result);
		}
	}
}