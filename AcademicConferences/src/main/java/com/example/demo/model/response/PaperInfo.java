package com.example.demo.model.response;

import com.example.demo.model.entity.AttachmentEntity;
import com.example.demo.model.entity.ConferenceEntity;
import com.example.demo.model.entity.PaperEntity;
import com.example.demo.model.entity.UserEntity;
import com.example.demo.utils.serializer.NameJsonSerializer;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

import java.util.Iterator;

public class PaperInfo extends PaperEntity {
    private int judgeStatusInt;

    public PaperInfo(PaperEntity paperEntity){
        this.judgeStatusInt = paperEntity.getJudgeStatus().ordinal();
        super.setOpinion(paperEntity.getOpinion());
        super.setAbstractinfo(paperEntity.getAbstractinfo());
        super.setAttachments(paperEntity.getAttachments());
        super.setAuthors(paperEntity.getAuthors());
        super.setId(paperEntity.getId());
        super.setInstitution(paperEntity.getInstitution());
        super.setTitle(paperEntity.getTitle());
        super.setFirstauthor(paperEntity.getFirstauthor());
        super.setConference(paperEntity.getConference());
    }
    @JsonIgnore
    private JudgeStatus judgeStatus;

    @JsonSerialize(using=NameJsonSerializer.class)
    public UserEntity getFirstauthor() {
        return super.getFirstauthor();
    }

    @JsonSerialize(using=NameJsonSerializer.class)
    public ConferenceEntity getConference() {
        return super.getConference();
    }

    public int getJudgeStatusInt() {
        return judgeStatusInt;
    }

    public void setJudgeStatusInt(int judgeStatusInt) {
        this.judgeStatusInt = judgeStatusInt;
    }

}
