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
		 * 
		 * 
		 * - Given: Multi Line comment.
		 *          This is line two of the Given: comment
		 *          This is line three
		 *   When : First line second comment.
		 *          Second line first comment.
		 *   Then : Last comment first line.
		 *          Last comment second line.
		 *          Last comment third line.
		 *          Last comment last line.
		 * 
		 *      `test_functionName6_test_case_6()`
		 * 
		 * 
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