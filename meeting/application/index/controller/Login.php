<?php
namespace app\index\controller;

use think\Controller;
use think\facade\Session;
use app\common\AES;
use app\common\RSA;
use app\common\Mail;
use app\common\PwdHash;
use app\common\model\User;
use app\common\model\Company;
use app\common\model\CompanyUnit;

class Login extends Controller {
    public function index() {
        return $this->fetch();
    }

    public function signUp() {
        return $this->fetch();
    }

    /*Interface: 会员登录
    Function: userLogin
    Url: index/login/userLogin
    Type: post
    Input: {email, password}
    Output: {errNo, msg}
        errNo: 0, msg: '登录成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '邮箱不能为空'
        errNo: 10, msg: '密码不能为空'
        errNo: 10, msg: '错误的邮箱或密码'
    */
    public function userLogin() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['email']) && isset($data['password'])) {
                $email = $data['email'];
                $password = $data['password'];

                //基本检查
                if (strlen($email) == 0) {
                    return json(['errNo' => 10, 'msg' => '邮箱不能为空']);
                }
                if (strlen($password) == 0) {
                    return json(['errNo' => 10, 'msg' => '密码不能为空']);
                }

                //安全性检查
                $user = User::where('email', $email)->find();
                if (!isset($user)) {
                    return json(['errNo' => 10, 'msg' => '错误的邮箱或密码']);
                } else {
                    if (PwdHash::getHashCode($password, $user->salt) != $user->hash) {
                        return json(['errNo' => 10, 'msg' => '错误的邮箱或密码']);
                    } else {

                        //登录成功
                        Session::pull('companyId');
                        Session::pull('companyUnitId');
                        Session::set('userId', $user->user_id);
                        return json(['errNo' => 0, 'msg' => '登录成功']);

                    }
                }
                
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 单位(或单位个体账号)登录
    Function: companyLogin
    Url: index/login/companyLogin
    Type: post
    Input: {account, password}
    Output: {errNo, msg}
        errNo: 0, msg: '登录成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '不能重复登录'
        errNo: 10, msg: '帐号不能为空'
        errNo: 10, msg: '密码不能为空'
        errNo: 10, msg: '错误的帐号或密码'
    */
    public function companyLogin() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['account']) && isset($data['password'])) {
                $account = $data['account'];
                $password = $data['password'];

                //基本检查
                if (strlen($account) == 0) {
                    return json(['errNo' => 10, 'msg' => '帐号不能为空']);
                }
                if (strlen($password) == 0) {
                    return json(['errNo' => 10, 'msg' => '密码不能为空']);
                }

                //安全性检查
                $company = Company::where('account', $account)->find();
                $companyUnit = CompanyUnit::where('account', $account)->find();
                if (isset($company)) {
                    
                    //作为单位登录
                    if (PwdHash::getHashCode($password, $company->salt) != $company->hash) {
                        return json(['errNo' => 10, 'msg' => '错误的帐号或密码']);
                    } else {

                        //登录成功
                        Session::pull('userId');
                        Session::pull('companyUnitId');
                        Session::set('companyId', $company->company_id);
                        return json(['errNo' => 0, 'msg' => '登录成功']);

                    }

                } else {
                    if (isset($companyUnit)) {
                        
                        //作为单位个体账号登录
                        if (AES::decrypt($companyUnit->password) != $password) {
                            return json(['errNo' => 10, 'msg' => '错误的帐号或密码']);
                        } else {

                            //登录成功
                                Session::pull('userId');
                                Session::pull('companyId');
                                Session::set('companyUnitId', $companyUnit->company_unit_id);
                                return json(['errNo' => 0, 'msg' => '登录成功']);

                        }

                    } else {
                        return json(['errNo' => 10, 'msg' => '错误的帐号或密码']);
                    }
                }
                
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 登出
    Function: logout
    Url: index/login/logout
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

    /*Interface: 会员注册
    Function: userRegister
    Url: index/login/userRegister
    Type: post
    Input: {email, password, rePassword, name}
    Output: {errNo, msg}
        errNo: 0, msg: '注册成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '邮箱不能为空'
        errNo: 10, msg: '邮箱格式错误'
        errNo: 10, msg: '邮箱已被注册'
        errNo: 10, msg: '密码不能为空'
        errNo: 10, msg: '两次输入密码不一致'
        errNo: 10, msg: '姓名不能为空'
    */
    public function userRegister() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['email']) && isset($data['password']) && isset($data['rePassword']) && isset($data['name'])) {
                $email = $data['email'];
                $password = $data['password'];
                $rePassword = $data['rePassword'];
                $name = $data['name'];

                //邮箱检查
                if (strlen($email) == 0) {
                    return json(['errNo' => 10, 'msg' => '邮箱不能为空']);
                }
                if (filter_var($email, FILTER_VALIDATE_EMAIL) == false) {
                    return json(['errNo' => 10, 'msg' => '邮箱格式错误']);
                }
                $user = User::where('email', $email)->find();
                if (isset($user)) {
                    return json(['errNo' => 10, 'msg' => '邮箱已被注册']);
                }

                //密码检查
                if (strlen($password) == 0) {
                    return json(['errNo' => 10, 'msg' => '密码不能为空']);
                }
                if ($password != $rePassword) {
                    return json(['errNo' => 10, 'msg' => '两次输入密码不一致']);
                }

                //姓名检查
                if (strlen($name) == 0) {
                    return json(['errNo' => 10, 'msg' => '姓名不能为空']);
                }

                //保存会员信息
                $user = new User();
                $user->email = $email;
                $user->salt = PwdHash::getSalt($password); //创建随机盐
                $user->hash = PwdHash::getHashCode($password, $user->salt); //存入哈希结果
                $user->name = $name;
                $user->confirm = 0;
                $user->save();
                Mail::sendUserConfirmMail($user->user_id);
                Session::set('userId', $user->user_id);
                Session::pull('companyId');
                Session::pull('companyUnitId');

                return json(['errNo' => 0, 'msg' => '注册成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 单位注册
    Function: companyRegister
    Url: index/login/companyRegister
    Type: post
    Input: {account, password, rePassword, name}
    Output: {errNo, msg}
        errNo: 0, msg: '注册成功'
        errNo: 1, msg: '参数错误'
        errNo: 10, msg: '帐号不能为空'
        errNo: 10, msg: '帐号已被注册'
        errNo: 10, msg: '密码不能为空'
        errNo: 10, msg: '两次输入密码不一致'
        errNo: 10, msg: '单位名称不能为空'
    */
    public function companyRegister() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['account']) && isset($data['password']) && isset($data['rePassword']) && isset($data['name'])) {
                $account = $data['account'];
                $password = $data['password'];
                $rePassword = $data['rePassword'];
                $name = $data['name'];

                //帐号检查
                if (strlen($account) == 0) {
                    return json(['errNo' => 10, 'msg' => '帐号不能为空']);
                }
                $company = Company::where('account', $account)->find();
                $companyUnit = CompanyUnit::where('account', $account)->find();
                if (isset($company) || isset($companyUnit)) {
                    return json(['errNo' => 10, 'msg' => '帐号已被注册']);
                }

                //密码检查
                if (strlen($password) == 0) {
                    return json(['errNo' => 10, 'msg' => '密码不能为空']);
                }
                if ($password != $rePassword) {
                    return json(['errNo' => 10, 'msg' => '两次输入密码不一致']);
                }

                //单位名称检查
                if (strlen($name) == 0) {
                    return json(['errNo' => 10, 'msg' => '单位名称不能为空']);
                }

                //保存用户信息
                $company = new Company();
                $company->account = $account;
                $company->salt = PwdHash::getSalt($password); //创建随机盐
                $company->hash = PwdHash::getHashCode($password, $company->salt); //存入哈希结果
                $company->name = $name;
                $company->confirm = 2;
                $company->save();
                Session::set('companyId', $company->company_id);
                Session::pull('userId');
                Session::pull('companyUnitId');

                return json(['errNo' => 0, 'msg' => '注册成功']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 单位添加个人帐号
    Function: companyCreateUnit
    Url: index/login/companyCreateUnit
    Type: post
    Input: {account, password, rePassword, name}
    Output: {errNo, msg}
        errNo: 0, msg: '添加单位个人帐号成功'
        errNo: 1, msg: '参数错误'
        errNo: 2, msg: '未以单位身份登录'
        errNo: 10, msg: '单位不存在'
        errNo: 10, msg: '单位未通过审核'
        errNo: 10, msg: '帐号不能为空'
        errNo: 10, msg: '帐号已被使用'
        errNo: 10, msg: '密码不能为空'
        errNo: 10, msg: '两次输入密码不一致'
        errNo: 10, msg: '昵称不能为空'
    */
    public function companyCreateUnit() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['account']) && isset($data['password']) && isset($data['rePassword']) && isset($data['name'])) {
                $account = $data['account'];
                $password = $data['password'];
                $rePassword = $data['rePassword'];
                $name = $data['name'];

                if (Session::has('companyId')) {
                    $companyId = Session::get('companyId');
                    $company = Company::get($companyId);
                    if (!isset($company)) {
                        return json(['errNo' => 10, 'msg' => '单位不存在']);
                    }
                    if ($company->confirm != 1) {
                        return json(['errNo' => 10, 'msg' => '单位未通过审核']);
                    }

                    //帐号检查
                    if (strlen($account) == 0) {
                        return json(['errNo' => 10, 'msg' => '帐号不能为空']);
                    }
                    $company = Company::where('account', $account)->find();
                    $companyUnit = CompanyUnit::where('account', $account)->find();
                    if (isset($company) || isset($companyUnit)) {
                        return json(['errNo' => 10, 'msg' => '帐号已被使用']);
                    }

                    //密码检查
                    if (strlen($password) == 0) {
                        return json(['errNo' => 10, 'msg' => '密码不能为空']);
                    }
                    if ($password != $rePassword) {
                        return json(['errNo' => 10, 'msg' => '两次输入密码不一致']);
                    }

                    //昵称检查
                    if (strlen($name) == 0) {
                        return json(['errNo' => 10, 'msg' => '昵称不能为空']);
                    }

                    //保存用户信息
                    $companyUnit = new CompanyUnit();
                    $companyUnit->account = $account;
                    $companyUnit->password = AES::encrypt($password);
                    $companyUnit->name = $name;
                    $companyUnit->company_id = $companyId;
                    $companyUnit->save();
                    
                    return json(['errNo' => 0, 'msg' => '添加单位个人帐号成功']);
                } else return json(['errNo' => 2, 'msg' => '未以单位身份登录']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 单位删除个人账号
    Function: companyDeleteUnit
    Url: index/login/companyDeleteUnit
    Type: post
    Input: {companyUnitId}
    Output: {errNo, msg}
        errNo: 0, msg: '删除单位个人帐号成功'
        errNo: 1, msg: '参数错误'
        errNo: 2, msg: '未以单位身份登录'
        errNo: 10, msg: '单位不存在'
        errNo: 10, msg: '单位未通过审核'
        errNo: 10, msg: '对应单位个人帐号不存在'
    */
    public function companyDeleteUnit() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['companyUnitId'])) {
                $companyUnitId = AES::decrypt($data['companyUnitId']);
                if (Session::has('companyId')) {
                    $companyId = Session::get('companyId');
                    $company = Company::get($companyId);
                    if (!isset($company)) {
                        return json(['errNo' => 10, 'msg' => '单位不存在']);
                    }
                    if ($company->confirm != 1) {
                        return json(['errNo' => 10, 'msg' => '单位未通过审核']);
                    }
                    $companyUnit = CompanyUnit::get($companyUnitId);
                    if (!isset($companyUnitId)) {
                        return json(['errNo' => 10, 'msg' => '对应单位个人帐号不存在']);
                    }
                    $companyUnit->delete();
                    return json(['errNo' => 0, 'msg' => '删除单位个人帐号成功']);
                } else return json(['errNo' => 2, 'msg' => '未以单位身份登录']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 会员修改密码
    Function: userModifyPassword
    Url: index/login/userModifyPassword
    Type: post
    Input: {originalPassword, password, rePassword}
    Output: {errNo, msg}
        errNo: 0, msg: '修改密码成功'
        errNo: 1, msg: '参数错误'
        errNo: 2, msg: '未以会员身份登录'
        errNo: 10, msg: '会员不存在'
        errNo: 10, msg: '会员未验证邮箱'
        errNo: 10, msg: '原密码错误'
        errNo: 10, msg: '新密码不能为空'
        errNo: 10, msg: '两次输入密码不一致'
    */
    function userModifyPassword() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['originalPassword']) && isset($data['password']) && isset($data['rePassword'])) {
                $originalPassword = $data['originalPassword'];
                $password = $data['password'];
                $rePassword = $data['rePassword'];
                if (Session::has('userId')) {
                    $userId = Session::get('userId');
                    $user = User::get($userId);
                    if (!isset($user)) {
                        return json(['errNo' => 10, 'msg' => '会员不存在']);
                    }
                    if (!$user->confirm) {
                        return json(['errNo' => 10, 'msg' => '会员未验证邮箱']);
                    }

                    //基本检查
                    if (strlen($password) == 0) {
                        return json(['errNo' => 10, 'msg' => '新密码不能为空']);
                    }
                    if ($password != $rePassword) {
                        return json(['errNo' => 10, 'msg' => '两次输入密码不一致']);
                    }

                    if (PwdHash::getHashCode($originalPassword, $user->salt) != $user->hash) {
                        return json(['errNo' => 10, 'msg' => '原密码错误']);
                    } else {
                        $user->salt = PwdHash::getSalt($password); //创建随机盐
                        $user->hash = PwdHash::getHashCode($password, $user->salt); //存入哈希结果
                        $user->save();
                        return json(['errNo' => 0, 'msg' => '修改密码成功']);
                    }
                } else return json(['errNo' => 2, 'msg' => '未会员身份登录']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    /*Interface: 单位修改密码
    Function: companyModifyPassword
    Url: index/login/companyModifyPassword
    Type: post
    Input: {originalPassword, password, rePassword}
    Output: {errNo, msg}
        errNo: 0, msg: '修改密码成功'
        errNo: 1, msg: '参数错误'
        errNo: 2, msg: '未以单位身份登录'
        errNo: 10, msg: '单位不存在'
        errNo: 10, msg: '单位未通过审核'
        errNo: 10, msg: '原密码错误'
        errNo: 10, msg: '新密码不能为空'
        errNo: 10, msg: '两次输入密码不一致'
    */
    function companyModifyPassword() {
        if ($this->request->isAjax()) {
            $data = input();
            if (isset($data['originalPassword']) && isset($data['password']) && isset($data['rePassword'])) {
                $originalPassword = $data['originalPassword'];
                $password = $data['password'];
                $rePassword = $data['rePassword'];
                if (Session::has('companyId')) {
                    $companyId = Session::get('companyId');
                    $company = Company::get($companyId);
                    if (!isset($company)) {
                        return json(['errNo' => 10, 'msg' => '单位不存在']);
                    }
                    if ($company->confirm != 1) {
                        return json(['errNo' => 10, 'msg' => '单位未通过审核']);
                    }

                    //基本检查
                    if (strlen($password) == 0) {
                        return json(['errNo' => 10, 'msg' => '新密码不能为空']);
                    }
                    if ($password != $rePassword) {
                        return json(['errNo' => 10, 'msg' => '两次输入密码不一致']);
                    }

                    if (PwdHash::getHashCode($originalPassword, $company->salt) != $company->hash) {
                        return json(['errNo' => 10, 'msg' => '原密码错误']);
                    } else {
                        $company->salt = PwdHash::getSalt($password); //创建随机盐
                        $company->hash = PwdHash::getHashCode($password, $company->salt); //存入哈希结果
                        $company->save();
                        return json(['errNo' => 0, 'msg' => '修改密码成功']);
                    }
                } else return json(['errNo' => 2, 'msg' => '未以单位身份登录']);
            } else return json(['errNo' => 1, 'msg' => '参数错误']);
        } else return $this->error('页面错误');
    }

    function userConfirm($p) {
        $data = AES::decrypt($p);
        $data = json_decode($data, true);
        $userId = $data['userId'];
        $user = User::get($userId);
        $sendTime = $data['sendTime'];
        $deltaTime = strtotime(date('Y-m-d H:i:s', time())) - strtotime($sendTime);
        if (!isset($user) || $user->confirm || $deltaTime > 60 * 60) {
            return "认证链接失效.";
        } else {
            $user->confirm = 1;
            $user->save();
            return "认证邮箱成功.";
        }
    } 
}