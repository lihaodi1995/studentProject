<?php
namespace app\common\model;

use think\Model;

class Review extends Model {
    protected $pk = 'review_id';
    protected $autoWriteTimestamp = 'datetime';//开启自动时间戳

    public function manuscript() {
        return $this->belongsTo('Manuscript');
    }
}
