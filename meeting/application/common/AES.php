<?php
namespace app\common;

use think\Facade;

class AES extends Facade {
    protected static function getFacadeClass() {
        return 'app\common\controller\AES';
    }
}