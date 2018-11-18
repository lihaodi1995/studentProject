<?php
// +----------------------------------------------------------------------
// | ThinkPHP [ WE CAN DO IT JUST THINK ]
// +----------------------------------------------------------------------
// | Copyright (c) 2006-2016 http://thinkphp.cn All rights reserved.
// +----------------------------------------------------------------------
// | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
// +----------------------------------------------------------------------
// | Author: 流年 <liu21st@gmail.com>
// +----------------------------------------------------------------------

// 应用公共文件

function sendMail() {
    $mail = new \PHPMailer();
    $mail->isSMTP();// 使用SMTP服务
    $mail->CharSet = 'utf8';// 编码格式为utf8，不设置编码的话，中文会出现乱码
    $mail->Host = 'smtp.163.com';// 发送方的SMTP服务器地址
    $mail->SMTPAuth = true;// 是否使用身份验证
    $mail->Username = 'li609754893@163.com';// 发送方的163邮箱用户名
    $mail->Password = 'li609754893';// 发送方的邮箱密码，注意用163邮箱这里填写的是“客户端授权密码”而不是邮箱的登录密码！
    $mail->SMTPSecure = 'ssl';// 使用ssl协议方式
    $mail->Port = 994;// 163邮箱的ssl协议方式端口号是465/994
    $mail->From = 'li609754893@163.com';
    $mail->setFrom('li609754893@163.com','Li');// 设置发件人信息，如邮件格式说明中的发件人，这里会显示为Mailer(xxxx@163.com），Mailer是当做名字显示
    $mail->addAddress('609754893@qq.com', 'Li');// 设置收件人信息，如邮件格式说明中的收件人，这里会显示为Liang(yyyy@163.com)
    $mail->IsHTML(true);
    $mail->Subject = 'hello';// 邮件标题
    $mail->Body = 'hello';// 邮件正文
    if (!$mail->send()) {// 发送邮件
        return json(['errNo' => 1, 'msg' => $mail->ErrorInfo]);// 输出错误信息
    } else {
        return json(['errNo' => 0, 'msg' => 'success']);
    }
}
