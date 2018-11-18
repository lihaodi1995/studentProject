<?php
namespace app\common\model;

use think\Model;

class Register extends Model {
    protected $pk = 'register_id';
    protected $autoWriteTimestamp = 'datetime';//开启自动时间戳

    public function user() {
        return $this->belongsTo('User');
    }

    public function meeting() {
        return $this->belongsTo('Meeting');
    }
    
    public function manuscript() {
        return $this->belongsTo('Manuscript');
    }

    public function registerPersons() {
        return $this->hasMany('RegisterPerson', 'register_id');
    }

    public function registerAdditions() {
        return $this->hasMany('RegisterAddition', 'register_id');
    }
}
