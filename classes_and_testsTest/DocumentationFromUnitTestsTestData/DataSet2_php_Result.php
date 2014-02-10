<?php
namespace  {
	/**
	 * @author Axel Ancona Esselmann
	 * @package 
	 */
	class DataClassFile {
		/**
		 * One Function (takes a parameter) with one test function 
		 * (with single line comments) where the documentation has not 
		 * been generated.
		 *
		 * ************************************************************
		 * ####UnitTest Specifications
		 * 
		 * 
		 * - Given: In the test function single line comments starting with given, when, then
		 *   When : one parameter is passed
		 *   Then : the documentation should be added before the parameter description.
		 * 
		 *      `test_functionName1_test_case_2()`
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