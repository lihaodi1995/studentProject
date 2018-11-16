package com.example.demo.exception;

import com.example.demo.utils.JsonUtil;
import com.sun.mail.smtp.SMTPAddressFailedException;
import org.apache.log4j.Logger;
import org.apache.shiro.authc.IncorrectCredentialsException;
import org.apache.shiro.authz.AuthorizationException;
import org.apache.shiro.authz.UnauthenticatedException;
import org.springframework.mail.MailAuthenticationException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import javax.mail.SendFailedException;
import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletResponse;
import javax.validation.constraints.NotNull;
import java.io.IOException;
import java.util.HashMap;

import static com.example.demo.exception.ExceptionInfo.*;

/**
 * @Author : 叶明林
 * @Description: 全局异常处理
 * @Date created at 2018/5/16 15:13
 **/
@ControllerAdvice
public class GlobalExceptionHandler {
    private Logger logger = Logger.getLogger(GlobalExceptionHandler.class);
    @ExceptionHandler(BusinessException.class)
    public void businessExceptionHandler(BusinessException e,HttpServletResponse response) throws IOException {
        ErrorUnit info = e.getInfo();
        this.logger.info(info.getErrorInfo());
        e.printStackTrace();
        addExceptionInfoToContent(info,response);
    }

    @ExceptionHandler(UnauthenticatedException.class)
    public void unauthenticatedExceptionHandler(UnauthenticatedException e,HttpServletResponse response) throws IOException {
        this.logger.info(e.getMessage());
        addExceptionInfoToContent(USER_PERMISSION_NEEDED,response);
    }

    @ExceptionHandler(AuthorizationException.class)
    public void authorizationExceptionHandler(AuthorizationException e,HttpServletResponse response) throws IOException {
        this.logger.info(e.getMessage());
        addExceptionInfoToContent(PERMISSION_DENIED,response);
    }

    @ExceptionHandler(IncorrectCredentialsException.class)
    public void incorrectCredentialsExceptionHandler(IncorrectCredentialsException e,HttpServletResponse response) throws IOException {
        this.logger.info(e.getMessage());
        addExceptionInfoToContent(PWD_NOT_MATHCHED,response);
    }

    @ExceptionHandler(MailAuthenticationException.class)
    public void mailAuthenticationExceptionHandler(MailAuthenticationException e,HttpServletResponse response) throws IOException {
        this.logger.info(e.getMessage());
        addExceptionInfoToContent(EMAIL_AUTHORIZE_ERROR,response);
    }

    @ExceptionHandler(SMTPAddressFailedException.class)
    public void sMTPAddressFailedExceptionHandler(SMTPAddressFailedException e,HttpServletResponse response) throws IOException {
        this.logger.info(e.getMessage());
        addExceptionInfoToContent(EMAIL_ADDRESS_NOT_EXIST,response);
    }

    @ExceptionHandler(SendFailedException.class)
    public void sendFailedExceptionHandler(SendFailedException e,HttpServletResponse response) throws IOException {
        this.logger.info(e.getMessage());
        addExceptionInfoToContent(EMAIL_ADDRESS_NOT_EXIST,response);
    }

    private void addExceptionInfoToContent(@NotNull ErrorUnit errorUnit, HttpServletResponse response)throws IOException
    {
        HashMap<String,Object> tmp = new HashMap<>();
        tmp.put("errorCode",errorUnit.getErrorCode());
        tmp.put("errorInfo",errorUnit.getErrorInfo());
        String json= JsonUtil.convertObjectToJSON(tmp);
        ServletOutputStream out = response.getOutputStream();
        out.write(json.getBytes());
        out.flush();
    }
}
