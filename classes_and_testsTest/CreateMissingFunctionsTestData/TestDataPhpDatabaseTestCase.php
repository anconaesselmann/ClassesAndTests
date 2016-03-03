<?php
namespace aae\model {
	require_once strstr(__FILE__, 'Test', true).'/../../../src/aae/autoload/AutoLoader.php';
    $dir = strstr(__FILE__, 'Test', true);
    \aae\autoload\AutoLoader::addDir($dir);
    /**
     * @group database
     */
    class PostTest extends \aae\unitTesting\DbTestCase {
        use \aae\unitTesting\TestFilesTrait;

        public $sut;

        public function setUp() {
            parent::setUp();
            $this->sut = new Post($this->fAPI);
        }

        public function test_fu() {
            # Given SETUP_CONDITIONS

            # When
            $result = $this->sut->fu();

            # Then
            $expected = 1;
            $this->assertEquals($expected, $result);
        }
    }
}