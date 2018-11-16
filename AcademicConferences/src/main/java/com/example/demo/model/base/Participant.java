package com.example.demo.model.base;

import com.fasterxml.jackson.annotation.JsonIgnore;
import io.swagger.annotations.ApiModelProperty;

import javax.persistence.*;

@MappedSuperclass
public class Participant {
    @Id
    @GeneratedValue
    @ApiModelProperty(value = "参会者id")
    private Integer ID;

    @ApiModelProperty(value = "报名表id")
    @JsonIgnore
    private Integer entryId;

    @ApiModelProperty(value = "姓名")
    private String name;

    @ApiModelProperty(value = "身份证号")
    private String realID;

    @ApiModelProperty(value = "性别")
    private String sex;

    @ApiModelProperty(value = "是否预订住宿")
    private Boolean ordered;

    public Integer getId() {
        return ID;
    }

    public void setId(Integer id) {
        this.ID = id;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public Boolean getOrdered() {
        return ordered;
    }

    public void setOrdered(Boolean ordered) {
        this.ordered = ordered;
    }

    public String getSex() {
        return sex;
    }

    public void setSex(String sex) {
        this.sex = sex;
    }

    public String getRealid() {
        return realID;
    }

    public void setRealid(String realid) {
        this.realID = realid;
    }

    public Participant(String name, String sex, String realID, Boolean ordered) {
        this.name = name;
        this.realID = realID;
        this.sex = sex;
        this.ordered = ordered;
    }

    public Participant(){

    }

    public void setEntryId(Integer entryId) {
        this.entryId = entryId;
    }

    public Integer getEntryId() {
        return entryId;
    }
}
