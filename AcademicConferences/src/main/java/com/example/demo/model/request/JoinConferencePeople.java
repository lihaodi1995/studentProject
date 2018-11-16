package com.example.demo.model.request;

import io.swagger.annotations.ApiModelProperty;

/**
 * Created by 44910_000 on 2018/7/1.
 */
public class JoinConferencePeople {
    @ApiModelProperty(value = "姓名")
    private String name;

    @ApiModelProperty(value = "身份证号")
    private String realID;

    @ApiModelProperty(value = "性别")
    private String sex;

    @ApiModelProperty(value = "是否预订住宿")
    private Boolean ordered;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getRealID() {
        return realID;
    }

    public void setRealID(String realID) {
        this.realID = realID;
    }

    public String getSex() {
        return sex;
    }

    public void setSex(String sex) {
        this.sex = sex;
    }

    public Boolean getOrdered() {
        return ordered;
    }

    public void setOrdered(Boolean ordered) {
        this.ordered = ordered;
    }
}
