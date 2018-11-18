<?php
namespace app\common\model;

use think\Model;

class Meeting extends Model {
    protected $pk = 'meeting_id';

    public function company() {
        return $this->belongsTo('Company');
    }

    public function meetingDate() {
        return $this->hasOne('MeetingDate', 'meeting_id')->bind([
            'manuscript_date', 'manuscript_modify_date', 'inform_date', 'register_begin_date', 'register_end_date', 'meeting_begin_date', 'meeting_end_date'
        ]);
    }

    public function users() {
        return $this->belongsToMany('User', '\\app\\common\\model\\Subscribe', 'user_id', 'meeting_id');
    }

    public function manuscripts() {
        return $this->hasMany('Manuscript', 'meeting_id');
    }

    public function registers() {
        return $this->hasMany('Register', 'meeting_id');
    }

    public function subscribes() {
        return $this->hasMany('Subscribe', 'meeting_id');
    }
}
