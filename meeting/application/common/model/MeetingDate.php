<?php
namespace app\common\model;

use think\Model;

class MeetingDate extends Model {
    protected $pk = 'meeting_date_id';

    public function meeting() {
        return $this->belongsTo('Meeting');
    }
}
