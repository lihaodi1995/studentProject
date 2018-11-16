package com.example.demo.component;

import com.sun.mail.util.MailConnectException;
import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.MailSendException;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Component;

import javax.mail.MessagingException;
import javax.mail.internet.MimeMessage;
import java.util.Collection;
import java.util.Map;
import java.util.concurrent.Future;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * @Author : 叶明林
 * @Description: 邮件相关
 * @Date created at 2018/7/2 8:58
 **/
@Component
public class EmailsUtil {
    private Logger logger = Logger.getLogger(EmailsUtil.class);

    final private JavaMailSender emailSender;

    public static final String SUCCESS = "发送邮件成功";

    @Value("${spring.mail.username}")
    private String emailServiceHost ;

    @Autowired
    public EmailsUtil(JavaMailSender emailSender) {
        this.emailSender = emailSender;
    }

    /**
     * 发送邮件
     * @param msg 邮件实体
     */
    @Async("asyncServiceExecutor")
    public Future<String> sendEmail(MimeMessage msg){
        this.logger.info("sending email");
        try
        {
            this.emailSender.send(msg);
            return new AsyncResult<>(SUCCESS);
        }
        catch (MailSendException e)
        {
            logger.info("发送邮件失败");
            e.printStackTrace();
            Map<Object,Exception> exceptionMap = e.getFailedMessages();
            Collection<Exception> exceptions = exceptionMap.values();
            for (Exception x: exceptions)
                if(x instanceof MailConnectException)
                {
                    logger.info("正在准备重新投递");
                    SendingEmailJob.addMessage(msg);
                    break;
                }
            throw e;
        }
    }

    /**
     * 生成邮件信息
     * @param to 目的邮箱地址
     * @param subject 主题
     * @param content 内容
     * @return 邮件实体
     */
    public MimeMessage generateMessage(String to,String subject,String content)
    {
        final MimeMessage mimeMessage = this.emailSender.createMimeMessage();
        final MimeMessageHelper message = new MimeMessageHelper(mimeMessage);
        try
        {
            message.setFrom(this.emailServiceHost);
            message.setTo(to);
            message.setSubject(subject);
            message.setText(content);
        }
        catch (MessagingException e) {
            e.printStackTrace();
        }
        return mimeMessage;
    }

    /**
     * 判断邮箱是否合法
     * @param string 邮箱地址
     * @return 是否合法
     */
    public static boolean isEmail(String string) {
        if (string == null ||string.isEmpty())
            return false;
        String regEx1 = "^([a-z0-9A-Z]+[-|.]?)+[a-z0-9A-Z]@([a-z0-9A-Z]+(-[a-z0-9A-Z]+)?\\.)+[a-zA-Z]{2,}$";
        Pattern p;
        Matcher m;
        p = Pattern.compile(regEx1);
        m = p.matcher(string);
        return m.matches();
    }
}
