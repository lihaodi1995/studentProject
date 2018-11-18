<?php
namespace app\meeting\controller;

use app\common\model\Manuscript;
use app\common\model\MeetingDate;
use think\Controller;
use think\facade\Session;
use app\common\AES;
use app\common\MeetingStatus;
use app\common\model\Meeting;
use app\common\model\User;
use app\common\model\RegisterPerson;
use app\common\model\RegisterAddition;

class Register extends controller {
    public function index() {
        return $this->fetch();
    }

    public function detail() {
        return $this->fetch();
    }

    public function list() {
        return $this->fetch();
    }

    /*
    Interface: 判断用户是否能以参会者注册
    Function: ifsubmit
    Url: meeting\register\ifsubmit
    Type: post
    Input: {meetingId}
    Output: {errNo, msg, data: {submission}}
        errNo: 0, msg: '查询成功', data: {submission}
        errNo: 1, msg: '参数错误', data: null
        errNo: 2, msg: '未以会员身份登录', data: null
    */
    public function ifsubmit() {
        if ($this->request->isAjax()) {
            $data = input();
            if(isset($data['meetingId'])) {
                if (Session::has('userId')) {
                    $meetingId = AES::decrypt($data['meetingId']);
                    $userId = Session::get('userId');
                    $user = User::get($userId);
                    if (!isset($user)) {
                        return json(['errNo' => 10, 'msg' => '会员不存在', 'data' => null]);
                    }
                    $meeting = Meeting::get($meetingId);
                    if (!isset($meeting)) {
                        return json(['errNo' => 10, 'msg' => '会议不存在', 'data' => null]);
                    }
                    $manuscript = Manuscript::where('valid', 1)->where('meeting_id', $meetingId)->where('user_id', $userId)->find();
                    if (!isset($manuscript)) {
                        $returnData['submission'] = 0;
                        return json(['errNo' => 0, 'msg' => '查询成功', 'data' => $returnData]);
                    }
                    $review = $manuscript->review()->find();
                    if (!isset($review) || $review->result != 1) {
                        $returnData['submission'] = 0;
                        return json(['errNo' => 0, 'msg' => '查询成功', 'data' => $returnData]);
                    }
                    $returnData['submission'] = 1;
                    return json(['errNo' => 0, 'msg' => '查询成功', 'data' => $returnData]);
                }
                else return json(['errNo' => 2, 'msg' => '未以会员身份登录', 'data' => null]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*
    Interface: 注册会议
    Function: createRegister
    Url: meeting\register\createRegister
    Type: post
    Input: {meetingId}
    Output: {errNo, msg, data: {registerId, type}}
        errNo: 0, msg: '注册成功', data: {registerId, type}
        errNo: 1, msg: '参数错误', data: null
        errNo: 2, msg: '未以会员身份登录', data: null
        errNo: 10, msg: '会员不存在', data: null
        errNo: 10, msg: '会议不存在', data: null
        errNo: 10, msg: '不在注册时间内', data: null
    NOTE: type: 1-投稿参会, 2-聆听参会
    */
    public function createRegister() {
        if ($this->request->isAjax()) {
            $data = input();
            if(isset($data['meetingId'])) {
                if (Session::has('userId')) {
                    $userId = Session::get('userId');
                    $user = User::get($userId);
                    if (!isset($user)) {
                        return json(['errNo' => 10, 'msg' => '会员不存在', 'data' => null]);
                    }
                    $meetingId = AES::decrypt($data['meetingId']);
                    $meeting = Meeting::get($meetingId);
                    if (!isset($meeting)) {
                        return json(['errNo' => 10, 'msg' => '会议不存在', 'data' => null]);
                    }
                    $status = MeetingStatus::getStatus($meetingId);
                    if ($status != 4) {
                        return json(['errNo' => 10, 'msg' => '不在注册时间内', 'data' => null]);
                    }
                    $manuscript = $user->manuscripts()->where('valid', 1)->where('meeting_id', $meetingId)->find();
                    if (!isset($manuscript)) {
                        $manuscriptId = 0;
                        $returnData['type'] = 2;
                    } else {
                        $review = $manuscript->review()->find();
                        if (!isset($review) || $review->result != 1) {
                            $manuscriptId = 0;
                            $returnData['type'] = 2;
                        }
                        else {
                            $manuscriptId = $manuscript->manuscript_id;
                            $returnData['type'] = 1;
                        }
                    }
                    $register = new \app\common\model\Register();
                    $register->user_id = $userId;
                    $register->meeting_id = $meetingId;
                    $register->manuscript_id = $manuscriptId;
                    $register->type = $returnData['type'];
                    $register->check = 1;
                    $register->save();
                    $returnData['registerId'] = AES::encrypt($register->register_id);
                    return json(['errNO' => 0, 'msg' => '注册会议成功', 'data' => $returnData]);
                } else return json(['errNo' => 2, 'msg' => '未以会员身份登录', 'data' => null]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 删除会议注册信息
    Function: deleteRegister
    Url: meeting/register/deleteRegister
    Type: post
    Input: {registerId}
    Output: {errNo, msg}
        errNo: 0, msg: '删除成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '注册信息不存在'
    */
    public function deleteRegister() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['registerId'])) {
                $registerId = AES::decrypt($data['registerId']);
                $register = \app\common\model\Register::get($registerId);
                if (!isset($register)) {
                    return json(['errNO' => 10, 'msg' => '注册信息不存在']); 
                }
                $registerPersons = $register->registerPersons()->select();
                foreach ($registerPersons as $registerPerson) {
                    $registerPerson->delete();
                }
                $register->delete();
                return json(['errNO' => 0, 'msg' => '删除成功']);
            } else return json(['errNO' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 创建注册人信息
    Function: createRegisterPerson
    Url: meeting/register/createRegisterPerson
    Type: post
    Input: {registerId, registerPersonList: array of {name, gender, accomodation}}
    Output: {errNo, msg}
        errNo: 0, msg: '创建成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '注册信息不存在'
        errNo: 10, msg: '姓名不能为空'
        errNo: 10, msg: '性别不能为空'
        errNo: 10, msg: '住宿信息不能为空'
    */
    public function createRegisterPerson() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['registerPersonList']) && isset($data['registerId'])) {
                $registerId = AES::decrypt($data['registerId']);
                $register = \app\common\model\Register::get($registerId);
                if (!isset($register)) {
                    return json(['errNO' => 10, 'msg' => '注册信息不存在']); 
                }
                $registerPersonList = json_decode($data['registerPersonList'], true);
                foreach ($registerPersonList as $rp) {
                    if (!isset($rp['name']) || !isset($rp['gender']) || !isset($rp['accomodation'])) {
                        return json(['errNO' => 1, 'msg' => '参数错误']);
                    }
                    if (strlen($rp['name']) == 0) {
                        return json(['errNO' => 10, 'msg' => '姓名不能为空']); 
                    }
                    if (strlen($rp['gender']) == 0) {
                        return json(['errNO' => 10, 'msg' => '性别不能为空']); 
                    }
                    if (strlen($rp['accomodation']) == 0) {
                        return json(['errNO' => 10, 'msg' => '住宿信息不能为空']); 
                    }
                }
                foreach ($registerPersonList as $rp) {
                    $registerPerson = new RegisterPerson();
                    $registerPerson->register_id = $registerId;
                    $registerPerson->name = $rp['name'];
                    $registerPerson->gender = $rp['gender'];
                    $registerPerson->accomodation = $rp['accomodation'];
                    $registerPerson->save();
                }
                return json(['errNO' => 0, 'msg' => '创建成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 上传缴费凭证信息
    Function: uploadReigsterAddition
    Url: meeting/register/uploadReigsterAddition
    Type: post
    Input: formData: {file, registerId, fileName}
    Output: {errNo, msg}
        errNo: 0, msg: '上传成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '注册信息不存在'
    */
    public function uploadReigsterAddition() {
        if ($this->request->isAjax()) {
            $file = request()->file('file');
            $registerId = request()->param('registerId');
            $fileName = request()->param('fileName');
            if (strlen($file) <= 0) {
                return json(['errNo' => 10, 'msg' => '请上传大小在0-10M范围内的文件', 'data' => null]);
            }
            if (isset($file) && isset($registerId) && isset($fileName)) {
                $registerId = AES::decrypt($registerId);
                $register = \app\common\model\Register::get($registerId);
                if (!isset($register)) {
                    return json(['errNo' => 10, 'msg' => '注册信息不存在']);
                }
                // $meeting = $register->meeting()->find();
                $dir = './../upload/meeting/' . AES::encrypt($register->meeting_id) . '/registerAdditions';
                $fileName = date('YmdHis', time()) . '_' . $fileName;
                $file->move($dir, $fileName);
                $fileUrl = str_replace("\\", '/', $dir . '/' . $fileName);

                $registerAddition = new RegisterAddition();
                $registerAddition->register_id = $registerId;
                $registerAddition->url = $fileUrl;
                $registerAddition->save();
                return json(['errNo' => 0, 'msg' => '上传成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取会议注册数量
    Function: getRegisterCount
    Url: meeting\register\getRegisterCount
    Type: post
    Input: {meetingId, check}
    Output: {errNo, msg, data: {count}}
        errNo: 0, msg: '获取成功', data: {count}
        errNo: 1, msg: '参数错误', data: null
        errNo: 10, msg: '会议不存在', data: null
    NOTE: check: 1-未审核, 2-审核通过, 3-审核未通过
    */
    public function getRegisterCount() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['meetingId']) && isset($data['check'])) {
                $meetingId = AES::decrypt($data['meetingId']);
                $meeting = Meeting::get($meetingId);
                if (!isset($meeting)) {
                    return json(['errNo' => 10, 'msg' => '会议不存在']);
                }
                $returnData['count'] = $meeting->registers()->where('check', $data['check'])->count();
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取会议注册列表
    Function: getRegisterList
    Url: meeting\register\getRegisterList
    Type: post
    Input: {meetingId, check, limit, page}
    Output: {errNo, msg, data: {registerList: array of {registerId, userId, meetingId, manuscriptId, type, createTime, updateTime,name,num}}
        errNo: 0, msg: '获取成功', data: {registerList: array of {registerId, userId, meetingId, manuscriptId, type, createTime, updateTime,name,num}
        errNo: 1, msg: '参数错误', data: null
        errNo: 3, msg: '分页信息错误', data: null
        errNo: 10, msg: '会议不存在', data: null
    NOTE: check: 1-未审核, 2-审核通过, 3-审核未通过
    */
    public function getRegisterList() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['meetingId']) && isset($data['check']) && isset($data['limit']) && isset($data['page'])) {
                $page = $data['page'];
                $limit = $data['limit'];
                if ($limit < 0 || $page < 0 || ($limit != 0 && $page == 0)) {
                    return json(['errNo' => 3, 'msg' => '分页信息错误', 'data' => null]);
                }
                $meetingId = AES::decrypt($data['meetingId']);
                $meeting = Meeting::get($meetingId);
                if (!isset($meeting)) {
                    return json(['errNo' => 10, 'msg' => '会议不存在']);
                }

                if ($limit == 0) {
                    $registers = $meeting->registers()->where('check', $data['check'])->select();
                } else {
                    $registers = $meeting->registers()->where('check', $data['check'])->page($page, $limit)->select();
                }
                $returnData['registerList'] = array();
                foreach ($registers as $item) {
                    $register = \app\common\model\Register::get($item->register_id);
                    $num = $register->registerPersons()->count();
                    $user = User::get($item->user_id);
                    $name = $user->name;
                    $info = array(
                        'registerId' => AES::encrypt($item->register_id), 
                        'userId' => AES::encrypt($item->user_id), 
                        'meetingId'=> AES::encrypt($item->meeting_id), 
                        'manuscriptId'=> AES::encrypt($item->manuscript_id),
                        'type'=> $item->type,
                        'createTime'=> $item->create_time, 
                        'updateTime'=> $item->update_time,
                        'name' => $name,
                        'num'=> $num
                    );
                    $returnData['registerList'][]=$info;
                }
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取注册详细信息
    Function: getRegisterDetail
    Url: meeting\register\getRegisterDetail
    Type: post
    Input: {registerId}
    Output: {errNo, msg, data: {registerId, userId, meetingId, manuscriptId, type, createTime, updateTime, name, num, url}}
        errNo: 0, msg: '获取成功', data: {registerId, userId, meetingId, manuscriptId, type, createTime, updateTime, name, num, url}
        errNo: 1, msg: '参数错误', data: null
        errNO: 10, msg: '注册信息不存在', data: null
        errNO: 10, msg: '注册缴费信息不存在', data: null
    */
    public function getRegisterDetail() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['registerId'])) {
                $registerId = AES::decrypt($data['registerId']);
                $register = \app\common\model\Register::get($registerId);
                if (!isset($register)) {
                    return json(['errNo' => 10, 'msg' => '注册信息不存在']);
                }
                $num = $register->registerPersons()->count();
                $user = User::get($register->user_id);
                $name = $user->name;
                $registerAddition = $register->registerAdditions()->find();
                if (!isset($registerAddition)) {
                    return json(['errNo' => 10, 'msg' => '注册缴费信息不存在']);
                }
                $returnData = array(
                    'registerId' => AES::encrypt($register->register_id), 
                    'userId' => AES::encrypt($register->user_id), 
                    'meetingId' => AES::encrypt($register->meeting_id), 
                    'manuscriptId' => AES::encrypt($register->manuscript_id),
                    'type' => $register->type, 
                    'createTime' => $register->create_time, 
                    'updateTime' => $register->update_time,
                    'name' => $name,
                    'num'=> $num,
                    'url' => $registerAddition->url
                );
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取注册信息中注册人列表
    Function: getRegisterPersonList
    Url: meeting/register/getRegisterPersonList
    Type: post
    Input: {registerId}
    Output: {errNo, msg, data: {registerPersonList: array of {registerPersonId, registerId, name, gender, accomodation}}}
        errNo: 0, msg: '获取成功', data: {registerPersonList: array of {registerPersonId, registerId, name, gender, accomodation}}
        errNo: 1, msg: '参数错误', data: null
        errNo: 10, msg: '注册信息不存在', data: null
    */
    public function getRegisterPersonList() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['registerId'])) {
                $registerId = AES::decrypt($data['registerId']);
                $register = \app\common\model\Register::get($registerId);
                if (!isset($register)) {
                    return json(['errNo' => 10, 'msg' => '注册信息不存在']);
                }

                $returnData['registerPersonList'] = array();
                $registerPersons = $register->registerPersons()->select();
                foreach ($registerPersons as $registerPerson) {
                    $registerPersonInfo = array(
                        'registerPersonId' => AES::encrypt($registerPerson->register_person_id),
                        'registerId' => AES::encrypt($registerPerson->register_id),
                        'name' => $registerPerson->name,
                        'gender' => $registerPerson->gender,
                        'accomodation' => $registerPerson->accomodation,
                    );
                    $returnData['registerPersonList'][] = $registerPersonInfo;
                }
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 审核注册信息
    Function: checkRegister
    Url: meeting\register\checkRegister
    Type: post
    Input: {registerId, check}
    Output: {errNo, msg, data: null}
        errNo: 0, msg: '修改成功', data: null
        errNo: 1, msg: '参数错误', data: null
        errNO: 10, msg: '注册信息不存在', data: null
    */
    public function checkRegister() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['registerId']) && isset($data['check'])) {
                $registerId = AES::decrypt($data['registerId']);
                $register = \app\common\model\Register::get($registerId);
                if (!isset($register)) {
                    return json(['errNo' => 10, 'msg' => '注册信息不存在']);
                }
                $register->check = $data['check'];
                $register->save();
                return json(['errNo' => 0, 'msg' => '修改成功', 'data' => null]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }
}