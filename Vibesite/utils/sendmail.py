import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.header import Header

SMTPpassword = 'Ph89gCGnW2bv5uCX'

username = 'admin@nvolatile.top'
replyto = 'yrsty@hotmail.com'

Nick_Name = 'NV Admin: Tosaka'

def sendmail(rcpttos, subject, html, nick_name = Nick_Name):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(subject).encode()
    msg['From'] = '%s <%s>' % (Header(Nick_Name).encode(), username)
    msg['To'] = ', '.join(rcpttos)
    msg['Reply-to'] = replyto
    msg['Message-id'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate()

    texthtml = MIMEText(html, _subtype='html', _charset='UTF-8')
    msg.attach(texthtml)

    # 发送邮件
    client = smtplib.SMTP()
    #python 2.7以上版本，若需要使用SSL，可以这样创建client
    #client = smtplib.SMTP_SSL()
    #SMTP普通端口为25或80
    client.connect('smtpdm.aliyun.com', 80)
    client.login(username, SMTPpassword)
    #发件人和认证地址必须一致
    #备注：若想取到DATA命令返回值,可参考smtplib的sendmaili封装方法:
    #      使用SMTP.mail/SMTP.rcpt/SMTP.data方法
    client.sendmail(username, rcpttos, msg.as_string())
    client.quit()

def main():
    sendmail(['739667463@qq.com'], '来自远坂的问候', '挺好的.jpg')

if __name__ == '__main__':
    main()