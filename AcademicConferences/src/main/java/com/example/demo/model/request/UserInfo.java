package com.example.demo.model.request;

import io.swagger.annotations.ApiModelProperty;

import java.io.Serializable;

/**
 * @Author : 叶明林
 * @Description:
 * @Date created at 2018/7/2 10:11
 **/
public class UserInfo implements Serializable{
    @ApiModelProperty(value = "用户名")
    private String userName;

    @ApiModelProperty(value = "密码")
    private String password;

    @ApiModelProperty(value = "姓名")
    private String name;

    @ApiModelProperty(value = "身份证号")
    private String realId;

    @ApiModelProperty(value = "性别")
    private String sex;

    @ApiModelProperty(value = "所属单位")
    private String institution;

    @ApiModelProperty(value = "邮箱")
    private String email;

    public String getUserName() {
        return userName;
    }

    public void setUserName(String userName) {
        this.userName = userName;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getRealId() {
        return realId;
    }

    public void setRealId(String realId) {
        this.realId = realId;
    }

    public String getSex() {
        return sex;
    }

    public void setSex(String sex) {
        this.sex = sex;
    }

    public String getInstitution() {
        return institution;
    }

    public void setInstitution(String institution) {
        this.institution = institution;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
