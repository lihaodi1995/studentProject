<?php
namespace app\index\controller;

use app\common\model\ManuscriptInfo;
use think\Controller;
use think\facade\Session;
use app\common\AES;
use app\common\MeetingStatus;
use app\common\model\Subscribe;
use app\common\model\Meeting;
use app\common\model\MeetingDate;

class User extends controller {
    public function index() {
        return $this->fetch();
    }

    /*Interface: 获取会员信息
    Function: getUserDetail
    Url: index/user/getUserDetail
    Type: post
    Input: {}
    Output: {errNo, msg, data: {userId, email, name, confirm}}
        errNo: 0, msg: '获取成功', data: {userId, email, name, confirm}
        errNo: 2, msg: '未以会员身份登录', data: null
        errNo: 10, msg: '会员不存在', data: null
    */
    public function getUserDetail() {
        if ($this->request->isAjax()) {
            if (Session::has('userId')) {
                $userId = Session::get('userId');
                $user = \app\common\model\User::get($userId);
                if (!isset($user)) {
                    return json(['errNo' => 10, 'msg' => '会员不存在', 'data' => null]);
                }
                $returnData = array(
                    'userId' => AES::encrypt($user->user_id),
                    'email' => $user->email,
                    'name' => $user->name,
                    'confirm' => $user->confirm
                );
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 2, 'msg' => '未以会员身份登录', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 修改会员信息
    Function: modifyUserDetail
    Url: index/user/modifyUserDetail
    Type: post
    Input: {name}
    Output: {errNo, msg}
        errNo: 0, msg: '修改成功'
        errNo: 1, msg: '参数错误'
        errNo: 2, msg: '未以会员身份登录'
        errNo: 10, msg: '会员不存在'
    */
    public function modifyUserDetail() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['name'])) {
                if (Session::has('userId')) {
                    $userId = Session::get('userId');
                    $user = \app\common\model\User::get($userId);
                    if (!isset($user)) {
                        return json(['errNo' => 10, 'msg' => '会员不存在']);
                    }
                    $user->name = $data['name'];
                    $user->save();
                    return json(['errNo' => 0, 'msg' => '修改成功']);
                } else return json(['errNo' => 2, 'msg' => '未以会员身份登录']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 会员收藏会议
    Function: subscribeMeeting
    Url: index/user/subscribeMeeting
    Type: post
    Input: {meetingId, type}
    Output: {errNo, msg}
        errNo: 0, msg: '收藏成功'
        errNo: 1, msg: '参数错误'
        errNo: 2, msg: '未以会员身份登录'
        errNo: 10, msg: '会员不存在'
        errNo: 10, msg: '已收藏该会议'
    NOTE: type: 1-主动收藏, 2-投稿收藏, 3-注册收藏
    */
    public function subscribeMeeting() {
        if ($this->request->isAjax()) {
            $data = input();
            if(isset($data['meetingId']) && isset($data['type'])) {
                if (Session::has('userId')) {
                    $userId = Session::get('userId');
                    $user = \app\common\model\User::get($userId);
                    if (!isset($user)) {
                        return json(['errNo' => 10, 'msg' => '会员不存在']);
                    }
                    $meetingId = AES::decrypt($data['meetingId']);
                    $subscribe = Subscribe::where('user_id', $userId)->where('meeting_id', $meetingId)->find();
                    if (isset($subscribe)) {
                        return json(['errNo' => 10, 'msg' => '已收藏该会议']);
                    }
                    $subscribe = new Subscribe();
                    $subscribe->user_id = Session::get('userId');
                    $subscribe->meeting_id = $meetingId;
                    $subscribe->type = $data['type'];
                    $subscribe->save();
                    return json(['errNo' => 0, 'msg' => '收藏成功']);
                } else return json(['errNo' => 2, 'msg' => '未以会员身份登录']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 会员取消收藏会议
    Function: unsubscribeMeeting
    Url: index/user/unsubscribeMeeting
    Type: post
    Input: {meetingId}
    Output: {errNo, msg}
        errNo: 0, msg: '取消收藏成功'
        errNo: 1, msg: '参数错误'
        errNo: 2, msg: '未以会员身份登录'
        errNo: 10, msg: '会员不存在'
        errNo: 10, msg: '未收藏该会议'
    */
    public function unsubscribeMeeting() {
        if ($this->request->isAjax()) {
            $data = input();
            if(isset($data['meetingId'])) {
                if (Session::has('userId')) {
                    $userId = Session::get('userId');
                    $user = \app\common\model\User::get($userId);
                    if (!isset($user)) {
                        return json(['errNo' => 10, 'msg' => '会员不存在']);
                    }
                    $meetingId = AES::decrypt($data['meetingId']);
                    $subscribe = Subscribe::where('user_id', $userId)->where('meeting_id', $meetingId)->find();
                    if (!isset($subscribe)) {
                        return json(['errNo' => 10, 'msg' => '未收藏该会议']);
                    }
                    $subscribe->delete();
                    return json(['errNo' => 0, 'msg' => '取消收藏成功']);
                } else return json(['errNo' => 2, 'msg' => '未以会员身份登录']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取会员收藏会议数量
    Function: getSubscribeMeetingCount
    Url: index/user/getSubscribeMeetingCount
    Type: post
    Input: {type}
    Output: {errNo, msg, data: {count}}
        errNo: 0, msg: '获取成功', data: {count}
        errNo: 2, msg: '未以会员身份登录', data: null
        errNo: 10, msg: '会员不存在', data: null
    */
    public function getSubscribeMeetingCount() {
        if ($this->request->isAjax()) {
            $data = input();
            if (Session::has('userId')) {
                $userId = Session::get('userId');
                $user = \app\common\model\User::get($userId);
                if (!isset($user)) {
                    return json(['errNo' => 10, 'msg' => '会员不存在', 'data' => null]);
                }
                $returnData['count'] = $user->subscribe()->count();
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 2, 'msg' => '未以会员身份登录', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取会员收藏会议列表
    Function: getSubscribeMeetingList
    Url: index/user/getSubscribeMeetingList
    Type: post
    Input: {limit, page}
    Output: {errNo, msg, data: {meetingList: array of {meetingId, title, organization, solicitInfo, meetingBeginDate, type, status, place}}}
        errNo: 0, msg: '获取成功', data: {meetingList: array of {meetingId, title, organization, solicitInfo, meetingBeginDate, type, status, place}}
        errNo: 1, msg: '参数错误', data: null
        errNo: 2, msg: '未以会员身份登录', data: null
        errNo: 3, msg: '分页信息错误', data: null
        errNo: 10, msg: '会员不存在', data: null
    NOTE: status: 0-截稿日期之前, 1-修改稿截止日期之前, 2-录用通知日期之前, 3-注册开始日期之前, 4-注册结束日期之前, 5-会议开始日期之前, 6-会议结束日期之前, 7-会议结束日期之后
    */
    public function getSubscribeMeetingList() {
        if ($this->request->isAjax()) {
            $data = input();
            if(isset($data['limit']) && isset($data['page'])) {
                $page = $data['page'];
                $limit = $data['limit'];
                if ($limit < 0 || $page < 0 || ($limit != 0 && $page == 0)) {
                    return json(['errNo' => 3, 'msg' => '分页信息错误', 'data' => null]);
                }
                if (Session::has('userId')) {
                    $userId = Session::get('userId');
                    $user = \app\common\model\User::get($userId);
                    if (!isset($user)) {
                        return json(['errNo' => 10, 'msg' => '会员不存在', 'data' => null]);
                    }
                    if ($limit == 0) {
                        $subscribe = $user->subscribe()->select();
                    } else  {
                        $subscribe = $user->subscribe()->page($page, $limit)->select();
                    }
                    
                    foreach ($subscribe as $item) {
                        $meetingId = $item->meeting_id;
                        $meeting = Meeting::get($meetingId);
                        $meetingBeginDate = MeetingDate::get($item->meeting_id)->meeting_begin_date;
                        $type = $item->type;
                        $info = array(
                            'meetingId' => AES::encrypt($meeting->meeting_id), 
                            'title' => $meeting->title, 
                            'solicitInfo' => $meeting->solicit_info, 
                            'organization' => $meeting->organization, 
                            'meetingBeginDate' => $meetingBeginDate, 
                            'status' => MeetingStatus::getStatus($meeting->meeting_id), 
                            'place' => $meeting->place, 
                            'type' =>  $type
                        );
                        $returnData['meetingList'][] = $info;
                    }
                    return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
                } else return json(['errNo' => 2, 'msg' => '未以会员身份登录', 'data' => null]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取会员收藏会议状态
    Function: getSubscribeMeetingStatus
    Url: index/user/getSubscribeMeetingStatus
    Type: post
    Input: {meetingId}
    Output: {errNo, msg, data: {status}}
        errNo: 0, msg: '获取成功', data: {status}
        errNo: 1, msg: '参数错误', data: null
        errNo: 2, msg: '未以会员身份登录', data: null
        errNo: 10, msg: '会员不存在', data: null
    NOTE: status: 0-未收藏, 1-主动收藏, 2-投稿收藏, 3-注册收藏
    */
    public function getSubscribeMeetingStatus() {
        if ($this->request->isAjax()) {
            $data = input();
            if(isset($data['meetingId'])) {
                if (Session::has('userId')) {
                    $userId = Session::get('userId');
                    $user = \app\common\model\User::get($userId);
                    if (!isset($user)) {
                        return json(['errNo' => 10, 'msg' => '会员不存在', 'data' => null]);
                    }
                    $meetingId = AES::decrypt($data['meetingId']);
                    $subscribe = Subscribe::where('user_id', $userId)->where('meeting_id', $meetingId)->find();
                    if (!isset($subscribe)) {
                        $status = 0;
                    } else {
                        $status = $subscribe->type;
                    }
                    $returnData['status'] = $status;
                    return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
                } else return json(['errNo' => 2, 'msg' => '未以会员身份登录', 'data' => null]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }



    /*Interface: 获取会员投稿信息
   Function: getSubmissionDeatil
   Url: index/user/getSubmissionDeatil
   Type: post
   Input: {}
   Output: {errNo, msg, data: { submissionDeatil:array of {userId,manuscriptId,meetingId,manuscriptInfoId,type,url,createTime,updateTime,author,title,organization,abstract,modifyInfo,result,suggestion}}
       errNo: 0, msg: '获取成功', data: {submissionDeatil:array of {userId,manuscriptId,meetingId,manuscriptInfoId,type,url,createTime,updateTime,author,title,organization,abstract,modifyInfo,result,suggestion}}
       errNo: 2, msg: '未以会员身份登录', data: null
       errNo: 10, msg: '会员不存在', data: null

   */
    public function getSubmissionDeatil()
    {
            $data = input();
            if (Session::has('userId')) {
                $userId = Session::get('userId');
                $user = \app\common\model\User::get($userId);
                $returnData['submissionDeatil'] = array();
                if (!isset($user)) {
                    return json(['errNo' => 10, 'msg' => '会员不存在', 'data' => null]);
                }
                $manuscripts = $user->manuscripts()->where('valid', 1)->select();
                foreach($manuscripts as $manuscriptItem)
                {
                    $manuscript = \app\common\model\Manuscript::get($manuscriptItem->manuscript_id);
                    $manuscriptInfo = $manuscript->manuscriptInfo()->find();
                    $review = $manuscript->review()->find();
                    $result = '';
                    $suggestion ='';
                    if(!isset($review))
                    {
                        $result = '待审核';
                        $suggestion = '待审核';
                    }
                    else {
                        $result = $review->result;
                        $suggestion = $review->suggestion;
                    }
                    $info = array(
                        'userId' => AES::encrypt($manuscript->user_id),
                        'manuscriptId' => AES::encrypt($manuscript->manuscript_id),
                        'meetingId' => AES::encrypt($manuscript->meeting_id),
                        'manuscriptInfoId' => AES::encrypt($manuscriptInfo->manuscript_info_id),
                        'type' => $manuscript->type,
                        'url' => $manuscript->url,
                        'createTime' => $manuscript->create_time,
                        'updateTime' => $manuscript->update_time,
                        'author' => $manuscriptInfo->author,
                        'title' => $manuscriptInfo->title,
                        'organization' => $manuscriptInfo->organization,
                        'abstract' => $manuscriptInfo->abstract,
                        'modifyInfo' => $manuscriptInfo->modify_info,
                        'result' => $result,
                        'suggestion' => $suggestion,
                    );
                    $returnData['submissionDeatil'][] = $info;
                }
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 2, 'msg' => '未以会员身份登录', 'data' => null]);
    }
    /*Interface: 获取会员注册信息
   Function: getRegisterDeatil
   Url: index/user/getRegisterDeatil
   Type: post
   Input: {}
   Output: {errNo, msg, data: {registerDeatil:array of {meetingId,title,status}}
         errNo: 0, msg: '获取成功',{registerDeatil:array of {meetingId,title,status}}
         errNo: 2, msg: '未以会员身份登录', data: null
         errNo: 10, msg: '会员不存在', data: null

   */

    public function getRegisterDeatil()
    {
        $data = input();
        if (Session::has('userId')) {
            $userId = Session::get('userId');
            $user = \app\common\model\User::get($userId);
            $returnData['registerDeatil'] = array();
            if (!isset($user)) {
                return json(['errNo' => 10, 'msg' => '会员不存在', 'data' => null]);
            }
            $registers = $user->registers()->select();
            foreach($registers as $registerItem)
            {
                $register = \app\common\model\Register::get($registerItem->register_id);
                //echo $registerItem->register_id."\n";
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
        } else return json(['errNo' => 2, 'msg' => '未以会员身份登录', 'data' => null]);
    }


}