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
		 * - Given: Old specifications Given: line
		 *   When : Old specifications When: line
		 *   Then : Old specifications Then: line
		 * 
		 *      `test_functionName5_test_case_5()`
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