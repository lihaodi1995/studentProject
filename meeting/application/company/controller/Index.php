<?php
namespace app\company\controller;

use think\Controller;
use think\facade\Session;
use app\common\AES;
use app\common\MeetingStatus;
use app\common\model\Meeting;
use app\common\model\MeetingDate;
use app\common\model\Company;
use app\common\model\CompanyUnit;

class Index extends controller {
    public function index() {
        return $this->fetch();
    }

    public function meeting() {
        return $this->fetch();
    }

    public function edit() {
        return $this->fetch();
    }

    /*Interface: 获取单位信息
    Function: getCompanyDetail
    Url: company/index/getCompanyDetail
    Type: post
    Input: {}
    Output: {errNo, msg, data: {companyId, account, name, confirm}}
        errNo: 0, msg: '获取成功', data: {companyId, account, name, confirm}
        errNo: 2, msg: '未以单位身份登录', data: null
        errNo: 10, msg: '单位不存在', data: null
    NOTE: confirm: 0-审核中, 1-通过审核, 2-未通过审核
    */
    public function getCompanyDetail() {
        if ($this->request->isAjax()) {
            if (Session::has('companyId')) {
                $companyId = Session::get('companyId');
                $company = Company::get($companyId);
                if (!isset($company)) {
                    return json(['errNo' => 10, 'msg' => '单位不存在']);
                }
                $returnData = array(
                    'companyId' => AES::encrypt($company->company_id), 
                    'account' => $company->account, 
                    'name' => $company->name, 
                    'confirm' => $company->confirm
                );
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 2, 'msg' => '未以单位身份登录']);
        } else return $this->error('页面错误');
    }

    /*Interface: 修改单位信息
    Function: modifyCompanyDetail
    Url: company/index/modifyCompanyDetail
    Type: post
    Input: {name}
    Output: {errNo, msg}
        errNo: 0, msg: '修改成功'
        errNo: 1, msg: '参数错误'
        errNo: 2, msg: '未以单位身份登录'
        errNo: 10, msg: '单位不存在'
    */
    public function modifyCompanyDetail() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['name'])) {
                if (Session::has('companyId')) {
                    $companyId = Session::get('companyId');
                    $company = Company::get($companyId);
                    if (!isset($company)) {
                        return json(['errNo' => 10, 'msg' => '单位不存在']);
                    }
                    $company->name = $data['name'];
                    $company->save();
                    return json(['errNo' => 0, 'msg' => '修改成功']);
                } else return json(['errNo' => 2, 'msg' => '未以单位身份登录']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取单位个人帐号信息
    Function: getCompanyUnitDetail
    Url: company/index/getCompanyUnitDetail
    Type: post
    Input: {}
    Output: {errNo, msg, data: {companyUnitId, companyId, account, password, name}}
        errNo: 0, msg: '获取成功', data: {companyUnitId, companyId, account, password, name}
        errNo: 2, msg: '未以单位个人帐号身份登录', data: null
        errNo: 10, msg: '单位个人帐号不存在', data: null
    */
    public function getCompanyUnitDetail() {
        if ($this->request->isAjax()) {
            if (Session::has('companyUnitId')) {
                $companyUnitId = Session::get('companyUnitId');
                $companyUnit = CompanyUnit::get($companyUnitId);
                if (!isset($companyUnit)) {
                    return json(['errNo' => 10, 'msg' => '单位个人帐号不存在']);
                }
                $returnData = array(
                    'companyUnitId' => AES::encrypt($companyUnit->company_unit_id),
                    'companyId' => AES::encrypt($companyUnit->company_id),
                    'account' => $companyUnit->account,
                    'password' => AES::decrypt($companyUnit->password),
                    'name' => $companyUnit->name
                );
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 2, 'msg' => '未以单位个人帐号身份登录']);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取单位中单位个人帐号数量
    Function: getCompanyUnitCount
    Url: company/index/getCompanyUnitCount
    Type: post
    Input: {}
    Output: {errNo, msg, data: {count}}
        errN0: 0, msg: '获取成功', data: {count}
        errNo: 2, msg: '未以单位身份登录', data: null
        errNo: 10, msg: '单位不存在', data: null
    */
    public function getCompanyUnitCount() {
        if ($this->request->isAjax()) {
            if (Session::has('companyId')) {
                $companyId = Session::get('companyId');
                $company = Company::get($companyId);
                if (!isset($company)) {
                    return json(['errNo' => 10, 'msg' => '单位不存在']);
                }
                $returnData['count'] = $company->companyUnits()->count();
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 2, 'msg' => '未以单位身份登录']);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取单位中单位个人帐号列表
    Function: getCompanyUnitList
    Url: company/index/getCompanyUnitList
    Type: post
    Input: {limit, page}
    Output: {errNo, msg, data: {companyUnitList: array of {companyUnitId, account, password, name}}}
        errNo: 0, msg: '获取成功', data: {companyUnitList: array of {companyUnitId, account, password, name}}
        errNo: 1, msg: '参数错误'，data: null
        errNo: 2, msg: '未以单位身份登录', data: null
        errNo: 3, msg: '分页信息错误', data: null
        errNo: 10, msg: '单位不存在', data: null
    */
    public function getCompanyUnitList() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['limit']) && isset($data['page'])) {
                $page = $data['page'];
                $limit = $data['limit'];
                if ($limit < 0 || $page < 0 || ($limit != 0 && $page == 0)) {
                    return json(['errNo' => 3, 'msg' => '分页信息错误', 'data' => null]);
                }
                if (Session::has('companyId')) {
                    $companyId = Session::get('companyId');
                    $company = Company::get($companyId);
                    if (!isset($company)) {
                        return json(['errNo' => 10, 'msg' => '单位不存在']);
                    }

                    if ($limit == 0) {
                        $companyUnits = $company->companyUnits()->order('company_unit_id', 'asc')->select();
                    } else {
                        $companyUnits = $company->companyUnits()->order('company_unit_id', 'asc')->page($page, $limit)->select();
                    }
                    $returnData['companyUnitList'] = array();
                    foreach ($companyUnits as $companyUnit) {
                        $info = array(
                            'companyUnitId' => AES::encrypt($companyUnit->company_unit_id), 
                            'account' => $companyUnit->account,
                            'password' => AES::decrypt($companyUnit->password),
                            'name' => $companyUnit->name
                        );
                        $returnData['companyUnitList'][] = $info;
                    }
                    return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
                } else return json(['errNo' => 2, 'msg' => '未以单位身份登录']);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 创建会议
    Function: createMeeting
    Url: company/index/createMeeting
    Type: post
    Input: {templateId, title, description, solicitInfo, agenda, organization, manuscriptTemplateUrl, fee, accomTraffic, contactUs, place, manuscriptDate, manuscriptModifyDate, informDate, registerBeginDate, registerEndDate, meetingBeginDate, meetingEndDate}}
    Output: {errNo, msg, data: {meetingId}}
        errNo: 0, msg: '创建成功', data: {meetingId}
        errNo: 1, msg: '参数错误', data: null
        errNo: 2, msg: '未以单位或单位个体账号身份登录', data: null
        errNo: 10, msg: '单位或单位个体账号不存在', data: null
        errNo: 10, msg: '标题不能为空', data: null
        errNo: 10, msg: '描述不能为空', data: null
        errNo: 10, msg: '日程信息不能为空', data: null
        errNo: 10, msg: '组织机构不能为空', data: null
        errNo: 10, msg: '费用信息不能为空', data: null
        errNo: 10, msg: '住宿交通信息不能为空', data: null
        errNo: 10, msg: '联系我们信息不能为空', data: null
        errNo: 10, msg: '地点不能为空', data: null
    */
    public function createMeeting() {
        if ($this->request->isAjax()) {
            $data = input();
            if(isset($data['title']) && isset($data['description']) && isset($data['solicitInfo']) && isset($data['templateId'])
            && isset($data['agenda']) && isset($data['organization']) && isset($data['manuscriptTemplateUrl']) && isset($data['fee'])
            && isset($data['accomTraffic']) && isset($data['contactUs']) && isset($data['place']) && isset($data['manuscriptDate'])
            && isset($data['manuscriptModifyDate']) && isset($data['informDate']) && isset($data['registerBeginDate'])
            && isset($data['registerEndDate']) && isset($data['meetingBeginDate']) && isset($data['meetingEndDate'])) {
                if (Session::has('companyId')) {
                    $companyId = Session::get('companyId');
                    $company = Company::get($companyId);
                    if (!isset($company)) {
                        return json(['errNo' => 10, 'msg' => '单位或单位个体账号不存在', 'data' => null]);
                    }
                } else if (Session::has('companyUnitId')) {
                    $companyUnitId = Session::get('companyUnitId');
                    $companyUnit = CompanyUnit::get($companyUnitId);
                    if (!isset($companyUnit)) {
                        return json(['errNo' => 10, 'msg' => '单位或单位个体账号不存在', 'data' => null]);
                    }
                    $company = $companyUnit->company()->find();
                    if (!isset($company)) {
                        return json(['errNo' => 10, 'msg' => '单位或单位个体账号不存在', 'data' => null]);
                    }
                } else {
                    return json(['errNo' => 2, 'msg' => '未以单位或单位个体账号身份登录', 'data' => null]);
                }

                if (strlen($data['title']) == 0) {
                    return json(['errNo' => 10, 'msg' => '标题不能为空', 'data' => null]);
                }
                if (strlen($data['description']) == 0) {
                    return json(['errNo' => 10, 'msg' => '描述不能为空', 'data' => null]);
                }
                if (strlen($data['agenda']) == 0) {
                    return json(['errNo' => 10, 'msg' => '日程信息不能为空', 'data' => null]);
                }
                if (strlen($data['organization']) == 0) {
                    return json(['errNo' => 10, 'msg' => '组织机构不能为空', 'data' => null]);
                }
                if (strlen($data['fee']) == 0) {
                    return json(['errNo' => 10, 'msg' => '费用信息不能为空', 'data' => null]);
                }
                if (strlen($data['accomTraffic']) == 0) {
                    return json(['errNo' => 10, 'msg' => '住宿交通信息不能为空', 'data' => null]);
                }
                if (strlen($data['contactUs']) == 0) {
                    return json(['errNo' => 10, 'msg' => '联系我们信息不能为空', 'data' => null]);
                }
                if (strlen($data['place']) == 0) {
                    return json(['errNo' => 10, 'msg' => '地点不能为空', 'data' => null]);
                }

                $meeting = new Meeting();
                $meeting->company_id = $companyId;
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

                $meetingDate = new MeetingDate();
                $meetingDate->meeting_id = $meeting->meeting_id;
                $meetingDate->manuscript_date = $data['manuscriptDate'];
                $meetingDate->manuscript_modify_date = $data['manuscriptModifyDate'];
                $meetingDate->inform_date = $data['informDate'];
                $meetingDate->register_begin_date = $data['registerBeginDate'];
                $meetingDate->register_end_date = $data['registerEndDate'];
                $meetingDate->meeting_begin_date = $data['meetingBeginDate'];
                $meetingDate->meeting_end_date = $data['meetingEndDate'];
                $meetingDate->save();

                $returnData['meetingId'] = AES::encrypt($meeting->meeting_id);
                return json(['errNo' => 0, 'msg' => '创建成功', 'data' => $returnData]);
            }
            else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 上传论文模版
    Function: uploadManuscriptTemplate
    Url: company/index/uploadManuscriptTemplate
    Type: post
    Input: formData: {file, fileName}
    Output: {errNo, msg, data: {url}}
        errNo: 0, msg: '上传成功', data: {url}
        errNo: 1, msg: '参数错误', data: null
        errNo: 2, msg: '未以单位或单位个体账号身份登录', data: null
        errNo: 10, msg: '单位或单位个体账号不存在', data: null
        errNo: 10, msg: '文件名不能为空', data: null
    */
    public function uploadManuscriptTemplate() {
        if ($this->request->isAjax()) {
            $file = request()->file('file');
            $fileName = request()->param('fileName');
            if (strlen($file) <= 0) {
                return json(['errNo' => 10, 'msg' => '请上传大小在0-10M范围内的文件', 'data' => null]);
            }
            if (isset($file) && isset($fileName)) {
                if (Session::has('companyId')) {
                    $companyId = Session::get('companyId');
                    $company = Company::get($companyId);
                    if (!isset($company)) {
                        return json(['errNo' => 10, 'msg' => '单位或单位个体账号不存在', 'data' => null]);
                    }
                } else if (Session::has('companyUnitId')) {
                    $companyUnitId = Session::get('companyUnitId');
                    $companyUnit = CompanyUnit::get($companyUnitId);
                    if (!isset($companyUnit)) {
                        return json(['errNo' => 10, 'msg' => '单位或单位个体账号不存在', 'data' => null]);
                    }
                    $company = $companyUnit->company()->find();
                    if (!isset($company)) {
                        return json(['errNo' => 10, 'msg' => '单位或单位个体账号不存在', 'data' => null]);
                    }
                } else {
                    return json(['errNo' => 2, 'msg' => '未以单位或单位个体账号身份登录', 'data' => null]);
                }

                $dir = './../upload/company/' . AES::encrypt($companyId) . '/template';
                $fileName = date('YmdHis', time()) . '_' . $fileName;

                $file->move($dir, $fileName);
                $returnData['url'] = str_replace("\\", '/', $dir . '/' . $fileName);
                return json(['errNo' => 0, 'msg' => '上传成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取单位会议数量
    Function: getCompanyMeetingCount
    Url: company/index/getCompanyMeetingCount
    Type: post
    Input: {}
    Output: {errNo, msg, data: {count}}
        errNo: 0, msg: '获取成功', data: {count}
        errNo: 2, msg: '未以单位或单位个体账号身份登录', data: null
        errNo: 10, msg: '单位或单位个体账号不存在', data: null
    */
    public function getCompanyMeetingCount() {
        if ($this->request->isAjax()) {
            if (Session::has('companyId')) {
                $companyId = Session::get('companyId');
                $company = Company::get($companyId);
                if (!isset($company)) {
                    return json(['errNo' => 10, 'msg' => '单位或单位个体账号不存在', 'data' => null]);
                }
            } else if (Session::has('companyUnitId')) {
                $companyUnitId = Session::get('companyUnitId');
                $companyUnit = CompanyUnit::get($companyUnitId);
                if (!isset($companyUnit)) {
                    return json(['errNo' => 10, 'msg' => '单位或单位个体账号不存在', 'data' => null]);
                }
                $company = $companyUnit->company()->find();
                if (!isset($company)) {
                    return json(['errNo' => 10, 'msg' => '单位或单位个体账号不存在', 'data' => null]);
                }
            } else {
                return json(['errNo' => 2, 'msg' => '未以单位或单位个体账号身份登录', 'data' => null]);
            }

            $returnData['count'] = $company->meetings()->count();
            return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取单位会议列表
    Function: getCompanyMeetingList
    Url: company/index/getCompanyMeetingList
    Type: post
    Input: {limit, page}
    Output: {errNo, msg, data: {meetingList: array of {meetingId, companyId, templateId, title, description, solicitInfo, agenda, organization, manuscriptTemplateUrl, fee, accomTraffic, contactUs, place, status, manuscriptDate, manuscriptModifyDate, informDate, registerBeginDate, registerEndDate, meetingBeginDate, meetingEndDate}}}
        errNo: 0, msg: '获取成功', data: {meetingList: array of {meetingId, companyId, title, description, solicitInfo, agenda, organization, manuscriptTemplateUrl, fee, accomTraffic, contactUs, place, status, manuscriptDate, manuscriptModifyDate, informDate, registerBeginDate, registerEndDate, meetingBeginDate, meetingEndDate}}
        errNo: 2, msg: '未以单位或单位个体账号身份登录', data: null
        errNo: 3, msg: '分页信息错误', data: null
        errNo: 10, msg: '单位或单位个体账号不存在', data: null
    */
    public function getCompanyMeetingList() {
        if ($this->request->isAjax()) {
            $data = input();
            if(isset($data['page']) && isset($data['limit'])){
                $page = $data['page'];
                $limit = $data['limit'];
                if ($limit < 0 || $page < 0 || ($limit != 0 && $page == 0)) {
                    return json(['errNo' => 3, 'msg' => '分页信息错误', 'data' => null]);
                }

                if (Session::has('companyId')) {
                    $companyId = Session::get('companyId');
                    $company = Company::get($companyId);
                    if (!isset($company)) {
                        return json(['errNo' => 10, 'msg' => '单位或单位个体账号不存在', 'data' => null]);
                    }
                } else if (Session::has('companyUnitId')) {
                    $companyUnitId = Session::get('companyUnitId');
                    $companyUnit = CompanyUnit::get($companyUnitId);
                    if (!isset($companyUnit)) {
                        return json(['errNo' => 10, 'msg' => '单位或单位个体账号不存在', 'data' => null]);
                    }
                    $company = $companyUnit->company()->find();
                    if (!isset($company)) {
                        return json(['errNo' => 10, 'msg' => '单位或单位个体账号不存在', 'data' => null]);
                    }
                } else {
                    return json(['errNo' => 2, 'msg' => '未以单位或单位个体账号身份登录', 'data' => null]);
                }

                $returnData['meetingList'] = array();
                if ($limit == 0) {
                    $meetings = $company->meetings()->select();
                } else {
                    $meetings = $company->meetings()->page($page, $limit)->select();
                }
                foreach ($meetings as $meeting) {
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
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }
}
