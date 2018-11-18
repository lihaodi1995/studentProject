<?php
namespace app\test\controller;

use think\Controller;
use think\facade\Session;
use app\common\AES;
use app\common\RSA;
use app\common\Solr;
use app\common\Mail;
use app\common\PwdHash;
use app\common\MeetingStatus;
use app\common\model\User;
use app\common\model\Subscribe;
use app\common\model\Company;
use app\common\model\CompanyUnit;
use app\common\model\Meeting;
use app\common\model\MeetingDate;
use app\common\model\Manuscript;
use app\common\model\ManuscriptInfo;
use app\common\model\RegisterPerson;
use app\common\model\RegisterAddition;

class Test extends Controller {

    public function phpinfo() {
        phpinfo();
    }

    public function test() {
        echo json_encode(array('1' => 100, '2' => 50));
    }

    public function AESEncrypt($p) {
        $p = AES::encrypt($p);
        echo $p;
        return;
    }

    public function AESDecrypt($p) {
        $p = AES::decrypt($p);
        echo $p;
        return;
    }

    public function addMeetingInfo() {
        // for ($i = 1; $i <= 25; $i++) {
        //     $meeting = Meeting::where('title', 'test_title' . $i)->find();
        //     if (!isset($meeting)) {
        //         $meeting = new Meeting();
        //         $meeting->company_id = 1;
        //         $meeting->title = 'test_title' . $i;
        //         $meeting->description = 'test_description' . $i;
        //         $meeting->solicit_info = 'test_solicit_info' . $i;
        //         $meeting->template = 1;
        //         $meeting->agenda = 'test_agenda' . $i;
        //         $meeting->organization = 'test_organization' . $i;
        //         $meeting->manuscript_template_url = 'null';
        //         $meeting->fee = json_encode(array('1' => 100, '2' => 50));
        //         $meeting->accom_traffic = 'test_accom_traffic' . $i;
        //         $meeting->contact_us = 'test_contact_us' . $i;
        //         $meeting->place = 'test_place' . $i;
        //         $meeting->save();
        //     }
        //     $meetingDate = $meeting->meetingdate()->find();
        //     if (!isset($meetingDate)) {
        //         $meetingDate = new MeetingDate();
        //         $meetingDate->meeting_id = $meeting->meeting_id;
        //         $meetingDate->manuscript_date = date('Y-m-d H:i:s', time() + 864000);
        //         $meetingDate->manuscript_modify_date = date('Y-m-d H:i:s', time() + 864000);
        //         $meetingDate->inform_date = date('Y-m-d H:i:s', time() + 864000);
        //         $meetingDate->register_begin_date = date('Y-m-d H:i:s', time() + 864000);
        //         $meetingDate->register_end_date = date('Y-m-d H:i:s', time() + 864000);
        //         $meetingDate->meeting_begin_date = date('Y-m-d H:i:s', time() + 864000);
        //         $meetingDate->meeting_end_date = date('Y-m-d H:i:s', time() + 864000);
        //         $meetingDate->save();
        //     }
        //     $meetings = Meeting::alias('m')->join('meeting_date d', 'm.meeting_id = d.meeting_id')->order('d.manuscript_date', 'asc')->select();
        //     foreach ($meetings as $meeting) {
        //         dump($meeting);
        //         echo "<br />\n";
        //     }
        // }
        $meeting = Meeting::where('title', '能投稿的会议')->find();
        if (!isset($meeting)) {
            $meeting = new Meeting();
            $meeting->company_id = 1;
            $meeting->template_id = 1;
            $meeting->title = '能投稿的会议';
            $meeting->description = 'test_description';
            $meeting->solicit_info = 'test_solicit_info';
            $meeting->agenda = 'test_agenda';
            $meeting->organization = 'test_organization';
            $meeting->manuscript_template_url = 'null';
            $meeting->fee = json_encode(array('1' => 100, '2' => 50));
            $meeting->accom_traffic = 'test_accom_traffic';
            $meeting->contact_us = 'test_contact_us';
            $meeting->place = 'test_place';
            $meeting->save();
        }
        $meetingDate = $meeting->meetingdate()->find();
        if (!isset($meetingDate)) {
            $meetingDate = new MeetingDate();
            $meetingDate->meeting_id = $meeting->meeting_id;
            $meetingDate->manuscript_date = date('Y-m-d H:i:s', time() + 86400 * 10);
            $meetingDate->manuscript_modify_date = date('Y-m-d H:i:s', time() + 86400 * 11);
            $meetingDate->inform_date = date('Y-m-d H:i:s', time() + 86400 * 12);
            $meetingDate->register_begin_date = date('Y-m-d H:i:s', time() + 86400 * 13);
            $meetingDate->register_end_date = date('Y-m-d H:i:s', time() + 86400 * 14);
            $meetingDate->meeting_begin_date = date('Y-m-d H:i:s', time() + 86400 * 15);
            $meetingDate->meeting_end_date = date('Y-m-d H:i:s', time() + 86400 * 16);
            $meetingDate->save();
        }
        $meetings = Meeting::alias('m')->join('meeting_date d', 'm.meeting_id = d.meeting_id')->select();
        foreach ($meetings as $meeting) {
            dump($meeting);
            echo "<br />\n";
        }
    }

    public function getSearchMeetingNumber($str) {
        //if ($this->request->isAjax()) {
            //$data = input();
            $data['searchString'] = $str;
            if (isset($data['searchString'])) {
                $searchString = $data['searchString'];
                if (!strlen($searchString)) {
                    return json(['errNo' => 10, 'msg' => '搜索内容不能为空', 'data' => null]);
                }
                $limit = 10;
                $page = 1;
                $results = Solr::search('meeting_core', $searchString, $limit, $page);
                if (!isset($results)) {
                    return json(['errNo' => 10, 'msg' => '搜索出现错误', 'data' => null]);
                }
                $number = $results['response']['numFound'];
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => ['number' => $number]]);
            } return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        //} else return $this->error('页面错误');
    }

    /*
    Function: searchMeetings
    Url: index/search/searchMeetings
    Type: post
    Input: {searchString, limit, page}
    Output {errNo, msg, data: {meetingList: array of {meetingId, companyId, templateId, title, description, solicitInfo, agenda, organization, manuscriptTemplateUrl, fee, accomTraffic, contactUs, place, status, manuscriptDate, manuscriptModifyDate, informDate, registerBeginDate, registerEndDate, meetingBeginDate, meetingEndDate}}}
        errNo: 0, msg: '搜索成功', data: {meetingList: array of {meetingId, companyId, templateId, title, description, solicitInfo, agenda, organization, manuscriptTemplateUrl, fee, accomTraffic, contactUs, place, status, manuscriptDate, manuscriptModifyDate, informDate, registerBeginDate, registerEndDate, meetingBeginDate, meetingEndDate}}
        errNo: 1, msg: '参数错误', data: null
        errNo: 3, msg: '请输入正确的分页信息', data: null
        errNo: 10, msg: '搜索内容不能为空', data: null
        errNo: 10, msg: '搜索出现错误', data: null
    */
    public function searchMeetings($str, $limit, $page) {
        //if ($this->request->isAjax()) {
            //$data = input();
            $data['searchString'] = $str;
            $data['limit'] = $limit;
            $data['page'] = $page;
            if (isset($data['searchString']) && isset($data['limit']) && isset($data['page'])) {
                $searchString = $data['searchString'];
                $limit = $data['limit'];
                $page = $data['page'];

                //检查
                if ($limit <= 0 || $page <= 0) {
                    return json(['errNo' => 3, 'msg' => '请输入正确的分页信息', 'data' => null]);
                }
                if (!strlen($searchString)) {
                    return json(['errNo' => 10, 'msg' => '搜索内容不能为空', 'data' => null]);
                }

                $results = Solr::search('meeting_core', $searchString, $limit, $page);
                if (!isset($results)) {
                    return json(['errNo' => 10, 'msg' => '搜索出现错误', 'data' => null]);
                }

                //获取数据
                $results = $results['response']['docs'];
                $returnData['meetingList'] = array();
                $cnt = 0;
                foreach ($results as $key => $result) {
                    $meetingId = $result['id'];
                    $meeting = Meeting::get($meetingId);
                    $meetingDate = $meeting->meetingDate()->find();
                    if (!isset($meetingDate)) {
                        continue;
                    }
                    $meetingDetail = array(
                        'meetingId' => AES::encrypt($meeting->meeting_id),
                        'companyId' => AES::encrypt($meeting->company_id),
                        'template' => AES::encrypt($meeting->template_id), 
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
                    $returnData['meetingList'][] = $meetingDetail;
                }
                return json(['errNo' => 0, 'msg' => '搜索成功', 'data' => $returnData]);
            } return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        //} else return $this->error('页面错误');
    }

    public function getRegisterDeatil()
    {
        $data = input();
       // if (Session::has('userId')) {
        //    $userId = Session::get('userId');
            $user = \app\common\model\User::get(2);
            $returnData['registerDeatil'] = array();
            if (!isset($user)) {
                return json(['errNo' => 10, 'msg' => '会员不存在', 'data' => null]);
            }
            $registers = $user->registers()->select();
            foreach($registers as $registerItem)
            {
                $register = \app\common\model\Register::get($registerItem->register_id);
               // echo $registerItem->register_id."\n";
                $meeting = $register->meeting()->find();
                if(!isset($review))
                    $result = '待审核';
                else
                    $result=$review->result;
                $info = array(
                    'meetingId' => AES::encrypt($meeting->meeting_id),
                    'title' =>$meeting->title,
                    'status'=>$register->check,
                    'type'=>$register->type
                );
                $returnData['registerDeatil'][] = $info;
            }
           return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
      //  } else return json(['errNo' => 2, 'msg' => '未以会员身份登录', 'data' => null]);
    }

}