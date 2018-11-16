package com.example.demo.model.entity;

import com.example.demo.model.base.Participant;
import io.swagger.annotations.ApiModelProperty;

import javax.persistence.Entity;

@Entity
public class SuperParticipantEntity extends Participant {
    @ApiModelProperty(value = "论文编号")
    private Integer paperID;

    public SuperParticipantEntity() {
    }

    public Integer getPaperid() {
        return paperID;
    }

    public void setPaperid(Integer paperID) {
        this.paperID = paperID;
    }

    public SuperParticipantEntity(Integer paperID,String name,String sex,String realId,boolean ordered) {
        super(name,sex,realId,ordered);
        this.paperID = paperID;
    }
}
