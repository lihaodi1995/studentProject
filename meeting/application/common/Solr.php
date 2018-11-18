<?php
namespace app\common;

use think\Facade;

class Solr extends Facade {
    protected static function getFacadeClass() {
        return 'app\common\controller\Solr';
    }
}