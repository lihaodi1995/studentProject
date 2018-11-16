package com.example.demo.exception;

import java.io.Serializable;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/6/30 15:58
 **/
public class ErrorUnit implements Serializable{
    private int errorCode;

    private String errorInfo;

    private ErrorUnit(int errorCode, String errorInfo) {
        this.errorCode = errorCode;
        this.errorInfo = errorInfo;
    }

    public static ErrorUnit info(int errorCode, String errorInfo)
    {
        return new ErrorUnit(errorCode,errorInfo);
    }

    public int getErrorCode() {
        return errorCode;
    }

    public void setErrorCode(int errorCode) {
        this.errorCode = errorCode;
    }

    public String getErrorInfo() {
        return errorInfo;
    }

    public void setErrorInfo(String errorInfo) {
        this.errorInfo = errorInfo;
    }
}
