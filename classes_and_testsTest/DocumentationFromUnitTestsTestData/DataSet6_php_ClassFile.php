<?php
namespace  {
	/**
	 * @author Axel Ancona Esselmann
	 * @package 
	 */
	class DataClassFile {
		public function functionWithNoDocumentation1($parameter1) {
			return false;
		}

		/**
		 * Function without any tests
		 */
		public function functionWithNoDocumentation2($parameter1, $parameter2) {
			return false;
		}

		/**
		 * Function with a test but without comments
		 */
		public function functionWithNoDocumentation3($parameter1, $parameter2) {
			return false;
		}

		/**
		 * One Function (takes a parameter) with one test function
		 * (with multi line comments) where outdated documentation
		 * exists. Class file has three functions without documentation
		 *
		 * ************************************************************
		 * ####UnitTest Specifications
		 * - Given: Old specifications Given: line
		 *   When : Old specifications When: line
		 *   Then : Old specifications Then: line
		 * 
		 *      `test_functionName6_test_case_6()`
		 * ************************************************************
		 * 
		 * @param  string $parameter1 a String
		 * @return string             a String
		 */
		public function functionName6($parameter1) {
			$say = "say";
			$fu = "fu";
			return $say . " " . $fu;
		}

		public function functionWithNoDocumentation4($parameter1, $parameter2) {
			return false;
		}
	}
}