package com.example.demo.model.response;

import com.example.demo.model.entity.ConferenceEntity;
import com.example.demo.model.entity.OrganizationEntity;
import com.example.demo.utils.serializer.OrganizationInfoSerializer;
import com.example.demo.utils.serializer.TimeStampJsonSerializer;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonValue;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import io.swagger.annotations.ApiModelProperty;

import java.io.Serializable;
import java.sql.Timestamp;

/**
 * @Author : 陈瀚清
 * @Description: 会议简要信息
 * @Date created at 2018/6/30
 **/
public class ConferenceListItem implements ListItem<ConferenceListItem,ConferenceEntity> {

    @ApiModelProperty(value = "会议id")
    private Integer id;
    @ApiModelProperty(value = "会议标题")
    private String title;
    @ApiModelProperty(value = "会议简介")
    private String introduction;
    @ApiModelProperty(value = "组织机构")
    private OrganizationInfo organization;
    @ApiModelProperty(value = "截稿日期")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",timezone = "GMT+8")
    private Timestamp ddlDate;
    @ApiModelProperty(value = "会议开始日期")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",timezone = "GMT+8")
    private Timestamp confBeginDate;
    @ApiModelProperty(value = "会议状态")
    private ConferenceState state;

    @ApiModelProperty(value = "页大小")
    public static final int PAGESIZE=15;

    @Override
    public ConferenceListItem getListItem(ConferenceEntity p) {
        ConferenceListItem item=new ConferenceListItem(p);
        return item;
    }

    public class OrganizationInfo {
        private Long id;
        private String name;

        public OrganizationInfo(Long id, String name) {
            this.id = id;
            this.name = name;
        }

        public Long getId() {
            return id;
        }

        public void setId(Long id) {
            this.id = id;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }
    }

    public enum ConferenceState{
        CONTRIBUTING("投稿中"),
        ENDCONTRIBUTING("已截稿"),
        REGISTING("注册中"),
        ENDREGISTING("截止注册"),
        MEETING("会议中"),
        ENDMEETING("会议完成");

        private String state;

        ConferenceState(String state) {
            this.state = state;
        }

        @JsonValue
        public String getState() {
            return state;
        }
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getIntroduction() {
        return introduction;
    }

    public void setIntroduction(String introduction) {
        this.introduction = introduction;
    }

    public OrganizationInfo getOrganization() {
        return organization;
    }

    public void setOrganization(OrganizationInfo organization) {
        this.organization = organization;
    }

    public Timestamp getDdlDate() {
        return ddlDate;
    }

    public void setDdlDate(Timestamp ddlDate) {
        this.ddlDate = ddlDate;
    }

    public Timestamp getConfBeginDate() {
        return confBeginDate;
    }

    public void setConfBeginDate(Timestamp confBeginDate) {
        this.confBeginDate = confBeginDate;
    }

    public ConferenceState getState() {
        return state;
    }

    public void setState(ConferenceState state) {
        this.state = state;
    }

    public ConferenceListItem(ConferenceEntity p) {
        this.id = p.getId();
        this.title = p.getName();
        this.introduction = p.getIntroduction();
        OrganizationEntity organization=p.getOrganization();
        this.organization=new OrganizationInfo(organization.getId(),organization.getName());
        this.ddlDate = p.getDdlDate();
        this.confBeginDate = p.getConfBeginDate();
        this.setState(p);
    }

    public ConferenceListItem() {
    }

    protected void setState(ConferenceEntity p){
        Timestamp ddl=p.getDdlDate();
        Timestamp confBegin=p.getConfBeginDate();
        Timestamp confEnd=p.getConfEndDate();
        Timestamp informDate=p.getInformDate();
        Timestamp registerDate=p.getRegisterDate();
        Timestamp now=new Timestamp(System.currentTimeMillis());
        if(now.before(ddl)){//投稿状态
            state=ConferenceState.CONTRIBUTING;
        }
        else if(now.before(informDate)){
            state=ConferenceState.ENDCONTRIBUTING;
        }
        else if(now.before(registerDate)){
            state=ConferenceState.REGISTING;
        }
        else if(now.before(confBegin)){
            state=ConferenceState.ENDREGISTING;
        }
        else if(now.before(confEnd)){
            state=ConferenceState.MEETING;
        }
        else{
            state=ConferenceState.ENDMEETING;
        }
    }
}
