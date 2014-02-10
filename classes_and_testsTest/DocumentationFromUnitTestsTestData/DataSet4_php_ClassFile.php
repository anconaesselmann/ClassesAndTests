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
		 * - Given: Old specifications Given: line
		 *   When : Old specifications When: line
		 *   Then : Old specifications Then: line
		 * 
		 *      `test_functionName1_test_case_4()`
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