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
		 *      `test_functionName7_test_case_6()`
		 * 
		 * - Given: Second Test function.
		 *          Line Two.
		 *          Line three
		 *   When : Second Test Function.
		 *          Second comment.
		 *   Then : Second Test Function.
		 *          Third comment.
		 *          Last Line
		 * 
		 *      `test_functionName7_alternate_format_1()`
		 * 
		 * 
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
		 * 
		 * ************************************************************
		 * ####UnitTest Specifications
		 * 
		 * 
		 * - Given: line 1
		 *          line 2
		 *          line 3
		 *   When : a line
		 *   Then : another line.
		 * 
		 *      `test_functionName8_only_function()`
		 * 
		 * 
		 * ************************************************************
		 */
		public function functionName8() {
			$say = "say";
			$fu = "fu";
			return $say . " " . $fu;
		}
	}
}