<?php
namespace app\common\model;

use think\Model;

class RegisterAddition extends Model {
    protected $pk = 'register_addition_id';

    public function register() {
        return $this->belongsTo('register');
    }
}
