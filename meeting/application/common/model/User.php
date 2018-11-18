<?php
namespace app\common\model;

use think\Model;

class User extends Model {
    protected $pk = 'user_id';

    public function subscribe() {
        return $this->hasMany('Subscribe', 'user_id');
    }

    public function meetings() {
        return $this->belongsToMany('Meeting', '\\app\\common\\model\\Subscribe', 'meeting_id', 'user_id');
    }

    public function manuscripts() {
        return $this->hasMany('Manuscript', 'user_id');
    }

    public function registers() {
        return $this->hasMany('register', 'user_id');
    }
}
