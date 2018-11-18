<?php
namespace app\common\model;

use think\Model;

class RegisterPerson extends model {
    protected $pk = 'register_person_id';

    public function register() {
        return $this->belongsTo('Register');
    }
}