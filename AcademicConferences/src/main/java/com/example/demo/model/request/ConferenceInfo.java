package com.example.demo.model.request;

import com.example.demo.utils.deserializer.TimeStampDeserializer;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;

import javax.persistence.Column;
import java.sql.Timestamp;

@ApiModel
public class ConferenceInfo {
    @ApiModelProperty(value = "会议标题")
    private String title;

    @ApiModelProperty(value = "会议简介")
    @Column(columnDefinition = "text")
    private String introduction;

    @ApiModelProperty(value = "征文信息")
    @Column(columnDefinition = "text")
    private String requirement;

    @ApiModelProperty(value = "截稿日期")
    private Timestamp ddlDate;

    @ApiModelProperty(value = "录用通知日期")
    private Timestamp informDate;

    @ApiModelProperty(value = "注册日期")
    private Timestamp registerDate;

    @ApiModelProperty(value = "会议开始日期")
    private Timestamp confBeginDate;

    @ApiModelProperty(value = "会议结束日期")
    private Timestamp confEndDate;

    @ApiModelProperty(value = "日程安排")
    @Column(columnDefinition = "text")
    private String schedule;

    @ApiModelProperty(value = "注册费用")
    private String cost;

    @ApiModelProperty(value = "住宿交通信息")
    @Column(columnDefinition = "text")
    private String accommodationInfo;

    @ApiModelProperty(value = "联系方式")
    private String contact;


    public void setTitle(String title) {
        this.title = title;
    }

    public String getTitle() {
        return title;
    }

    public String getAccommodationInfo() {
        return accommodationInfo;
    }

    public void setAccommodationInfo(String accommodationInfo) {
        this.accommodationInfo = accommodationInfo;
    }

    public String getContact() {
        return contact;
    }

    public void setContact(String contact) {
        this.contact = contact;
    }

    public String getCost() {
        return cost;
    }

    public void setCost(String cost) {
        this.cost = cost;
    }

    public String getIntroduction() {
        return introduction;
    }

    public void setIntroduction(String introduction) {
        this.introduction = introduction;
    }

    public String getRequirement() {
        return requirement;
    }

    public void setRequirement(String requirement) {
        this.requirement = requirement;
    }

    public Timestamp getConfBeginDate() {
        return confBeginDate;
    }

    @JsonDeserialize(using = TimeStampDeserializer.class)
    public void setConfBeginDate(Timestamp confBeginDate) {
        this.confBeginDate = confBeginDate;
    }

    public Timestamp getConfEndDate() {
        return confEndDate;
    }

    @JsonDeserialize(using = TimeStampDeserializer.class)
    public void setConfEndDate(Timestamp confEndDate) {
        this.confEndDate = confEndDate;
    }

    public Timestamp getDdlDate() {
        return ddlDate;
    }

    @JsonDeserialize(using = TimeStampDeserializer.class)
    public void setDdlDate(Timestamp ddlDate) {
        this.ddlDate = ddlDate;
    }

    public Timestamp getInformDate() {
        return informDate;
    }

    @JsonDeserialize(using = TimeStampDeserializer.class)
    public void setInformDate(Timestamp informDate) {
        this.informDate = informDate;
    }

    public Timestamp getRegisterDate() {
        return registerDate;
    }

    @JsonDeserialize(using = TimeStampDeserializer.class)
    public void setRegisterDate(Timestamp registerDate) {
        this.registerDate = registerDate;
    }

    public String getSchedule() {
        return schedule;
    }

    public void setSchedule(String schedule) {
        this.schedule = schedule;
    }

}
