<?php
namespace DocumentationFromUnitTestsTestData {
	require_once strstr(__FILE__, 'Test', true).'/aae/std/AutoLoader.php';
	class DataClassFileTest extends \PHPUnit_Framework_TestCase {
		public function test_functionName1_only_test() {
			// Given this special circumstance
			$obj = new aClass();
			$expected = "Some result";
		
			// When this thing happens
			$result = $obj->functionName1();
			
			// Then the thing with the thing gets returned
			$this->assertEquals($expected, $result);
		}
	}
}