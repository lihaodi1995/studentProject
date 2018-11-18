<?php
namespace app\admin\controller;

use think\Controller;
use app\common\AES;

class Template extends controller {
    public function index() {
        return $this->fetch();
    }

    /*Interface: 获取模板列表
    Function: getTemplateList
    Url: admin/template/getTemplateList
    Type: post
    Input: {}
    Output: {errNo, msg, data: {templateList: array of {templateId, name, imgUrl}}}
        errNo: 0, msg: '获取成功', data: {templateList: array of {templateId, name, imgUrl}}
    */
    public function getTemplateList() {
        if ($this->request->isAjax()) {
            $templates = \app\common\model\Template::order('template_id', 'asc')->select();
            $returnData['templateList'] = array();
            foreach ($templates as $template) {
                $templateInfo = array (
                    'templateId' => AES::encrypt($template->template_id),
                    'name' => $template->name,
                    'imgUrl' => $template->imgUrl
                );
                $returnData['templateList'][] = $templateInfo;
            }
            return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
        } else return $this->error('页面错误');
    }

    /*Interface: 获取模板信息
    Function: getTemplateDetail
    Url: admin/template/getTemplateDetail
    Type: post
    Input: {templateId}
    Output: {errNo, msg, data: {templateId, name, imgUrl}}
        errNo: 0, msg: '获取成功', data: {templateId, name, imgUrl}
        errNo: 1, msg: '参数错误', data: null
        errNo: 10, msg: '模板不存在', data:null
    */
    public function getTemplateDetail() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['templateId'])) {
                $templateId = AES::decrypt($data['templateId']);
                $template = \app\common\model\Template::get($templateId);
                if (!isset($template)) {
                    return json(['errNo' => 10, 'msg' => '模板不存在', 'data' => null]);
                }
                $returnData = array(
                    'templateId' => AES::encrypt($template->template_id),
                    'name' => $template->name,
                    'imgUrl' => $template->imgUrl,
                );
                return json(['errNo' => 0, 'msg' => '获取成功', 'data' => $returnData]);
            } else return json(['errNo' => 1, 'msg' => '参数错误', 'data' => null]);
        } else return $this->error('页面错误');
    }

    /*Interface: 删除模板
    Function: deleteTemplate
    Url: admin/template/deleteTemplate
    Type: post
    Input: {templateId}
    Output: {errNo, msg}
        errNo: 0, msg: '删除成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '模板不存在'
    */
    public function deleteTemplate() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['templateId'])) {
                $templateId = AES::decrypt($data['templateId']);
                $template = \app\common\model\Template::get($templateId);
                if (!isset($template)) {
                    return json(['errNo' => 10, 'msg' => '模板不存在']);
                }
                $template->delete();
                return json(['errNo' => 0, 'msg' => '删除成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 创建模版
    Function: createTemplate
    Url: admin/template/createTemplate
    Type: post
    Input: {name}
    Output: {errNo, msg}
        errNo: 0, msg: '创建成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '模板名不能为空'
        errNo: 10, msg: '模版名已经使用'
    */
    public function createTemplate() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['name'])) {
                $name = trim($data['name']);
                $template = \app\common\model\Template::where('name', $name)->find();
                if (isset($template) || $name == 'index') {
                    return json(['errNo' => 1, 'msg' => '模版名已经使用']);
                }
                $template = new \app\common\model\Template();
                $template->name = $name;
                $template->imgUrl = null;
                $template->save();
                return json(['errNo' => 0, 'msg' => '创建成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 上传模板图片
    Function: uploadTemplateImg
    Url: admin/template/uploadTemplateImg
    Type: post
    Input: formData: {file, fileName, templateId}
    Output: {errNo, msg}
        errNo: 0, msg: '上传成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '模版不存在'
    */
    public function uploadTemplateImg() {
        if ($this->request->isAjax()) {
            $file = request()->file('file');
            $fileName = request()->param('fileName');
            $templateId = request()->param('templateId');
            if (strlen($file) <= 0) {
                return json(['errNo' => 10, 'msg' => '请上传大小在0-10M范围内的文件', 'data' => null]);
            }
            if (isset($file) && isset($fileName) && isset($templateId)) {
                $templateId = AES::decrypt($templateId);
                $template = \app\common\model\Template::get($templateId);
                if (!isset($template)) {
                    return json(['errNo' => 10, 'msg' => '模版不存在']);
                }
                $dir = './templateImg/' . AES::encrypt($templateId);
                $fileName = date('YmdHis', time()) . '_' . $fileName;
                $file->move($dir, $fileName);
                $fileUrl = str_replace("\\", '/', $dir . '/' . $fileName);
                $template->imgUrl = $fileUrl;
                $template->save();
                return json(['errNo' => 0, 'msg' => '上传成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 上传模板html文件
    Function: uploadTemplateHtml
    Url: admin/template/uploadTemplateHtml
    Type: post
    Input: formData: {file, templateId}
    Output: {errNo, msg}
        errNo: 0, msg: '上传成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '模版不存在'
    */
    public function uploadTemplateHtml() {
        if ($this->request->isAjax()) {
            $file = request()->file('file');
            $templateId = request()->param('templateId');
            if (strlen($file) <= 0) {
                return json(['errNo' => 10, 'msg' => '请上传大小在0-10M范围内的文件', 'data' => null]);
            }
            if (isset($file) && isset($templateId)) {
                $templateId = AES::decrypt($templateId);
                $template = \app\common\model\Template::get($templateId);
                if (!isset($template)) {
                    return json(['errNo' => 10, 'msg' => '模版不存在']);
                }
                $dir = './../application/meeting/view/index';
                $fileName = $template->name . '.html';
                $file->move($dir, $fileName);
                return json(['errNo' => 0, 'msg' => '上传成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }
}