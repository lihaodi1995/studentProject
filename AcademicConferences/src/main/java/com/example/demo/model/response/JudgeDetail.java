package com.example.demo.model.response;

import com.example.demo.model.entity.AttachmentEntity;
import com.example.demo.model.entity.ConferenceEntity;
import com.example.demo.model.entity.PaperEntity;
import com.example.demo.utils.serializer.TimeStampJsonSerializer;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import io.swagger.annotations.ApiModelProperty;

import java.sql.Timestamp;
import java.util.Set;

public class JudgeDetail {
    @ApiModelProperty(value = "论文编号")
    private Integer id;

    @ApiModelProperty(value = "论文标题")
    private String title;

    @ApiModelProperty(value = "最后修改日期")
    private Timestamp lastModDate;

    @ApiModelProperty(value = "修改稿截止日期")
    private Timestamp repostDdlDate;

    @ApiModelProperty(value = "评审意见")
    private String opinion;

    @ApiModelProperty(value = "会议标题")
    private String conferenceTitle;

    @ApiModelProperty(value = "附件")
    private Set<AttachmentEntity> attachments;

    @JsonIgnore
    private PaperEntity.JudgeStatus judgeStatus;

    private int judgeStatusInt;

    public JudgeDetail(PaperEntity paperEntity, ConferenceEntity conferenceEntity){
        this.opinion = paperEntity.getOpinion();
        this.judgeStatus = paperEntity.getJudgeStatus();
        this.judgeStatusInt = judgeStatus.ordinal();
        this.id = paperEntity.getId();
        this.title = paperEntity.getTitle();
        this.lastModDate = paperEntity.getLastModDate();
        this.attachments = paperEntity.getAttachments();
        this.repostDdlDate = conferenceEntity.getRepostDdlDate();
        this.conferenceTitle = conferenceEntity.getName();
    }

    public void setJudgeStatus(PaperEntity.JudgeStatus judgeStatus) {
        this.judgeStatus = judgeStatus;
    }

    public PaperEntity.JudgeStatus getJudgeStatus() {
        return judgeStatus;
    }

    public String getOpinion() {
        return opinion;
    }

    public void setOpinion(String opinion) {
        this.opinion = opinion;
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

    public void setLastModDate(Timestamp lastModDate) {
        this.lastModDate = lastModDate;
    }

    @JsonSerialize(using = TimeStampJsonSerializer.class)
    public Timestamp getLastModDate() {
        return lastModDate;
    }

    public Set<AttachmentEntity> getAttachments() {
        return attachments;
    }

    public void setAttachments(Set<AttachmentEntity> attachments) {
        this.attachments = attachments;
    }

    public Timestamp getRepostDdlDate() {
        return repostDdlDate;
    }

    public void setRepostDdlDate(Timestamp repostDdlDate) {
        this.repostDdlDate = repostDdlDate;
    }

    public int getJudgeStatusInt() {
        return judgeStatusInt;
    }

    public void setJudgeStatusInt(int judgeStatusInt) {
        this.judgeStatusInt = judgeStatusInt;
    }

    public String getConferenceTitle() {
        return conferenceTitle;
    }

    public void setConferenceTitle(String conferenceTitle) {
        this.conferenceTitle = conferenceTitle;
    }
}
