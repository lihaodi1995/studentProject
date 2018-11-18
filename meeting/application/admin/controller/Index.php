<?php
namespace app\admin\controller;

use app\common\Mail;
use app\common\model\Meeting;
use app\common\model\Subscribe;
use think\Controller;
use think\facade\Session;
use app\common\AES;
use app\common\MeetingStatus;
use app\common\model\Company;
use app\common\model\MeetingDate;
use app\common\model\User;

class Index extends Controller {
    public function index() {
        return $this->fetch();
    }

    public function verify() {
        return $this->fetch();
    }

    public function test()
    {
    }
    /*Interface: 获取审核单位数量
    Function: getVerifyCount
    Url: admin\index\getVerifyCount
    Type: post
    Input: {}
    Output: {errNo, msg, data: {count}
        errNo: 0, msg: '获取成功', data:{count}
    */
    public function getVerifyCount() {
        $returnData['count'] = Company::where('confirm', 0)->count();
        return json(['errNo' => 0, 'msg' => '获取成功', 'data' =>$returnData]);
    }

    /*Interface: 获取审核单位列表
    Function: getVerifyList
    Url: admin\index\getVerifyList
    Type: post
    Input: {page, limit}
    Output: {errNo, msg, data: {verifyList: array of {companyId, account, name, companyAdditionList:{array of {companyAdditionId, type, url}}}
        errNo: 0, msg: '获取成功', data: {verifyList: array of {companyId, account, name, companyAdditionList:{array of {companyAdditionId, type, url}}
        errNo: 1, msg: '参数错误', data: null
        errNo: 3, msg: '分页信息错误', data: null
    */
    public function getVerifyList() {
        $data = input();
        if(isset($data['page']) && isset($data['limit'])) {
            $page = $data['page'];
            $limit = $data['limit'];
            if ($limit < 0 || $page < 0 || ($limit != 0 && $page == 0)) {
                return json(['errNo' => 3, 'msg' => '分页信息错误', 'data' => null]);
            }

            if ($limit == 0) {
                $company = Company::where('confirm', 0)->select();
            } else {
                $company = Company::where('confirm', 0)->page($page, $limit)->select();
            }
            $returnData['verifyList'] = array();
            foreach ($company as $item) {
                $companyAddition = $item->companyAdditions()->select();
                $additionList = array();
                foreach ($companyAddition as $addition) {
                    $additionitem = array(
                        'companyAdditionId' => AES::encrypt($addition->company_addition_id),
                        'url' => $addition->url, 
                    );
                    $additionList[] = $additionitem;
                }
                $info = array(
                    'companyId' => AES::encrypt($item->company_id), 
                    'account' => $item->account, 
                    'name' => $item->name, 
                    'companyAdditionList' => $additionList, 
                );
                $returnData['verifyList'][] = $info;
            }
            return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
        } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
    }


    /*Interface: 获取审核详细信息
    Function: getVerifyDetail
    Url: admin\index\getVerifyDetail
    Type: post
    Input:{companyId}
    Output: {errNo, msg, data: {companyId, account, name, companyAdditionList: {array of {companyAdditionId, type, url}}
        errNo: 0, msg: '获取成功', data: {companyId, account, name, companyAdditionList: {array of {companyAdditionId, type, url}}
        errNo: 1, msg: '参数错误', data: null
        errNo; 10, msg: '单位不存在', data: null
    */
    public function getVerifyDetail() {
        $data = input();
        if (isset($data['companyId'])) {
            $companyId = AES::decrypt($data['companyId']);
            $company = Company::get($companyId);
            if (!isset($company)) {
                return json(['errNo' => 10, 'msg' => '单位不存在', 'data' => null]);
            }
            $companyAddition = $company->companyAdditions()->select();
            $additionList = array();
            foreach ($companyAddition as $addition) {
                $additionitem = array(
                    'companyAdditionId' => AES::encrypt($addition->company_addition_id),
                    'url' => $addition->url, 
                );
                $additionList[]=$additionitem;
            }
            $returnData = array(
                'companyId' => AES::encrypt($company->company_id), 
                'account' => $company->account, 
                'name' => $company->name, 
                'companyAdditionList' => $additionList, 
            );
            return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
        } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
    }

    /*
    Interface: 邮件提醒
    Function: endInform
    Url: admin\index\endInform
    Type: post
    Input:{leads,frequency,status} 提前量 （秒）/ 调用间隔（秒）/ 状态
    Output: {errNo, msg, data: null}
        errNo: 0, msg: '发送成功', data: null
        errNo: 1, msg: '参数错误', data: null

    status :
    截稿日期之前：0
    修改稿截止日期之前：1,
    注册结束日期之前：4,

    */

    public function endInform()
    {
        $data = input();
        if (isset($data['leads'])&&isset($data['status'])&&isset($data['frequency']))
        {
            $time = time();
            $time = $time + $data['leads'];
            $leadtime = date('Y-m-d H:i:s', $time+$data['leads']+$data['frequency']);
            $datetime = date('Y-m-d H:i:s', time()+$data['leads']);
            $status = $data['status'];
            $field = array(
                '0'=>'manuscript_date',
                '1'=>'manuscript_date',
                '4'=>'manuscript_modify_date'
            );
            $meetingDate=MeetingDate::where("'$datetime' < $field[$status] and  '$leadtime'  > $field[$status]")->select();
            foreach($meetingDate as $meetingItem)
            {
                $meetingId=$meetingItem->meeting_id;
                $meeting = Meeting::get($meetingId);
                $name = $meeting->title;
                $subscribes = $meeting->subscribes()->select();
                foreach ($subscribes as $subscribeItem)
                {
                    $userId = $subscribeItem->user_id;
                    $result=Mail::sendInformMail($userId,$name,$meetingId,$status);
                }
            }

            return json(['errNo' => 0, 'msg' => '发送成功', 'data' => null]);
        }
        else
            return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
    }
    /*Interface: 判断是否是管理员
    Function: checkAdminStatus
    Url: admin/index/checkAdminStatus
    Type: post
    Input: {}
    Output: {errNo, msg}
        errNo: 0, msg: '是管理员身份'
        errNo: 2, msg: '未以管理员身份登录'
    */
    public function checkAdminStatus()
    {
        if (Session::has('adminId')) {
            return json(['errNo' => 0, 'msg' => '是管理员身份']);
        }else
            return json(['errNo' => 2, 'msg' => '未以管理员身份登录']);
    }
    /*Interface: 更改审核状态
    Function: changeConfirmStatus
    Url: admin/index/changeConfirmStatus
    Type: post
    Input: {confirm,companyId}
    Output: {errNo, msg}
        errNo: 0, msg: '修改成功'
        errNo: 1, msg: '参数错误'
    */
    public function changeConfirmStatus()
    {
        $data = input();
        if (isset($data['companyId'])&&isset($data['confirm'])) {
            $companyId = AES::decrypt($data['companyId']);
            $company = Company::get($companyId);
            if (!isset($company)) {
                return json(['errNo' => 10, 'msg' => '单位不存在', 'data' => null]);
            }
            $company->confirm = $data['confirm'];
            $company->save();
            $companyAddition = $company->companyAdditions()->select();
            foreach ($companyAddition as $addition) {
                $addition->delete();
            }
            return json(['errNo' => 0, 'msg' => '修改成功成功', 'data' => null]);
        } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
    }

}

