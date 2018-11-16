package com.example.demo.model.request;

import com.example.demo.model.base.Identification;
import com.example.demo.model.entity.UserEntity;
import io.swagger.annotations.ApiModelProperty;

import java.io.Serializable;

/**
 * @Author : 叶明林
 * @Description: 用户信息修改请求参数
 * @Date created at 2018/7/4 15:12
 **/
public class UserInfoModificationReq implements Serializable,IModifyUserInfo{
    @ApiModelProperty(value = "姓名")
    private String name;

    @ApiModelProperty(value = "身份证号")
    private String realId;

    @ApiModelProperty(value = "所属单位")
    private String institution;

    @ApiModelProperty(value = "邮箱")
    private String nickname;

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

    public String getInstitution() {
        return institution;
    }

    public void setInstitution(String institution) {
        this.institution = institution;
    }

    public void modifyUser(Identification userInfo)
    {
        UserEntity user = (UserEntity) userInfo;
        user.setName(this.name);
        user.setRealId(this.realId);
        user.setNickName(this.nickname);
        user.setInstitution(this.institution);
    }

    public String getNickname() {
        return nickname;
    }

    public void setNickname(String nickname) {
        this.nickname = nickname;
    }
}
