package com.example.demo.model.entity;


import com.example.demo.component.EmailsUtil;
import com.example.demo.exception.BusinessException;
import com.example.demo.model.base.EntityBase;
import com.example.demo.model.base.Identification;
import com.example.demo.model.base.Role;
import com.example.demo.security.PasswordEncryption;
import com.fasterxml.jackson.annotation.JsonIgnore;
import io.swagger.annotations.ApiModelProperty;

import javax.persistence.*;
import java.io.Serializable;
import java.util.Set;

import static com.example.demo.exception.ExceptionInfo.EMAIL_INVALID;

@Entity
public class UserEntity implements Serializable,Identification,EntityBase {
    @Id
    @GeneratedValue
    @ApiModelProperty(value = "会员id")
    private Long id;

    @Column(unique = true,columnDefinition = "nvarchar(20)")
    @ApiModelProperty(value = "用户名")
    private String nickName;

    @ApiModelProperty(value = "密码")
    @JsonIgnore
    private String password;

    @ApiModelProperty(value = "姓名")
    private String name;

    @ApiModelProperty(value = "身份证号")
    private String realId;

    @ApiModelProperty(value = "性别")
    private String sex;

    @ApiModelProperty(value = "所属单位")
    private String institution;

    @ApiModelProperty(value = "盐，用于加密")
    @JsonIgnore
    private String salt;

    @Column(columnDefinition = "char(10)")
    @ApiModelProperty(value = "系统角色")
    private String role= Role.ROLE_USER;

    @ApiModelProperty(value = "邮箱")
    @Column(unique = true, nullable = false)
    private String email;

    @ApiModelProperty(value = "投搞论文")
    @OneToMany(mappedBy = "firstauthor",fetch = FetchType.EAGER)
    @JsonIgnore
    private Set<PaperEntity> papers;

    @ApiModelProperty(value = "收藏分类")
    @OneToMany(mappedBy = "owner",fetch = FetchType.EAGER)
    @JsonIgnore
    private Set<CollectionClassificationEntity> classifications;

    public void setRole(String role) {
        this.role = role;
    }

    public String getRole() {
        return role;
    }

    public void setPassword(String password) {
        this.salt = PasswordEncryption.generateSalt();
        this.password = PasswordEncryption.encryptPassword(password,this.salt);
    }

    public String getUserName() {
        return this.email;
    }

    public String getPassword() {
        return password;
    }

    public void setUserName(String email) {
        this.email = email;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setSex(String sex) {
        this.sex = sex;
    }

    public String getSex() {
        return sex;
    }

    public void setInstitution(String institution) {
        this.institution = institution;
    }

    public String getInstitution() {
        return institution;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        if(!EmailsUtil.isEmail(email))
            throw new BusinessException(EMAIL_INVALID);
        this.email = email;
    }

    public String getSalt() {
        return salt;
    }

    public void setSalt(String salt) {
        this.salt = salt;
    }

    public Set<CollectionClassificationEntity> getClassifications() {
        return classifications;
    }

    public void setClassifications(Set<CollectionClassificationEntity> classifications) {
        this.classifications = classifications;
    }

    public String getRealId() {
        return realId;
    }

    public void setRealId(String realId) {
        if(realId!=null&&realId.length()== 18)
            this.realId = realId;
        if(this.realId!=null&&!this.realId.isEmpty()&&this.realId.length()>=2)
        {
            int lastChar = this.realId.charAt(this.realId.length()-2);
            if(lastChar%2==0)
                this.setSex("女");
            else
                this.setSex("男");
        }

    }

    public void setPapers(Set<PaperEntity> papers) {
        this.papers = papers;
    }

    public Set<PaperEntity> getPapers() {
        return papers;
    }

    public String getNickName() {
        return nickName;
    }

    public void setNickName(String nickName) {
        this.nickName = nickName;
    }
}
