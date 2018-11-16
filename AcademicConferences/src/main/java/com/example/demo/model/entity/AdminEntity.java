package com.example.demo.model.entity;

import com.example.demo.model.base.Identification;
import com.example.demo.model.base.Role;
import com.example.demo.security.PasswordEncryption;
import com.fasterxml.jackson.annotation.JsonIgnore;
import io.swagger.annotations.ApiModelProperty;

import javax.persistence.*;
import java.io.Serializable;
import java.util.Objects;

@Entity
public class AdminEntity implements Identification,Serializable {
    @Id
    @GeneratedValue
    @ApiModelProperty(value = "管理员Id")
    private Long id;

    @Column(unique = true,columnDefinition = "nvarchar(50)")
    @ApiModelProperty(value = "用户名")
    private String userName;

    @ApiModelProperty(value = "密码")
    @JsonIgnore
    private String password;

    @ApiModelProperty(value = "盐，用于加密")
    @JsonIgnore
    private String salt;

    @ApiModelProperty(value = "所属组织机构")
    @ManyToOne
    private OrganizationEntity organization;

    @ApiModelProperty(value = "是否为root管理员")
    private boolean isRoot=false;

    @Column(columnDefinition = "char(10)")
    @ApiModelProperty(value = "系统角色")
    private String role= Role.ROLE_ORGANIZER;

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public Boolean getRoot() {
        return isRoot;
    }

    public void setRoot(Boolean root) {
        isRoot = root;
    }

    public void setId(Long id) {
        this.id = id;
    }

    @Override
    public Long getId() {
        return id;
    }

    public void setPassword(String password) {
        this.salt = PasswordEncryption.generateSalt();
        this.password = PasswordEncryption.encryptPassword(password,this.salt);
    }

    public String getUserName() {
        return this.userName;
    }

    public String getPassword() {
        return password;
    }

    public void setUserName(String username) {
        this.userName = username;
    }

    public String getSalt() {
        return salt;
    }

    public void setSalt(String salt) {
        this.salt = salt;
    }

    public void setOrganization(OrganizationEntity organization) {
        this.organization = organization;
    }

    public OrganizationEntity getOrganization() {
        return organization;
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof AdminEntity && this.userName.equals(((AdminEntity) obj).userName);
    }

    @Override
    public int hashCode() {
        return Objects.hash(this.userName);
    }
}
