<?php
namespace app\test\controller;

use think\Controller;
use think\facade\Session;
use app\common\AES;
use app\common\RSA;
use app\common\Mail;
use app\common\PwdHash;
use app\common\MeetingStatus;
use app\common\model\User;
use app\common\model\Subscribe;
use app\common\model\Company;
use app\common\model\CompanyUnit;
use app\common\model\CompanyAddition;
use app\common\model\Meeting;
use app\common\model\MeetingDate;

class Upload extends controller {
    public function index() {
        return $this->fetch();
    }

    public function uploadManuscript() {
        if ($this->request->isAjax()) {
            $file = request()->file('file');
            //$meetingId = request()->param('meetingId');
            $fileName = request()->param('fileName');
            //if (isset($meetingId) && isset($file) && isset($fileName)) {
                // Session::set('userId', 4);
                // if (Session::has('userId')) {
                    // $userId = Session::get('userId');
                    // $user = User::get($userId);
                    // if (!isset($user)) {
                    //     return json(['errNo' => 10, 'msg' => '会员不存在', 'data' => null]);
                    // }
                    // $meetingId = AES::decrypt($meetingId);
                    // $meeting = Meeting::get($meetingId);
                    // if (!isset($meeting)) {
                    //     return json(['errNo' => 10, 'msg' => '会议不存在', 'data' => null]);
                    // }
                    // if (strlen($fileName) == 0) {
                    //     return json(['errNo' => 10, 'msg' => '文件名不能为空', 'data' => null]);
                    // }
                    return json(['errNo' => 0, 'msg' => '文件大小', 'data' => strlen($file)]);
                    
                    $dir = './../upload/meeting/' . AES::encrypt($meetingId) . '/manuscripts';
                    $fileName = AES::encrypt($userId) . '_' . date('YmdHis', time()) . '_' . $fileName;
                    $file->move($dir, $fileName);
                    $returnData['url'] = str_replace("\\", '/', $dir . '/' . $fileName);
                    return json(['errNo' => 0, 'msg' => '上传成功', 'data' => $returnData]);
                // }
            //} else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    public function upload() {
        if ($this->request->isAjax()) {
            $file = request()->file('file');
            $meetingId = request()->param('meetingId');
            $userId = request()->param('userId');
            $moveUrl = './../upload/meetingId/userId';
            $info = $file->move($moveUrl, 'test.pdf');
            $returnData['fileUrl'] = str_replace("\\", '/', $moveUrl . '/' . $info->getSaveName());
            return json(['errNo' => 0, 'msg' => '上传成功', 'data' => $returnData]);
        } else return $this->error('页面错误');
    }

    public function uploadRename() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['originUrl']) && isset($data['fileDir']) && isset($data['fileName'])) {
                $originUrl = $data['originUrl'];
                $fileDir = $data['fileDir'];
                $fileName = $data['fileName'] . substr($originUrl, strrpos($originUrl, '.'));
                if (!file_exists($fileDir)) {
                    mkdir($fileDir, 777, true);
                }
                $fileUrl = './../upload/' . $fileDir . '/' . $fileName;
                echo $fileUrl;
                rename($originUrl, $fileUrl);
                $returnData['fileUrl'] = $fileUrl;
                return json(['errNo' => 0, 'msg' => '重命名成功', 'data' => $returnData]);
            } return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    public function download($fileUrl, $fileName) {
        if (isset($fileUrl) && isset($fileName)) {
            $url = $fileUrl;
            $name = $fileName . substr($url, strrpos($url, '.'));
            if(!file_exists($url)){ //检查文件是否存在  
                return json(['errNo' => 4, 'msg' => '文件不存在']);
            }
            $fileName = basename($url);  
            $fileType = explode('.', $url);  
            $fileType = $fileType[count($fileType) - 1];  
            $fileName = urlencode($name);  
            $fileType = fopen($url,'r'); //打开文件  
            //输入文件标签 
            header("Content-type: application/octet-stream");  
            header("Accept-Ranges: bytes");  
            header("Accept-Length: " . filesize($url));  
            header("Content-Disposition: attachment; filename=" . $fileName);  
            //输出文件内容  
            echo fread($fileType, filesize($url));  
            fclose($fileType);
            return json(['errNo' => 0, 'msg' => '下载成功']);
        } return $this->error('页面错误');
    }

    public function packCompanyAddition() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['companyId'])) {
                $companyId = AES::decrypt($data['companyId']);
                $company = Company::get($companyId);
                if (!isset($company)) {
                    return json(['errNo' => 10, 'msg' => '单位不存在', 'data' => null]);  
                }

                $zipDir = './../upload/companyAddition/' . AES::encrypt($companyId);
                $zipName = 'companyAdditions_' . date('YmdHis', time()) . '.zip';
                $zip = new \ZipArchive();
                $zip->open($zipDir . '/'. $zipName, \ZipArchive::CREATE);
                $companyAdditions = $company->companyAdditions()->select();
                foreach ($companyAdditions as $companyAddition) {
                    $url = $companyAddition->url;
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
}
