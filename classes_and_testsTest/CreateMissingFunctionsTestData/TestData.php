<?php
class SomeClassNameTest {
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
	public function test_aMemberFunctionWithoutParameters() {
		$obj = new SomeClassName();
		$obj->aMemberFunctionWithoutParameters();
	}
}