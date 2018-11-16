package com.example.demo.model.request;

import io.swagger.annotations.ApiModelProperty;

import java.io.Serializable;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/7/5 10:18
 **/
public class UserRegisterInfo implements Serializable{
    @ApiModelProperty(value = "邮箱")
    private String email;

    @ApiModelProperty(value = "密码")
    private String password;

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
