<?php
namespace app\common;

use think\Facade;

class Pwdhash extends Facade {
    protected static function getFacadeClass() {
        return 'app\common\controller\PwdHash';
    }
}