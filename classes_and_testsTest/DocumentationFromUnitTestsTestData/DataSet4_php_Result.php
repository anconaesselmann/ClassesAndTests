<?php
namespace  {
	/**
	 * @author Axel Ancona Esselmann
	 * @package 
	 */
	class DataClassFile {
		/**
		 * One Function (takes a parameter) with three test functions 
		 * (with single line comments) where outdated documentation
		 * exists.
		 *
		 * ************************************************************
		 * ####UnitTest Specifications
		 * 
		 * 
		 * - Given: First test function line one
		 *   When : First test function line two
		 *   Then : First test function line three
		 * 
		 *      `test_functionName1_test_case_4()`
		 * 
		 * - Given: Second test function Given: line
		 *   When : Second test function When: line
		 *   Then : Second test function Then: line
		 * 
		 *      `test_functionName1_second_test_function()`
		 * 
		 * - Given: Last test function third from last line
		 *   When : Last test function second from last line
		 *   Then : Last test function last line
		 * 
		 *      `test_functionName1_third_test_function()`
		 * 
		 * 
		 * ************************************************************
		 * 
		 * @param  string $parameter1 a String
		 * @return string             a String
		 */
		public function functionName1($parameter1) {
			$say = "say";
			$fu = "fu";
			return $say . " " . $fu;
		}
	}
}