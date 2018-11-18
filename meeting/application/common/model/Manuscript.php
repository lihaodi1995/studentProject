<?php
namespace app\common\model;

use think\Model;

class Manuscript extends Model {
    protected $pk = 'manuscript_id';
    protected $autoWriteTimestamp = 'datetime';//开启自动时间戳

    public function user() {
        return $this->belongsTo('User');
    }

    public function meeting() {
        return $this->belongsTo('Meeting');
    }

    public function manuscriptInfo() {
        return $this->hasOne('ManuscriptInfo', 'manuscript_id');
    }

    public function review() {
        return $this->hasOne('Review', 'manuscript_id');
    }

    public function register() {
        return $this->hasOne('register', 'manuscript_id');
    }
}
