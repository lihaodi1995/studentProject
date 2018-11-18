<?php
namespace app\meeting\controller;

use think\Controller;
use think\facade\Session;
use app\common\AES;
use app\common\MeetingStatus;
use app\common\model\Meeting;
use app\common\model\MeetingDate;
use app\common\model\User;
use app\common\model\Template;

class Index extends controller{
    public function index($meetingId = '') {
        if (strlen($meetingId) == 0) {
            return $this->fetch();
        } else {
            $meetingId = AES::decrypt($meetingId);
            $meeting = Meeting::get($meetingId);
            if (!isset($meeting)) {
                return $this->fetch();
            }
            $template = Template::get($meeting->template_id);
            if (!isset($template)) {
                return $this->fetch();
            }
            $name = $template->name;
            return $this->fetch($name);
        }
    }

    public function indexTest($templateName) {
        return $this->fetch($templateName);
    }

    /*Interface: 查看会议详细信息
    Function: getMeetingDetail
    Url: meeting\index\getMeetingDetail
    Type: post
    Input:{meetingId}
    Output: {errNo, msg, data: {meetingId, companyId, templateId, title, description, solicitInfo, agenda, organization, manuscriptTemplateUrl, fee, accomTraffic, contactUs, place, status, manuscriptDate, manuscriptModifyDate, informDate, registerBeginDate, registerEndDate, meetingBeginDate, meetingEndDate}}
        errNo: 0, msg: '创建成功'，data: {meetingId, companyId, templateId, title, description, solicitInfo, agenda, organization, manuscriptTemplateUrl, fee, accomTraffic, contactUs, place, status, manuscriptDate, manuscriptModifyDate, informDate, registerBeginDate, registerEndDate, meetingBeginDate, meetingEndDate}
        errNo: 1, msg: '参数错误'，data: null
        errNo: 10, msg: '会议不存在', data: null
        errNo: 10, msg: '会议日程不存在', data: null
    NOTE: status: 0-截稿日期之前, 1-修改稿截止日期之前, 2-录用通知日期之前, 3-注册开始日期之前, 4-注册结束日期之前, 5-会议开始日期之前, 6-会议结束日期之前, 7-会议结束日期之后
    */
    public function getMeetingDetail() {
        if ($this->request->isAjax()) {
            $data = input();
            if(isset($data['meetingId'])) {
                $meetingId = AES::decrypt($data['meetingId']);
                $meeting = Meeting::get($meetingId);
                if (!isset($meeting)) {
                    return json(['errNo' => 10, 'msg' => '会议不存在', 'data' => null]);
                }
                $meetingDate = $meeting->meetingDate()->find();
                if (!isset($meetingDate)) {
                    return json(['errNo' => 10, 'msg' => '会议日程不存在', 'data' => null]);
                }

                $returnData = array(
                    'meetingId' => AES::encrypt($meeting->meeting_id),
                    'companyId' => AES::encrypt($meeting->company_id),
                    'templateId' => AES::encrypt($meeting->template_id), 
                    'title' => $meeting->title, 
                    'description' => $meeting->description, 
                    'solicitInfo' => $meeting->solicit_info, 
                    'agenda' => $meeting->agenda, 
                    'organization' => $meeting->organization, 
                    'manuscriptTemplateUrl' => $meeting->manuscript_template_url, 
                    'fee' => $meeting->fee, 
                    'accomTraffic' => $meeting->accom_traffic, 
                    'contactUs' => $meeting->contact_us, 
                    'place' => $meeting->place, 
                    'status' => MeetingStatus::getStatus($meeting->meeting_id), 
                    'manuscriptDate' => $meetingDate->manuscript_date, 
                    'manuscriptModifyDate' => $meetingDate->manuscript_modify_date, 
                    'informDate' => $meetingDate->inform_date, 
                    'registerBeginDate' => $meetingDate->register_begin_date, 
                    'registerEndDate' => $meetingDate->register_end_date, 
                    'meetingBeginDate' => $meetingDate->meeting_begin_date, 
                    'meetingEndDate' => $meetingDate->meeting_end_date, 
                );
                return json(['errNo' => 0, 'msg' => '获取会议详细信息成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }


    /*Interface: 修改会议信息
    Function: modifyMeetingDetail
    Url: meeting/index/modifyMeetingDetail
    Type: post
    Input: {meetingId, templateId, title, description, solicitInfo, agenda, organization, manuscriptTemplateUrl, fee, accomTraffic, contactUs, place, manuscriptDate, manuscriptModifyDate, informDate, registerBeginDate, registerEndDate, meetingBeginDate, meetingEndDate}
        Output: {errNo, msg}
        errNo: 0, msg: '修改成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '会议不存在'
        errNo: 10, msg: '会议日程不存在'
    */
    public function modifyMeetingDetail() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['meetingId'])
            && isset($data['title']) && isset($data['description']) && isset($data['solicitInfo']) && isset($data['templateId'])
            && isset($data['agenda']) && isset($data['organization']) && isset($data['manuscriptTemplateUrl']) && isset($data['fee'])
            && isset($data['accomTraffic']) && isset($data['contactUs']) && isset($data['place']) && isset($data['manuscriptDate'])
            && isset($data['manuscriptModifyDate']) && isset($data['informDate']) && isset($data['registerBeginDate'])
            && isset($data['registerEndDate']) && isset($data['meetingBeginDate']) && isset($data['meetingEndDate'])) {
                $meetingId = AES::decrypt($data['meetingId']);
                $meeting = Meeting::get($meetingId);
                if (!isset($meeting)) {
                    return json(['errNo' => 10, 'msg' => '会议不存在']);
                }
                $meetingDate = $meeting->meetingDate()->find();
                if (!isset($meetingDate)) {
                    return json(['errNo' => 10, 'msg' => '会议日程不存在']);
                }

                $meeting->template_id = AES::decrypt($data['templateId']);
                $meeting->title = $data['title'];
                $meeting->description = $data['description'];
                $meeting->solicit_info = $data['solicitInfo'];
                $meeting->agenda = $data['agenda'];
                $meeting->organization = $data['organization'];
                $meeting->manuscript_template_url = $data['manuscriptTemplateUrl'];
                $meeting->fee = $data['fee'];
                $meeting->accom_traffic = $data['accomTraffic'];
                $meeting->contact_us = $data['contactUs'];
                $meeting->place = $data['place'];
                $meeting->save();

                $meetingDate->meeting_id = $meeting->meeting_id;
                $meetingDate->manuscript_date = $data['manuscriptDate'];
                $meetingDate->manuscript_modify_date = $data['manuscriptModifyDate'];
                $meetingDate->inform_date = $data['informDate'];
                $meetingDate->register_begin_date = $data['registerBeginDate'];
                $meetingDate->register_end_date = $data['registerEndDate'];
                $meetingDate->meeting_begin_date = $data['meetingBeginDate'];
                $meetingDate->meeting_end_date = $data['meetingEndDate'];
                $meetingDate->save();
                
                return json(['errNo' => 0, 'msg' => '修改成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

}