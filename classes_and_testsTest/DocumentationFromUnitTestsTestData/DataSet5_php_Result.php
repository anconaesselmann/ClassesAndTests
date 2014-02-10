<?php
namespace  {
	/**
	 * @author Axel Ancona Esselmann
	 * @package 
	 */
	class DataClassFile {
		/**
		 * One Function (takes a parameter) with one test function
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
		 *      `test_functionName5_test_case_5()`
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
		 *      `test_functionName5_alternate_format_1()`
		 * 
		 * 
		 * ************************************************************
		 * 
		 * @param  string $parameter1 a String
		 * @return string             a String
		 */
		public function functionName5($parameter1) {
			$say = "say";
			$fu = "fu";
			return $say . " " . $fu;
		}
	}
}