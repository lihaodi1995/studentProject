<?php
namespace app\common;

use think\Facade;

class MeetingStatus extends Facade {
    protected static function getFacadeClass() {
        return 'app\common\controller\MeetingStatus';
    }
}