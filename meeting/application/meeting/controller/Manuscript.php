<?php
namespace app\meeting\controller;

use think\Controller;
use think\facade\Session;
use app\common\AES;
use app\common\Excel;
use app\common\model\User;
use app\common\model\Meeting;
use app\common\model\ManuscriptInfo;

class Manuscript extends controller {
    public function index() {
        return $this->fetch();
    }

    public function detail() {
        return $this->fetch();
    }

    public function list() {
        return $this->fetch();
    }

    /*Interface: 创建稿件
    Function: createManuscript
    Url: meeting/manuscript/createManuscript
    Type: post
    Input: {meetingId, type, url, author, title, organization, abstract, modify_info}
    Output: {errNo, msg}
        errNo: 0, msg: 创建成功
        errNo: 1, msg: 参数错误
        errNo: 2, msg: 未以用户身份登录
        errNo: 10, msg: 会员不存在
        errNo: 10, msg: 会议不存在
    NOTE: type: 1-投稿, 2-修改稿
    NOTE: type为1不传入修改信息, type为2必须传入修改信息
    NOTE: author: json(array of {name, email, org})
    */
    public function createManuscript() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['meetingId']) && isset($data['type']) && isset($data['url'])
            && isset($data['author']) && isset($data['title']) && isset($data['organization']) && isset($data['abstract'])) {
                if ($data['type'] == 1 && isset($data['modify_info'])) {
                    return json(['errNo' => 1, 'msg' => '参数错误']);
                }
                if ($data['type'] == 2 && !isset($data['modify_info'])) {
                    return json(['errNo' => 1, 'msg' => '参数错误']);
                }
                if (Session::has('userId')) {
                    $userId = Session::get('userId');
                    $user = User::get($userId);
                    if (!isset($user)) {
                        return json(['errNo' => 10, 'msg' => '会员不存在']);
                    }
                    $meetingId = AES::decrypt($data['meetingId']);
                    $meeting = Meeting::get($meetingId);
                    if (!isset($meeting)) {
                        return json(['errNo' => 10, 'msg' => '会议不存在']);
                    }

                    $manuscript = \app\common\model\Manuscript::where('user_id', $userId)->where('meeting_id', $meetingId)->where('valid', 1)->find();
                    if (isset($manuscript)) {
                        $manuscript->valid = 0;
                        $manuscript->save();
                    }

                    $manuscript = new \app\common\model\Manuscript();
                    $manuscript->user_id = $userId;
                    $manuscript->meeting_id = $meetingId;
                    $manuscript->type = $data['type'];
                    $manuscript->valid = 1;
                    $manuscript->url = $data['url'];
                    $manuscript->save();

                    $manuscriptInfo = new ManuscriptInfo();
                    $manuscriptInfo->manuscript_id = $manuscript->manuscript_id;
                    $manuscriptInfo->author = $data['author'];
                    $manuscriptInfo->title = $data['title'];
                    $manuscriptInfo->organization = $data['organization'];
                    $manuscriptInfo->abstract = $data['abstract'];
                    if ($data['type'] == 2) {
                        $manuscriptInfo->modify_info = $data['modify_info'];
                    } else {
                        $manuscriptInfo->modify_info = null;
                    }
                    $manuscriptInfo->save();
                    return json(['errNo' => 0, 'msg' => '创建成功']);
                } else return json(['errNo' => 2, 'msg' => '未以会员身份登录']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取稿件详细信息
    Function: getManuscriptDetail
    Url: meeting/manuscript/getManuscriptDetail
    Type: post
    Input: {manuscriptId}
    Output: {errNo, msg, data: {manuscriptId, userId, meetingId, type, valid, url, author, title, organization, abstract, modify_info}}
        errNo: 0, msg: '获取成功', data: {manuscriptId, userId, meetingId, type, valid, url, author, title, organization, abstract, modify_info}
        errNo: 1, msg: '参数错误', data: null
        errNo: 10, msg: '稿件不存在', data: null
        errNo: 10, msg: '稿件信息不存在', data: null
    */
    public function getManuscriptDetail() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['manuscriptId'])) {
                $manuscriptId = AES::decrypt($data['manuscriptId']);
                $manuscript = \app\common\model\Manuscript::get($manuscriptId);
                if (!isset($manuscript)) {
                    return json(['errNo' => 10, 'msg' => '稿件不存在', 'data' => null]);
                }
                $manuscriptInfo = $manuscript->manuscriptInfo()->find();
                if (!isset($manuscriptInfo)) {
                    return json(['errNo' => 10, 'msg' => '稿件信息不存在', 'data' => null]);
                }
                
                $returnData = array(
                    'manuscriptId' => AES::encrypt($manuscript->manuscript_id),
                    'userId' => AES::encrypt($manuscript->user_id),
                    'meetingId' => AES::encrypt($manuscript->meeting_id),
                    'type' => $manuscript->type,
                    'valid' => $manuscript->valid,
                    'url' => $manuscript->url,
                    'author' => $manuscriptInfo->author,
                    'title' => $manuscriptInfo->title,
                    'organization' => $manuscriptInfo->organization,
                    'abstract' => $manuscriptInfo->abstract,
                    'modify_info' => $manuscriptInfo->modify_info
                );
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取用户会议投稿状态
    Function: getUserMeetingManuscriptStatus
    Url: meeting/manuscript/getUserMeetingManuscriptStatus
    Type: post
    Input: {meetingId}
    Output: {errNo, msg, data: {status}}
        errNo: 0, msg: '获取成功', data: {status}
        errNo: 1, msg: '参数错误', data: null
        errNo: 2, msg: '未以会员身份登录', data: null
        errNo: 10, msg: '会员不存在', data: null
        errNo: 10, msg: '会议不存在', data: null
    NOTE: status: 0-未投稿, 1-已投稿未审核, 2-已投稿且审核结果为未录用, 3-已投稿且审核结果为录用, 4-已投稿且审核结果为修改后录用, 5-已投修改稿未审核, 6-已投修改稿审核结果为未录用, 7-已投修改稿审核结果为录用
    */
    public function getUserMeetingManuscriptStatus() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['meetingId'])) {
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

                    $manuscript = \app\common\model\Manuscript::where('user_id', $userId)->where('meeting_id', $meetingId)->where('valid', 1)->find();
                    if (!isset($manuscript)) {
                        $returnData['status'] = 0; //0-未投稿
                    } else {
                        $type = $manuscript->type;
                        if ($type == 1) {
                            $review = $manuscript->review()->find();
                            if (!isset($review)) {
                                $returnData['status'] = 1; //1-已投稿未审核
                            } else {
                                $returnData['status'] = 2 + $review->result; //2, 3, 4-已投稿已审核
                            }
                        } else {
                            $review = $manuscript->review()->find();
                            if (!isset($review)) {
                                $returnData['status'] = 5; //5-已投修改稿未审核
                            } else {
                                $returnData['status'] = 6 + $review->result; //6, 7-已投修改稿已审核
                            }
                        }
                    }
                    return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
                } else return json(['errNo' => 2, 'msg' => '未以会员身份登录']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }
    
    /*Interface: 获取当前用户在某会议投稿的稿件详细信息
    Function: getUserMeetingManuscriptDetail
    Url: meeting/manuscript/getUserMeetingManuscriptDetail
    Type: post
    Input: {meetingId}
    Output: {errNo, msg, data: {manuscriptId, userId, meetingId, type, valid, url, author, title, organization, abstract, modify_info}}
        errNo: 0, msg: '获取成功', data: {manuscriptId, userId, meetingId, type, valid, url, author, title, organization, abstract, modify_info}
        errNo: 1, msg: '参数错误', data: null
        errNo: 2, msg: '未以会员身份登录', data: null
        errNo: 10, msg: '会员不存在', data: null
        errNo: 10, msg: '会议不存在', data: null
        errNo: 10, msg: '稿件不存在', data: null
        errNo: 10, msg: '稿件信息不存在', data: null
    */
    public function getUserMeetingManuscriptDetail() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['meetingId'])) {
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

                    $manuscript = \app\common\model\Manuscript::where('user_id', $userId)->where('meeting_id', $meetingId)->where('valid', 1)->find();
                    if (!isset($manuscript)) {
                        return json(['errNo' => 10, 'msg' => '稿件不存在', 'data' => null]);
                    }
                    $manuscriptInfo = $manuscript->manuscriptInfo()->find();
                    if (!isset($manuscriptInfo)) {
                        return json(['errNo' => 10, 'msg' => '稿件信息不存在', 'data' => null]);
                    }
                    
                    $returnData = array(
                        'manuscriptId' => AES::encrypt($manuscript->manuscript_id),
                        'userId' => AES::encrypt($manuscript->user_id),
                        'meetingId' => AES::encrypt($manuscript->meeting_id),
                        'type' => $manuscript->type,
                        'valid' => $manuscript->valid,
                        'url' => $manuscript->url,
                        'author' => $manuscriptInfo->author,
                        'title' => $manuscriptInfo->title,
                        'organization' => $manuscriptInfo->organization,
                        'abstract' => $manuscriptInfo->abstract,
                        'modify_info' => $manuscriptInfo->modify_info
                    );
                    return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
                } else return json(['errNo' => 2, 'msg' => '未以会员身份登录']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取会议稿件数量
    Function: getMeetingManuscriptCount
    Url: meeting/manuscript/getMeetingManuscriptCount
    Type: post
    Input: {meetingId, inputType}
    Output: {errNo, msg, data: {count}}
        errNo: 0, msg: '获取成功', data: {count}
        errNo: 1, msg: '传入参数错误', data: null
        errNo: 10, msg: '会议不存在', data: null
    NOTE: inputType: 0-全部, 1-未审核, 2-未录用, 3-录用, 4-修改后录用
    */
    public function getMeetingManuscriptCount() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['meetingId']) && isset($data['inputType'])) {
                $meetingId = AES::decrypt($data['meetingId']);
                $meeting = Meeting::get($meetingId);
                if (!isset($meeting)) {
                    return json(['errNo' => 10, 'msg' => '会议不存在', 'data' => null]);
                }

                $count = 0;
                $manuscripts = $meeting->manuscripts()->where('valid', 1)->order('create_time', 'asc')->select();
                foreach ($manuscripts as $manuscript) {
                    $manuscriptInfo = $manuscript->manuscriptInfo()->find();
                    if (!isset($manuscriptInfo)) {
                        continue;
                    }
                    switch ($data['inputType']) {
                        case 0:
                            $count++;
                            break;
                        case 1:
                            $review = $manuscript->review()->find();
                            if (!isset($review)) {
                                $count++;
                            }
                            break;
                        case 2:
                        case 3:
                        case 4:
                            $review = $manuscript->review()->find();
                            if (isset($review) && $review->result + 2 == $data['inputType']) {
                                $count++;
                            }
                            
                        break;
                    }
                }
                $returnData['count'] = $count;
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取会议稿件列表
    Function: getMeetingManuscriptList
    Url: meeting/manuscript/getMeetingManuscriptList
    Type: post
    Input: {meetingId, limit, page, inputType}
    Output: {errNo, msg, data: {manuscriptList: array of {manuscriptId, userId, meetingId, type, valid, url, author, title, organization, abstract, modify_info, type}}}
        errNo: 0, msg: '获取成功', data: {manuscriptList: array of {manuscriptId, userId, meetingId, type, valid, url, author, title, organization, abstract, modify_info, type}}
        errNo: 1, msg: '传入参数错误', data: null
        errNo: 3, msg: '分页信息错误', data: null
        errNo: 10, msg: '会议不存在', data: null
    NOTE: type: 1-未审核, 2-未录用, 3-录用, 4-修改后录用
    */
    public function getMeetingManuscriptList() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['meetingId']) && isset($data['limit']) && isset($data['page']) && isset($data['inputType'])) {
                $page = $data['page'];
                $limit = $data['limit'];
                if ($limit < 0 || $page < 0 || ($limit != 0 && $page == 0)) {
                    return json(['errNo' => 3, 'msg' => '分页信息错误', 'data' => null]);
                }

                $meetingId = AES::decrypt($data['meetingId']);
                $meeting = Meeting::get($meetingId);
                if (!isset($meeting)) {
                    return json(['errNo' => 10, 'msg' => '会议不存在', 'data' => null]);
                }

                // if ($limit == 0) {
                //     $manuscripts = $meeting->manuscripts()->where('valid', 1)->order('create_time', 'desc')->select();
                // } else {
                //     $manuscripts = $meeting->manuscripts()->where('valid', 1)->order('create_time', 'desc')->page($page, $limit)->select();
                // }
                
                $manuscripts = $meeting->manuscripts()->where('valid', 1)->order('create_time', 'asc')->select();
                $returnData['manuscriptList'] = array();
                $count = 0;
                foreach ($manuscripts as $manuscript) {
                    $manuscriptInfo = $manuscript->manuscriptInfo()->find();
                    if (!isset($manuscriptInfo)) {
                        continue;
                    }
                    $review = $manuscript->review()->find();
                    if (!isset($review)) {
                        $type = 1;
                    } else {
                        $type = 2 + $review->result;
                    }
                    $manuscriptDetail = array(
                        'manuscriptId' => AES::encrypt($manuscript->manuscript_id),
                        'userId' => AES::encrypt($manuscript->user_id),
                        'meetingId' => AES::encrypt($manuscript->meeting_id),
                        'type' => $manuscript->type,
                        'valid' => $manuscript->valid,
                        'url' => $manuscript->url,
                        'author' => $manuscriptInfo->author,
                        'title' => $manuscriptInfo->title,
                        'organization' => $manuscriptInfo->organization,
                        'abstract' => $manuscriptInfo->abstract,
                        'modify_info' => $manuscriptInfo->modify_info,
                        'type' => $type
                    );

                    
                    switch ($data['inputType']) {
                        case 0:
                            $count++;
                            if ((($page - 1) * $limit < $count) && ($count <= $page * $limit)) {
                                $returnData['manuscriptList'][] = $manuscriptDetail;
                            }
                            break;
                        case 1:
                            $review = $manuscript->review()->find();
                            if (!isset($review)) {
                                $count++;
                                if ((($page - 1) * $limit < $count) && ($count <= $page * $limit)) {
                                    $returnData['manuscriptList'][] = $manuscriptDetail;
                                }
                            }
                            break;
                        case 2:
                        case 3:
                        case 4:
                            $review = $manuscript->review()->find();
                            if (isset($review) && $review->result + 2 == $data['inputType']) {
                                $count++;
                                if ((($page - 1) * $limit < $count) && ($count <= $page * $limit)) {
                                    $returnData['manuscriptList'][] = $manuscriptDetail;
                                }
                            } 
                            break;
                    }
                }
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 上传稿件
    Function: uploadManuscript
    Url: meeting/manuscript/uploadManuscript
    Type: post
    Input: formData: {file, meetingId, fileName}
    Output: {errNo, msg, data: {url}}
        errNo: 0, msg: '上传成功', data: {url}
        errNo: 1, msg: '参数错误', data: null
        errNo: 10, msg: '会员不存在', data: null
        errNo: 10, msg: '会议不存在', data: null
        errNo: 10, msg: '文件名不能为空', data: null

    Sample:
    
        var file = document.getElementById('inputUpload').files[0];
        if (file == null) {
            alert('请选择上传的文件。');
            return;
        }
        var fileName = file.name.trim();
        console.log('fileName: ' + fileName);
        // var fileExtension = fileName.substring(fileName.lastIndexOf('.'), fileName.length).toLowerCase();
        // var acceptFileExtension = new Array('.pdf', '.jpg', '.jpeg', '.png');
        // if (acceptFileExtension.indexOf(fileExtension) == -1){
        //     alert('请上传pdf/jgp/jpeg/png格式的审核信息。');
        //     return;
        // }
    
        var formData = new FormData();
        formData.append('file', file);
        formData.append('meetingId', 'L3ZOOUwzUzNRNlcrZUVKekJLZytJdz09');
        formData.append('fileName', fileName);
        $.ajax({
            type: 'post',
            url: "{:url('meeting/manuscript/uploadManuscript')}",
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            async: false,
            success: function(data) {
                fileUrl = data['data']['url'];
                console.log('fileUrl: ' + fileUrl);
            }
        })
        
    */
    public function uploadManuscript() {
        if ($this->request->isAjax()) {
            $file = request()->file('file');
            $meetingId = request()->param('meetingId');
            $fileName = request()->param('fileName');
            if (strlen($file) <= 0) {
                return json(['errNo' => 10, 'msg' => '请上传大小在0-10M范围内的文件', 'data' => null]);
            }
            if (isset($meetingId) && isset($file) && isset($fileName)) {
                if (Session::has('userId')) {
                    $userId = Session::get('userId');
                    $user = User::get($userId);
                    if (!isset($user)) {
                        return json(['errNo' => 10, 'msg' => '会员不存在', 'data' => null]);
                    }
                    $meetingId = AES::decrypt($meetingId);
                    $meeting = Meeting::get($meetingId);
                    if (!isset($meeting)) {
                        return json(['errNo' => 10, 'msg' => '会议不存在', 'data' => null]);
                    }
                    if (strlen($fileName) == 0) {
                        return json(['errNo' => 10, 'msg' => '文件名不能为空', 'data' => null]);
                    }
                    
                    $dir = './../upload/meeting/' . AES::encrypt($meetingId) . '/manuscripts';
                    $fileName = AES::encrypt($userId) . '_' . date('YmdHis', time()) . '_' . $fileName;
                    $file->move($dir, $fileName);
                    $returnData['url'] = str_replace("\\", '/', $dir . '/' . $fileName);
                    return json(['errNo' => 0, 'msg' => '上传成功', 'data' => $returnData]);
                }
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 打包会议投稿
    Function: packMeetingManuscripts
    Url: meeting/manuscript/packMeetingManuscripts
    Type: post
    Input: {meetingId}
    Output: {errNo, msg, data: {url}}
        errNo: 0, msg: '打包成功', data: {url}
        errNo: 1, msg: '参数错误', data: null
        errNo: 10, msg: '会议不存在', data: null
    */
    public function packMeetingManuscripts() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['meetingId'])) {
                $meetingId = AES::decrypt($data['meetingId']);
                $meeting = Meeting::get($meetingId);
                if (!isset($meeting)) {
                    return json(['errNo' => 10, 'msg' => '会议不存在', 'data' => null]);
                }

                $zipDir = './../upload/meeting/' . AES::encrypt($meetingId);
                $zipName = 'manuscripts_' . date('YmdHis', time()) . '.zip';
                $zip = new \ZipArchive();
                $zip->open($zipDir . '/'. $zipName, \ZipArchive::CREATE);
                $manuscripts = $meeting->manuscripts()->where('valid', 1)->select();
                foreach ($manuscripts as $manuscript) {
                    $url = $manuscript->url;
                    if (file_exists($url)) {
                        $zip->addFile($url, basename($url));
                    }
                }
                $zip->close();
                $returnData['url'] = $zipDir . '/' . $zipName;
                return json(['errNo' => 0, 'msg' => '打包成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 导出会议稿件Excel
    Function: exportMeetingManuscriptExcel
    Url: meeting/manuscript/exportMeetingManuscriptExcel

    Sample:
    function export() {
        strUrl = "{:url('meeting/manuscript/exportMeetingManuscriptExcel')}";
        strUrl += '?meetingId=L3ZOOUwzUzNRNlcrZUVKekJLZytJdz09';
        window.location.href = strUrl;
    }
    */
    public function exportMeetingManuscriptExcel($meetingId = '') {
        if (strlen($meetingId) == 0) {
            return $this->error('页面错误');
        }
        $meetingId = AES::decrypt($meetingId);
        $meeting = Meeting::get($meetingId);
        if (!isset($meeting)) {
            return $this->error('页面错误');
        }

        $eName = '会议投稿汇总表';
        $eHeader = array();
        $eData = array();
        $eHeader[] = '投稿编号';
        $eHeader[] = '作者信息';
        $eHeader[] = '题目';
        $eHeader[] = '单位';
        $eHeader[] = '摘要';

        $cnt = 0;
        $manuscripts = $meeting->manuscripts()->where('valid', 1)->order('create_time', 'asc')->select();
        foreach ($manuscripts as $manuscript) {
            $manuscriptInfo = $manuscript->manuscriptInfo()->find();
            if (!isset($manuscriptInfo)) continue;
            $eData[$cnt] = array();
            $eData[$cnt][] = $cnt + 1;
            $authorArray = json_decode($manuscriptInfo->author, true);
            if (!isset($authorArray)) continue;
            $authorCnt = 0;
            $author = '';
            foreach ($authorArray as $authorInfo) {
                $authorCnt++;
                $author.='第' . $authorCnt . '作者姓名: ' . $authorInfo['name'] . ', 所属组织: ' . $authorInfo['org'] . ', 邮箱: ' . $authorInfo['email'] . "\r\n"; 
            }
            $eData[$cnt][] = $author;
            $eData[$cnt][] = $manuscriptInfo->title;
            $eData[$cnt][] = $manuscriptInfo->organization;
            $eData[$cnt][] = $manuscriptInfo->abstract;
            $cnt++;
        }
        Excel::export($eName, $eHeader, $eData);
    }
}