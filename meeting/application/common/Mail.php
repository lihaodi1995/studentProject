<?php
namespace app\common;

use think\Facade;

class Mail extends Facade {
    protected static function getFacadeClass() {
        return 'app\common\controller\Mail';
    }
}