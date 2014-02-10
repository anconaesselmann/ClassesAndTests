<?php
class SomeClassNameTest {
	/**
	 * This is the first documentation block.
	 */
	public function test_aMemberFunctionWithParameters() {
		$expected = true;
		$obj = new SomeClassName();
		$parameter1 = "aString";
		$parameter2 = 69;
		$parameter3 = 0.5;
		$parameter4 = false;
		$result = $obj->aMemberFunctionWithParameters(parameter1, parameter2, parameter3, parameter4);

		$this->assertEquals($expected, $result);
	}
	/**
	 * This is the second documentation block.
	 * Sentence two.
	 */
	public function test_aMemberFunctionWithParameters_second_test () {

	}
	/**
	 * This is the third documentation block.
	 * 		Sentence two.
	 * 		Sentence three
	 */
	public function test_aMemberFunctionWithParameters_third_test() {

	}
		/**
		*This is the fourth documentation block.
		*/
		public function test_aMemberFunctionWithParameters_fourth_test(someParameter) 
		{

		}
	public function test_aMemberFunctionWithoutParameters() {
		$obj = new SomeClassName();
		$obj->aMemberFunctionWithoutParameters();
	}
}