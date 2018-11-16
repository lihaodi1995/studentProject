package com.example.demo.model.entity;

import com.example.demo.utils.serializer.TimeStampJsonSerializer;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import io.swagger.annotations.ApiModelProperty;

import javax.persistence.*;
import java.io.Serializable;
import java.sql.Timestamp;
import java.util.Set;

@Entity
public class PaperEntity implements Serializable {
    @Id
    @GeneratedValue
    @ApiModelProperty(value = "论文编号")
    private Integer id;

    @ApiModelProperty(value = "第一作者")
    @ManyToOne
    private UserEntity firstauthor;

    @ApiModelProperty(value = "其他作者")
    private String authors;

    @ApiModelProperty(value = "论文标题")
    private String title;

    @ApiModelProperty(value = "所属单位")
    private String institution;

    @ApiModelProperty(value = "参加会议")
    @OneToOne
    private ConferenceEntity conference;

    @ApiModelProperty(value = "摘要")
    private String abstractinfo;

    @ApiModelProperty(value = "最后修改日期")
    private Timestamp lastModDate;

    @ApiModelProperty(value = "附件")
    @OneToMany(fetch = FetchType.LAZY,cascade = CascadeType.PERSIST)
    private Set<AttachmentEntity> attachments;

    @ApiModelProperty(value = "评审意见")
    private String opinion;

    @ApiModelProperty(value = "修改说明")
    private String modInfo;

    public enum JudgeStatus{
        Not_qualified("not_qualified"),
        Pending("pending"),
        Qualified("qualified"),
        Qualified_after_modified("qualified_after_modified");



        private String status;

        JudgeStatus(String status) {
            this.status = status;
        }

        public String getStatus() {
            return status;
        }

        public void setStatus(String status) {
            this.status = status;
        }
    }

    @Column(columnDefinition = "char(10)")
    private JudgeStatus judgeStatus = JudgeStatus.Pending;

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getId() {
        return id;
    }

    public String getAuthors() {
        return authors;
    }

    public void setAuthors(String authors) {
        this.authors = authors;
    }

    public String getAbstractinfo() {
        return abstractinfo;
    }

    public void setAbstractinfo(String abstractinfo) {
        this.abstractinfo = abstractinfo;
    }

    public String getInstitution() {
        return institution;
    }

    public void setInstitution(String institution) {
        this.institution = institution;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public UserEntity getFirstauthor() {
        return firstauthor;
    }

    public void setFirstauthor(UserEntity firstauthor) {
        this.firstauthor = firstauthor;
    }

    public void setConference(ConferenceEntity conference) {
        this.conference = conference;
    }

    public ConferenceEntity getConference() {
        return conference;
    }

    public Set<AttachmentEntity> getAttachments() {
        return attachments;
    }

    public void setAttachments(Set<AttachmentEntity> attachments) {
        this.attachments = attachments;
    }

    public PaperEntity() {
    }

    public PaperEntity(UserEntity firstauthor, String authors, String title, String institution, ConferenceEntity conference, String abstractinfo) {
        this.firstauthor = firstauthor;
        this.authors = authors;
        this.title = title;
        this.institution = institution;
        this.conference = conference;
        this.abstractinfo = abstractinfo;
    }

    public JudgeStatus getJudgeStatus() {
        return judgeStatus;
    }

    public void setJudgeStatus(JudgeStatus judgeStatus) {
        this.judgeStatus = judgeStatus;
    }

    public String getOpinion() {
        return opinion;
    }

    public void setOpinion(String opinion) {
        this.opinion = opinion;
    }

    @JsonSerialize(using = TimeStampJsonSerializer.class)
    public Timestamp getLastModDate() {
        return lastModDate;
    }

    public void setLastModDate(Timestamp lastModDate) {
        this.lastModDate = lastModDate;
    }

    public String getModInfo() {
        return modInfo;
    }

    public void setModInfo(String modInfo) {
        this.modInfo = modInfo;
    }
}
