<?php
namespace app\common\controller;

use app\common\model\Meeting;

class MeetingStatus {

    public function getStatus($meeting_id){
        $meeting = Meeting::get($meeting_id);
        $time = time();
        $meeting_date = $meeting->meetingDate()->find();
        $manuscript_date = $meeting_date->manuscript_date;
        $manuscript_modify_date = $meeting_date->manuscript_modify_date;
        $inform_date = $meeting_date->inform_date;
        $register_begin_date = $meeting_date->register_begin_date;
        $register_end_date = $meeting_date->register_end_date;
        $meeting_begin_date = $meeting_date->meeting_begin_date;
        $meeting_end_date = $meeting_date->meeting_end_date;

        $manuscript_date = strtotime($manuscript_date);
        $manuscript_modify_date = strtotime($manuscript_modify_date);
        $inform_date = strtotime($inform_date);
        $register_begin_date = strtotime($register_begin_date);
        $register_end_date = strtotime($register_end_date);
        $meeting_begin_date = strtotime($meeting_begin_date);
        $meeting_end_date = strtotime($meeting_end_date);


        if(time() < $manuscript_date)
            return 0;
        if(time()< $manuscript_modify_date)
            return 1;
        if(time()< $inform_date)
            return 2;
        if(time()< $register_begin_date)
            return 3;
        if(time()< $register_end_date)
            return 4;
        if(time()< $meeting_begin_date)
            return 5;
        if(time()< $meeting_end_date)
            return 6;
        return 7;
    }
}
