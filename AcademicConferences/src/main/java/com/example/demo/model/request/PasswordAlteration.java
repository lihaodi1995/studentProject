package com.example.demo.model.request;

/**
 * @Author : 叶明林
 * @Description: 密码更改
 * @Date created at 2018/6/9 12:33
 **/
public class PasswordAlteration {
    private String originalPassword;

    private String newPassword;

    public String getOriginalPassword() {
        return originalPassword;
    }

    public void setOriginalPassword(String originalPassword) {
        this.originalPassword = originalPassword;
    }

    public String getNewPassword() {
        return newPassword;
    }

    public void setNewPassword(String newPassword) {
        this.newPassword = newPassword;
    }
}
