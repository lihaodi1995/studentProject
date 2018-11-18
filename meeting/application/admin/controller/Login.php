<?php
namespace app\admin\controller;

use app\common\model\Admin;
use app\common\model\ManuscriptInfo;
use think\Controller;
use think\facade\Session;
use app\common\AES;
use app\common\MeetingStatus;
use app\common\model\Subscribe;
use app\common\PwdHash;
use app\common\model\Meeting;
use app\common\model\MeetingDate;
use think\Request;

class Login extends controller {
    public function index() {
        return $this->fetch();
    }
    public function test()
    {
    }

    /*Interface: 管理员登录
    Function: adminLogin
    Url: admin/login/adminLogin
    Type: post
    Input: {account, password}
    Output: {errNo, msg}
        errNo: 0, msg: '登录成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '邮箱不能为空'
        errNo: 10, msg: '密码不能为空'
        errNo: 10, msg: '错误的邮箱或密码'
    */
    public function adminLogin() {
            $data = input();
            if (isset($data['account']) && isset($data['password'])) {
                $account = $data['account'];
                $password = $data['password'];
                //基本检查
                if (strlen($account) == 0) {
                    return json(['errNo' => 10, 'msg' => '用户名不能为空']);
                }
                if (strlen($password) == 0) {
                    return json(['errNo' => 10, 'msg' => '密码不能为空']);
                }

                //安全性检查
                $admin = Admin::where('account', $account)->find();
                if (!isset($admin)) {
                    return json(['errNo' => 10, 'msg' => '错误的用户名或密码']);
                } else {
                    if (PwdHash::getHashCode($password, $admin->salt) != $admin->hash) {
                        return json(['errNo' => 10, 'msg' => '错误的用户名或密码']);
                    } else {
                        //登录成功
                        Session::pull('companyId');
                        Session::pull('companyUnitId');
                        Session::set('adminId', $admin->admin_id);
                        return json(['errNo' => 0, 'msg' => '登录成功']);
                    }
                }
            } else return json(['errNo' => 1, 'msg' => '参数错误']);

    }
    /*Interface: 登出
    Function: logout
    Url: admin/login/logout
    Type: post
    Input: {}
    Output: {errNo, msg}
        errNo: 0, msg: '登出成功'
    */
    public function logout() {
        if ($this->request->isAjax()) {
            Session::pull('userId');
            Session::pull('companyId');
            Session::pull('companyUnitId');
            Session::pull('adminId');
            return json(['errNo' => 0, 'msg' => '登出成功']);
        } else return $this->error('页面错误');
    }

    /*Interface: 管理员注册
    Function: adminRegister
    Url: admin/login/adminRegister
    Type: post
    Input: {account, password, rePassword}
    Output: {errNo, msg}
         errNo: 0, msg: '注册成功'
        errNo: 1, msg:  '参数错误'
        errNo: 10, msg: '账号已被注册'
        errNo: 10, msg: '密码不能为空'
        errNo: 10, msg: '两次输入密码不一致'
        errNo: 10, msg: '没有操作权限'
    */
    public function adminRegister() {
            $data = input();
            if (isset($data['account']) && isset($data['password']) && isset($data['rePassword'])) {
                $account = $data['account'];
                $password = $data['password'];
                $rePassword = $data['rePassword'];

                //检查访问ip
                $request = \request();
                $ip_address=$request->ip();
                if($ip_address != '127.0.0.1' && $ip_address != '123.206.34.20' &&$ip_address != '172.21.16.17')
                    return json(['errNo' => 10, 'msg' => '没有操作权限']);

                //邮箱检查
                if (strlen($account) == 0) {
                    return json(['errNo' => 10, 'msg' => '邮箱不能为空']);
                }

                $admin = Admin::where('account', $account)->find();
                if (isset($admin)) {
                    return json(['errNo' => 10, 'msg' => '邮箱已被注册']);
                }

                //密码检查
                if (strlen($password) == 0) {
                    return json(['errNo' => 10, 'msg' => '密码不能为空']);
                }
                if ($password != $rePassword) {
                    return json(['errNo' => 10, 'msg' => '两次输入密码不一致']);
                }

                //保存会员信息
                $admin = new Admin();
                $admin->account = $account;
                $admin->salt = PwdHash::getSalt($password); //创建随机盐
                $admin->hash = PwdHash::getHashCode($password, $admin->salt); //存入哈希结果
                $admin->save();

                Session::set('adminId', $admin->admin_id);
                Session::pull('companyId');
                Session::pull('companyUnitId');

                return json(['errNo' => 0, 'msg' => '注册成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
    }

    public function register($account, $password) {
        $admin = new Admin();
        $admin->account = $account;
        $admin->salt = PwdHash::getSalt($password); //创建随机盐
        $admin->hash = PwdHash::getHashCode($password, $admin->salt); //存入哈希结果
        $admin->save();
        return '新建管理员成功';
    }
    /*Interface: 管理员修改密码
    Function: adminModifyPassword
    Url: admin/login/adminModifyPassword
    Type: post
    Input: {originalPassword, password, rePassword}
    Output: {errNo, msg}
        errNo: 0, msg: '修改密码成功'
        errNo: 1, msg: '参数错误'
        errNo: 2, msg: '未以管理员身份登录'
        errNo: 10, msg: '管理员不存在'
        errNo: 10, msg: '原密码错误'
        errNo: 10, msg: '新密码不能为空'
        errNo: 10, msg: '两次输入密码不一致'
    */
    function adminModifyPassword() {
        $data = input();
        if (isset($data['originalPassword']) && isset($data['password']) && isset($data['rePassword'])) {
            $originalPassword = $data['originalPassword'];
            $password = $data['password'];
            $rePassword = $data['rePassword'];
            if (Session::has('adminId')) {
                $adminId = Session::get('adminId');
                $admin = Admin::get($adminId);
                if (!isset($admin)) {
                    return json(['errNo' => 10, 'msg' => '管理员不存在']);
                }
                //基本检查
                if (strlen($password) == 0) {
                    return json(['errNo' => 10, 'msg' => '新密码不能为空']);
                }
                if ($password != $rePassword) {
                    return json(['errNo' => 10, 'msg' => '两次输入密码不一致']);
                }

                if (PwdHash::getHashCode($originalPassword, $admin->salt) != $admin->hash) {
                    return json(['errNo' => 10, 'msg' => '原密码错误']);
                } else {
                    $admin->salt = PwdHash::getSalt($password); //创建随机盐
                    $admin->hash = PwdHash::getHashCode($password, $admin->salt); //存入哈希结果
                    $admin->save();
                    return json(['errNo' => 0, 'msg' => '修改密码成功']);
                }
            } else return json(['errNo' => 2, 'msg' => '未以管理员身份登录']);
        } else return json(['errNo' => 1, 'msg' => '参数错误']);
    }

    /*Interface: deleteAdmin
   Function: deleteAdmin
   Url: admin/login/deleteAdmin
   Type: post
   Input: {password}
   Output: {errNo, msg}
       errNo: 0, msg: '成功销毁管理员账号'
       errNo: 1, msg: '参数错误'
       errNo: 2, msg: '未以管理员身份登录'

   */

    public function deleteAdmin()
    {
        $data = input();
        if(isset($data['password']))
        {
            if (Session::has('adminId'))
            {
                $adminId = Session::get('adminId');
                $admin = Admin::get($adminId);
                $password = $data['password'];
                if (PwdHash::getHashCode($password, $admin->salt) != $admin->hash)
                    return json(['errNo' => 10, 'msg' => '密码错误']);
                $admin->delete();
                $this->logout();
                return json(['errNo' => 0, 'msg' => '成功销毁管理员账号']);
            }else
                return json(['errNo' => 2, 'msg' => '未以管理员身份登录']);
        }
        else return json(['errNo' => 1, 'msg' => '参数错误']);
    }









}
