<?php
namespace app\index\controller;

use think\Controller;
use think\facade\Session;
use app\common\AES;
use app\common\Solr;
use app\common\Mail;
use app\common\MeetingStatus;
use app\common\model\Meeting;
use app\common\model\MeetingDate;

/*
模块: index
    控制器: index
        页面方法: index(主页)
    控制器: login
        页面方法: index(登录页), signUp(注册页)
    控制器: user
        页面方法: index(会员主页)

模块: company
    控制器: index
        页面方法: index(单位主页), meeting(发布会议页面), edit(修改会议页面)
    控制器: verify
        页面方法: index(单位填写认证信息页)
    控制器: review
        页面方法: index(单位录入评审结果)

模块: meeting
    控制器: index
        页面方法: index(会议详细信息页,判断查看者身份)
    控制器: manuscript
        页面方法: index(会议投稿页), list(查看会议收到稿件列表页), detail(查看稿件详细信息页)
    控制器: register
        页面方法: index(会议注册页), list(查看会议注册列表页), detail(查看注册详细信息页)

模块: admin
    控制器: index
        页面方法: index(单位审核列表页面), verify(查看单位审核信息页)
    控制器: login
        页面方法: index(管理员登录页)
    控制器: template
        页面方法: index(管理模板页)
*/

class Index extends Controller {
    public function index() {
      return $this->fetch();
    }

    /*Interface: 获取登录状态
    Function: getLoginStatus
    Url: index/index/getLoginStatus
    Type: post
    Input: {}
    Output: {errNo, msg, data: {status}}
        errNo: 0, msg: '获取成功'
        NOTE: status: 0-未登录, 1-会员登录, 2-单位登录, 3-单位个人帐号登录
    */
    public function getLoginStatus() {
        if ($this->request->isAjax()) {
            if (Session::has('userId')) {
                Session::pull('companyId');
                Session::pull('companyUnitId');
                $status = 1;
            } else if (Session::has('companyId')) {
                Session::pull('companyUnitId');
                $status = 2;
            } else if (Session::has('companyUnitId')) {
                $status = 3;
            } else $status = 0;
            $returnData['status'] = $status;
            return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取状态为投稿中的会议数量
    Function: getMeetingCountStatusSolicit
    Url: index/index/getMeetingCountStatusSolicit
    Type: post
    Input: {}
    Output: {errNo, msg, data: {count}}
        errNo: 0, msg: '获取成功'
    */
    public function getMeetingCountStatusSolicit() {
        if ($this->request->isAjax()) {
            $now = date('Y-m-d H:i:s', time());
            $returnData['count'] = Meeting::alias('m')->join('meeting_date d', 'm.meeting_id = d.meeting_id')->where("manuscript_date > '$now'")->count();
            return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取状态为投稿中的会议列表
    Function: getMeetingListStatusSolicit
    Url: index/index/getMeetingListStatusSolicit
    Type: post
    Input: {limit, page}
    Output: {errNo, msg, data: {meetingList: array of {meetingId, companyId, title, description, solicitInfo, agenda, organization, manuscriptDate, informDate, manuscriptModifyDate, registerBeginDate, registerEndDate, meetingBeginDate, meetingEndDate, status, place}}}
        errNo: 0, msg: '获取成功'，data: {meetingList: array of {meetingId, companyId, title, description, solicitInfo, agenda, organization, manuscriptDate, informDate, manuscriptModifyDate, registerBeginDate, registerEndDate, meetingBeginDate, meetingEndDate, status, place}}
        errNo: 1, msg: '参数错误'，data: null
        errNo: 3, msg: '分页信息错误', data: null
    NOTE: status: 0-截稿日期之前, 1-修改稿截止日期之前, 2-录用通知日期之前, 3-注册开始日期之前, 4-注册结束日期之前, 5-会议开始日期之前, 6-会议结束日期之前, 7-会议结束日期之后
    */
    public function getMeetingListStatusSolicit() {
        if ($this->request->isAjax()) {
            $data = input();
            if(isset($data['page']) && isset($data['limit'])){
                $page = $data['page'];
                $limit = $data['limit'];
                if ($limit < 0 || $page < 0 || ($limit != 0 && $page == 0)) {
                    return json(['errNo' => 3, 'msg' => '分页信息错误', 'data' => null]);
                }
                $now = date('Y-m-d H:i:s', time());
                if ($limit == 0) {
                    $meetings = Meeting::alias('m')->join('meeting_date d', 'm.meeting_id = d.meeting_id')->where("(manuscript_date > '$now') OR ((register_begin_date < '$now') AND (register_end_date > '$now'))")->order('manuscript_date', 'asc')->select();
                } else {
                    $meetings = Meeting::alias('m')->join('meeting_date d', 'm.meeting_id = d.meeting_id')->where("(manuscript_date > '$now') OR ((register_begin_date < '$now') AND (register_end_date > '$now'))")->order('manuscript_date', 'asc')->page($page, $limit)->select();
                } 
                $returnData['meetingList'] = array();
                foreach ($meetings as $meeting) {
                    $info = array(
                        'meetingId' => AES::encrypt($meeting->meeting_id), 
                        'companyId' => AES::encrypt($meeting->company_id),
                        'title' => $meeting->title, 
                        'description' => $meeting->description, 
                        'solicitInfo' => $meeting->solicit_info, 
                        'agenda' => $meeting->agenda, 
                        'organization' => $meeting->organization, 
                        'manuscriptDate' => $meeting->manuscript_date, 
                        'informDate' => $meeting->inform_date, 
                        'manuscriptModifyDate' => $meeting->manuscript_modify_date, 
                        'registerBeginDate' => $meeting->register_begin_date, 
                        'registerEndDate' => $meeting->register_end_date, 
                        'meetingBeginDate' => $meeting->meeting_begin_date, 
                        'meetingEndDate' => $meeting->meeting_end_date, 
                        'status' => MeetingStatus::getStatus($meeting->meeting_id), 
                        'place' => $meeting->place, 
                    );
                    $returnData['meetingList'][] = $info;
                }
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

        /*
    Function: getSearchMeetingNumber
    Url: index/index/getSearchMeetingNumber
    Type: post
    Input: {searchString}
    Output {errNo, msg, data: {number}}
        errNo: 0, msg: '获取成功', data: {number}
        errNo: 1, msg: '参数错误', data: null
        errNo: 10, msg: '搜索内容不能为空', data: null
        errNo: 10, msg: '搜索出现错误', data: null
    */
    public function getSearchMeetingNumber() {
        if ($this->request->isAjax()) {
            $data = input();
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
        } else return $this->error('页面错误');
    }

    /*
    Function: searchMeetings
    Url: index/index/searchMeetings
    Type: post
    Input: {searchString, limit, page}
    Output {errNo, msg, data: {meetingList: array of {meetingId, companyId, templateId, title, description, solicitInfo, agenda, organization, manuscriptTemplateUrl, fee, accomTraffic, contactUs, place, status, manuscriptDate, manuscriptModifyDate, informDate, registerBeginDate, registerEndDate, meetingBeginDate, meetingEndDate}}}
        errNo: 0, msg: '搜索成功', data: {meetingList: array of {meetingId, companyId, templateId, title, description, solicitInfo, agenda, organization, manuscriptTemplateUrl, fee, accomTraffic, contactUs, place, status, manuscriptDate, manuscriptModifyDate, informDate, registerBeginDate, registerEndDate, meetingBeginDate, meetingEndDate}}
        errNo: 1, msg: '参数错误', data: null
        errNo: 3, msg: '请输入正确的分页信息', data: null
        errNo: 10, msg: '搜索内容不能为空', data: null
        errNo: 10, msg: '搜索出现错误', data: null
    */
    public function searchMeetings() {
        if ($this->request->isAjax()) {
            $data = input();
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
        } else return $this->error('页面错误');
    }

    /*Interface: 下载文件
    Function: download
    Url: index/index/download

    Sample:
    function download() {
        var fileName = 'newFileName';
        strUrl = "{:url('index/index/download')}";
        strUrl += '?fileUrl=' + encodeURIComponent(fileUrl);
        window.location.href = strUrl;
    }
    */
    public function download($fileUrl) {
        if (isset($fileUrl)) {
            $url = $fileUrl;
            //$name = $fileName . substr($url, strrpos($url, '.'));
            if(!file_exists($url)){ //检查文件是否存在  
                return '文件不存在';
            }
            $fileName = basename($url);  
            $fileType = explode('.', $url);  
            $fileType = $fileType[count($fileType) - 1];  
            //$fileName = urlencode($name);  
            $fileType = fopen($url,'r'); //打开文件  
            //输入文件标签 
            header("Content-type: application/octet-stream");  
            header("Accept-Ranges: bytes");  
            header("Accept-Length: " . filesize($url));  
            header("Content-Disposition: attachment; filename=" . $fileName);  
            //输出文件内容  
            echo fread($fileType, filesize($url));  
            fclose($fileType);
            return;
        } else return $this->error('页面错误');
    }
}