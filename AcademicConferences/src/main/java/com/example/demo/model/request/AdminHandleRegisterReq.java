package com.example.demo.model.request;

import java.io.Serializable;

/**
 * @Author : 叶明林
 * @Description: 管理员处理机构注册传递参数
 * @Date created at 2018/7/4 9:58
 **/
public class AdminHandleRegisterReq implements Serializable{
    private boolean organizationStatus;
    private String result;

    public boolean isOrganizationStatus() {
        return organizationStatus;
    }

    public void setOrganizationStatus(boolean organizationStatus) {
        this.organizationStatus = organizationStatus;
    }

    public String getResult() {
        return result;
    }

    public void setResult(String result) {
        this.result = result;
    }
}
