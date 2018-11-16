package com.example.demo.model.response;

import com.example.demo.model.entity.AttachmentEntity;
import com.example.demo.model.entity.ConferenceEntity;
import com.example.demo.utils.serializer.TimeStampJsonSerializer;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import io.swagger.annotations.ApiModelProperty;

import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;

/**
 * @Author : 陈瀚清
 * @Description: 会议详细信息
 * @Date created at 2018/6/30
 **/
public class ConferenceDetail extends ConferenceListItem {
    @ApiModelProperty(value = "征文信息")
    private String requirement;

    @ApiModelProperty(value = "录用通知日期")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",timezone = "GMT+8")
    private Timestamp informDate;

    @ApiModelProperty(value = "注册日期")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",timezone = "GMT+8")
    private Timestamp registerDate;

    @ApiModelProperty(value = "创建日期")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",timezone = "GMT+8")
    private Timestamp setDate;

    @ApiModelProperty(value = "会议结束日期")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",timezone = "GMT+8")
    private Timestamp confEndDate;

    @ApiModelProperty(value = "修改稿截止日期")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",timezone = "GMT+8")
    private Timestamp repostDdlDate;

    @ApiModelProperty(value = "日程安排")
    private String schedule;

    @ApiModelProperty(value = "论文模板")
    private List<String> storagePath;

    @ApiModelProperty(value = "注册费用")
    private String cost;

    @ApiModelProperty(value = "住宿交通信息")
    private String accommodationInfo;

    @ApiModelProperty(value = "联系方式")
    private String contact;

    public ConferenceDetail(ConferenceEntity p) {
        super(p);
        this.requirement = p.getRequirement();
        this.informDate = p.getInformDate();
        this.registerDate = p.getRegisterDate();
        this.confEndDate = p.getConfEndDate();
        this.schedule = p.getSchedule();
        addStoragePath(p.getTemplate());
        this.cost = p.getCost();
        this.accommodationInfo = p.getAccommodationInfo();
        this.setDate=p.getSetDate();
        this.contact=p.getContact();
        this.repostDdlDate=p.getRepostDdlDate();
    }

    public void addStoragePath(List<AttachmentEntity> list){
        storagePath=new ArrayList<String>();
        for(AttachmentEntity one:list){
            storagePath.add(one.getStoragePath());
        }
    }

    public String getRequirement() {
        return requirement;
    }

    public void setRequirement(String requirement) {
        this.requirement = requirement;
    }

    public Timestamp getInformDate() {
        return informDate;
    }

    public void setInformDate(Timestamp informDate) {
        this.informDate = informDate;
    }

    public Timestamp getRegisterDate() {
        return registerDate;
    }

    public void setRegisterDate(Timestamp registerDate) {
        this.registerDate = registerDate;
    }

    public Timestamp getConfEndDate() {
        return confEndDate;
    }

    public void setConfEndDate(Timestamp confEndDate) {
        this.confEndDate = confEndDate;
    }

    public String getSchedule() {
        return schedule;
    }

    public void setSchedule(String schedule) {
        this.schedule = schedule;
    }

    public List<String> getStoragePath() {
        return storagePath;
    }

    public void setStoragePath(List<String> storagePath) {
        this.storagePath = storagePath;
    }

    public String getCost() {
        return cost;
    }

    public void setCost(String cost) {
        this.cost = cost;
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

    public Timestamp getSetDate() {
        return setDate;
    }

    public void setSetDate(Timestamp setDate) {
        this.setDate = setDate;
    }

    public Timestamp getRepostDdlDate() {
        return repostDdlDate;
    }

    public void setRepostDdlDate(Timestamp repostDdlDate) {
        this.repostDdlDate = repostDdlDate;
    }
}
