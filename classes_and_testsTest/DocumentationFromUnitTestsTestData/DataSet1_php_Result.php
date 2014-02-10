<?php
/**
 * One Function (without parameters) with one test function (with single line comments)
 * where the documentation had not been generated.
 */
namespace  {
	/**
	 * @author Axel Ancona Esselmann
	 * @package 
	 */
	class DataClassFile {
		/**
		 * In General, this fnctn does pretty much just this pretty
		 * simple thing. This can't be deduced by the test's documentation
		 * though, and must be written by the author.
		 * 
		 * ************************************************************
		 * ####UnitTest Specifications
		 * 
		 * 
		 * - Given: this special circumstance
		 *   When : this thing happens
		 *   Then : the thing with the thing gets returned
		 * 
		 *      `test_functionName1_only_test()`
		 * 
		 * 
		 * ************************************************************
		 */
		public function functionName1() {
			$say = "say";
			$fu = "fu";
			return $say . " " . $fu;
		}
	}
}