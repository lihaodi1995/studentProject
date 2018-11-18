<?php
namespace app\common;

use think\Facade;

class RSA extends Facade {
    protected static function getFacadeClass() {
        return 'app\common\controller\RSA';
    }
}