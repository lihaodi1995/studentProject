package com.example.demo.model.entity;


import io.swagger.annotations.ApiModelProperty;

import javax.persistence.*;
import java.util.Set;

@Entity
public class EntryFormEntity {
    @Id
    @GeneratedValue
    @ApiModelProperty(value = "报名表id")
    private Integer id;

    @ManyToOne
    @JoinColumn(name = "conf_id")
    private ConferenceEntity conference;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private UserEntity user;

    @ApiModelProperty(value = "参会者信息")
    @OneToMany(cascade = CascadeType.PERSIST)
    private Set<SuperParticipantEntity> participants;

    @ApiModelProperty(value = "注册费缴纳凭证")
    @OneToMany(cascade = CascadeType.PERSIST)
    private Set<AttachmentEntity> proof;

    public enum HandleStatus{
        Pending("pending"),
        Accepted("accepted"),
        Rejected("rejected");

        private String status;

        HandleStatus(String status) {
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
    private HandleStatus handleStatus = HandleStatus.Pending;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public void setProof(Set<AttachmentEntity> proof) {
        this.proof = proof;
    }

    public Set<AttachmentEntity> getProof() {
        return proof;
    }

    public ConferenceEntity getConference() {
        return conference;
    }

    public void setConference(ConferenceEntity conference) {
        this.conference = conference;
    }

    public Set<SuperParticipantEntity> getParticipants() {
        return participants;
    }

    public void setParticipants(Set<SuperParticipantEntity> participants) {
        this.participants = participants;
    }

    public UserEntity getUser() {
        return user;
    }

    public void setUser(UserEntity user) {
        this.user = user;
    }

    public HandleStatus getHandleStatus() {
        return handleStatus;
    }

    public void setHandleStatus(HandleStatus handleStatus) {
        this.handleStatus = handleStatus;
    }
}
