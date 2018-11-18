<?php
namespace app\common\controller; 

use app\common\model\Manuscript;
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP; 
use PHPMailer\PHPMailer\Exception; 

use app\common\AES; 
use app\common\model\User; 

class Mail {
    /*
        recevierAddress: 接受者邮件地址
        receiverName: 接受者称呼
        mailSubject: 邮件主题
        mailBody: 邮件内容
        isHtml: 是否采用HTML编码
    */
    public function sendMail($recevierAddress, $receiverName, $mailSubject, $mailBody, $isHtml = 1) {
        $mail = new PHPMailer(); 
        try {
            $mail->isSMTP(); // 使用SMTP服务
            $mail->CharSet = 'utf8'; // 编码格式为utf8，不设置编码的话，中文会出现乱码
            $mail->Host = 'smtp.163.com'; // 发送方的SMTP服务器地址
            $mail->SMTPAuth = true; // 是否使用身份验证
            $mail->Username = 'li609754893@163.com'; // 发送方的163邮箱用户名
            $mail->Password = 'li609754893'; // 发送方的邮箱密码，注意用163邮箱这里填写的是“客户端授权密码”而不是邮箱的登录密码！
            $mail->SMTPSecure = 'ssl'; // 使用ssl协议方式
            $mail->Port = 994; // 163邮箱的ssl协议方式端口号是465/994
            $mail->From = 'li609754893@163.com'; 
            $mail->setFrom('li609754893@163.com', '在线学术会议管理平台(Powered by 善良之队)'); // 设置发件人信息，如邮件格式说明中的发件人，这里会显示为Mailer(xxxx@163.com），Mailer是当做名字显示
            $mail->addAddress($recevierAddress, '在线学术会议管理平台用户:' . $receiverName); // 设置收件人信息，如邮件格式说明中的收件人，这里会显示为Liang(yyyy@163.com)
            $mail->IsHTML($isHtml); 
            $mail->Subject = $mailSubject; // 邮件标题
            $mail->Body = $mailBody; // 邮件正文
            $mail->send(); 
            return json(['errNo' => 0, 'msg' => 'Maile has been sent.']); 
        } catch (Exception $e) {
            return json(['errNo' => 1, 'msg' => $mail->ErrorInfo]); 
        }
    }

    public function sendUserConfirmMail($userId) {
        $user = User::get($userId); 
        if (!isset($user) || $user->confirm) return; 
        $email = $user->email;
        $name = $user->name; 
        $domain = $_SERVER['HTTP_HOST']; 
        $confirmStr = json_encode(array('userId' => $userId, 'sendTime' => date('Y-m-d H:i:s', time()))); 
        $confirmStr = AES::encrypt($confirmStr); 
        $strUrl = 'http://' . $domain . url('index/login/userConfirm', ['p' => $confirmStr]); 
        $subject = '请认证您的邮箱'; 
        $body = 
<<<Eof
<table style="-webkit-font-smoothing: antialiased; font-family:&#39; 微软雅黑&#39; padding:35px 50px; margin: 25px auto; background:rgb(247,246, 242); border-radius:5px" border="0" cellspacing="0" cellpadding="0" width="640" align="center">
    <tbody>
    <tr>
        <td style="padding: 20px 20px 20x 20px;">
            尊敬的 $name ,
        </td>
    </tr>
    <tr>
        <td style="padding: 20px 20px 20x 20px;">
            在线学术会议管理平台提醒您, 请点击以下链接认证您的邮箱:
        </td>
    </tr>
    <tr>
        <td style="height: 50px; color: white;" valign="middle">
            <div style="padding:10px 10px; border-radius:5px; background: black;">
                <a style="word-break:break-all; line-height:23px; color:white; font-size:15px; text-decoration:none;" href="$strUrl">
                    $strUrl
                </a>
            </div>
        </td>
    </tr>
    <tr>
        <td style="padding: 20px 20px 20x 20px;">
            <p style="margin: 8px 0;">请勿回复此邮件, 如果有疑问, 请联系我们: <a style="color:#5083c0; text-decoration:none" href="mailto:li609754893@163.com">li609754893@163.com</a>
            </p>
        </td>
    </tr>
    <tr>
        <td style="padding: 20px 20px 20x 20px;" align="right">
            - 在线学术会议管理平台(Powered by 善良之队)
        </td>
    </tr>
    <tr>
        <td>
            <hr style="border:none; border-top:1px solid #ccc;" />
        </td>
    </tr>
    <tr>
        <td style="font-size:9pt; color:#b5b0b0">
            <span style="float:left;">如果你没有注册过在线学术会议管理平台，请忽略此邮件。</span>
        </td>
    </tr>
    </tbody>
</table>
Eof;
        $this->sendMail($email, $name, $subject, $body); 
    }

    public function sendReviewResultMail($userId,$reviewData,$manuscriptTitle,$meetingName) {
        $user = User::get($userId);
        $email = $user->email;
        $name = $user->name;
        $domain = $_SERVER['HTTP_HOST'];
        $subject ='稿件审核结果';
        if($reviewData['result'] == 1) $result = '通过';
        else if($reviewData['result'] == 2) $result = '须修改';
        else if($reviewData['result'] == 0) $result = '未通过';
        $suggestion = $reviewData['suggestion'];
        $body =
            <<<Eof
<table style="-webkit-font-smoothing: antialiased; font-family:&#39; 微软雅黑&#39; padding:35px 50px; margin: 25px auto; background:rgb(247,246, 242); border-radius:5px" border="0" cellspacing="0" cellpadding="0" width="640" align="center">
    <tbody>
    <tr>
        <td style="padding: 20px 20px 20x 20px;">
            尊敬的 $name ,
        </td>
    </tr>
    <tr>
        <td style="padding: 20px 20px 20x 20px;">
            在线学术会议管理平台提醒您, 您在会议：$meetingName 投递的稿件: $manuscriptTitle 审核结果为：$result 
        </td>
    </tr>
    <tr>
        <td style="height: 50px; " valign="middle">
            会议主办方对该稿件的建议是：$suggestion
        </td>
    </tr>
    <tr>
        <td style="padding: 20px 20px 20x 20px;">
            <p style="margin: 8px 0;">请勿回复此邮件, 如果有疑问, 请联系我们: <a style="color:#5083c0; text-decoration:none" href="mailto:li609754893@163.com">li609754893@163.com</a>
            </p>
        </td>
    </tr>
    <tr>
        <td style="padding: 20px 20px 20x 20px;" align="right">
            - 在线学术会议管理平台(Powered by 善良之队)
        </td>
    </tr>
    <tr>
        <td>
            <hr style="border:none; border-top:1px solid #ccc;" />
        </td>
    </tr>
    <tr>
        <td style="font-size:9pt; color:#b5b0b0">
            <span style="float:left;">如果你没有注册过在线学术会议管理平台，请忽略此邮件。</span>
        </td>
    </tr>
    </tbody>
</table>
Eof;
        $this->sendMail($email, $name, $subject, $body);

    }

    public function sendInformMail($userId,$meetingName,$meetingId,$status) {
        $user = User::get($userId);
        $email = $user->email;
        $name = $user->name;
        $message = array(
            '0'=> '投稿',
            '1'=> '修改稿',
            '4'=> '注册',
        );
        $domain = $_SERVER['HTTP_HOST'];
        $confirmStr = AES::encrypt($meetingId);
        $strUrl = 'http://' . $domain . '/meeting/index/index?meetingId='.$confirmStr;
        $subject = $message[$status].'结束提醒';

        $body =
            <<<Eof
<table style="-webkit-font-smoothing: antialiased; font-family:&#39; 微软雅黑&#39; padding:35px 50px; margin: 25px auto; background:rgb(247,246, 242); border-radius:5px" border="0" cellspacing="0" cellpadding="0" width="640" align="center">
    <tbody>
    <tr>
        <td style="padding: 20px 20px 20x 20px;">
            尊敬的 $name ,
        </td>
    </tr>
    <tr>
        <td style="padding: 20px 20px 20x 20px;">
            在线学术会议管理平台提醒您, 您关注的会议  $meetingName $message[$status]即将截止
        </td>
    </tr>
    <tr>
        <td style="height: 50px; color: white;" valign="middle">
            <div style="padding:10px 10px; border-radius:5px; background: black;">
                <a style="word-break:break-all; line-height:23px; color:white; font-size:15px; text-decoration:none;" href="$strUrl">
                    $strUrl
                </a>
            </div>
        </td>
    </tr>
    <tr>
        <td style="padding: 20px 20px 20x 20px;">
            <p style="margin: 8px 0;">请勿回复此邮件, 如果有疑问, 请联系我们: <a style="color:#5083c0; text-decoration:none" href="mailto:li609754893@163.com">li609754893@163.com</a>
            </p>
        </td>
    </tr>
    <tr>
        <td style="padding: 20px 20px 20x 20px;" align="right">
            - 在线学术会议管理平台(Powered by 善良之队)
        </td>
    </tr>
    <tr>
        <td>
            <hr style="border:none; border-top:1px solid #ccc;" />
        </td>
    </tr>
    <tr>
        <td style="font-size:9pt; color:#b5b0b0">
            <span style="float:left;">如果你没有注册过在线学术会议管理平台，请忽略此邮件。</span>
        </td>
    </tr>
    </tbody>
</table>
Eof;
        $this->sendMail($email, $name, $subject, $body);

    }

    public function sendAcceptInformMail($author,$title,$meetingTitle) {
        $name = $author['name'];
        $email = $author['email'];
        $domain = $_SERVER['HTTP_HOST'];
        $title = $title;
        $meetingTitle = $meetingTitle;
        $subject = "论文收录通知";
        $body =
            <<<Eof
<table style="-webkit-font-smoothing: antialiased; font-family:&#39; 微软雅黑&#39; padding:35px 50px; margin: 25px auto; background:rgb(247,246, 242); border-radius:5px" border="0" cellspacing="0" cellpadding="0" width="640" align="center">
    <tbody>
    <tr>
        <td style="padding: 20px 20px 20x 20px;">
            尊敬的 $name ,
        </td>
    </tr>
    <tr>
        <td style="padding: 20px 20px 20x 20px;">
            在线学术会议管理平台提醒您, 您参与创作的论文: $title 已经被会议: $meetingTitle 收录。
        </td>
    </tr>
    <tr>
        <td style="height: 50px; color: white;" valign="middle">
           
        </td>
    </tr>
    <tr>
        <td style="padding: 20px 20px 20x 20px;">
            <p style="margin: 8px 0;">请勿回复此邮件, 如果有疑问, 请联系我们: <a style="color:#5083c0; text-decoration:none" href="mailto:li609754893@163.com">li609754893@163.com</a>
            </p>
        </td>
    </tr>
    <tr>
        <td style="padding: 20px 20px 20x 20px;" align="right">
            - 在线学术会议管理平台(Powered by 善良之队)
        </td>
    </tr>
    <tr>
        <td>
            <hr style="border:none; border-top:1px solid #ccc;" />
        </td>
    </tr>
    <tr>
        <td style="font-size:9pt; color:#b5b0b0">
            <span style="float:left;">如果你没有注册过在线学术会议管理平台，请忽略此邮件。</span>
        </td>
    </tr>
    </tbody>
</table>
Eof;
        $this->sendMail($email, $name, $subject, $body);

    }





}