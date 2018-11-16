package com.example.demo.model.request;

import io.swagger.annotations.ApiModelProperty;

import javax.persistence.Column;
import java.io.Serializable;

/**
 * @Author : 叶明林
 * @Description: 单位用户注册表单
 * @Date created at 2018/6/30 19:35
 **/
public class OrganizationRegisterForm implements Serializable{
    @ApiModelProperty(value = "机构名称")
    private String organizationName;

    @ApiModelProperty(value = "统一社会信用代码")
    private String creditCode;

    @ApiModelProperty(value = "其他信息")
    @Column(columnDefinition = "text")
    private String legalInfo;

    @ApiModelProperty(value = "联系邮箱")
    private String mail;

    @ApiModelProperty(value = "注册附件")
    private String file;

    public OrganizationRegisterForm() {
    }

    public String getOrganizationName() {
        return organizationName;
    }

    public void setOrganizationName(String organizationName) {
        this.organizationName = organizationName;
    }

    public String getCreditCode() {
        return creditCode;
    }

    public void setCreditCode(String creditCode) {
        this.creditCode = creditCode;
    }

    public String getLegalInfo() {
        return legalInfo;
    }

    public void setLegalInfo(String legalInfo) {
        this.legalInfo = legalInfo;
    }

    public String getMail() {
        return mail;
    }

    public void setMail(String mail) {
        this.mail = mail;
    }

    public String getFile() {
        return file;
    }

    public void setFile(String file) {
        this.file = file;
    }
}
