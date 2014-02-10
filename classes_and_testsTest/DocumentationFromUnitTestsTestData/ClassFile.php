<?php
namespace a\namespace {
	function SomeFunction() {

	}
	class ClassFile {
		/**
		 * [function1 description]
		 * @return [type] [description]
		 */
		public function function1 () {
			return;
		}
		/**
		 * [_function2 description]
		 * @param  int $parameter1 [description]
		 */
		public function _function2($parameter1) {
			return;
		}
		/**
		 * In General, this function does pretty much just this pretty
		 * simple thing. This can't be deduced by the test's documentation
		 * though, and must be written by the author.
		 *
		 ************************************************************
		 * ####UnitTest Speciffications
		 * - When everything is working like it should, this happens.
		 * 
		 *      `aae\mvc\ClassFileTest::test__function2()`
		 *
		 * - When this type of object is passed as parameter
		 *   and the second parameter is NULL,
		 *   the function behaves in this very specific way.
		 *   
		 *      `aae\mvc\ClassFileTest::test__function2_second_test()`
		 *
		 * - When this very specific edge case happens,
		 *   the function has to react in this very different way
		 *   to ensure that this other really bad thing doesn't happen.
		 *   
		 *      `aae\mvc\ClassFileTest::test__function2_thired_test()`
		 *
		 * - In rare cases, this might actually happen. It only happens
		 *   when this other thing happens, and it is dealt with. Trust me.
		 *   Again, this pretty much never happens.
		 *   
		 *      `aae\mvc\ClassFileTest::test__function2_fourth_test()`
		 ************************************************************
		 *
		 * @param  string $parameter1 a String
		 * @param  string $parameter2 a String
		 * @return string             a String
		 */
		public function 	function3	($parameter1, $parameter2) {
			return;
		}
/**
 * 
 */
function function4
() 
{
	return;
}
	}
}