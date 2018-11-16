package com.example.demo.model.response;

import com.example.demo.model.entity.AttachmentEntity;
import com.example.demo.model.entity.EntryFormEntity;
import com.example.demo.model.entity.SuperParticipantEntity;
import io.swagger.annotations.ApiModelProperty;

import java.util.Set;

public class EntryFormInfo {
    @ApiModelProperty(value = "报名表id")
    private Integer entryId;

    @ApiModelProperty(value = "会议id")
    private Integer conferenceId;

    @ApiModelProperty(value = "会议标题")
    private String conferenceName;

    @ApiModelProperty(value = "参会者信息")
    private Set<SuperParticipantEntity> participants;

    @ApiModelProperty(value = "注册费缴纳凭证")
    private Set<AttachmentEntity> proof;

    @ApiModelProperty(value = "处理状态")
    private EntryFormEntity.HandleStatus handleStatus;

    public void setHandleStatus(EntryFormEntity.HandleStatus handleStatus) {
        this.handleStatus = handleStatus;
    }

    public EntryFormEntity.HandleStatus getHandleStatus() {
        return handleStatus;
    }

    public Set<AttachmentEntity> getProof() {
        return proof;
    }

    public void setProof(Set<AttachmentEntity> proof) {
        this.proof = proof;
    }

    public void setParticipants(Set<SuperParticipantEntity> participants) {
        this.participants = participants;
    }

    public Set<SuperParticipantEntity> getParticipants() {
        return participants;
    }

    public Integer getConferenceId() {
        return conferenceId;
    }

    public void setConferenceId(Integer conferenceId) {
        this.conferenceId = conferenceId;
    }

    public Integer getEntryId() {
        return entryId;
    }

    public void setEntryId(Integer entryId) {
        this.entryId = entryId;
    }

    public String getConferenceName() {
        return conferenceName;
    }

    public void setConferenceName(String conferenceName) {
        this.conferenceName = conferenceName;
    }

    public EntryFormInfo(EntryFormEntity entryFormEntity){
        this.conferenceId = entryFormEntity.getConference().getId();
        this.conferenceName = entryFormEntity.getConference().getName();
        this.entryId = entryFormEntity.getId();
        this.handleStatus = entryFormEntity.getHandleStatus();
        this.participants = entryFormEntity.getParticipants();
        this.proof = entryFormEntity.getProof();
    }
}
