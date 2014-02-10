<?php
namespace  {
	/**
	 * @author Axel Ancona Esselmann
	 * @package 
	 */
	class DataClassFile {
		/**
		 * One Function (takes a parameter) with two test functions
		 * (with multi line comments) where outdated documentation
		 * exists.
		 *
		 * ************************************************************
		 * ####UnitTest Specifications
		 * - Given: Old specifications Given: line
		 *   When : Old specifications When: line
		 *   Then : Old specifications Then: line
		 * 
		 *      `test_functionName7_test_case_6()`
		 * ************************************************************
		 * 
		 * @param  string $parameter1 a String
		 * @return string             a String
		 */
		public function functionName7($parameter1) {
			$say = "say";
			$fu = "fu";
			return $say . " " . $fu;
		}
		
		/**
		 * Second function (no parameters) with one test function
		 */
		public function functionName8() {
			$say = "say";
			$fu = "fu";
			return $say . " " . $fu;
		}
	}
}