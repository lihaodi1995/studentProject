package com.example.demo.exception;

/**
 * @Author : 叶明林
 * @Description: 运行时异常类，用于记录报错信息
 * @Date created at 2018/5/16 15:45
 **/
public class BusinessException extends RuntimeException{

    private ErrorUnit info;

    public BusinessException(ErrorUnit info)
    {
        this.info = info;
    }

    public ErrorUnit getInfo()
    {
        return this.info;
    }
}
