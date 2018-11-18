<?php
namespace app\company\controller;

use think\Controller;
use think\facade\Session;
use app\common\AES;
use app\common\model\Company;
use app\common\model\CompanyAddition;

class Verify extends controller {
    public function index() {
        return $this->fetch();
    }

    /*Interface: 上传单位审核信息
    Function: uploadCompanyAddition
    Url: company/verify/uploadCompanyAddition
    Type: post
    Input: formData: {file, fileName}
    Output: {errNo, msg}
        errNo: 0, msg: '上传成功'
        errNo: 1, msg: '参数错误'
        errNo: 2, msg: '未以单位身份登录'
        errNo: 10, msg: '单位不存在'
        errNo: 10, msg: '单位已审核通过'
    */
    public function uploadCompanyAddition() {
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
                        return json(['errNo' => 10, 'msg' => '单位不存在']);
                    }
                    if ($company->confirm == 1) {
                        return json(['errNo' => 10, 'msg' => '单位已审核通过']);
                    }
                    if (strlen($fileName) == 0) {
                        return json(['errNo' => 10, 'msg' => '文件名不能为空']);
                    }

                    $dir = './../upload/company/' . AES::encrypt($companyId) . '/companyAdditions';
                    $fileName = date('YmdHis', time()) . '_' . $fileName;
                    $file->move($dir, $fileName);
                    $fileUrl = str_replace("\\", '/', $dir . '/' . $fileName);

                    $companyAddition = new CompanyAddition();
                    $companyAddition->company_id = $companyId;
                    $companyAddition->url = $fileUrl;
                    $companyAddition->save();
                    $company->confirm = 0;
                    $company->save();
                    return json(['errNo' => 0, 'msg' => '上传成功']);
                } else return json(['errNo' => 2, 'msg' => '未以单位身份登录']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 删除单位审核信息
    Function: deleteCompanyAddition
    Url: company/verify/deleteCompanyAddition
    Input: {companyAdditionId}
    Output: {errNo, msg}
        errNo: 0, msg: '删除成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '审核信息不存在'
    */
    public function deleteCompanyAddition() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['companyAdditionId'])) {
                $companyAdditionId = AES::decrypt($data['companyAdditionId']);
                $companyAddition = CompanyAddition::get($companyAdditionId);
                if (!isset($companyAddition)) {
                    return json(['errNo' => 10, 'msg' => '审核信息不存在']);  
                }
                $companyAddition->delete();
                return json(['errNo' => 0, 'msg' => '删除成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取单位审核信息列表
    Function: getCompanyAdditionList
    Url: company/verify/getCompanyAdditionList
    Input: {companyId}
    Output: {errNo, msg, data: {companyAdditionList: array of {companyAdditionId, companyId, url}}}
        errNo: 0, msg: '获取成功', data: {companyAdditionList: array of {companyAdditionId, companyId, url}}
        errNo: 1, msg: '参数错误', data: null
        errNo: 10, msg: '单位不存在', data: null
    */
    public function getCompanyAdditionList() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['companyId'])) {
                $companyId = AES::decrypt($data['companyId']);
                $company = Company::get($companyId);
                if (!isset($company)) {
                    return json(['errNo' => 10, 'msg' => '单位不存在', 'data' => null]);  
                }
                $companyAdditions = $company->companyAdditions()->select();
                $returnData['companyAdditionList'] = array();
                foreach ($companyAdditions as $companyAddition) {
                    $companyAdditionInfo = array(
                        'companyAdditionId' => AES::encrypt($companyAddition->company_addition_id),
                        'companyId' => AES::encrypt($company->company_id),
                        'url' => $companyAddition->url
                    );
                }
                return json(['errNo' => 0, 'msg' => '删除成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 打包单位审核信息
    Function: packCompanyAddition
    Url: company/verify/packCompanyAddition
    Input: {companyId}
    Output: {errNo, msg, data: {url}}
        errNo: 0, msg: '打包成功', data: {url}
        errNo: 1, msg: '参数错误', data: null
        errNo: 10, msg: '单位不存在', data: null
    */
    public function packCompanyAddition() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['companyId'])) {
                $companyId = AES::decrypt($data['companyId']);
                $company = Company::get($companyId);
                if (!isset($company)) {
                    return json(['errNo' => 10, 'msg' => '单位不存在', 'data' => null]);  
                }

                $zipDir = './../upload/company/' . AES::encrypt($companyId);
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