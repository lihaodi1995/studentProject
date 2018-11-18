<?php
namespace app\common;

use think\Facade;

class Excel extends Facade {
    protected static function getFacadeClass() {
        return 'app\common\controller\Excel';
    }
}